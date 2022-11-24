from pymongo.collection import Collection


def add_an_article(dblp: Collection):

    while True:

        # ask for a unique id
        _id = input("Please provide a unique id: ")
        if len(_id) == 0:
            print('id can not be empty')
            continue
        res = dblp.find_one({"id": _id})
        if res:
            print("id not unique")
            continue

        # ask for a title
        title = input("Provide a title: ")
        while len(title) == 0:
            print("title cannot be empty")
            title = input("Provide a title: ")

        # ask for multiple authors
        authors = []
        i = 1
        while True:
            if i != 1:
                aut = input(f"Enter Author {i} or press ENTER to finish: ")
                if aut == "":
                    break
            else:
                aut = input(f"Enter Author {i}: ")
                if aut == "":
                    print(
                        "Authors cannot be empty. At least 1 author need to be provided.")
                    continue
            authors.append(aut)
            i += 1

        # ask for year
        while True:
            try:
                year = int(input("Enter year: "))
                break
            except ValueError:
                print("Year is not valid.")
                continue
        
        # get referenced by count
        referenced_by_count = dblp.find({"references": _id})
        reference_list = list(set([r["id"] for r in referenced_by_count]))

        # insert the new article
        # user provided: id, title, authors, year
        # empty field: abstract (null), venue (null), references ([]), n_citations (0)
        # extra field: yearStr, referenced_by_count
        article = {
            'abstract': None,
            'venue': None,
            'references': [],
            'n_citations': 0,
            'id': _id,
            'title': title,
            'authors': authors,
            'year': year,
            'yearStr': str(year),
            'referenced_by_count': reference_list,
            'referenced_by_count_num': len(reference_list)
        }
        dblp.insert_one(article)
        print("Add an article successful")
        break
