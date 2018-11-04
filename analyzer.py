from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_links(soup):
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

def is_html_page(url):
    parsed_url = urlparse(url)
    result = True
    if parsed_url.path != '':
        path = [item for item in parsed_url.path.split('/') if item != '']
        if len(path) > 0:
            last = path[-1]
            splitted_last = last.split('.')
            ext = splitted_last[-1]
            if len(splitted_last) > 1 and ext != 'html' and ext != 'htm' and ext != 'php':
                result = False
    return result