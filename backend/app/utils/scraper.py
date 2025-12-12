import requests
from bs4 import BeautifulSoup
from app.core.config import logger
from typing import Optional, Dict

def scrape_text_from_url(url: str, max_chars: int = 5000) -> Optional[Dict[str, str]]:
    """
    Fetches the content of a URL and extracts the main text.
    Returns a dict with 'title', 'source', 'content' or None on failure.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
            
        # Extract title
        title = soup.title.string if soup.title else url
        
        # Extract text
        text = soup.get_text(separator='\n')
        
        # Clean text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Truncate if too long (tokens are precious)
        if len(text) > max_chars:
            text = text[:max_chars] + "... (truncated)"
            
        return {
            "title": title.strip(),
            "source": url,
            "content": text
        }
        
    except Exception as e:
        logger.warning(f"Failed to scrape {url}: {e}")
        return None
