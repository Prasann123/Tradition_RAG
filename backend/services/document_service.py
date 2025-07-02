import os
from werkzeug.utils import secure_filename
from backend.factory.parser_factory import get_parser
from langchain_openai import OpenAIEmbeddings
from langchain_milvus import Milvus
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.docstore.document import Document
from motor.motor_asyncio import AsyncIOMotorClient
from keybert import KeyBERT

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
0
async def process_file(filepath:str,config:dict,job_id:str,statuses: dict):
    """Process an uploaded file through RAG pipeline asynchronously"""
    def update_status(message, progress=None):
        statuses[job_id] = {"status": "processing", "message": message, "progress": progress}

    vectordb = config.get("vectordb", "milvus").lower()
    collection_name = config.get("collection_name", "documents")
    
    try:

        update_status("Loading document content...")
        filename = os.path.basename(filepath)
        loader = PyPDFLoader(filepath) if filename.endswith(".pdf") else TextLoader(filepath)
        documents = loader.load()

        update_status("Splitting document into chunks...")
        text_splitter = get_parser(config)
        chunks = text_splitter.split_documents(documents)
        total_chunks = len(chunks)
        update_status(f"Preparing to embed {total_chunks} chunks...")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
      
        update_status(f"Embedding and ingesting {total_chunks} chunks into {vectordb}...")
        if vectordb == "milvus":
            Milvus.from_documents(
                documents=chunks, embedding=embeddings, collection_name=collection_name,
                connection_args={"uri": os.environ.get("MILVUS_URL"), "token": os.environ.get("MILVUS_TOKEN")},
            )
        elif vectordb == "chroma":
            persist_directory = config.get("persist_directory", "chroma_db")
            Chroma.from_documents(
                documents=chunks, embedding=embeddings, collection_name=collection_name,
                persist_directory=persist_directory
            )
        statuses[job_id] = {"status": "complete", "message": f"Successfully ingested {total_chunks} chunks."}    

        return f"Successfully ingested {len(chunks)} chunks into {vectordb}."
    except Exception as e:
        statuses[job_id] = {"status": "error", "message": f"An error occurred: {e}"}
    finally:
       if os.path.exists(filepath):
            os.remove(filepath)


async def process_text(text_content:str, config:dict):
    """Process plain text through RAG pipeline asynchronously"""
    vectordb = config.get("vectordb", "milvus").lower()
    collection_name = config.get("collection_name", "documents")

    try:
        documents = [Document(page_content=text_content)]
        text_splitter = get_parser(config)
        chunks = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        if vectordb == "milvus":
            Milvus.from_documents(
                documents=chunks, embedding=embeddings, collection_name=collection_name,
                connection_args={"uri": os.environ.get("MILVUS_URL"), "token": os.environ.get("MILVUS_TOKEN")},
            )
        elif vectordb == "chroma":
            persist_directory = config.get("persist_directory", "chroma_db")
            Chroma.from_documents(
                documents=chunks, embedding=embeddings, collection_name=collection_name,
                persist_directory=persist_directory
            )
        return f"Successfully ingested {len(chunks)} text chunks into {vectordb}."
    except Exception as e:
        return f"An error occurred: {e}"


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

