import requests
import os
import json
from dotenv import load_dotenv
import urllib3
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

load_dotenv()

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
search_context_size="low"
search_domain_filter=["https://edition.cnn.com/","https://www.bbc.com/","https://www.nytimes.com/","https://www.washingtonpost.com/","https://indianexpress.com/","https://timesofindia.indiatimes.com/","https://www.hindustantimes.com/","https://www.ndtv.com/","https://www.indiatoday.in/","https://www.thehindu.com/"]
system_prompt=""
with open("system_prompt.txt") as f:
    system_prompt=f.read()

def perplexity_results(content):
    query = f"""
        Generate comprehensive, professional news articles based on the following topic information. For each topic, conduct thorough research and create a complete news article that covers all relevant aspects of the subject.

        **Instructions for Each Topic:**
        1. **Research Thoroughly**: Use the provided title to research current developments, background information, expert opinions, and related news
        2. **Create Original Content**: Generate a unique headline (different from the input title), compelling summary, and comprehensive article content
        3. **Maintain Professional Standards**: Follow journalistic best practices with proper structure, attribution, and balanced reporting
        4. **Preserve Metadata**: Keep the original url, thumbnail, and source information exactly as provided
        5. **Add Value**: Include statistics, expert quotes, multiple perspectives, and contextual information

        **Research Focus Areas:**
        - Latest developments and current status
        - Background and historical context
        - Expert opinions and analysis
        - Impact and implications
        - Related trends and connections
        - Supporting data and statistics


        Generate only one professional, well-researched news article for each topic that would be suitable for publication in a major news outlet.
    **Output Format (JSON):**
    [{{
    "title": "Engaging, professional headline"(str),
    "summary": "Compelling 2-3 sentence summary that draws readers in"(str),
    "content": "Comprehensive markdown content with proper formatting, headings, and structure. Include relevant details, context, and analysis while maintaining journalistic integrity."(str),
    "thumbnail_url": "original_url_or_null"(str), Original thumbnail url
    "url": "original_source_url"(str). It should be the original url
    "source": "original_source_name"(str). Original Source
    "keywords": ["relevant", "keywords", "for", "SEO"](["ABC"]),
    "category": "general|business|sports|nature|technology|politics|health|entertainment"(str)
    }}]

    **Categories Available**: general, business, sports, nature, technology, politics, health, entertainment

    **Topics to Research and Generate Articles For:**
    {content}
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
    }

    response = requests.post(url, headers=headers, json=payload, verify=False).json()
    json_response=(response["choices"][0]["message"]["content"])
    json_response=json.loads(json_response)
    json_response=json_response["articles"]
    # print(json_response)
    json_response_json = json.dumps(json_response,indent=2)
    with open("perOutput.json","w") as f:
        f.write(json_response_json)
    # si=json_response.find("[")
    # ei=json_response.rfind("]")
    # json_dump = json.loads(json_response[si:ei+1])
    return json_response
    json_response=json.dumps(json_response,indent=2)
    #response = requests.get(url, verify=False)
    print(response["citations"])
