import json
import os
import urllib.request
from dotenv import load_dotenv
load_dotenv()

apikey = os.getenv("NEWS_API")

def getArticles(category):
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max=10&apikey={apikey}"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]
        return articles
