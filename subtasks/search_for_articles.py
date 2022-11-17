from pymongo.collection import Collection
from ui import *
from add_an_article import add_article

def search_for_articles(dblp:Collection):
    
    # get all user keywords, make them as phrases to perform AND semantic
    keywords = []
    while len(keywords) == 0:
        keywords = set(input("Enter your keywords, separated by spaces: ").split(" "))
        keywords.discard("")
        keywords = [f"\"{k}\"" for k in keywords]

    # apply text searching on those keywords
    query = {"$text": {"$search": f"{' '.join(keywords)}"}}
    
    # match to title, authors, abstract, venue, yearStr
    articles = dblp.find(query)
    
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
    selected_ind = input(
        "Select one of the articles, or type enter to cancel: ")
    while selected_ind not in select_dict:
        print("Please make a proper selection.")
        selected_ind = input(
            "\nSelect one of the articles, or type enter to cancel: ")
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
    