import requests
import os
import json
from dotenv import load_dotenv
import urllib3
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

urllib3.disable_warnings()

class ExpandedArticle(BaseModel):
    title: str
    summary: str
    content: str  # Markdown content, LLM should escape newlines as \\n
    thumbnail_url: Optional[HttpUrl] = None # Making it optional and validating as a URL
    url: Optional[HttpUrl] = None           # Original or relevant URL, optional
    source: Optional[str] = None            # Original source, optional
    keywords: List[str]
    category: str # e.g., "general", "business", "sports", "nature"

class ArticleListResponse(BaseModel):
    articles: List[ExpandedArticle]

# load_dotenv()
perplexity_api=os.getenv("PERPLEXITY_API")
model="sonar-pro"
search_context_size="medium"
search_domain_filter=["https://edition.cnn.com/","https://www.bbc.com/","https://www.nytimes.com/","https://www.washingtonpost.com/","https://indianexpress.com/","https://timesofindia.indiatimes.com/","https://www.hindustantimes.com/","https://www.ndtv.com/","https://www.indiatoday.in/","https://www.thehindu.com/"]
system_prompt=""
with open("system_prompt.txt") as f:
    system_prompt=f.read()

def perplexity_results(articles):
    query=f"""
    Please expand on the following news articles, using its titles and contents as a foundation. Conduct web research to gather more details, provide deeper context, elaborate on key points, and incorporate any relevant recent developments or background information. The new, AI-generated articles should be significantly more in-depth and comprehensive than the original, while staying true to the core subject matter.
    Give the result in json format:
        [{{
		"title": "str",
		"summary" : "str",
		"content" : "str in markdown, could contain images 
        "thumbnail_url" : optional: "str"
		"url" : "str",
		"source" : "str",
		"keywords" : ["ABC"],
		"category" : "str, options: general, business, sports, nature"
        }}]

    The number of articles should remain the same and so should be the thumbnail url for each article(if no thumbnail then take one that is the most similar from the content itself), just title,summary and content should be different.
    Original List of Raw Articles: [{articles}]
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
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": ArticleListResponse.model_json_schema()},
        },
        #"search_domain_filter": search_domain_filter
    }

    response = requests.post(url, headers=headers, json=payload, verify=False).json()
    json_response=(response["choices"][0]["message"]["content"])
    json_response=json.loads(json_response)
    print(json_response)
    json_response=json_response["articles"]
    # si=json_response.find("[")
    # ei=json_response.rfind("]")
    # json_dump = json.loads(json_response[si:ei+1])
    return json_response
    json_response=json.dumps(json_response,indent=2)
    with open("one.json","w") as f:
        f.write(json_response)
    #response = requests.get(url, verify=False)
    print(response["citations"])
