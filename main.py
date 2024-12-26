import streamlit as st
from crawl.scrape import *
from crawl.heartbeat import get_user_id
from crawl.parse import parse_with_ollama

def create_options(list):
   return { value: key for  key,value in enumerate(list) }


st.session_state.proxy_list = []
#st.session_state.proxy_picked = None
#st.session_state.selected_proxy_key = None

st.title("Web Scraper")

url = st.text_input("Enter a url: ")
previous_urls = [1,2]

col1, col2 = st.columns([2, 2])

user = get_user_id()
print(user)

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
        
        print("\n"*5)

        body_content_static = extract_body_content(dom_content["static"])
        body_content_dynamic = extract_body_content(dom_content["dynamic"])

        cleaned_content_static = clean_body_content(body_content_static)
        cleaned_content_dynamic = clean_body_content(body_content_dynamic)


        # Store the DOM content in Streamlit session state
        st.session_state.dom_content = cleaned_content_static
        
        # Display the DOM content in an expandable text box
        with st.expander("View DOM Content"):
            st.text_area("Static DOM Content", cleaned_content_static, height=300)
            st.text_area("Dynamic DOM Content", cleaned_content_dynamic, height=300)
       

        print("dom", len(st.session_state.dom_content), "dom_content" in st.session_state)

if "dom_content" in st.session_state:
    desc = st.text_area("Describe what you want to scrape? 0_0")
    print(desc)
    if st.button("Parse Content"):
        if desc:
            st.write("Paring the content")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            print(dom_chunks)
            parsed_result = parse_with_ollama(dom_chunks, desc)
            print(parsed_result)
            st.write(parsed_result)


