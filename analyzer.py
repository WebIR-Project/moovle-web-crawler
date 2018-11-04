<<<<<<< HEAD
from bs4 import BeautifulSoup
from urllib.parse import urlparse
=======
import urllib
>>>>>>> feature/normalize-url
import re
from urllib.parse import urljoin
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_links(soup):
    links = []
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))
    return links
    
#รับ hostname และ links
def normalize_url(hostname,links) :
    urls = []
    if links != None and len(links) > 0 :
        full_link = urllib.parse.unquote(urljoin(hostname,links)).strip()
        if full_link not in urls :
            urls.append(full_link)
    return urls

<<<<<<< HEAD
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
=======
def main():
    links = []
    soup = parse_html()
    links = extract_links(soup)
    full_urls = normalize_url()

if __name__ == '__main__':
    main()

>>>>>>> feature/normalize-url
