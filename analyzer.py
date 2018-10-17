from bs4 import BeautifulSoup

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_links(soup_object):
    links = [for link in soup_object.find_all('a')]
    return links

def main():
    soup_object = parse_html()
    extract_links(soup_object)

if __name__ == '__main__':
    main()

