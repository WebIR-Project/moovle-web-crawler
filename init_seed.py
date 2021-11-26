from pymongo import MongoClient
from urllib.parse import urlparse
from datetime import datetime

def read_seed():
    f = open('./seed.txt')
    seeds = f.read().split('\n')
    f.close()
    return seeds

seeds = read_seed()
client = MongoClient()
db = client.moovle
for seed in seeds:
    p = urlparse(seed)
    db.queue.insert({'url': seed, 'host': p.netloc, 'timestamp': datetime.now()})