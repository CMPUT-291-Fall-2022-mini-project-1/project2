import re

from pymongo.collection import Collection
from ui import *
from subtasks.search_for_articles import search_for_articles
from subtasks.search_for_author import search_for_authors
from subtasks.add_an_article import add_an_article


def list_the_venues(dblp: Collection):

    # check for inut number n
    while True:
        try:
            topN = int(input("Please provide top number: "))
            if topN <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid top number.")
    
    result = dblp.find({})

    print("==================== Venues ====================")

    index = 1
    for venue in result:
        if venue["_id"] is None or venue["_id"] == "":
            continue
        print(str(index) + ".")
        print("     " + "venue: " + venue["_id"])
        print("     " + "article count: " + str(venue["article_count"]))
        print("     " + "citation count: " +
              str(venue["referenced_by_count"]))
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
