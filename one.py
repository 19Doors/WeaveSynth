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

enc = tiktoken.encoding_for_model("gpt-4")

def token_length(text):
    """Calculate number of tokens in a text using GPT-4 tokenizer."""
    return len(enc.encode(text))

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter_base_url = os.getenv("OPENROUTER_BASE_URL")

def create_undetectable_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("start-maximized")  # Maximize to avoid headless detection
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36") #Setting a custom user agent[3][4]

    driver = webdriver.Chrome(options=options)

    # Apply Selenium Stealth settings
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
You are an expert news article extractor. You will be given the HTML content of a news webpage and its URL.

Your task is to extract the following information automatically:
- source_url: The URL of the news article (this should be the same as the URL provided below).
- title: The main headline of the article.
- source_publisher: The name of the news publisher (e.g., BBC News, Reuters). If unknown, return null.
- body: The main textual content of the article, cleaned and free of navigation, ads, and boilerplate.

Please output the extracted information strictly as a JSON object with the keys: source_url, title, source_publisher, and body.

HTML Content:
\"\"\"
\"\"\"

URL:

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
                    chunk_size=120000,  # Characters per chunk (adjust based on typical paragraph/section size and LLM input preference)
                    chunk_overlap=12000, # Overlap to maintain context
                    length_function=token_length,
                    )
    chunks=text_splitter.split_text(str(soup))
    print(len(chunks))
    return chunks

def scrape(url, thumbnail_url):

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )

    merged_chunks_result=""
    def process_chunk(i,chunk):
          prompt = f"""
                Given an HTML chunk, chunk number: {i} \n of a larger article, analyze it, don't give explanation, convert it into markdown format.


                Instructions:
                1. Make sure you DO NOT ALTER/CHANGE/MAKE any text by your own.
                2. Remove all Ads/Not relevant things like copyright or nav.
                3. Remove anything other than the main article, remove all the side or extra articles and their data.
                4. Don't give any html tags instead you can convert to headings or subheadings or any markdown tag.

                Chunk: {chunk}
            """
          result=llm.invoke(prompt)
          return str(result.content)

    def combine(file):
        with open(file) as f:
              content=f.read()
              result=llm.invoke(f"""
                Given jsons from multiple chunks, combine them into one, making sure to remove all advertisements, make sure body contains the whole article content(make sure you do not change text, you just combine them, same with title) and remove param "is_ad". Don't give any explanation, content: {content}
                """)
              with open("c.txt","w") as ff:
                    ff.write(result.content)

    def reset(files):
          for i in files:
                with open(i,'w') as f:
                      f.write("")

    reset(["b.txt",'c.txt'])
    chunks = page_extract(url)

    if chunks is None:
        print("No chunks to process, likely a page load failure.")
        return None

    for index,chunk in enumerate(chunks):
          print("Processing Chunk",index)
          result=process_chunk(index,chunk)
          merged_chunks_result+=result+"\n"

    # print(merged_chunks_result)
    result=llm.invoke(f"""
        Given a webpage, scrape the following in json format
        [
            {{
		"title": "str",
		"summary" : "str",
		"content" : "str in markdown, could contain images",
		"thumbnail_url" : "{thumbnail_url}"
		"url" : "{url}",
		"source" : "str",
		"keywords" : ["ABC"],
		"category" : "str, options: general, business, sports, nature"
            }}
        ]

        Don't give any explanation whatsoever
        Markdown text: {merged_chunks_result}
    """)

    return result.content
