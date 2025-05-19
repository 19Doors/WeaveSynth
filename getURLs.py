import os
from serpapi import search

serp_key = os.getenv("SERPAPI_KEY")
def get_urls(query):
    params = {
      "engine": "google_news",
      "q": query,
      "hl": "en",
      "api_key": serp_key
    }

    search_results = search(params)
    results = search_results["news_results"]
    return results
