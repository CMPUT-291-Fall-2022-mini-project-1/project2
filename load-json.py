import pymongo
import sys
import json
from pymongo.collection import Collection

dblp:Collection = None

def connect_db(port:str) -> None:
    
    global dblp

    # Use client = MongoClient('mongodb://localhost:27017') for specific ports!
    # Connect to the default port on localhost for the mongodb server.
    client = pymongo.MongoClient(f'mongodb://localhost:{port}')


    db = client["291db"]


    # List collection names.
    collist = db.list_collection_names()
    if "dblp" in collist:
        print("The collection exists.")

    # Create or open the collection in the db
    dblp = db["dblp"]
    dblp.delete_many({})

    print('connect successful')

    return dblp



def insert_data(filename:str) -> None:
    cnt = 1
    batch = 100000
    datas = []
    print(f'batch size = {batch}')
    with open(filename,'r') as f:
        while line := f.readline():
            datas.append(json.loads(line))
            if len(datas) == batch:
                dblp.insert_many(datas)
                print(f'batch {cnt} insert successful')
                cnt += 1
                datas = []
        if len(datas)!=batch and len(datas)!=0:
            dblp.insert_many(datas)
            print(f'batch {cnt+1} insert successful')
    print('insert successful')



def main(filename:str, port:str) -> None:
    connect_db(port)
    insert_data(filename)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("filename and port required")
        exit()
    main(sys.argv[1], sys.argv[2])