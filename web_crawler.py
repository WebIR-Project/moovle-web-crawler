import analyzer, json
from pymongo import MongoClient
import threading
import downloader
from robots_parser import RobotParser
from urllib.parse import urlparse
from scheduler import Scheduler

client = MongoClient()
db = client.moovle
sch = Scheduler()
rp = RobotParser(user_agent='random')
lock = threading.Lock()

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

def t_print(thread_name, msg):
    print(f'{thread_name}: {msg}')

def worker():
    global db, sch, rp
    t_name = threading.current_thread().getName()
    d = downloader.Downloader(use_proxies=True)
    while True:
        lock.acquire()
        if sch.get_queue_length() == 0:
            break
        url = sch.dequeue()
        lock.release()

        t_print(t_name, f'Downloading {url}')

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
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc
        links = [analyzer.normalize_url(hostname, link) for link in analyzer.extract_links(parsed_html)]

        lock.acquire()
        if html is not None:
            t_print(t_name, f'Saving {url}')
            save_page(url, parsed_html, html, links)
        else:
            t_print(t_name, f'Cannot download {url}')
        for link in [link for link in links if analyzer.is_html_page(link) and rp.is_allowed(link) and len(urlparse(link).path.split('/')) <= 20]:
            sch.enqueue(link)
        sch.visited(url)
        lock.release()

config = read_config()
threads = []
for i in range(config['n_thread']):
    t = threading.Thread(name=i, target=worker)
    threads.append(t)
    t.start()
