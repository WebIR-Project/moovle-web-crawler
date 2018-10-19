from bs4 import BeautifulSoup
import urllib2
import re

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_links(soup):
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

def main():
    links = []
    soup = parse_html()
    links = extract_links(soup)

if __name__ == '__main__':
    main()

