from googlesearch import search
import warnings
warnings.filterwarnings("ignore")

def find_company_website(company_name):
    try:
        # Search Google for the company's website
        query = f"{company_name} official website"
        for result in search(query, num_results=1, lang='fr'):  # Get the first result
            return result
    except Exception as e:
        print(f"Error searching for company website: {e}")
        return None
    
import requests
from bs4 import BeautifulSoup
# import asyncio

# async def scrape_company_website_handlecookies(url):
#     try:
#         # Use async_playwright as a context manager
#         async with async_playwright() as playwright:
#             # Launch a headless browser
#             browser = await playwright.chromium.launch(headless=True)
#             page = await browser.new_page()
            
#             # Navigate to the website
#             await page.goto(url)
            
#             # Wait for the cookie banner to appear and click "Accept"
#             try:
#                 await page.click("text=Accepter", timeout=5000)  # Click "Accept" button
#             except Exception as e:
#                 print(f"Cookie banner not found or already accepted: {e}")
            
#             # Get the page content after accepting cookies
#             content = await page.content()
            
#             # Close the browser
#             await browser.close()

#             # Parse the content with BeautifulSoup
#             soup = BeautifulSoup(content, "html.parser")
#             text = " ".join(p.get_text().strip() for p in soup.find_all(["p", "h1", "h2", "h3", "article"]))
            
#             # Filter out unwanted phrases
#             unwanted_phrases = [
#                 "copyright", "all rights reserved", "trademark", "legal notice",
#                 "terms of use", "terms and conditions", "privacy policy", "cookie policy",
#                 "©", "®", "™", "patent", "intellectual property"
#             ]
#             filtered_text = " ".join(
#                 sentence for sentence in text.split(".") 
#                 if not any(phrase.lower() in sentence.lower() for phrase in unwanted_phrases)
#             )

#             return filtered_text
#     except Exception as e:
#         print(f"Error scraping website: {e}")
#         return None
    
def scrape_company_website(url):
    try:
        print(f"Fetching URL: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract text from meaningful tags
        text = " ".join(p.get_text().strip() for p in soup.find_all(["p", "h1", "h2", "h3", "article"]))

        # Filter out unwanted phrases (e.g., copyright-related text)
        unwanted_phrases = [
            "copyright", "all rights reserved", "trademark", "legal notice",
            "terms of use", "terms and conditions", "privacy policy", "cookie policy",
            "©", "®", "™", "patent", "intellectual property"
        ]
        filtered_text = " ".join(
            sentence for sentence in text.split(".") 
            if not any(phrase.lower() in sentence.lower() for phrase in unwanted_phrases)
        )

        return filtered_text
    except Exception as e:
        print(f"Error scraping website(Could becookies related): {e}")
        return None

    
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# IBM Watson API setup
API_KEY = os.getenv("API_KEY")
url = "https://iam.cloud.ibm.com/identity/token"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": API_KEY,
}

response = requests.post(url, headers=headers, data=data)
if response.status_code == 200:
    token_info = response.json()
    ACCESS_TOKEN = token_info["access_token"]
else:
    raise Exception(f"Error getting access token: {response.text}")

API_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}

def summarize_text(text, model_id="ibm/granite-3-2b-instruct", max_tokens=300):
    try:
        # Prepare the prompt for summarization
        prompt = f"Summarize the content of this scrapped website to provide a comprehensive overview of the company's nature, operations, work, and other relevant details. Focus only on delivering the summary without additional commentary:\n\n{text}"

        # Prepare the request body
        body = {
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "max_new_tokens": max_tokens,
                "min_new_tokens": 0,
                "repetition_penalty": 1,
            },
            "model_id": model_id,
            "project_id": "7f1f5582-3e1f-4330-a539-e2d20b58041e",  # Replace with your project ID
        }

        # Send the request to IBM Watson
        response = requests.post(API_URL, headers=HEADERS, json=body)
        if response.status_code == 200:
            try:
                return response.json()["results"][0]["generated_text"]
            except (KeyError, IndexError):
                return "Error: Unexpected response format from IBM API"
        else:
            return f"Error: IBM API returned {response.status_code} - {response.text}"
    except Exception as e:
        print(f"Error summarizing text with IBM Watson: {e}")
        return None
    
def get_company_info(company_name):
    # Step 1: Find the company's website
    website_url = find_company_website(company_name)
    if not website_url:
        return {
            "company": company_name,
            "data": "Failed to find the company's website.",
        }

    # Step 2: Scrape the company's website
    # text = scrape_company_website_handlecookies(website_url)
    text = scrape_company_website(website_url)
    print('text', text) 
    if not text:
        return {
            "company": company_name,
            "data": "Failed to scrape the company's website.",
        }

    # Step 3: Summarize the scraped text
    summary = summarize_text(text)
    if not summary:
        return {
            "company": company_name,
            "full data": text,
            "data": "Failed to summarize the company's information.",
        }

    return {
        "company": company_name,
        "website": website_url,
        "full data": text,
        "data": summary,
    }

# if __name__ == "__main__":
#     company_name = "J-Texon"  # Replace with the company name
#     result = get_company_info(company_name)
#     print(result)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for your Next.js app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", 'https://leads-gen-ai.vercel.app'],  # Replace with your Next.js app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/company-info")
async def company_info(company: str):
    result = get_company_info(company)
    return result
