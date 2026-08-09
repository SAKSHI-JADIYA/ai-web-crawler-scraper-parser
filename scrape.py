from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.parse import urljoin, urlparse
import os

# Load environment variables from .env file
load_dotenv()

CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "./chromedriver.exe")

def scrape_page(url):
    """Scrape a single page with Selenium and return HTML."""
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html

def crawl_site(base_url, max_pages=20):
    """Crawl a site starting from base_url, following internal links."""
    to_visit = [base_url]
    visited = set()
    all_html = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            html = scrape_page(url)
            all_html.append(html)

            soup = BeautifulSoup(html, "html.parser")
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    if full_url not in visited:
                        to_visit.append(full_url)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    return all_html

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    # Keep all text nodes
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content
