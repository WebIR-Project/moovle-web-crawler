"""
Clean duplicated pages
"""
import time
from pymongo import MongoClient
start_time = time.time()
c = MongoClient()
db = c.moovle
dups = list(db.pages.aggregate([
    {'$group': {'_id': '$url', 'count': {'$sum': 1}}},
    {'$match': {'count': {'$gt': 1}}}
]))
for dup in dups:
    for i in range(dup['count'] - 1):
        db.pages.delete_one({'url': dup['_id']})
print(f'Time used: {(time.time() - start_time):.3f} s')