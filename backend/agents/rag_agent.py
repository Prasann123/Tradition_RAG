import os
from langchain_openai import OpenAIEmbeddings
from langchain_milvus import Milvus
from langchain_community.vectorstores import Chroma
from backend.factory.retriever_factory import get_retriever
from backend.utils.metrics import time_agent_node


@time_agent_node
def rag_agent(state):
    """ RAG agent which will retrieve relevant docsfrom cloud or memory db based
    on user input"""

    config = state.config
    query = state.query
    k= config.get("k", 5)

    vectordb = config.get("vectordb", "milvus").lower()

    

    embeddings = OpenAIEmbeddings(model ="text-embedding-3-small",client=None)

    vector_store = None
    if vectordb == "milvus":
        milvus_url = os.environ.get("MILVUS_URL")
        milvus_token = os.environ.get("MILVUS_TOKEN")
        collection_name = config.get("collection_name", "documents")

        vector_store = Milvus(
            embedding_function=embeddings,
            collection_name=collection_name,
            connection_args={"uri": milvus_url, "token": milvus_token},
            text_field="text",  # Name of document attributes to holding text
            vector_field="embedding"  # name of doc attribute to hold vector
        )
    elif vectordb == "chroma":
        persist_directory = config.get("persist_directory", "chroma_db")
        collection_name = config.get("collection_name", "documents")
        vector_store = Chroma(
            embedding_function=embeddings,
            collection_name=collection_name,
            persist_directory=persist_directory
        )
        
    else:
        state.context = []
        state.sources = []
        state.error = f"Invalid vectordb '{vectordb}'. Valid options: ['milvus', 'chroma']"
        return state
    
    retriever = get_retriever(vector_store, config)

    doc_and_stores = retriever.get_relevant_documents(query)

    state.context = [doc.page_content for doc in doc_and_stores]
    #state.scores = [float(score) for _, score in doc_and_stores]
    state.sources = [{
        "source_name": doc.metadata.get("source", "unknown"),
        "page_content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
        "metadata": doc.metadata
    } for doc in doc_and_stores]

    return state
    




    