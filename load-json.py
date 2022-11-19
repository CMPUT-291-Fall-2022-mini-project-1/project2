import sys
import os
import multiprocessing

from pymongo import MongoClient, TEXT
from pymongo.collection import Collection
from datetime import datetime

def insert_data(filename:str, port:str) -> None:
    print(multiprocessing.cpu_count())
    cmd_str = f"mongoimport --port {port} --db 291db --collection dblp --drop --batchSize 15000 --file {filename} --numInsertionWorkers {multiprocessing.cpu_count()}"
    os.system(cmd_str)
    
    client = MongoClient(f"mongodb://localhost:{port}")
    db = client["291db"]
    dblp = db["dblp"]
    #dblp.update_many({}, {"$set": {"yearStr": "$year"}})
    dblp.create_index(
        keys = [
            ("references", 1)
        ]
    )
    print(f"Reference index create complete, time: {datetime.now()}")
    
    dblp.aggregate([
        {"$addFields":
            {"yearStr": {"$toString": "$year"}},
        },
        {
            "$lookup": {
                "from": "dblp",
                "localField": "id",
                "foreignField": "references",
                "as": "referenced_by_count"
            }
        },
        {"$addFields":
            {"referenced_by_count": {"$size": "$referenced_by_count"}},
        },
        # {"$project": {
        #     "_id": "$_id",
        #     ""
        # }}
        {"$out": "dblp"}
    ])
    print(f"Aggregation complete, time: {datetime.now()}")
    
    dblp.create_index(
        keys = [
            ("title", TEXT),
            ("authors", TEXT),
            ("abstract", TEXT),
            ("venue", TEXT),
            ("yearStr", TEXT)
        ],
        # default_language='none'
    )
    print(f"Search index create complete, time: {datetime.now()}")


def main() -> None:
    filename:str = input('file name: ')
    port:str = input('port: ')
    insert_data(filename,port)

if __name__ == "__main__":
    main()