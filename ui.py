MAIN_UI = """
==================================
= 1. Search for articles
= 2. Search for authors
= 3. List the venues
= 4. Add an article
= 5. Exit
==================================
"""

def ARTICLE_UI(article, index, fields):
    if index:
        print(f"{index}.")
    for f in fields:
        if f not in article:
            article[f] = ""
        print(f"     {f}: {article[f]}")



def AUTHOR_UI(author, index, num_publications):
    if index == 1:
        print("===================== Author Name & Number of Publications ===================")
    print(f"{index}. {author} | num_publications: {num_publications}")
