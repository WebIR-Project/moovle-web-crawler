import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_links(soup):
    links = [link.get('href') for link in soup.findAll('a') if link.get('href') is not None]
    return links
    
def normalize_url(root_url, link) :
    url = unquote(unquote(urljoin(root_url, link))).strip()
    parsed_url = urlparse(url)
    path = parsed_url.path
    path = re.sub('index\\.(html?|php)$', '', path)
    if re.search('/[^/.]+$', path):
        path += '/'
    url = f'{parsed_url.scheme}://{parsed_url.netloc}{path if path != "/" else ""}'
    return url

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
