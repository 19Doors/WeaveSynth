from serpapi import search

def get_urls(query):
    params = {
      "engine": "google_news",
      "q": query,
      "hl": "en",
      "api_key": "84398d532c48aaa41d4c4bdcf339c241ea040e9eb1b707021df2d0cc04e031c8"
    }

    search_results = search(params)
    results = search_results["news_results"]
    return results
