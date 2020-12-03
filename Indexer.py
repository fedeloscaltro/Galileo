from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.query import *
import os.path


def main():
    schema = Schema(    # the schema of an indexed file
        data=DATETIME,  # date of the article
        path=ID(stored=True),   # url of the article
        title=TEXT,     # title of the article
        content=TEXT    # content of the article
    )

    if not os.path.exists("index"):     # create the directory with the index
        os.mkdir("index")

    ix = create_in("index", schema)     # instance of the index

    writer = ix.writer()    # instance of the writer, used to add the files to the index

    for filename in os.listdir("Articles"):     # iterate on every file in the directory of articles
        with open("Articles/"+filename, 'r', encoding='utf-8') as file:
            writer.add_document(    # add the article to the index with its fields
                data=file.readline(),
                path=file.readline(),
                title=file.readline(),
                content=file.readlines()
            )

    writer.commit()     # saves the added documents to the index


    """with ix.searcher() as searcher:
        result = searcher.search(query)
        print(result)"""


if __name__ == '__main__':
    main()