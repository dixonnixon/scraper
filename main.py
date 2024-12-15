import streamlit as st
from crawl.scrape import *

st.title("Web Scraper")

url = st.text_input("Enter a url: ")


col1, col2 = st.columns([2, 2])

#col1.subheader("A narrow column with the data")
with col1:
    if st.toggle("Activate proxy"):
        st.write("Feature activated!")
        st.session_state.add_element = True



with col2:
    if 'add_element' in st.session_state and st.session_state.add_element:
        select_proxy = st.selectbox(
                "Select the Server: ",
                ("Email", "Home phone", "Mobile phone"),
            ) 




#if selcet_proxy:
    

#if proxy:
#        st.write("Great!")
#        col2.write(st.selectbox(
#            "How would you like to be contacted?",
#            ("Email", "Home phone", "Mobile phone"),
#        ))


#        col2.subheader("")

        #st.write("You selected:", option)
        #col2.write(option)


if st.button("Scrape!"):
    if url:    
        st.write("processing...")
        result = scrape_website(url)
        #print(result)
        dom_content = scrape_website(url)
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)

        # Store the DOM content in Streamlit session state
        st.session_state.dom_content = cleaned_content
        print(st.session_state)
        
        # Display the DOM content in an expandable text box
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)


