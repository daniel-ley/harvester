from time import sleep
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sys
import re
from os import path


download_path = f"{path.expanduser('~')}/Documents/"

if 'lxml' not in sys.modules:
    USEABLE_PARSER = 'html.parser'
else:
    USEABLE_PARSER = 'lxml'

RQ_AGENTS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' 
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/70.0.3538.77 Safari/537.36'}


def read_web_page(uri: str, headers: dict) -> BeautifulSoup:
    '''Retrieve a webpage from the given url, and return soup object'''

    with requests.get(uri, headers=headers) as response:
        if response.status_code != 200:
            print(f'Issue encountered: {response.status_code}')
            print(response.text)
        else:
            soup = BeautifulSoup(response.text, USEABLE_PARSER)
            return soup


def get_links(soup: BeautifulSoup, css_class=None) -> list:
    '''Read a beautiful soup and return all of the anchor-tag "a" links
    pass None is not. Will look for particular css class - Unused'''

    list_of_links = []
    
    if not css_class:
        for a in soup.find_all('a', href=True):
            list_of_links.append(a['href'])
        return list_of_links
    else:
        for a in soup.find_all('a', href=True, class_=css_class):
            list_of_links.append(a['href'])
        return list_of_links


def get_list_of_available_resources(links: list) -> list:
    resource_types = []
    for link in links:
        if len(link) > 3:
            extension = link[-4:]
            if extension[0] == '.':
                resource_types.append(extension[1:])
    resource_types = list(set(resource_types))
    return resource_types


def filter_links(list_of_links: list, filetype: str) -> list:
    '''Filter the list of links to only the requested file type'''

    filtered_links = []

    for link in list_of_links:
        if link.endswith(filetype):
            filtered_links.append(link)

    return filtered_links


def get_filename_from_url(url: str) -> str: 
    '''Find the section of the given URL from the last slash to the end'''

    topic = re.search(r".*/(.*?)$", url)

    return topic.group(1)


def file_handler(file_url: str, file_name: str) -> None:
    '''Download and write a file to disk'''

    with requests.get(file_url, headers=RQ_AGENTS) as response:
        if response.status_code != 200:
            print(f'Issue encountered: {response.status_code}')
            print(response.text)
        else:
            downloaded_file = response.content

    with open(f"{download_path}{file_name}", 'wb') as file:
        file.write(downloaded_file)


def main() -> None:
    '''Main program'''

    url = input('Enter URL: ')

    print(f'Started {datetime.now().strftime("%H:%M:%S")}')

    page_soup = read_web_page(url, RQ_AGENTS)
    links = get_links(page_soup)
    available_resources = get_list_of_available_resources(links)

    print(f"Available resources: {available_resources}")
    
    filetype_to_download = input("Enter filetype to download:")

    links = filter_links(links, filetype_to_download)

    for link in links:
        focus_file_name = get_filename_from_url(link)
        print(f'processing file {focus_file_name}')
        # file_handler(link, focus_file_name)

    print(f'Completed {datetime.now().strftime("%H:%M:%S")}')
    print(f'Downloaded {len(links)} Dcouments')


if __name__ == '__main__':
    main()
    