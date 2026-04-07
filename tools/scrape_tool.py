import requests
from bs4 import BeautifulSoup

def scrape_page(url: str, max_chars: int = 1000) -> str:
    """Fetch a URL and return clean readable text."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove noise
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        # Return first max_chars to stay within token limits
        return text[:max_chars]
    except Exception as e:
        return f"Could not scrape {url}: {str(e)}"
