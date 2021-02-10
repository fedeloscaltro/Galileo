from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser, QueryParser, WildcardPlugin, OrGroup
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.query import Term

import datetime

import nltk
from nltk.corpus import stopwords

import pandas as pd

import re


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
    """
    Function that filter by the sources. It uses a QueryParser that works on the "path" field of the schema.
    It selects only the sources that the user wants the links belong to.
    :param query: the query submitted by the user
    :param ix: the index, used to access the schema
    :return: the sources on which the user wants to perform the query
    """
    qparser = QueryParser("path", ix.schema)
    qparser.add_plugin(WildcardPlugin())    # utilize the Wildcard plugin to match the sources in the url

    esa = ""
    space = ""
    blue_origin = ""

    if query['esa']:  # if the user wants articles from ESA
        esa = "*www.esa.int*"

    if query['space']:    # if the user wants articles from space.com
        space = "*www.space.com*"

    if query['blue_origin']:  # if the user wants articles from blueorigin.com
        blue_origin = "*www.blueorigin.com*"

    # if no source is selected add all by default
    if (not query['esa']) and (not query['space']) and (not query['blue_origin']):
        sources = qparser.parse("*www.space.com* OR *www.esa.int* OR *www.blueorigin.com*")
        
    else:
        sources = qparser.parse(f"({esa} OR {blue_origin}) OR {space}")
    
    return sources


def date_filter(query):
    """
    Function that manipulates the dates and find the articles in a date range
    :param query: the query submitted by the user
    :return: the range of dates
    """
    from_date = str.replace(query['from'], '-', '')
    to_date = str.replace(query['to'], '-', '')

    date_range = f"date:[{from_date} to {to_date}]"  # initialize the range with retrieved data from the gui

    if not from_date and to_date is not None:  # if just the initial date is unset
        date_range = f"date:[to {to_date}]"
    elif from_date is not None and not to_date:   # if just the ending date is unset
        date_range = f"date:[{from_date} to today]"

    return date_range


def processer(query):
    """
    Function that processes the "query" submitted by the user.
    It processes the dates and filter by sources.
    :param query: the query submitted by the user
    :return: the results of the query, a list of articles
    """
    query_string = query['text']
    ix = open_dir("../index")  # open the index and assign it to "ix"

    sources = source_filter(query, ix)  # call the filter function for sources 
    date_range = date_filter(query)  # call the filter function for dates

    parser = MultifieldParser(["title", "content"],
                              ix.schema, group=OrGroup)  # setting the query parse with the specified field of the schema
    parser.add_plugin(DateParserPlugin(free=True))   # Add the DateParserPlugin to the parser
    print(query_string)
    final_string, th_dym = query_expansion(query_string)
    final_string += " " + date_range    # add the search by date
    #query_string = query_string[:-1]
    user_query = parser.parse(final_string)  # parsing the query and returning a query object to search (use "date:")
    print(user_query)

    results = {}
    with ix.searcher() as searcher:
        result = searcher.search(user_query, filter=sources, limit=None, terms=True)  # search the query
        result.fragmenter.charlimit = None
        result.fragmenter.maxchars = 300  # Allow larger fragments
        result.fragmenter.surround = 40  # Show more context before and after

        results = []
        for i in result:
            article_dict = {}
            for f in i.fields():
                article_dict[f] = i[f]
            article_dict["highlights"] = i.highlights("content")
            results.append(article_dict)

        # Try correcting the query
        corrected = searcher.correct_query(user_query, query_string)
        dym = ""
        if corrected.query != user_query:
            dym = "Did you mean: <b>" + corrected.string +'</b>?</br>'

        dym += th_dym
    
    return results, dym


def concept_query(concept, df):
    """
    Function to handle the content-based term inserted in the user's query
    :param concept: the i-th concept to analyze and expand
    :param df: the thesaurus to consult
    :return: the expanded concept
    """

    """
    RELAZIONI THESAURUS
    - gerarchiche
        BT - Broader Term (X)
        NT - Narrower Term (x)
    - di equivalenza
        UF - Rinvio da un termine accettato a uno non accettato (X)
    """

    ix = open_dir("../thesaurus/index")
    parser = QueryParser("key", ix.schema)
    term = parser.parse(concept[0])
    parser = QueryParser("relationship", ix.schema)
    rel = parser.parse(concept[1])

    query_exp_list = []  # list of all the terms found with the thesaurus
    with ix.searcher() as searcher:
        result = searcher.search(term, filter=rel)
        for r in result:
            query_exp_list.append(r['related'])

        # Try correcting the query
        corrected = searcher.correct_query(term, concept[0])
        dym = ""
        if corrected.query != term:
            dym = "Did you mean: <b>" + corrected.string +'</b>?'


    """
    query_exp_list = []  # list of all the terms found with the thesaurus
    for index, row in df.iterrows():
        if concept[0] == row["Key Descriptor"]:  # if the concept match with a word in the DataFrame
            if row["Relationship Type"] == concept[1]:  # check if the relationship is what the user wants
                query_exp_list.append(row["Related Descriptor"])  # if so, thus add the related term in the list
    """

    return query_exp_list, dym


def query_expansion(query_string):
    """
    Function to expand the whole query
    :param query_string: the input query the user has typed into the system
    :return: the expanded query
    """
    exp = re.compile("\{.*?\}")  # the relevant R.E. to look up
    df = pd.read_csv("../thesaurus/NASA_Thesaurus_CSV.csv")  # the chosen thesaurus

    for e in exp.findall(query_string):  # looking for all the expressions that match my R.E.
        e = e.replace("{", '')
        e = e.replace("}", '')
        e = e.split(",") # split term and relationship
        term = e[0]
        rel = e[1]

        concepts, dym = concept_query((term, rel), df)  # extracts all the concepts based on the tuple (term, relationship)
        concepts_set = set(concepts)  # action performed looking to keep all the terms but not duplicated
        query_expanded = ""
        for c in concepts_set:  # iterates over the set of terms and then adds them into the final query string
            query_expanded += '"' + c + '" ' 

        query_string = query_string.replace("{"+term+","+rel+"}", "("+query_expanded+")")  # replaces the tuple w/ the found concepts

    return query_string, dym

"""
if __name__ == "__main__":
    query_expansion("{2001 Mars Odyssey,BT} OR nasa AND {2001 Mars Odyssey,RT}")
"""