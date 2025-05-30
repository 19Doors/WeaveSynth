import json
from getURLs import get_urls
from hashing import url_to_sha256_id
from per import perplexity_results
from one import scrape
import os
from dotenv import load_dotenv
import libsql_experimental as libsql
load_dotenv()

url = os.getenv("DATABASE_URL")
auth_token = os.getenv("DATABASE_AUTH_TOKEN")

conn = libsql.connect("weavesynth.db", sync_url=url, auth_token=auth_token)
conn.sync()
print("CONNECTED")

articles=[]
r = scrape("https://news.google.com/search?q=world%20news&hl=en-US&gl=US&ceid=US%3Aen")
number_of_urls=3
i=0
while i<len(r) and number_of_urls!=0:
    url = r[i]['url']
    i+=1
    articlesLen = len(conn.execute(f"select * from articles as a where a.url='{url}'").fetchall())
    if(articlesLen>0):
        print("Already exists")
        continue

    number_of_urls-=1
    articles.extend(r[i-1])

if(len(articles)!=0):
    try:
        per_results = perplexity_results(articles)
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
        cmd="""insert into articles (id, url, title, summary, content, thumbnail_url, source, keywords, category) values (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values_to_insert = (
            url_to_sha256_id(article['url']),
            article['url'],
            article['title'],
            article['summary'],
            article['content'],
            article['thumbnail_url'],
            article['source'],
            keywords,
            article['category']
        )
        try:
            result_set = conn.execute(cmd, values_to_insert)
            conn.commit()
            print(f"Successfully inserted article with url: {article['url']}")
        except:
            print(f"Error inserting article with url {article['url']}")
