from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Path to your local ChromeDriver (set in .env as CHROMEDRIVER_PATH or defaults to ./chromedriver.exe)
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "./chromedriver.exe")


def scrape_website(website):
    print("Launching local ChromeDriver...")

    options = Options()
    options.add_argument("--start-maximized")

    # Start a local Chrome session
    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

    driver.get(website)

    # --- Optional: CAPTCHA Solver Integration ---
    # Selenium alone cannot solve CAPTCHAs.
    # If you want to integrate an external solver (like 2Captcha or Anti-Captcha):
    # 1. Sign up at the solver service website.
    # 2. Install their Python SDK (e.g., pip install 2captcha-python).
    # 3. Get your API key.
    # 4. Replace the placeholder code below with the snippet provided by the solver service.
    # 5. Uncomment it to enable CAPTCHA solving.
    #
    # Example (placeholder only):
    # from twocaptcha import TwoCaptcha
    # solver = TwoCaptcha('YOUR_API_KEY')
    # result = solver.recaptcha(
    #     sitekey='SITE_KEY',
    #     url=website
    # )
    # driver.execute_script(
    #     f'document.getElementById("g-recaptcha-response").value="{result["code"]}"'
    # )
    # ------------------------------------------------

    print("Navigated! Scraping page content...")
    html = driver.page_source
    driver.quit()
    return html



def extract_body_content(html_content):
     soup= BeautifulSoup(html_content,"html.parser")
     body_content = soup.body
     if body_content:
        return str(body_content)
     return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content,"html.parser")
# Remove scripts and styles
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get cleaned text
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
