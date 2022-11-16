import sys
import os

from pymongo import MongoClient
from pymongo.collection import Collection


def insert_data(filename:str, port:str) -> None:
    cmd_str = f"mongoimport --port {port} --db 291db --collection dblp --drop --batchSize 15000 --file {filename}"
    os.system(cmd_str)
    
    client = MongoClient(f"mongodb://localhost:{port}")
    db = client["291db"]
    dblp = db["dblp"]
    #dblp.update_many({}, {"$set": {"yearStr": "$year"}})
    dblp.aggregate([
        {"$addFields": {"yearStr": {"$toString": "$year"}}},
        {"$out": "dblp"}
    ])
    
    dblp.create_index([
        ("title", "text"),
        ("authors", "text"),
        ("abstract", "text"),
        ("venue", "text"),
        ("yearStr", "text")
    ])



def main() -> None:
    filename:str = input('file name: ')
    port:str = input('port: ')
    insert_data(filename,port)

if __name__ == "__main__":
    main()