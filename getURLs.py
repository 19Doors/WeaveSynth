import os
from serpapi import search
from dotenv import load_dotenv

# load_dotenv()

serp_key = os.getenv("SERPAPI_KEY")
def get_urls(query):

    if not serp_key:
        raise ValueError("SERPAPI_KEY environment variable is not set")
    params = {
      "engine": "google_news",
      "q": query,
      "hl": "en",
      "api_key": serp_key,
    }

    search_results = search(params)
    results = search_results["news_results"]
    return results
