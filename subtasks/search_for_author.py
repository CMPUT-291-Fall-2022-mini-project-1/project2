from pymongo.collection import Collection
from ui import *

def search_for_authors(dblp:Collection):
    
    # get single keyword
    keyword = ""
    while keyword.isspace() or keyword == "":
        keyword = input("Enter your keyword: ")
    dot_placeholder = "<dot"
    keyword = keyword.replace(".", dot_placeholder)
    keyword_regex = f".*\\b{keyword}\\b.*"
    
    # match to authors; author arrays need to be splitted
    # result should be sorted based on year with more recent articles shown first
    search_res = dblp.aggregate([
        {"$match": {"$text": {"$search": keyword}}},
        {"$unwind": "$authors"},
        {"$set": {"author_search_only": {"$replaceAll": {"input": "$authors", "find": ".", "replacement": dot_placeholder}}}},
        {"$match": {"author_search_only": {"$regex": keyword_regex, "$options": "i"}}},
        {"$sort": {"year": -1}}
    ])
    
    # store the search result for later reference; no need to search again
    author_dict = {}
    for res in search_res:
        author = res["authors"]
        if author not in author_dict:
            author_dict[author] = [res]
        else:
            author_dict[author].append(res)
    
    # for each author, list the author name and the number of publications
    i = 0
    index_dict = {}
    for author in author_dict.keys():
        i += 1
        AUTHOR_UI(author, i, len(author_dict[author]))
        index_dict[str(i)] = author
    
    # let user select an author and see the title, year, and venue of all articles by that author
    while True:
        selection = input("Enter your selection or press ENTER to cancel: ")
        if selection == "":
            return
        if selection not in index_dict:
            print("Invalid selection.")
        else:
            break
    selected_author = index_dict[selection]
    
    # see the title, year, and venue of all articles by that author
    fields = ["title", "year", "venue"]
    print(f"==================== {selected_author}'s Articles ====================")
    i = 1
    for article in author_dict[selected_author]:
        ARTICLE_UI(article, i, fields)
        i += 1
    
    