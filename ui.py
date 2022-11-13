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
        print(f"     {f}: {article[f]}")
