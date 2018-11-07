import sys
from bs4 import BeautifulSoup
from pymongo import MongoClient
c = MongoClient()
db = c.moovle
count = 0
while db.pages.find({'fixed': {'$exists': False}}).count() > 0:
    doc = db.pages.find_one({'fixed': {'$exists': False}})
    html = doc['html']
    parsed_html = BeautifulSoup(html, 'html.parser')

    for script in parsed_html(["script", "style"]):
        script.decompose()
    text = parsed_html.get_text()
    lines = [line.strip() for line in text.splitlines() if line.strip() != '']
    lines = [phrase.strip() for line in lines for phrase in line.split("  ")]
    text = '\n'.join(lines)
    db.pages.update({'url': doc['url']}, {'$set': {'text': text, 'fixed': True}}, multi=True)
    count += 1
    print(count)