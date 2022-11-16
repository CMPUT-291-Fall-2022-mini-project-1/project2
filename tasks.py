import re

from pymongo.collection import Collection
from ui import *
from add_an_article import add_article

def search_for_articles(dblp:Collection):
    
    # get all user keywords
    keywords = list(set(input("Enter your keywords, separated by spaces: ").split(" ")))
    keywords = [re.compile(f".*{k}.*", re.IGNORECASE) for k in keywords]
    
    # match to title, authors, abstract, venue, year
    default_value = "N/A"
    articles = dblp.aggregate([
        {"$addFields": {"yearStr": {"$toString": "$year"}}},
        {"$match": {
            "$or": [
                {"title": {"$in": keywords}},
                {"authors": {"$in": keywords}},
                {"abstract": {"$in": keywords}},
                {"venue": {"$in": keywords}},
                {"yearStr": {"$in": keywords}}
                ]
            }
        },
        {"$project": {
            "_id": 0,
            "id": {"$ifNull": ["$id", default_value]},
            "title": {"$ifNull": ["$title", default_value]},
            "year": {"$ifNull": ["$year", default_value]},
            "venue": {"$ifNull": ["$venue", default_value]},
            "abstract": {"$ifNull": ["$abstract", default_value]},
            "authors": {"$ifNull": ["$authors", default_value]}
        }}
    ])
    
    # display search result for user to select
    print("==================== Articles ====================")
    i = 1
    fields = ["id", "year", "venue", "title"]
    select_dict = {"": None}
    for ac in articles:
        ARTICLE_UI(ac, i, fields)
        select_dict[str(i)] = ac
        i += 1
    
    # let user select one option
    selected_ind = input("Select one of the articles, or type enter to cancel: ")
    while selected_ind not in select_dict:
        print("Please make a proper selection.")
        selected_ind = input("\nSelect one of the articles, or type enter to cancel: ")
    selected_article = select_dict[selected_ind]
    if selected_article is None:
        return
    
    # display the detail of selected article
    fields = ["id", "year", "venue", "authors", "title", "abstract"]
    print("\nArticle detail:")
    ARTICLE_UI(selected_article, 0, fields)
    referenced_by_articles = dblp.find({"references": selected_article["id"]})
    i = 1
    for rba in referenced_by_articles:
        if i == 1:
            print("This article is referenced by:")
        ARTICLE_UI(rba, i, ["id", "title", "year"])
        i += 1
    if i == 1:
        print("This article is not being referenced.")



def search_for_authors(dblp:Collection):
    
    # get single keyword
    keyword = input("Enter your keyword: ")
    keyword = re.compile(f".*{keyword}.*", re.IGNORECASE)
    
    # match to authors
    _temp_res = dblp.find({"authors": {"$regex": keyword}})
    # authors = dblp.distinct("authors", {"authors": {"$regex": keyword}})
    authors = set()
    for _r in _temp_res:
        authors.update(_r["authors"])
    i = 1
    author_dict = {"": None}
    for aname in authors:
        if not re.match(keyword, aname):
            continue
        # for each author find number of publications
        num_publications = dblp.count_documents({"authors": aname})
        AUTHOR_UI(aname, i, num_publications)
        author_dict[str(i)] = aname
        i += 1
    
    # let user select one author
    while True:
        selected_author = author_dict.get(input("Enter your selection or press ENTER to cancel: "), "")
        if selected_author is None:
            return
        if selected_author == "":
            print("Invalid selection.")
        else:
            break
    
    # use the selected author to find all articles
    default_value = "N/A"
    articles = dblp.aggregate([
        {"$match": {"authors": selected_author}},
        {"$sort": {"year": -1}},
        {"$project": {
            "_id": 0,
            "id": {"$ifNull": ["$id", default_value]},
            "title": {"$ifNull": ["$title", default_value]},
            "year": {"$ifNull": ["$year", default_value]},
            "venue": {"$ifNull": ["$venue", default_value]},
            "abstract": {"$ifNull": ["$abstract", default_value]},
            "authors": {"$ifNull": ["$authors", default_value]}
        }}
    ])
    
    # display all articles by that author
    fields = ["title", "year", "venue"]
    print(f"==================== {selected_author}'s Articles ====================")
    i = 1
    for a in articles:
        ARTICLE_UI(a, i, fields)
        i += 1


def list_the_venues(dblp:Collection):
    return

def add_an_article(dblp:Collection):
    
    while True:
        
        # ask for a unique id
        _id = input("Please provide a unique id: ")
        if len(_id) == 0:
            print('id can not be empty')
            continue
        res = dblp.find_one({"id": _id})
        if res:
            print("id not unique")
            continue
        
        # ask for a title
        title = input("Provide a title: ")
        while len(title) == 0:
            print("title cannot be empty")
            title = input("Provide a title: ")
        
        # ask for multiple authors
        authors = []
        i = 1
        while True:
            if i != 1:
                aut = input(f"Enter Author {i} or press ENTER to finish: ")
                if aut == "":
                    break
            else:
                aut = input(f"Enter Author {i}: ")
                if aut == "":
                    print("Authors cannot be empty. At least 1 author need to be provided.")
                    continue
            authors.append(aut)
            i += 1
        
        # ask for year
        while True:
            try:
                year = int(input("Enter year: "))
                break
            except ValueError:
                print("Year is not valid.")
                continue
        
        # insert the new article
        article = {
                'abstract': None,
                'venue': None,
                'references': [],
                'n_citations': 0,
                'id': _id,
                'title': title,
                'authors': authors,
                'year': year
            }
        dblp.insert_one(article)
        print("Add an article successful")
        break


task_dict = {
    "1": search_for_articles,
    "2": search_for_authors,
    "3": list_the_venues,
    "4": add_an_article,
    "5": None
}
