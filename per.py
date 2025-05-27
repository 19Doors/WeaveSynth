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
    query = f"""
    You are a professional news editor and journalist. Your task is to transform the provided raw articles into comprehensive, well-researched news pieces that meet professional journalism standards.

    **Instructions:**
    1. **Expand and Enhance**: Take each article's core information and significantly expand it with:
       - Additional context and background information
       - Expert analysis and implications
       - Related developments and connections to broader trends
       - Multiple perspectives on the topic
       - Relevant data, statistics, or quotes (when appropriate)

    2. **Professional News Standards**: Ensure each article follows proper journalistic structure:
       - Compelling, accurate headlines that capture the essence
       - Lead paragraphs that answer who, what, when, where, why
       - Inverted pyramid structure (most important information first)
       - Objective, balanced tone with proper attribution
       - Clear, engaging writing suitable for general audiences

    3. **Content Requirements**:
       - **Title**: Create engaging, informative headlines (60-80 characters)
       - **Summary**: Write compelling 2-3 sentence summaries that hook readers
       - **Content**: Develop comprehensive articles (300-500 words) in markdown format
       - **Structure**: Use proper headings (##), subheadings (###), bullet points, and formatting
       - **Images**: Include relevant image suggestions in markdown format where appropriate

    4. **Maintain Integrity**:
       - Keep the same number of articles as provided
       - Preserve original thumbnail URLs (if available)
       - Maintain the core subject matter and factual foundation
       - Ensure accuracy while expanding content

    **Output Format (JSON):**
    [{{
    "title": "Engaging, professional headline"(str),
    "summary": "Compelling 2-3 sentence summary that draws readers in"(str),
    "content": "Comprehensive markdown content with proper formatting, headings, and structure. Include relevant details, context, and analysis while maintaining journalistic integrity."(str),
    "thumbnail_url": "original_url_or_most_relevant_alternative"(str),
    "url": "original_source_url"(str),
    "source": "original_source_name"(str),
    "keywords": ["relevant", "keywords", "for", "SEO"](["ABC"]),
    "category": "general|business|sports|nature|technology|politics|health|entertainment"(str)
    }}]

    **Categories Available**: general, business, sports, nature, technology, politics, health, entertainment

    **Original Articles to Transform:**
    {articles}

    Transform these articles into professional, comprehensive news pieces that would be suitable for publication in a major news outlet.
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
