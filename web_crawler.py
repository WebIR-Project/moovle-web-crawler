import analyzer, json
from pymongo import MongoClient
from threading import Thread, Lock
import downloader
from robots_parser import RobotParser
from scheduler import Scheduler

client = MongoClient()
db = client.moovle
sch = Scheduler()
rp = RobotParser(user_agent='random')

def read_config():
    f = open('config.json')
    config = json.load(f)
    f.close()
    return config

def save_page(url, parsed_html, html, links):
    global db
    title = parsed_html.title.string
    text = parsed_html.get_text()
    db.moovle.insert({
        'url': url,
        'title': title,
        'text': text,
        'links': links,
        'html': html
    })

def worker():
    global db, sch, rp
    d = downloader.Downloader(use_proxies=True)
    while True:
        lock.acquire()
        if sch.get_queue_length() == 0:
            break
        url = sch.dequeue()
        lock.release()

        html = None
        while True:
            try:
                html = d.get_page(url)
                break
            except downloader.PageNotFound:
                break
            except downloader.NetworkError:
                pass
        parsed_html = analyzer.parse_html(html)
        links = analyzer.extract_links(parsed_html)

        lock.acquire()
        save_page(url, parsed_html, html, links)
        for link in [link for link in links if analyzer.is_html_page(link) and rp.is_allowed(url)]:
            sch.enqueue(link)
        sch.visited(url)
        lock.release()

config = read_config()
threads = []
lock = Lock()
for i in range(config['n_thread']):
    t = Thread(target=worker)
    threads.append(t)
    t.start()
