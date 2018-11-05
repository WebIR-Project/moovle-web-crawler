import analyzer, json, time, sys
from pymongo import MongoClient
import threading
import downloader
from robots_parser import RobotParser
from urllib.parse import urlparse
from scheduler import Scheduler

client = MongoClient()
db = client.moovle
sch = Scheduler()
sch.clean_buffer()
rp = RobotParser(user_agent='random')
lock = threading.Lock()

def read_config():
    f = open('config.json')
    config = json.load(f)
    f.close()
    return config

def save_page(url, parsed_html, html, links):
    global db
    title = None
    if parsed_html.title is not None:
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
    t_print(t_name, 'Started')
    d = downloader.Downloader(use_proxies=True)
    while True:
        lock.acquire()
        if sch.get_queue_length() == 0:
            # t_print(t_name, 'Nothing to do')
            lock.release()
            continue
        url = sch.dequeue()
        lock.release()
        try:
            t_print(t_name, f'Downloading {url}')

            html = None
            while True:
                try:
                    html = d.get_page(url)
                    break
                except downloader.PageNotFound:
                    break
                except downloader.NetworkError:
                    t_print(t_name, f'Retrying download {url}')
                    pass
            if html is not None:
                t_print(t_name, f'Downloaded {url}')
                parsed_html = analyzer.parse_html(html)
                parsed_url = urlparse(url)
                root_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
                links = [analyzer.normalize_url(root_url, link) for link in analyzer.extract_links(parsed_html)]
                lock.acquire()
                t_print(t_name, f'Saving {url}')
                save_page(url, parsed_html, html, links)
                t_print(t_name, f'Saved {url}')
                t_print(t_name, f'Filtering links')
                filtered_links = [link for link in links if analyzer.is_html_page(link) and len(urlparse(link).path.split('/')) <= 20]
                # for link in [link for link in links if analyzer.is_html_page(link) and rp.is_allowed(link) and len(urlparse(link).path.split('/')) <= 20]:
                for link in filtered_links:
                    sch.enqueue(link)
                t_print(t_name, f'Added {len(filtered_links)} links to queue')
            else:
                t_print(t_name, f'Cannot download {url}')
            sch.debuffer(url)
            sch.visited(url)
            lock.release()
        except Exception:
            t_print(t_name, 'Error')
            lock.release()
            sch.debuffer(url)
            sch.enqueue(url)            

    t_print(t_name, 'Done')

config = read_config()
threads = []
print('Starting...')
for i in range(config['n_thread']):
    t = threading.Thread(name=i+1, target=worker)
    t.daemon = True
    threads.append(t)
    t.start()
while True:
    all_terminated = True
    for t in threads:
        if t.is_alive():
            all_terminated = False
            break
    if all_terminated:
        break
    time.sleep(1)