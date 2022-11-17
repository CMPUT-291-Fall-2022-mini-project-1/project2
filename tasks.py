import re

from pymongo.collection import Collection
from ui import *
from subtasks.search_for_articles import search_for_articles
from subtasks.search_for_author import search_for_authors
from subtasks.add_an_article import add_an_article


def list_the_venues(dblp: Collection):

    venueCount = {}
    venues = dblp.distinct("venue")
    venues.remove("")

    for venue in venues:
        articleInVenue = dblp.find({"venue": venue})
        venueCount[venue] = [0]
        articleCount = 0
        for article in articleInVenue:
            articleCount += 1
            venueCount[venue][0] += article["n_citation"]
        venueCount[venue].append(articleCount)

    topN = int(input("Enter top number: "))
    print("==================== Venues ====================")

    index = 1
    for venueName in sorted(venueCount, key=venueCount.get, reverse=True):
        print(str(index) + ".")
        print("     " + "venue: " + venueName)
        print("     " + "article count: " + str(venueCount[venueName][1]))
        print("     " + "citation count: " + str(venueCount[venueName][0]))
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
