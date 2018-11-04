import json
from pymongo import MongoClient

class Scheduler:
    def __init__(self):
        self.read_config()
        client = MongoClient()
        self.db = client[self.config['DB']]

    def read_config(self):
        f = open('config.json')
        self.config = json.load(f)
        f.close()
