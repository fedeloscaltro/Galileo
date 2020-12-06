from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh.qparser.dateparse import DateParserPlugin


def main():
    ix = open_dir("index")  # open the index and assign it to "ix"

    parser = MultifieldParser(["title", "content", "date"],
                              ix.schema)  # setting the query parse with the specified field of the schema
    parser.add_plugin(DateParserPlugin(free=True))   # Add the DateParserPlugin to the parser
    query = parser.parse(u"date:15 oct 2019")  # parsing the query and returning a query object to search (use "date:")

    with ix.searcher() as searcher:
        result = searcher.search(query)  # search the query
        print(result[0:])  # print the top 10 results


if __name__ == '__main__':
    main()
