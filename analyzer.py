from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_links(soup):
    links = []
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))
    return links
    
def normalize_url(hostname, link) :
    urls = []
    if link is not None and len(link) > 0 :
        full_link = unquote(unquote(urljoin(hostname, link))).strip()
        if full_link not in urls :
            urls.append(full_link)
    return urls

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
