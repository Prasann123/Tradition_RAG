from langchain.retrievers import MultiQueryRetriever
from langchain_openai import ChatOpenAI

def get_retriever(vector_store, config:dict):
    """Builds and returns vector store retriever based on configuration
    """

    retriever_type = config.get("retriever_type","vectorstore")
    llm =ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0, max_tokens=1000)

    if retriever_type == "vectorstore":
        # Use the vector store directly
        return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    
    elif retriever_type == "multi_query":

        return MultiQueryRetriever.from_llm(
            llm = llm,
            retriever=vector_store.as_retriever()
        )