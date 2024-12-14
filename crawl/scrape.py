from config import settings

import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from os import environ, path

from crawl.driver import create_instance, singleton

print(settings.DRV_CHROME)

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
            # Define custom options for the Selenium driver
            options = Options()
            proxy_server_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
            options.add_argument(f'--proxy-server={proxy_server_url}')

            # Create the ChromeDriver instance with custom options 
            driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
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
    '''sbr_connection = ChromiumRemoteConnection(settings.DRV_CHROME, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source
        time.sleep(10)
        
        return html
    '''
    creator = create_instance("crawl.scrape.Runner")
    driver = create_instance("crawl.scrape.Runner").driver
    #instance1 = create_instance("crawl.scrape.Runner")
    #instance2 = create_instance("crawl.scrape.Runner")

    print(creator.driver is driver)
    #print(instance1 is instance2)


    try:
        driver.get(website)
        print("Page loaded...")
        html = driver.page_source.encode("utf-8")
        print(html)
        print(creator.wait_for_page_load())
#        driver.quit()
        #if creator.wait_for_page_load():
        return html
        #else:
        #    return "Page not loaded or js disabled"
    except Exception as e:
        print(e)
    finally:
         driver.close()
    #    driver.quit()        




def extract_body_content(html_content):
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
