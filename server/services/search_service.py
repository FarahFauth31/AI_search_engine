import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from config import Settings
from tavily import TavilyClient
import trafilatura

settings = Settings()
tavily_client = TavilyClient(api_key = settings.TAVILY_API)

class SearchService:
    def web_search(self, query: str):
        # create different queries to search google
        # or tavily
        results = []
        try:
            response = tavily_client.search(query, max_results=5)
            search_results = response.get("results", [])

            for result in search_results:
                downloaded_content = trafilatura.fetch_url(result.get('url'))
                content = trafilatura.extract(downloaded_content, include_comments=False)
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url"),
                    "content": content,
                })
            return results
        
        except Exception as e:
            print("Unexpected error in Search Service occurred: ", e)
            return []