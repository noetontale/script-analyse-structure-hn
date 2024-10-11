import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup 

# Streamlit app setup
st.title("SERP Hn Hierarchy Scraper")
st.write("Upload an Excel file with a list of URLs to scrape the hn hierarchy.")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    # Read the uploaded Excel file
    df = pd.read_excel(uploaded_file)

    # Function to fetch and parse hn hierarchy from URL
    def get_hn_hierarchy(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract heading tags h1, h2, ..., h6
            headings = {}
            for i in range(1, 7):  # h1 to h6
                headings[f'h{i}'] = [tag.get_text(strip=True) for tag in soup.find_all(f'h{i}')]

            return headings
        except Exception as e:
            return f"Error fetching {url}: {e}"

    # Loop over the URLs and extract heading tags
    df['headings'] = df['URL'].apply(get_hn_hierarchy)

    # Display results
    st.write("Results:", df)