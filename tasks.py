import re

from pymongo.collection import Collection
from ui import *

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
    return

def list_the_venues(dblp:Collection):
    return

def add_an_article(dblp:Collection):
    return

task_dict = {
    "1": search_for_articles,
    "2": search_for_authors,
    "3": list_the_venues,
    "4": add_an_article,
    "5": None
}
