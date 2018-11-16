from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

c = MongoClient()
db = c.moovle

def extract_images(url, soup):
    image_tags = soup.find_all('img')
    image_urls = [urljoin(url, item.get('src')) for item in image_tags]
    return image_urls

if __name__ == '__main__':
    count = 0
    while True:
        docs = list(db.pages.aggregate([{'$match': {'extracted': {'$exists': False}}}, {'$limit': 1}]))
        if len(docs) == 0:
            break
        doc = docs[0]
        soup = bs(doc['html'], 'html.parser')
        image_urls = extract_images(doc['url'], soup)
        db.pages.update({'url': doc['url']}, {'$set': {'images': image_urls, 'extracted': True}})
        count += 1
        if count % 100 == 0:
            print('.', end='', flush=True)
    print()
    print('cleaning...')
    db.pages.update({}, {'$unset': {'extracted': True}}, multi=True)