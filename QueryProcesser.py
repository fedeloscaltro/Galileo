from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, QueryParser, WildcardPlugin
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.query import Term

import datetime

import nltk
from nltk.corpus import stopwords


def tokenize(raw):
    """
    Function to get tokens from the query text
    :param raw: the query text
    :return: the processed tokens
    """
    tokens = nltk.word_tokenize(raw)  # isolate single words
    return tokens


def lemmatize(tokens):
    """
    Function to delete the stopwords and lemmatize the tokens from the original query
    :param tokens: words to analyze from the query
    :return: a list of words yet to finish their processing phase
    """

    wln = nltk.WordNetLemmatizer()

    list_words = [wln.lemmatize(t) for t in tokens if t not in stopwords.words('english')]  # delete stopwords
    return list_words


def source_filter(query, ix):
    qparser = QueryParser("path", ix.schema)
    qparser.add_plugin(WildcardPlugin())

    esa = ""
    space = ""
    blue_origin = ""

    if (query['esa']):
        esa = "*www.esa.int*"

    if (query['space']):
        space = "*www.space.com*"

    if (query['blue_origin']):
        blue_origin = "*www.blueorigin.com*"

    if ((not query['esa']) and (not query['space']) and (not query['blue_origin'])):
        sources = qparser.parse("*www.space.com* OR *www.esa.int* OR *www.blueorigin.com*")

    else:
        sources = qparser.parse(f"({esa} OR {blue_origin}) OR {space}")
    
    return sources


def date_filter(query, ix):
    qparser = QueryParser("date", ix.schema)
    qparser.add_plugin(DateParserPlugin())
    date_range = qparser.parse(f"<{datetime.datetime.strptime(query['from'], '%Y-%m-%d')} AND >{datetime.datetime.strptime(query['to'], '%Y-%m-%d')}")

    print(date_range)



def processer(query):
    print(query)
    tokens = tokenize(query['text'])
    query_string = ""
    for w in lemmatize(tokens):     # for each lemmatized word
        query_string += w + " "    # add it to the final query object
    # print(query, '\n')  # TODO: Delete this print statement when the query process is finished

    ix = open_dir("../index")  # open the index and assign it to "ix"

    sources = source_filter(query, ix)
    date_filter(query, ix)

    parser = MultifieldParser(["title", "content", "date"],
                              ix.schema)  # setting the query parse with the specified field of the schema
    parser.add_plugin(DateParserPlugin(free=True))   # Add the DateParserPlugin to the parser
    user_query = parser.parse(query_string)  # parsing the query and returning a query object to search (use "date:")

    results = {}
    with ix.searcher() as searcher:
        result = searcher.search(user_query, filter=sources)  # search the query
        # print(result[0:])  # print the top 10 results
        results = [{f:i[f] for f in i.fields()} for i in result]
    
    return results