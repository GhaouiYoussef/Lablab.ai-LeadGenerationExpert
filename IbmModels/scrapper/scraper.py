import os
import requests
import warnings
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

warnings.filterwarnings("ignore")

# Load environment variables
BROWSERLESS_API_KEY = os.getenv("BROWSERLESS_API")

def find_company_website(company_name):
    """Find the official website of a company using Google Search."""
    from googlesearch import search

    try:
        query = f"{company_name} official website"
        results = list(search(query, num_results=1, lang='fr'))
        return results[0] if results else None
    except Exception as e:
        print(f"Error searching for company website: {e}")
        return None

def scrape_with_selenium(url):
    """Scrape a website using Selenium with Browserless."""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.set_capability('browserless:token', BROWSERLESS_API_KEY)
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        driver = webdriver.Remote(
            command_executor="https://chrome.browserless.io/webdriver",
            options=chrome_options
        )

        driver.get(url)

        # Handle potential cookie popups
        try:
            cookie_accept = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept') or contains(., 'Agree')]"))
            )
            cookie_accept.click()
        except Exception:
            pass  # No cookie banner found

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        return extract_text(soup)
    
    except Exception as e:
        print(f"Selenium scraping error: {e}")
        if 'driver' in locals():
            driver.quit()
        return None

def scrape_company_website(url):
    """Scrape a website using Requests first, fallback to Selenium if needed."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Cookie": "cookies_accepted=true; cookie_consent=accepted;"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        return extract_text(soup)
    
    except requests.RequestException as e:
        print(f"Requests scraping error: {e}")
        return scrape_with_selenium(url)

def extract_text(soup):
    """Extract and clean text from HTML using BeautifulSoup."""
    text = " ".join(p.get_text().strip() for p in soup.find_all(["p", "h1", "h2", "h3", "article"]))
    
    # Remove unwanted phrases
    unwanted_phrases = {"copyright", "all rights reserved", "trademark", "legal notice",
                        "terms of use", "terms and conditions", "privacy policy", "cookie policy",
                        "©", "®", "™", "patent", "intellectual property"}
    
    return " ".join(sentence for sentence in text.split(".") if not any(phrase in sentence.lower() for phrase in unwanted_phrases))
