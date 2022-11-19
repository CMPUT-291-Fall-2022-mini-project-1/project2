import re

from pymongo.collection import Collection
from ui import *
from subtasks.search_for_articles import search_for_articles
from subtasks.search_for_author import search_for_authors
from subtasks.add_an_article import add_an_article


def list_the_venues(dblp: Collection):
    
    while True:
        try:
            topN = int(input("Please provide top number: "))
            if topN <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid top number.")
    result = dblp.aggregate([
        {
                "$match": {
                    "venue": {
                        "$exists": "true",
                        "$nin": ["", "null"]
                    }
                }
            },
            {
                "$group":
                {
                    "_id": "$venue",
                    "citation_sum": {"$sum": "$referenced_by_count"},
                    "article_sum": {"$sum": 1}
                }
            },
            {
                "$sort": {"citation_sum": -1}
            },

    ])
    
    print("==================== Venues ====================")

    index = 1
    for venue in result:
        print(str(index) + ".")
        print("     " + "venue: " + venue["_id"])
        print("     " + "article count: " + str(venue["article_sum"]))
        print("     " + "citation count: " +
              str(venue["citation_sum"]))
        if index == topN:
            break
        else:
            index += 1

    return


task_dict = {
    "1": search_for_articles,
    "2": search_for_authors,
    "3": list_the_venues,
    "4": add_an_article,
    "5": None
}
