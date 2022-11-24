import sys
import os
import time
import multiprocessing

from pymongo import MongoClient, TEXT
from pymongo.collection import Collection
from datetime import datetime


def insert_data(filename:str, port:str) -> None:
    start = datetime.now()
    c = multiprocessing.cpu_count()
    print(c)
    cmd_str = f"mongoimport --port {port} --db 291db --collection dblp --drop --batchSize 15000 --file {filename} --numInsertionWorkers {c}"
    os.system(cmd_str)
    
    client = MongoClient(f"mongodb://localhost:{port}")
    db = client["291db"]
    dblp = db["dblp"]
    
    dblp.create_index(
        keys = [
            ("references", 1)
        ]
    )
    # print(f"Reference index create complete, time: {datetime.now()}")
    
    dblp.aggregate([
        {
            "$lookup": {
                "from": "dblp",
                "localField": "id",
                "foreignField": "references",
                "as": "referenced_by_count"
            }
        },
        {
            "$addFields":{
                "referenced_by_count": "$referenced_by_count.id", #{"$size": "$referenced_by_count"},
                "referenced_by_count_num": {"$size": "$referenced_by_count"},
                "yearStr": {"$toString": "$year"}
            }
        },
        {"$out": "dblp"}
    ])
    # print(f"Aggregation complete, time: {datetime.now()}")
    
    dblp.create_index(
        keys = [
            ("title", TEXT),
            ("authors", TEXT),
            ("abstract", TEXT),
            ("venue", TEXT),
            ("yearStr", TEXT)
        ],
        #default_language='none'
    )
    
    dblp.aggregate([
        {
            "$match": {
                "venue": {
                    "$exists": "true",
                    "$nin": ["", "null"]
                }
            }
        },
        
        {
            "$group": {
                "_id": "$venue",
                "article_count": {"$sum": 1}
            }
        },
        {"$out": "dblp-article-count"}
    ])
    
    dblp.aggregate([
        {
            "$match": {
                "venue": {
                    "$exists": "true",
                    "$nin": ["", "null"]
                }
            }
        },
        {
            "$group": {
                "_id": "$venue",
                "referenced_by_count": {"$sum": "$referenced_by_count_num"}
            }
        },
        {
            "$match": {"referenced_by_count": 0}
        },
        {
            "$lookup": {
                "from": "dblp-article-count",
                "localField": "_id",
                "foreignField": "_id",
                "as": "article_count"
            }
        },
        {"$unwind": "$article_count"},
        {
            "$project": {
                #"venue": "$_id",
                "referenced_by_count": "$referenced_by_count",
                "article_count": "$article_count.article_count"
            }
        },
        {"$out": "dblp-zero-citation"}
    ])
    
    result = dblp.aggregate([

        # execlude null and empty venue name
        {
            "$match": {
                "venue": {
                    "$exists": "true",
                    "$nin": ["", "null"]
                }
            }
        },
        
        {
            "$unwind": {
                "path": "$referenced_by_count",
                # "preserveNullAndEmptyArrays": True
            }
        },
        
        {
            "$group": {
                "_id": {
                    "venue": "$venue",
                    "referenced_by_count": "$referenced_by_count"
                }
            }
        },
        
        {
            "$group": {
                "_id": "$_id.venue",
                "referenced_by_count": {
                    "$sum": 1
                },
            }
        },
        {
            "$lookup": {
                "from": "dblp-article-count",
                "localField": "_id",
                "foreignField": "_id",
                "as": "article_count"
            }
        },
        {"$unwind": "$article_count"},
        {
            "$project": {
                #"venue": "$_id",
                "referenced_by_count": "$referenced_by_count",
                "article_count": "$article_count.article_count"
            }
        },
        
        {
            "$unionWith": {"coll": "dblp-zero-citation"}
        },
        
        {
            "$sort": {"referenced_by_count": -1}
        },
        {"$out": "dblp-citation-count"}
        
        # {
        #     "$group":
        #         {
        #             "_id": "$venue",
        #             "referenced_by_count": {"$push": "$referenced_by_count"},
        #             "article_sum": {"$sum": 1}
        #         }
        # },
        # {
        #     "$addFields": {
        #         "referenced_by_count": {
        #             "$reduce": {
        #                 "input": "$referenced_by_count",
        #                 "initialValue": [],
        #                 "in": { "$concatArrays": [ "$$value", "$$this" ] }
        #             }
        #         }
        #     }
        # },
        # {
        #     "$sort": {"referenced_by_count": -1}
        # },

    ])
    
    print(f"Database Construction complete, running time: {datetime.now()-start}")
    # print(f"Database construction finished in {time.time() - t} sec.")

def main() -> None:
    filename:str = input('file name: ')
    port:str = input('port: ')
    insert_data(filename,port)

if __name__ == "__main__":
    main()