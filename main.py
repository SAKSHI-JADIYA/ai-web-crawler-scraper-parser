import base64
import streamlit as st
from parse import parse_with_ollama
from scrape import (
    clean_body_content,
    crawl_site,
    extract_body_content,
    scrape_page,
    split_dom_content,
)

# --- BACKGROUND IMAGE SECTION ---
st.markdown(
    f'<style>[data-testid="stAppViewContainer"] {{background-image: url("data:image/avif;base64,{base64.b64encode(open("realistic-halloween-spider-web-background_52683-72550.avif", "rb").read()).decode()}"); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;}} [data-testid="stHeader"] {{background: rgba(0,0,0,0);}}</style>',
    unsafe_allow_html=True,
)
# --------------------------------

st.title("AI WEB SCRAPER")
url = st.text_input("Enter a Website URL:")

mode = st.radio("Choose scraping mode:", ["Single Page", "Crawl Whole Site"])

# Initialize session state so it persists across button clicks
if "dom_content" not in st.session_state:
    st.session_state.dom_content = ""

if st.button("Scrape Site"):
    st.write("Scraping the website...")

    if mode == "Single Page":
        html = scrape_page(url)
        body_content = extract_body_content(html)
        cleaned_content = clean_body_content(body_content)
        st.session_state.dom_content = cleaned_content

    else:  # Crawl Whole Site
        html_pages = crawl_site(url, max_pages=10)  # adjust max_pages as needed
        all_cleaned = []
        for html in html_pages:
            body_content = extract_body_content(html)
            cleaned_content = clean_body_content(body_content)
            all_cleaned.append(cleaned_content)
        st.session_state.dom_content = "\n\n".join(all_cleaned)

# Check if dom_content actually has content instead of just existing
if st.session_state.dom_content:
    with st.expander("View DOM content"):
        st.text_area("DOM Content", st.session_state.dom_content, height=300)

    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.markdown(result)   # renders Markdown tables correctly
