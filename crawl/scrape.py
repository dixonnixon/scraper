
from config import settings

from streamlit import cache_data, secrets

import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException  # Import TimeoutException explicitly
from selenium.webdriver.support import expected_conditions as EC

from playwright.sync_api import sync_playwright

from fake_useragent import UserAgent  # Install with: pip install fake-useragent

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from os import environ, path

import requests
from random import choice


from crawl.driver import create_instance, singleton

#print(settings.DRV_CHROME)


import cloudscraper
from cloudscraper.exceptions import (
    CloudflareLoopProtection,
    CloudflareIUAMError,
    CloudflareCaptchaError,
    CloudflareCaptchaProvider,
    CaptchaParameter
)

@cache_data
def get_proxies():
    try:
        response = requests.get(
                "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=25",
                 headers={ "Authorization": f"Token {settings.WS_KEY}" }
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
       if err.response.status_code == 401:
           print("Webshare Auth failed: Authentication failed. Status 401")
           raise Exception(err)
       else:
           print("Error getting Proxies: ", err.args[0])
    print(response,  response.status_code)
    
    return response.json()["results"]



def extract_one(proxy):
    lables = ['IP','port','Country']
    keys = ['proxy_address','port', 'country_code']
    values = [ str(proxy[key]) for key in keys]
    pairs = [f"{key}:{value}" for key, value in zip(lables, values)]
    result = " ".join(pairs)
    return result


def get_random_proxy(proxies, option=None):
    keys = ['username', 'password', 'proxy_address', 'port']
    if option:
        return [proxies[option][key] for key in keys]
    return [choice(proxies)[key] for key in keys]

def get_proxy_url(option=None):
    proxies = get_proxies()
    if not option:
        user, password, proxy_address, port = get_random_proxy(proxies)
    else:
        user, password, proxy_address, port = get_random_proxy(proxies, option=option)

    return f"http://{user}:{password}@{proxy_address}:{port}"




@singleton
class Runner():
    def __init__(self, proxy=False):
        print('init done! Runner')
        ua = UserAgent()
        user_agent = ua.random  # Get a random User-Agent string

        options = webdriver.ChromeOptions()
#      options.add_argument("--headless=new") 
        options.add_argument('--headless')  # Run Chrome in headless mode
        options.add_argument('--disable-gpu')  # Disable GPU acceleration
        options.add_argument('--no-sandbox')  # Bypass sandbox mode (for non-standard environments)
        options.add_argument(f'user-agent={user_agent}')
    #options.add_argument("--enable-javascript")
    #options.add_argument("--ignore-certificate-errors") #Insecure
        #:TODO logic in a way that if no drivers supported for runner use cloudscrapper
        # if drivers supported then use Selenium
        # if selenium preferred to use -> force download driver, advice download driver
        
        print("Proxy: ", proxy)
        if proxy["option"] is not None:
            proxy_server_url = get_proxy_url(proxy["option"])

            options.add_argument(f'--proxy-server={proxy_server_url}')

            # Create the ChromeDriver instance with custom options 
            driver = webdriver.Chrome(
#            service=Service(ChromeDriverManager().install()),
            service=Service(settings.SBR_WEBDRIVER),
 
               options=options
            )
            self._driver = driver
            return None
        else:
            self._driver = webdriver.Chrome(service=Service(settings.SBR_WEBDRIVER), options=options)

    def wait_for_page_load(self, timeout=5):  # Added timeout parameter
        try:
            # Wait for the document to be fully loaded (DOMContentLoaded)
            WebDriverWait(self._driver, timeout).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            return True # Page loaded successfully
        except TimeoutException:
            print(f"Page load timed out after {timeout} seconds.")
            return False # Page load timed out
        except Exception as e:
            print(f"An error occurred during page load: {e}")
            return False # Some other error occurred

    @property
    def driver(self):
        return self._driver

    @property
    def quit(self):
        return self._driver.quit


def scrape_website(website, proxy=None):
    print("Connecting to Scraping Browser...")
    proxy_cs = None

    def _drv():
        creator_driver = create_instance("crawl.scrape.Runner", proxy=proxy)
        creator_driver.driver.execute_script('document.documentElement.style.setProperty("javascript.enabled", "true")')
        creator_driver.driver.execute_script("return navigator.userAgent")
        #creator_driver.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        #driver = create_instance("crawl.scrape.Runner", proxy=proxy).driver
        creator_driver.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
          "source": """
            delete navigator.webdriver;
          """
        })

        return creator_driver


    def _rsp(creator_driver):
        r = creator_driver.driver.get(website)
        print(r)
        if creator_driver.wait_for_page_load():
            print("Page loaded...")
            WebDriverWait(creator_driver.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body'))) 
            #print(creator_driver.driver.page_source)
        #html = driver.page_source.encode("utf-8")
        #print(html)
        #print(creator.wait_for_page_load())

        return creator_driver.driver.page_source

    
    
    scraper = cloudscraper.create_scraper(debug=False,
    browser={
        "browser": "chrome",
        "platform": "windows",
        "desktop": True
        },
    #interpreter='v8eval')
    )
    print(proxy)



    #:TODO change approach of passing proxy
    if str(proxy["option"]) and proxy["option"] is not None:
        if proxy["option"] > -1:

            proxy_cs = {
                "http": get_proxy_url(proxy["option"]),
                "https": get_proxy_url(proxy["option"]),
            }

            try:
                tokens, user_agent = cloudscraper.get_tokens(website, proxies=proxy_cs)
                print("Tokens", tokens, user_agent, proxy_cs)

            except CloudflareIUAMError as e:
                print("No cloudflare on the site") 


    #print(driver, creator.driver is driver, "Current session is {}".format(driver.session_id),  driver.get_log('driver'))
    
    try:
        response = scraper.get(website, proxies=proxy_cs)

#        response = scraper.get(website, proxies=proxy_cs)
        print(f"The status code is {response.status_code}", dir(response), response.is_redirect, response.iter_content, 
                response.reason, response.headers
        )
#        print(f"Content compare {response.text.encode('utf-8') == creator_driver.driver.page_source.encode('utf-8')}",
#                response.encoding
#        )
        #print("\n\n\n\n", response.text.encode("utf-8"))
        #return html
 

        return {"static": response.content.decode("utf-8"), "dynamic": _rsp(_drv())} 


    except Exception as e:
        print("Error occured: ", e)
        raise Exception(e)
    #finally:
    #     print("Current session is {}".format(driver.session_id))
    #    driver.close()
#        creator_driver.quit()        




def extract_body_content(html_content):
    #create_instance("crawl.scrape.Runner").driver.quit()
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
