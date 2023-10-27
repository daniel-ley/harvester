from selenium import webdriver
from bs4 import BeautifulSoup
import time, sys

url = "https://en.wikipedia.org"

if 'lxml' not in sys.modules:
    USEABLE_PARSER = 'html.parser'
else:
    USEABLE_PARSER = 'lxml'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
headless_browser = webdriver.Chrome(options=options)

def get_page_src(uri, browser):
    # get source code
    browser.get(uri)

    html = browser.page_source
    # Close the browser
    browser.close()

    return html


def make_soup(html_src):
    soup = BeautifulSoup(html_src, USEABLE_PARSER)

    return soup


def scrape_links(soup):
    list_of_links = []
    for a in soup.find_all('a', href=True):
        list_of_links.append(a['href'])
    
    return list_of_links


def main():
    page_html = get_page_src(url, headless_browser)
    soup = make_soup(page_html)
    links = scrape_links(soup)
    
    for link in links:
        print(link)

if __name__ == '__main__':
    main()
