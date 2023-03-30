import concurrent.futures
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import codecs
from urllib.parse import urlparse


#Adicione a URL de posts do seu sitemap.

response = requests.get('seu-sitemap.xml')
soup = BeautifulSoup(response.text, 'lxml')

URLS = [url.get_text() for url in soup.find_all('loc')]

def page_to_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

#Apenas para criar uma regra de nomenclatura, depois se for preciso abrir algum arquivo html e desejarmos saber a url de origem é só trocar o ';' por '/'. 

    path = urlparse(url).path.replace('/', ';')
#É importante que seu chromedriver esteja no diretório abaixo.
    with webdriver.Chrome('C:\Program Files\chromedriver.exe', options=options) as driver:
        driver.get(url)
        time.sleep(3)
        html = driver.page_source

#Será salvo na pasta abaixo.
        with codecs.open(f"seu-diretorio\{path}.html", "w", 'utf-8') as file:
            file.write(html)

def print_progress(n, total):
    print(f"Progress: {n}/{total}")

with concurrent.futures.ThreadPoolExecutor(max_workers = None) as executor:
    future_to_url = {executor.submit(page_to_html, url): url for url in URLS}
    for i, future in enumerate(concurrent.futures.as_completed(future_to_url)):
        url = future_to_url[future]
        print_progress(i+1, len(future_to_url))
