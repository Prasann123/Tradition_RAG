import os
from tavily import TavilyClient

def web_agent(state):
    """web agent where it crawls the data for present informations"""

    query = state.query

    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


    response = tavily_client.search(query=query, search_depth="advanced")


    # Step 2: Crawl each URL
    web_data = [result['content'] for result in response['results']]

    state.web_data = web_data
    return state        

