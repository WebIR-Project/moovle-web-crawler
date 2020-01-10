import json
from urllib.parse import urlparse
from pymongo import MongoClient
from datetime import datetime

class Scheduler:
    def __init__(self):
        self.read_config()
        client = MongoClient()
        self.db = client[self.config['DB']]

    def read_config(self):
        f = open('config.json')
        self.config = json.load(f)
        f.close()

    def enqueue(self, url):
        visited = True if self.db['visited'].find({'url': url}).count() > 0 else False
        in_queue = True if self.db['queue'].find({'url': url}).count() > 0 else False
        in_buffer = True if self.db['buffer'].find({'url': url}).count() > 0 else False
        banned = True if self.db['ban'].find({'url': url}).count() > 0 else False
        if not visited and not in_queue and not in_buffer and not banned:
            parsed_url = urlparse(url)
            host = parsed_url.netloc
            self.db.queue.insert_one({'url': url, 'host': host, 'timestamp': datetime.now()})

    def get_new_host_url(self):
        host_counts = list(self.db.host_count.find())
        hosts = [host['host'] for host in host_counts]
        urls = list(self.db.queue.aggregate([{'$match': {'host': {'$nin': hosts}}}, {'$sort': {'timestamp': 1}}, {'$limit': 1}]))
        if len(urls) > 0:
            return urls[0]
        else:
            return None

    def get_queue_length(self):
        return self.db.queue.count()
        
    def dequeue(self):
        url = None
        if self.get_queue_length() > 0:
            url = self.get_new_host_url()
            host_counts = list(self.db.host_count.aggregate([{'$sort': {'count': 1}}]))
            if url is None:
                for host in host_counts:
                    url_result = list(self.db.queue.aggregate([{'$match': {'host': host['host']}}, {'$sort': {'timestamp': 1}}, {'$limit': 1}]))
                    if len(url_result) > 0:
                        url = url_result[0]
                        break
        if url is not None:
            self.db.queue.remove({'url': url['url']})
            self.db.buffer.insert_one({'host': url['host'], 'url': url['url']})
        return url['url']

    def debuffer(self, url):
        self.db.buffer.remove({'url': url})

    def clean_buffer(self):
        urls = list(self.db.buffer.find())
        if len(urls) > 0:
            for url in urls:
                self.db.queue.insert_one({'host': url['host'], 'url': url['url'], 'timestamp': 0})
                self.db.buffer.remove({'url': url['url']})

    def visited(self, url):
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        self.db['visited'].insert_one({'url': url})
        if self.db.host_count.find({'host': host}).count() > 0:
            self.db.host_count.update({'host': host}, {'$inc': {'count': 1}})
        else:
            self.db.host_count.insert_one({'host': host, 'count': 1})