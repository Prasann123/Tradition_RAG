import time  # Import the time module directly, not from datetime
import os
import threading
import asyncio
from langchain.chains import LLMChain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_milvus import Milvus


from backend.utils.enums import SearchType
def patch_thread_with_event_loop():
    """Patch Thread class to ensure every thread has an event loop"""
    original_thread_init = threading.Thread.__init__
    
    def new_thread_init(self, *args, **kwargs):
        original_thread_init(self, *args, **kwargs)
        original_run = self.run
        
        def patched_run(*args, **kwargs):
            try:
                asyncio.get_event_loop()
            except RuntimeError:
                # Thread has no event loop, create one
                asyncio.set_event_loop(asyncio.new_event_loop())
            return original_run(*args, **kwargs)
            
        self.run = patched_run
        
    threading.Thread.__init__ = new_thread_init

# Apply the patch
patch_thread_with_event_loop()
def process_message(message,search_type_str="knnBeta"):
    """Process a chat message using RAG pipeline"""
    try:
        # Load the vector store if it exists
        try:
            search_type = SearchType[search_type_str.upper()].value
        except KeyError:
            return {
                "error": f"Invalid search_type '{search_type_str}'. Valid options: {[e.value for e in SearchType]}"
            }
        milvus_url = os.environ.get("MILVUS_URL")
        milvus_token = os.environ.get("MILVUS_TOKEN")
        collection_name = "documents"
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", client=None)
        search_kwargs = {"k": 5}
        
        # Initialize a Milvus-backed vector store for retrieval-augmented generation
        vectorstore = Milvus(
            embedding_function=embeddings,
            collection_name=collection_name,
            connection_args={"uri": milvus_url, "token": milvus_token},
            text_field="text", # Name of document attributes to holding text
            vector_field="embedding" # name of doc attribute to gold vector 
        )

        docs_and_scores = vectorstore.similarity_search_with_score(message, k=5,fetch_k=15,lambda_mult=0.7)
        scores = [float(score) for _, score in docs_and_scores]
        if not docs_and_scores:
            return {
            "answer": "No relevant documents found.",
            "sources": [],
            "similarity_scores": [],
            "search_time_seconds": 0,
            "total_sources": 0
            }
            # 3) Build context from retrieved chunks merge those chunks into a single string
        # Example of docs_and_scores format:
        # docs_and_scores = [(doc1, 0.9), (doc2, 0.8)]
        # doc1.page_content = "This is the first chunk."
        # doc2.page_content = "This is the second chunk." """
    
        context = "\n\n".join(doc.page_content for doc, _ in docs_and_scores)
        scores  = [float(score) for _, score in docs_and_scores]
        # Create retrieval chain with improved parameters for fuller responses
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.5,  # Slightly higher temperature for more detailed outputs
            max_tokens=2000   # Increase the token limit for longer responses
        )
        max_score = max(scores) if scores else 1.0
        accuracy_percentages = [round((s / max_score) * 100, 2) for s in scores]

        # Enhanced prompt template to encourage comprehensive answers
        stuff_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "Use the following pieces of context to answer the question at the end.\n"
                "Be comprehensive, detailed and thorough in your response.\n"
                "Don't truncate or abbreviate your answer.\n"
                "Explain concepts fully when they're relevant to the question.\n\n"
                "{context}\n\n"
                "Question: {question}\n"
                "Comprehensive answer:"
            )
        )

        # 3) call your prompt/LLM


        llm_chain = LLMChain(llm=llm, prompt=stuff_prompt)


        # Execute query
        start_time = time.time()
        answer = llm_chain.run({"context": context, "question": message})
        elapsed_time = time.time() - start_time
        # use the docs we already retrieved
        source_docs = [doc for doc, _ in docs_and_scores]
        sources = []
        for doc in source_docs:
            source_info = {
                "source_name": doc.metadata.get("source", "Unknown"),
                "page_content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": {
                    "date_processed": doc.metadata.get("date_processed"),
                    "chunk_index": doc.metadata.get("chunk_index"),
                    "score": doc.metadata.get("score"),
                    "page": doc.metadata.get("page"),
                    "file_name": doc.metadata.get("file_name"),
                }
            }
            sources.append(source_info)
        return {
            "answer": answer,
            "sources": sources,
            "similarity_scores": scores,
            "accuracy_percentages": accuracy_percentages, 
            "search_time_seconds": elapsed_time,
            "total_sources": len(sources),
            "search_type_used": search_type
        }
    
    except Exception as e:
        print(f"Error in process_message: {e}")
        return f"I encountered an error processing your request: {str(e)}"