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
            "$group":
                {
                    "_id": "$venue",
                    "referenced_by_count": {"$push": "$referenced_by_count"},
                    "article_sum": {"$sum": 1}
                }
        },
        {
            "$addFields": {
                "referenced_by_count": {
                    "$reduce": {
                        "input": "$referenced_by_count",
                        "initialValue": [],
                        "in": { "$concatArrays": [ "$$value", "$$this" ] }
                    }
                }
            }
        },
        {
            "$sort": {"referenced_by_count": -1}
        },

    ])

    print("==================== Venues ====================")

    index = 1
    for venue in result:
        if venue["_id"] is None or venue["_id"] == "":
            continue
        print(str(index) + ".")
        print("     " + "venue: " + venue["_id"])
        print("     " + "article count: " + str(venue["article_sum"]))
        print("     " + "citation count: " +
              str(len(set(venue["referenced_by_count"]))))
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
