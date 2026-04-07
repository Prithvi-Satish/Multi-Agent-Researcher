from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(query: str, max_results: int = 5) -> list[dict]:
    """Search the web and return results with URLs and snippets."""
    response = client.search(
        query=query,
        max_results=max_results,
        include_raw_content=False,
        search_depth="advanced"
    )
    results = []
    for r in response.get("results", []):
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", "")
        })
    return results
