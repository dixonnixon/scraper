import requests
from bs4 import BeautifulSoup
import cloudscraper

from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from urllib3.util.ssl_ import SSLContext
from urllib3.util.retry import Retry
import ssl
import certifi

'''
Stopped here when uncertain on how to use proxies to scrape forbidden pages/but vpn?
'''

import os
from random import choice

import urllib3
from urllib3 import PoolManager
from urllib3.util import create_urllib3_context



ctx = create_urllib3_context()
ctx.load_default_certs()
ctx.options |= ssl.OP_ENABLE_MIDDLEBOX_COMPAT


# send the request


response = requests.get("https://www.g2.com/products/jira/reviews")
# create a cloudscraper instance
scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
    },
)

# specify the target URL
url = "https://opensea.io/rankings"

print("The status code is ", response.status_code)
print(response.text)
# validate and print the response
if response.status_code!=200:
    print(f"The request failed with an error {response.status_code}")
else:
    print(response.text)

# request the target website
response = scraper.get(url)

# get the response status code
print(f"The status code is {response.status_code}")
soup = BeautifulSoup(response.text, "html.parser")
print(soup.find_all("title"))


def get_req(url, headers=None):
    addr, port = choice(get_proxies()).split(":")
    print(addr, port)
    proxy = urllib3.ProxyManager(f"http://localhost:8080/") 
    #print(get_free_proxies())    
 
    #proxy = urllib3.ProxyManager(f"http://{addr}:{port}/") 
    print("g", proxy)
        
    
   # with PoolManager(ssl_context=ctx) as pool:
    r = proxy.request("GET", url, headers=headers)
    print(r.status,  r.headers)
    return r

session = requests.Session()


def get_free_proxies(countries=[]):
    
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

def get_proxies():
  r = requests.get('https://free-proxy-list.net')
  soup = BeautifulSoup(r.content, 'html.parser')
  table = soup.find('tbody')

  proxies = []
  for row in table:
    if row.find_all('td')[4].text == 'elite proxy':
      proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
      proxies.append(proxy)
    else:
      pass

  return proxies

def check_website(url):
  try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    #session = requests.Session()
    ssl_context = SSLContext(ssl.PROTOCOL_TLSv1_2)
    #http.mount('https://', HTTPAdapter(max_retries=3, ssl_context=ssl_context))

#    http.mount('https://', HTTPAdapter(max_retries=3, ssl_context=SSLContext()))
    #retry = Retry(connect=1, backoff_factor=0.5)
    #adapter = HTTPAdapter(max_retries=retry)
    #session.mount('http://', adapter)
    #session.mount('https://', adapter)

    print("session", session, url)

    #print(certifi.where())
#    try:
        #proxy = choice(get_proxies())

 #       proxy = {
  #          "http": f"http://{proxy}",
   #         "https": f"http://{proxy}",
            
   #     }
        

        #response = session.get(url, headers=headers, timeout=5, verify = False, proxies=proxy)
        #print(dir(response),  response.headers["Content-Type"])
        #response.raise_for_status()  # Підняти виключення, якщо статус не 200
    #except requests.exceptions.RequestException as  r_ex:
     #   print("Request excp.:", r_ex)
    #except requests.exceptions.ConnectionError as e:
    #    print(e)
    #except HTTPError as http_err:
    #    print(f"HTTP error occurred: {http_err}")
    #except Exception as err:
    #    print(f"Other error occurred: {err}")
    #else:
    #    print("Success!")

    
    response = get_req(url, headers=headers)

    soup = BeautifulSoup(response.data, 'html.parser')
    
    # ... ваш код для парсингу даних
    print(response.status, "\n\n", soup.find_all("title"))

    return True
  except requests.exceptions.RequestException as e:
    print(f"Помилка при перевірці сайту {url}: {e}")
    return False

