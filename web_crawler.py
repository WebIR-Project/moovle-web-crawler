import analyzer, json
from pymongo import MongoClient
from threading import Thread, Lock
from downloader import Downloader
from robots_parser import RobotParser
from scheduler import Scheduler

def read_config():
    f = open('config.json')
    config = json.load(f)
    f.close()
    return config

def worker(thread_name, ):
    downloader = Downloader(use_proxies=True)
    while True:
        lock.acquire()
        if db.queue.count() == 0:
            break
        url = scheduler.dequeue()
        lock.release()


if __name__ == '__main__':
    config = read_config()
    client = MongoClient()
    db = client.moovle
    scheduler = Scheduler()
    rp = RobotParser(user_agent='random')
    threads = []
    lock = Lock()
    for i in range(config['n_thread']):
        t = Thread(target=worker)
        threads.append(t)
        t.start()
