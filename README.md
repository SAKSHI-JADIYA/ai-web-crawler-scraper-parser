# AI Web Scraper & Parser

A modular Web Scraper and Parser application built to crawl websites, extract and clean DOM content, and leverage a local Llama 3.1 model to parse data directly into structured Markdown tables based on custom user prompts.

## Tech Stack

- **Streamlit**: Web interface and conversational execution state orchestration.
- **LangChain & LangChain-Ollama**: Model prompt management, context-chaining, and model pipeline control.
- **Selenium**: Automated web browser control for handling static, dynamic, and JavaScript-heavy pages.
- **BeautifulSoup4**: HTML syntax traversal, structural content isolation, and text noise removal.
- **Lxml & Html5lib**: High-performance parser engines for resilient HTML structure decoding.
- **Python-Dotenv**: Decoupled environmental property declaration for system assets.

## How It Works


<img width="1408" height="768" alt="image" src="https://github.com/user-attachments/assets/6e930230-8e5f-4f5a-9ff8-f1e3c0789e86" />


1. **Request & Initialization**: The user selects a target scope and triggers the web action inside the Streamlit frontend (`main.py`).
2. **Browser Emulation & Crawling**: The execution layer (`scrape.py`) fires up a Chrome instance using Selenium WebDriver to gather source files. Depending on the operational depth chosen, it isolates specific sub-links within the domain boundary.
3. **Data Scrubbing**: Content is piped into BeautifulSoup. It drops non-semantic elements like `<script>` and `<style>` blocks, normalizes white space, and condenses structural text.
4. **State Persistence**: The application caches the cleaned, full-text data layout inside Streamlit Session State memory. This prevents context loss when the app refreshes during subsequent actions.
5. **Context Window Chunking**: To meet the specific constraint boundaries of the target LLM, the data engine cuts the text down into individual, smaller byte chunks.
6. **Local LLM Parsing**: The system builds structured instructions using LangChain ChatPromptTemplates and streams the individual content pieces down to a local instance of Ollama running Llama 3.1 (`parse.py`).
7. **Response Aggregation**: The resulting text fragments are consolidated on-the-fly and rendered visually on the UI dashboard as a fully formatted Markdown data table.

## Core Features

### Single Page Mode
- targets the primary top-level domain URL provided by the user.
- Quickly handles isolated pages, landing pages, and standalone data sheets without traversing sub-links.
- Ideal for fast, highly directed parsing of known schemas.

### Full Site Crawling Mode
- Recursively discovers and builds an processing queue from internal hyperlinks that match the base host domain network layout.
- Processes up to a specified threshold dynamically (defaulting to 10 pages deep).
- Combines disparate page layouts into a single consolidated string block for batch semantic entity resolution.

## Prerequisites

- Python 3.10 or higher
- Google Chrome Browser installed
- Chrome WebDriver matching your browser version
- Ollama framework running locally

## Installation

1. Install the required project dependencies:
```bash
pip install streamlit selenium beautifulsoup4 lxml html5lib langchain-ollama langchain-core python-dotenv
```

2. Download and run the local foundational LLM through Ollama:
```bash
ollama run llama3.1
```

3. Create a `.env` file in your root folder and set the exact file route to your Chrome WebDriver binary:
```env
CHROMEDRIVER_PATH="./chromedriver.exe"
```

## Usage

1. Launch the Streamlit development app execution frame:
```bash
streamlit run main.py
```
2. Open the network URL provided in your console shell.
3. Input your target site URL and pick your execution scope layout ("Single Page" or "Crawl Whole Site").
4. Click **Scrape Site**.
5. Type out precise properties you wish to locate inside the description text field (e.g., "Extract product names, prices, and review ratings").
6. Click **Parse Content** to display your structured Markdown matrix output.
