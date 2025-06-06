import json
from articles import getArticles
from hashing import url_to_sha256_id
from per import perplexity_results
import os
from dotenv import load_dotenv
import libsql_experimental as libsql
load_dotenv()

url = os.getenv("DATABASE_URL")
auth_token = os.getenv("DATABASE_AUTH_TOKEN")

conn = libsql.connect("weavesynth.db", sync_url=url, auth_token=auth_token)
conn.sync()
print("CONNECTED")

articles=getArticles("world")
final_articles=[]
number_of_urls=3
i=0
while i<len(articles) and number_of_urls!=0:
    url = articles[i]['url']
    i+=1
    articlesLen = len(conn.execute(f"select * from articles as a where a.url='{url}'").fetchall())
    if(articlesLen>0):
        print("Already exists")
        continue

    number_of_urls-=1
    thisarticle = {"title":articles[i-1]['title'],"url":articles[i-1]['url'],"thumbnail_url":articles[i-1]['image'],"source":articles[i-1]['source']}
    final_articles.append(thisarticle)

if(len(final_articles)!=0):
    try:
        per_results = perplexity_results(final_articles)
        articles=per_results
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
