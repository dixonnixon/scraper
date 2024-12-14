import streamlit as st
from crawl.scrape import *

st.title("Web Scraper")
url = st.text_input("Enter a url: ")

if st.button("Scrape!"):
    if url:    
        st.write("processing...")
        result = scrape_website(url)
        print(result)
        dom_content = scrape_website(url)
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)

        # Store the DOM content in Streamlit session state
        st.session_state.dom_content = cleaned_content
        print(st.session_state)
        
        # Display the DOM content in an expandable text box
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)
