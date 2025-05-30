from typing import List, Optional
import random
from pydantic import BaseModel, Field
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup, NavigableString, Comment
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureChatOpenAI, ChatOpenAI
import os
from dotenv import load_dotenv
import tiktoken
import json
from selenium_stealth import stealth  # Import Selenium Stealth
from per import perplexity_results

# Define the data structure using Pydantic
class ArticleMetadata(BaseModel):
    title: str = Field(description="Main article headline (clean text, no HTML tags)")
    url: str = Field(description="Full article link (must be a complete, valid URL)")
    thumbnail_url: Optional[str] = Field(description="Primary image URL", default="")
    source_publisher: Optional[str] = Field(description="Publication name", default="N/A")

class ArticleList(BaseModel):
    articles: List[ArticleMetadata] = Field(description="List of extracted articles")

load_dotenv()

enc = tiktoken.encoding_for_model("gpt-4")

def token_length(text):
    """Calculate number of tokens in a text using GPT-4 tokenizer."""
    return len(enc.encode(text))

# load_dotenv()

# openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
# openrouter_base_url = os.getenv("OPENROUTER_BASE_URL")

def create_undetectable_chrome_driver():
    options = webdriver.ChromeOptions()
    
    # Enhanced anti-detection options
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Randomize window size
    window_sizes = ["1920,1080", "1366,768", "1440,900", "1536,864"]
    selected_size = random.choice(window_sizes)
    options.add_argument(f"--window-size={selected_size}")
    
    # Rotate user agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    options.add_argument(f"user-agent={random.choice(user_agents)}")
    
    # Additional stealth options
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")  # Faster loading
    options.add_argument("--disable-javascript")  # Optional: disable JS if not needed
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-default-apps")
    
    # Proxy rotation (optional - add your proxy list)
    # options.add_argument("--proxy-server=http://your-proxy:port")

    driver = webdriver.Chrome(options=options)
    
    # Execute script to remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Apply Selenium Stealth settings with randomized parameters
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    return driver

driver = create_undetectable_chrome_driver() # Create the driver

prompt_str = f"""
You are an expert information extractor. You will be given the HTML content of a webpage and its URL.

Your task is to extract the following information automatically:
- source_url: The URL of the news article.
- title: The main headline of the article.
- source_publisher: The name of the news publisher (e.g., BBC News, Reuters). If unknown, return null.
- thumbnail_url: thumbnail url. If unknown, return ""

Please output the extracted information strictly as a JSON object with the keys: source_url, title, source_publisher, and thumbnail_url

HTML Content:
\"\"\"
\"\"\"

Output JSON:
"""

def page_extract(url):
    print("# Fetching Page",url)
    driver.get(url)

    # Wait for the page to load completely
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))  # Wait for the body tag
        )
    except:
        print("Page Load Timeout")
        return None

    page_source = driver.page_source
    print("# Preprocessing")
    soup = BeautifulSoup(page_source,"html.parser")
    for tag_name in ['script', 'style', 'iframe', 'svg', 'path', 'noscript', 'form', 'button', 'input', 'textarea', 'label', 'meta', 'link']:
        for tag in soup.find_all(tag_name):
            tag.decompose()
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    boilerplate_selectors = [
        "nav", "aside", "header[role='banner']", "footer[role='contentinfo']",
        "div#orb-banner", "div#orb-footer", ".advertisement", ".ad-slot",
        ".related-articles", ".sidebar", ".share-tools", ".comments-section",
        "[class*='cookie']", "[id*='cookie']", "[class*='modal']", "[id*='modal']",
        "[class*='popup']", "[id*='popup']", "[aria-modal='true']"
    ]
    for selector in boilerplate_selectors:
        for tag in soup.select(selector):
            tag.decompose()


    text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=500000,  # Characters per chunk (adjust based on typical paragraph/section size and LLM input preference)
                    chunk_overlap=50000, # Overlap to maintain context
                    length_function=token_length,
                    )
    chunks=text_splitter.split_text(str(soup))
    print(len(chunks))
    return chunks

def scrape(url):

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )

    structured_llm = llm.with_structured_output(ArticleList)

    def process_chunk(i,chunk):
        prompt_str = f"""
            Act as a web content analyzer. I need you to extract article metadata from the provided content. 

            **Task**: Extract the following fields for each article:
            - **Title**: Main article headline (clean text, no HTML tags)
            - **URL**: Full article link (must be a complete, valid URL and should not contain google news)
            - **Thumbnail URL**: Primary image URL (preferably high resolution)
            - **Source Publisher**: Publication name (e.g., "BBC News", "The Guardian")

            **Requirements**:
            - Skip any content that isn't a news article (ads, navigation, etc.)
            - Ensure URLs are complete and functional
            - For thumbnails, prioritize the main article image over logos or icons
            - Standardize publisher names (remove "www." or ".com" suffixes)
            - If any field is missing, mark it as "N/A"
            - Give top 3

            **Output Format**: JSON array with consistent structure

            **Content to analyze**:
            {chunk}
        \"\"\"
        \"\"\"
        """
        result=structured_llm.invoke(prompt_str)
        return result

    def reset(files):
          for i in files:
                with open(i,'w') as f:
                      f.write("")

    reset(["b.txt",'c.txt'])
    chunks = page_extract(url)

    if chunks is None:
        print("No chunks to process, likely a page load failure.")
        return None

    
    # for index,chunk in enumerate(chunks):
    #       print("Processing Chunk",index)
    #       result=process_chunk(index,chunk)
    #       merged_chunks_result+=result+"\n"

    result = process_chunk(1,chunks[0])
    result = result.model_dump()
    print(result)
    articles = result['articles']
    with open("scrapedData.json",'w') as f:
        f.write(json.dumps(articles,indent=2))
    print("Data Saved in scrapedData.json")
    # print(merged_chunks_result)
    return articles

