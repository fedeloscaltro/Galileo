from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.query import *
import os.path


def main():
    schema = Schema(    # the schema of an indexed file
        date=DATETIME(stored=True),  # date of the article
        path=ID(stored=True),   # url of the article
        title=TEXT(stored=True),     # title of the article
        content=TEXT(stored=True)    # content of the article
    )

    if not os.path.exists("index"):     # create the directory with the index
        os.mkdir("index")

    ix = create_in("index", schema)     # instance of the index

    writer = ix.writer()    # instance of the writer, used to add the files to the index

    for filename in os.listdir("Articles"):     # iterate on every file in the directory of articles
        with open("Articles/"+filename, 'r', encoding='utf-8') as file:
            writer.add_document(    # add the article to the index with its fields
                date=file.readline(),
                path=file.readline(),
                title=file.readline(),
                content=str(file.readlines()).replace("\\n", "\n")
            )

    writer.commit()     # saves the added documents to the index

    parser = QueryParser("content", ix.schema)
    query = parser.parse(u"yah")

    with ix.searcher() as searcher:
        result = searcher.search(query)
        print(result[0:])


if __name__ == '__main__':
    main()