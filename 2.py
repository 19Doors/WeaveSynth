from fastapi import FastAPI
import requests
import os
import json
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings()
load_dotenv()

perplexity_api=os.getenv("PERPLEXITY_API")
model="sonar"
search_context_size="low"
search_domain_filter=["https://edition.cnn.com/","https://www.bbc.com/","https://www.nytimes.com/","https://www.washingtonpost.com/","https://indianexpress.com/","https://timesofindia.indiatimes.com/","https://www.hindustantimes.com/","https://www.ndtv.com/","https://www.indiatoday.in/","https://www.thehindu.com/"]
system_prompt=""
with open("system_prompt.txt") as f:
    system_prompt=f.read()

query="""
User Location Context:
  Country: India
  City: Mumbai
  Region: Maharashtra

Request:
Generate a set of news articles covering current events at different scales, specifically:
1.  Atleast three article on a top GLOBAL news story.
2.  Atleast two article on a top NATIONAL news story relevant to 'India'.
3.  Atleast two article on a top LOCAL news story relevant to 'Mumbai, Maharashtra'.

Instructions for WeaverSynth:
- Your response MUST be a single JSON array containing article objects.
- Each article object MUST strictly follow the JSON structure defined in the System Prompt (including fields like "id", "scale", "topicContext", "title", "introduction", "sections", "sources", "generatedAt", "image_urls").
- For the "id" field in each article object, generate a unique UUID.
- For the "scale" field, correctly label each article as 'global', 'national', or 'local'.
- The "topicContext" field should briefly describe the event each article is about.
- Focus on significant developments from the past 24-48 hours for all articles.
- Each article should synthesize information from atleast 2-3 reputable sources.
- Each article MUST be well-structured with a compelling introduction (if appropriate) that summarizes the key points.
- Each article MUST have at least 4 sections, each with a descriptive subheading and several paragraphs of content.
- Each paragraph MUST be in detail.
- Each section should provide in-depth coverage of a specific aspect of the news story.
- Aim for a total word count of approximately 700-800 words per article to ensure sufficient depth and detail.
- Add bullet points or numbered lists where appropriate to present information clearly.
- Ensure the content is factually accurate and cite sources appropriately.
- The "generatedAt" field should be the current UTC timestamp in ISO 8601 format.
- Write in a clear, and engaging journalistic style.

"""
url = "https://api.perplexity.ai/chat/completions"
headers = {"Authorization": f"Bearer {perplexity_api}"}  
payload = {
    "model": model,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ],
    "web_search_options": {
        "search_context_size": search_context_size
    },
    #"search_domain_filter": search_domain_filter
}

app = FastAPI()
root_data={}

@app.get("/")
async def root():
    response = requests.post(url, headers=headers, json=payload, verify=False).json()
    json_response=str(response["choices"][0]["message"]["content"])
    start_index=json_response.find("[")
    end_index=json_response.rfind("]")
    json_response=json_response[start_index:end_index+1]
    json_response=json.loads(json_response)
    root_data=json_response
    return json_response

@app.post("/article/{article_id}")
async def create_or_update_article_data(article_id:str):
    for article in root_data:
        if(article["id"]==article_id):
            return article

    return {}
