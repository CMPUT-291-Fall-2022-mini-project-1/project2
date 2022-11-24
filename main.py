import sys

from pymongo import MongoClient
from pymongo.collection import Collection

from ui import *
from tasks import task_dict

def main(port):
    
    # make a connection
    try:
        client = MongoClient(f"mongodb://localhost:{port}")
    except:
        print(f"Invalid port: {port}")
        exit()
    
    # load the collection
    db = client["291db"]
    try:
        collection_list = db.list_collection_names()
    except:
        print(f"Invalid port: {port}")
        exit()
    if "dblp" not in collection_list:
        print("Data not loaded yet")
        exit()
    if "dblp-article-count" in collection_list:
        db["dblp-article-count"].drop()
    if "dblp-zero-citation" in collection_list:
        db["dblp-zero-citation"].drop()
    dblp = db["dblp"]
    
    # display UI & ask for selection
    while True:
        print(MAIN_UI)
        opt = input("Select one option: ")
        while opt not in task_dict:
            print("Please make a proper selection")
            opt = input("Select one option: ")
        
        if opt == "3":
            dblp_venue = db["dblp-citation-count"]
            task_dict[opt](dblp_venue)
            continue
    
        # process corresponding action
        if task_dict[opt] is None:
            client.close()
            exit()
        task_dict[opt](dblp)
    

if __name__ == "__main__":
    port = input("port: ")
    main(port)
