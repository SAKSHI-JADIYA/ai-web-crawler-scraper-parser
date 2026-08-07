import streamlit as st
st.title("AI WEB SCRAPER")
url=st.text_input("Enter a Website URL: ")

if st.button("Scrape Site"):
    st.write("Scraping the website")