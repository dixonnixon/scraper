import streamlit as st
from crawl.scrape import *

from config import settings

def create_options(list):
   return { value: key for  key,value in enumerate(list) }


st.session_state.proxy_list = []
#st.session_state.proxy_picked = None
#st.session_state.selected_proxy_key = None

st.title("Web Scraper")

url = st.text_input("Enter a url: ")
previous_urls = [1,2]

col1, col2 = st.columns([2, 2])

#col1.subheader("A narrow column with the data")
with col1:
    if st.toggle("Activate proxy"):
        st.write("Feature activated!")
        st.session_state.proxy = True
        st.session_state.proxy_list =  [extract_one(p) for p in get_proxies()] 
    else:
        st.session_state.proxy = False 
        st.session_state.proxy_picked = None
        st.session_state.selected_proxy_key = None


with col2:
    if 'proxy' in st.session_state and st.session_state.proxy:
        options = create_options(st.session_state.proxy_list) 
#        print(options, options.items())

        select_proxy = st.selectbox(
                "Select the Server: ",
                #("Email", "Home phone", "Mobile phone"),
                #st.session_state.proxy_list,
                options.keys(),
                key='proxy_picked',
                #format_func=lambda x: f"{x[1]}"
            ) 
        if select_proxy:
            st.session_state.selected_proxy_key = options[select_proxy]
            col1.write(f"Selectd proxy {select_proxy}")
        

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
        print(st.session_state.proxy_picked)
        #result = scrape_website(url)
        #print(result)
        dom_content = scrape_website(url, proxy={"option": st.session_state.selected_proxy_key})
        
        print("\n"*5, dom_content)

        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)

        # Store the DOM content in Streamlit session state
        st.session_state.dom_content = cleaned_content
        
        # Display the DOM content in an expandable text box
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)

