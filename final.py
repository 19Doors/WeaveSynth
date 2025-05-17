import json
from getURLs import get_urls
from per import perplexity_results
from one import scrape
from fastapi import FastAPI

app = FastAPI()

@app.get("/getArticles")
async def getWorldNews():
    raw_urls=get_urls("Global News Articles")
    # raw_urls=["https://www.bbc.com/news/articles/c2e373yzndro",
    #           "https://www.bbc.com/news/articles/cgmj7l0lne3o"]

    articles=[]
    r=""
    for i in range(2):
        url = raw_urls[i]["link"]
        # url = raw_urls[i]
        print("# Creating Article :",url)
        scraped_data=scrape(url,raw_urls[i]["thumbnail"])
        r=r+scraped_data+"\n"
    print("="*30)
    print("Perplexity Results:")
    try:
        per_results = perplexity_results(r)
        articles=per_results
        # print(result)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")

    print("="*30)
    print("Articles:")
    print("="*30)
    print(articles)
    return articles
