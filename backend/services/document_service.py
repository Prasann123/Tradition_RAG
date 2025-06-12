import os
import tempfile
import asyncio
import time  # Added for timing
from datetime import datetime
from keybert import KeyBERT
import pymongo
from werkzeug.utils import secure_filename
from langchain_milvus import Milvus
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_mongodb import MongoDBAtlasVectorSearch
from motor.motor_asyncio import AsyncIOMotorClient
from langchain_openai import OpenAIEmbeddings



async def process_file(file, index_mech="FLAT"):
    """Process an uploaded file through RAG pipeline asynchronously"""
    file_path = None
    try:
        filename = secure_filename(file.filename)
        print(f"Starting async processing for file: {filename}")
        fd, temp_file_path = await asyncio.to_thread(tempfile.mkstemp, suffix=os.path.splitext(filename)[1])
        await asyncio.to_thread(os.close, fd)
        file_path = temp_file_path
        await asyncio.to_thread(file.save, file_path)
        print(f"File saved temporarily to: {file_path}")
      

        if filename.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif filename.endswith('.txt'):
            loader = TextLoader(file_path)
        else:
            if file_path and await asyncio.to_thread(os.path.exists, file_path):
                await asyncio.to_thread(os.remove, file_path)
            print(f"Unsupported file type: {filename}")
            return {
                "status": "error",
                "message": "Unsupported file type. Please upload PDF or TXT files.",
                "source": filename,
                "index_mechanism": index_mech,
                "num_documents": 0,
                "num_chunks": 0,
                "time_taken_seconds": 0
            }

        print(f"Loading documents from: {filename} using {type(loader).__name__}")
        t0 = time.perf_counter()
        documents = await asyncio.to_thread(loader.load)
        t1 = time.perf_counter()
        print(f"Successfully loaded {len(documents)} documents from: {filename}")
        if not documents:
            print(f"Warning: No documents loaded from {filename}. File might be empty or unreadable by the loader.")
            return {
                "status": "error",
                "message": f"Could not load any content from file: {filename}",
                "source": filename,
                "index_mechanism": index_mech,
                "num_documents": 0,
                "num_chunks": 0,
                "time_taken_seconds": round(t1 - t0, 3)
            }

        # Process through RAG pipeline
        result = await _process_documents(
            documents, f"File '{filename}'", index_mech=index_mech, t_load=t1-t0
        )
        return result
    except Exception as e:
        print(f"Error processing file {filename if 'filename' in locals() else 'unknown'}: {e}")
        return {
            "status": "error",
            "message": f"Error processing file: {str(e)}",
            "source": filename if 'filename' in locals() else None,
            "index_mechanism": index_mech,
            "num_documents": 0,
            "num_chunks": 0,
            "time_taken_seconds": 0
        }
    finally:
        if file_path and await asyncio.to_thread(os.path.exists, file_path):
            try:
                await asyncio.to_thread(os.remove, file_path)
                print(f"Temporary file {file_path} removed.")
            except Exception as e_clean:
                print(f"Error cleaning up temporary file {file_path}: {e_clean}")

async def process_video(file):
    """Process a video file asynchronously"""
    return f"Video '{file.filename}' received. Video processing is not fully implemented yet."

async def process_text(text, index_mech="FLAT"):
    """Process plain text through RAG pipeline asynchronously"""
    try:
        from langchain_core.documents import Document
        doc = Document(page_content=text)
        print("Processing plain text input asynchronously.")
        return await _process_documents([doc], "Uploaded text", index_mech=index_mech)
    except Exception as e:
        print(f"Error processing text: {e}")
        return f"Error processing text: {str(e)}"

async def _process_documents(documents, source_name, metadata=None, index_mech="FLAT", t_load=None):
    try:
        print(f"Starting async _process_documents for source: {source_name} with {len(documents)} documents. Index mechanism: {index_mech}")
        t0 = time.perf_counter()
        milvus_url = os.environ.get("MILVUS_URL")
        milvus_token = os.environ.get("MILVUS_TOKEN")
        if metadata is None:
            metadata = {
                "source": source_name,
                "date_processed": datetime.now().isoformat(),
            }
        for doc in documents:
            doc.metadata.update(metadata)

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        text_splitter = SemanticChunker(
            embeddings=embeddings,
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95.0,
            min_chunk_size=200,
        )


        all_chunks = []
        for doc_to_split in documents:
            doc_chunks = await asyncio.to_thread(text_splitter.split_documents, [doc_to_split])
            all_chunks.extend(doc_chunks)
        t1 = time.perf_counter()
        chunks = all_chunks
        if not chunks:
            return {
                "status": "error",
                "message": f"{source_name} processed, but no content was suitable for adding to knowledge base (0 chunks).",
                "source": source_name,
                "index_mechanism": index_mech,
                "num_documents": len(documents),
                "num_chunks": 0,
                "time_taken_seconds": round((t1-t0) + (t_load or 0), 3)
            }

        t2 = time.perf_counter()
        
        vector_store=  Milvus(embedding_function=embeddings,
                collection_name="documents",
                connection_args={"uri": milvus_url, "token": milvus_token},
                text_field="text",
                vector_field="embedding")
        
        vector_store.add_documents(chunks)
        t3 = time.perf_counter()

        return {
            "status": "success",
            "message": f"{source_name} processed successfully. Added {len(chunks)} chunks to knowledge base.",
            "source": source_name,
            "index_mechanism": index_mech,
            "num_documents": len(documents),
            "num_chunks": len(chunks),
            "time_taken_seconds": round((t3-t0) + (t_load or 0), 3),
            "timing_details": {
                "load_seconds": round(t_load or 0, 3),
                "split_seconds": round(t1-t0, 3),
                "db_upload_seconds": round(t3-t2, 3)
            }
        }

    except Exception as e:
        print(f"Error in _process_documents for source {source_name}: {e}")
        return {
            "status": "error",
            "message": f"Error during document processing for {source_name}: {str(e)}",
            "source": source_name,
            "index_mechanism": index_mech,
            "num_documents": len(documents) if documents else 0,
            "num_chunks": 0,
            "time_taken_seconds": 0,

        }

async def list_documents(query=None, limit=20):
    """List documents in the MongoDB collection asynchronously"""
    try:
        mongodb_uri = os.environ.get("MONGO_DB_URI")
        client = AsyncIOMotorClient(mongodb_uri)
        db_name = "rag_db"
        collection_name = "documents"
        collection = client[db_name][collection_name]
        if query is None:
            query = {}
        docs_cursor = collection.find(query).limit(limit)
        docs = await docs_cursor.to_list(length=limit)
        for doc in docs:
            doc["_id"] = str(doc["_id"])
        return docs
    except Exception as e:
        print(f"Error listing documents: {e}")
        return []
    

# Example usage (would need to be run in an asyncio event loop):
# async def main():
#   # Example: text_result = await process_text("This is a test document.", index_mech="FLAT")
#   # print(text_result)
#   # documents = await list_documents()
#   # print(documents)
#
# if __name__ == "__main__":
#   # import asyncio
#   # asyncio.run(main())
#   pass

async def extract_topics_from_documents(limit=20):
    docs = await list_documents(limit=limit)
    kw_model = KeyBERT()
    topics = []
    for doc in docs:
        text = doc.get("page_content", "")
        if text:
            keywords = kw_model.extract_keywords(text, top_n=5)
            topics.append({
                "source": doc.get("metadata", {}).get("source"),
                "topics": [kw for kw, _ in keywords]
            })
    return topics