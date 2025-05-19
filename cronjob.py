import json
from getURLs import get_urls
from per import perplexity_results
from one import scrape
import os
from dotenv import load_dotenv
import libsql_experimental as libsql
load_dotenv()

raw_urls=get_urls("World News Articles")
number_of_urls=3

url = os.getenv("DATABASE_URL")
auth_token = os.getenv("DATABASE_AUTH_TOKEN")

conn = libsql.connect("weavesynth.db", sync_url=url, auth_token=auth_token)
conn.sync()
print("CONNECTED")

articles=[]
r=""
for i in range(1000):
    if number_of_urls==0:
        break

    url=raw_urls[i]["link"]
    # Check if url is already present in db
    articlesLen = len(conn.execute(f"select * from articles as a where a.url='{url}'").fetchall())
    if(articlesLen>0):
        print("Already exists")
        continue

    number_of_urls-=1
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

for article in articles:
    keywords=",".join(article['keywords'])
    cmd="""insert into articles (url, title, summary, content, thumbnail_url, source, keywords, category) values (?, ?, ?, ?, ?, ?, ?, ?)"""
    values_to_insert = (
        article['url'],
        article['title'],
        article['summary'],
        article['content'],
        article['thumbnail_url'],
        article['source'],
        keywords,
        article['category']
    )
    result_set = conn.execute(cmd, values_to_insert)
    conn.commit()
    print(f"Successfully inserted article with url: {article['url']}")
