from pymongo import MongoClient
from pymongo.collection import Collection
def add_article(dblp:Collection) -> None:
   while True:
        _id = input('provide a unique id: ')
        if len(_id) == 0:
            print('id can not be empty')
            continue
        res = dblp.find_one({'id':_id})
        if not res:
            _title = input('input a title: ')
            if len(_title) == 0:
                print('title can not be empty')
                continue
            _authors = input('One or more authors separated by spaces: ').split()
            if len(_authors) == 0:
                print('authors can not be empty')
                continue
            try:
                _year = int(input('year: '))
            except ValueError:
                print('year not a valid value')
                continue
            article = {
                'abstract':None,
                'venue':None,
                'references': [],
                'n_citations': 0,
                'id':_id,
                'title':_title,
                'authors':_authors,
                'year':_year,
            }
            dblp.insert_one(article)
            print('Add an article successful')
            break
        else:
            print("id not unique")
            continue


def main() -> None:
    port = '27012'
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
    dblp = db["dblp"]
    add_article(dblp)

if __name__ == "__main__":
    main()