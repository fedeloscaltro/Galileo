import os.path

from whoosh.fields import *
from whoosh.index import create_in
from whoosh.analysis import StemmingAnalyzer


def main():
    schema = Schema(    # the schema of an indexed file
        date=DATETIME(stored=True),  # date of the article
        path=ID(stored=True),   # url of the article
        title=TEXT(stored=True, field_boost=2.0, analyzer=StemmingAnalyzer()),     # title of the article
        content=TEXT(stored=True, analyzer=StemmingAnalyzer())    # content of the article
    )

    if not os.path.exists("index"):     # create the directory with the index
        os.mkdir("index")

    ix = create_in("index", schema)     # instance of the index

    writer = ix.writer()    # instance of the writer, used to add the files to the index

    for filename in os.listdir("Articles"):     # iterate on every file in the directory of articles
        with open("Articles/"+filename, 'r', encoding='utf-8') as file:
            article_date = file.readline().replace("\n", "")    # extract the date from the file
            try:
                article_date = datetime.datetime.strptime(article_date, "%Y-%m-%d")     # convert the string in a date obj
            except (ValueError):
                article_date = datetime.datetime.strptime("1970-01-02", "%Y-%m-%d")
            
            path = file.readline()
            title = file.readline()
            article_content = ""
            for row in file.readlines():
                article_content += row
            article_content = article_content.replace("\\n", "\n")
            article_content = article_content.replace("\\xa0", " ")
            writer.add_document(    # add the article to the index with its fields
                date=article_date,
                path=path,
                title=title,
                content=article_content
            )

    writer.commit()     # saves the added documents to the index


if __name__ == '__main__':
    main()
