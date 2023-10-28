#!venv/bin/python
from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
import time, sys

url = "https://www.google.com"
patterns = []


def init_parser_and_browser() -> tuple[str, webdriver]:
    '''Setup of the webdriver for Selenium and 
    determine the parser for BeautifulSoup'''

    if 'lxml' not in sys.modules:
        usable_parser = 'html.parser'
    else:
        usable_parser = 'lxml'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    headless_browser = webdriver.Chrome(options=options)

    return usable_parser, headless_browser


def get_page_src(uri: str, browser: webdriver) -> str:
    # get the page in the browser
    browser.get(uri)
    # get the page html source as html
    html = browser.page_source
    # Close the browser
    browser.close()

    return html


def make_soup(html_src: str, parser: str) -> BeautifulSoup:
    soup = BeautifulSoup(html_src, parser)

    return soup


def scrape_links(soup: BeautifulSoup) -> list:
    list_of_links = []

    for a in soup.find_all('a', href=True):
        list_of_links.append(a['href'])
    
    # Dedupe
    list_of_links = list(set(list_of_links))
    
    return list_of_links

def filter_links(list_of_links: list, pattern: str) -> list:
    '''Filter the list of links to only the requested file type'''

    filtered_links = []

    if len(pattern) == 0:
        return list_of_links

    for link in list_of_links:
        if pattern.lower() in link.lower():
            filtered_links.append(link)

    return filtered_links


def main() -> None:

    parser, browser = init_parser_and_browser()

    start_time = datetime.now()
    print(f'Started {datetime.now().strftime("%H:%M:%S")}')
    
    page_html = get_page_src(url, browser)
    soup = make_soup(page_html, parser)
    links = scrape_links(soup)

    for pattern in patterns:
        links = filter_links(links, pattern)
    
    for link in links:
        print(link)
    
    run_duration = datetime.now() - start_time
    
    print(f'Completed: {datetime.now().strftime("%H:%M:%S")}')
    print(f"{len(links)} relevant links found, ", end="")
    print(f"taking {run_duration.total_seconds()} seconds.")


if __name__ == '__main__':
    main()