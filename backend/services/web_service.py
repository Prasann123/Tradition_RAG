import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from .document_service import _process_documents

def scrape_website_content(url):
    """Scrape content from a website and process it through RAG pipeline"""
    try:
        # Send request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content (adjust as needed)
        paragraphs = soup.find_all('p')
        content = "\n".join([p.get_text() for p in paragraphs])
        
        if not content.strip():
            return "Could not extract content from this website"
        
        # Create document
        doc = Document(page_content=content, metadata={'source': url})
        
        # Process through RAG pipeline
        return _process_documents([doc], f"Website {url}")
    except Exception as e:
        print(f"Error scraping website: {e}")
        return f"Error scraping website: {str(e)}"