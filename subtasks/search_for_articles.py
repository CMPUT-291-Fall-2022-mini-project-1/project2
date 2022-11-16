from pymongo.collection import Collection
from ui import *
from add_an_article import add_article

def search_for_articles(dblp:Collection):
    
    # get all user keywords, 
    keywords = list(set(input("Enter your keywords, separated by spaces: ").split(" ")))
    keywords_text, keywords_number = [], []
    for k in keywords:
        try:
            keywords_number.append(int(k))
            keywords_text.append(k)
        except ValueError:
            keywords_text.append(k)
    
    