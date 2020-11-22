import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet as wn


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


def stemmization(words_list):
    """
    Function to retrieve the listed words's base form
    :param words_list: the list obtained from the lemmatize(tokens) function
    :return: stemmed_words listed words's base form
    """

    porter = PorterStemmer()
    stemmed_words = [porter.stem(t) for t in words_list]
    return stemmed_words


def expansion(words):
    """
    Function useful to expand the meaning of the query-processed words
    :param words: the list of the processed words
    :return: the final set of words to match the documents's content
    """
    final_set = []
    for w in words:     # for every word
        syns = wn.synsets(w)    # select its sets of meanings
        for s in syns:  # for every set
            for l in s.lemmas():    # consider the synonyms
                final_set.append(l.name().lower())  # add to the list

    final_set = set(final_set)  # delete the repeated terms
    print(final_set)

if __name__ == "__main__":
    query = "When is the date of the next Artemis mission"
    tokens = tokenize(query)
    words_list = lemmatize(tokens)
    print(words_list, '\n')
    expansion(words_list)
    # stemmed_words = stemmization(words_list)
    # print(stemmed_words)
