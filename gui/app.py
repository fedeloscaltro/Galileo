from flask import Flask, render_template, request
from QueryProcesser import processer
import math

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/results", methods=['GET', 'POST'])
def results():
    """
	Function used to link the data retrieved from gui and the processer that run the query on the index
	"""

    # retrieve the data from the gui and store them in a dictionary
    query = {'text': request.args.get('query'), 'esa': request.args.get('ESA'),
             'space': request.args.get('Space.com'), 'blue_origin': request.args.get('BlueOrigin'),
             'from': request.args.get('dataInizio'), 'to': request.args.get('dataFine')}
    articles, dym = processer(query)  # call the processor on the "query"

    return render_template('results.html', context=articles, dym=dym)


"""
	ap = [0 for j in range(11)]  # list for average precision at recall level R
	mean_ap = 0  # MAP
	mean_NDCG = 0  # NDCG
	with open("../benchmark/test_queries", "r") as file:  # file containig the queries for testing
		n = 1  # number of queries
		for q in file.readlines():
			query['text'] = q
			articles, dym = processer(query)  # process the query
			test_ap, NDCG = benchmark(articles, query, n)  # retrieve AP and NDCG
			for i in range(11):
				print(test_ap[i])
				ap[i] += test_ap[i]  # sum the values for the AP
			mean_ap += sum(test_ap) / 10  # sum the values for the MAP
			mean_NDCG += NDCG  # sum the NDCG of each query
			print(NDCG)
			n += 1

	n -= 1
	for i in range(11):
		ap[i] /= n  # calculate the AP at each recall level
	print(ap)

	mean_ap /= n  # calculate the MAP
	print(mean_ap)

	mean_NDCG /= n  # calculate the mean NDCG
	print(mean_NDCG)
	"""


# benchmark tools

def find_nth(haystack, needle, n):
    """
	function used to process the file of test queries
	"""
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1

    return start


def benchmark(articles, query, i):
    """
	function for calculating the benchmark measures for each query
	"""
    ap = [0 for j in range(11)]
    DCG_dict = {}  # DCG values of top 10 articles for each query
    with open("../benchmark/relevant_documents", "r") as file:  # file containing the relevant documents
        lines = ""
        for row in file.readlines():
            lines += row

    start = find_nth(lines, '[', i) + 1
    end = find_nth(lines, ']', i)
    lines = lines[start:end]
    lines = lines.replace("\'", "")
    lines = lines.replace("\n", "")
    lines = lines.strip()

    relevant_docs = lines.split(',')
    recall = 0
    art_cont = 0  # articles counter
    rel_cont = 0  # relevants counter
    rank_rel = 6  # actual rank of article (for NDCG)
    c = 1  # flag
    GT_DCG = 6
    for doc in relevant_docs:  # set the "ground truth" DCG and values of relevant articles
        if c > 1:
            GT_DCG += rank_rel / math.log(c, 2)
        c += 1
        if rank_rel >= 2:
            DCG_dict[doc] = rank_rel
            rank_rel -= 1
        else:
            DCG_dict[doc] = rank_rel

    s = 0  # query DCG
    for i in range(1, 11, 1):  # calculate the DCG for the articles retrieved
        if i > len(DCG_dict):
            break
        try:
            if i == 1:
                s += DCG_dict[articles[i - 1]['path'][:-1]]
            else:
                s += DCG_dict[articles[i - 1]['path'][:-1]] / math.log(i, 2)
        except KeyError:
            continue

    NDCG = s / GT_DCG  # normalize the DCG by the "ground truth"

    for a in articles:  # calculate the precision at each recall level for each article
        art_cont += 1
        for doc in relevant_docs:
            if a['path'][:-1] == doc:
                rel_cont += 1
                recall += 1
                precision = (rel_cont / art_cont) * 100
                ap[recall] += int(precision)

    return ap, NDCG  # return the AP and the NDCG


if __name__ == "__main__":
    app.run(debug=True)
