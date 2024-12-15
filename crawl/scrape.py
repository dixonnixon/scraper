from config import settings

import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from os import environ, path

import requests
from random import choice


from crawl.driver import create_instance, singleton

print(settings.DRV_CHROME)


import cloudscraper

def get_proxies():
    print(settings.WS_KEY)
    response = requests.get(
                "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=25",
                 headers={ "Authorization": f"Token {settings.WS_KEY}" }
            )
    fetched = response.json()
    return fetched['results']
#          {'id': 'd-15982962554', 'username': 'vhywotkf', 'password': 'wqhwhowlp0zx', 'proxy_address': '167.160.180.203', 'port': 6754, 
#           'valid': True, 'last_verification': '2024-12-15T11:45:28.374501-08:00', 'country_code': 'US', 'city_name': 'Los Angeles', 
#           'asn_name': 'Asn-Quadranet-Global', 'asn_number': 8100, 'high_country_confidence': True, 'created_at': '2024-07-12T08:07:13.049836-07:>

def get_random_proxy(proxies):
    keys = ['username', 'password', 'proxy_address', 'port']
    return [choice(proxies)[key] for key in keys]

@singleton
class Runner():
    def __init__(self, proxy=False):
        print('init done! Runner')
        options = webdriver.ChromeOptions()
#    options.add_argument("--headless=new") 
        options.add_argument('--headless')  # Run Chrome in headless mode
        options.add_argument('--disable-gpu')  # Disable GPU acceleration
        options.add_argument('--no-sandbox')  # Bypass sandbox mode (for non-standard environments)

        if proxy:
            proxies = get_proxies()
#           random_proxy = get_random_proxy(proxies)

#           print(choice(fetch['results']), choice(fetch['results']).items())
#           keys = ['username', 'password', 'proxy_address', 'port']
            #user, password, proxy_address, port = [choice(fetch['results'])[key] for key in keys]
            user, password, proxy_address, port = get_random_proxy(proxies)

            # Define custom options for the Selenium driver
            # options = Options()
            proxy_server_url = f"http://{user}:{password}@{proxy_address}:{port}"
            options.add_argument(f'--proxy-server={proxy_server_url}')

            # Create the ChromeDriver instance with custom options 
            driver = webdriver.Chrome(
#            service=Service(ChromeDriverManager().install()),
            service=Service(settings.DRV_CHROME),
 
               options=options
            )
            self._driver = driver
            return None


        self._driver = webdriver.Chrome(service=Service(settings.DRV_CHROME), options=options)
    

    def wait_for_page_load(self):
        self._driver.execute_script("return document.readyState") == "complete"

    @property
    def driver(self):
        return self._driver

    @property
    def quit(self):
        return self._driver.quit


def scrape_website(website):
    print("Connecting to Scraping Browser...")
    creator = create_instance("crawl.scrape.Runner", proxy=True)
    driver = create_instance("crawl.scrape.Runner", proxy=True).driver

    scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
        },
    )


    print(driver, creator.driver is driver, "Current session is {}".format(driver.session_id),  driver.get_log('driver'))
    try:

        #driver.get(website)
        print("Page loaded...")
        #html = driver.page_source.encode("utf-8")
        #print(html)
        #print(creator.wait_for_page_load())
        response = scraper.get(website)
        print(f"The status code is {response.status_code}")
        #print("\n\n\n\n", response.text.encode("utf-8"))
        #return html
 
        return response.text
    except Exception as e:
        print("Error occured: ", e)
        raise Exception(e)
    finally:
         print("Current session is {}".format(driver.session_id))
    #    driver.close()
    #    driver.quit()        




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
