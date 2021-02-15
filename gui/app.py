from flask import Flask, render_template, request
from QueryProcesser import processer

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
    # articles, dym = processer(query)  # call the processor on the "query"

    ap = [0 for j in range(11)]

    with open("../benchmark/test_queries", "r") as file:
    	n = 1
    	for q in file.readlines():
    		query['text'] = q
    		print(q)
    		articles, dym = processer(query)
    		test_ap = benchmark(articles, query, n)
    		for i in range(11):
    			print(test_ap[i])
    			ap[i] += test_ap[i]
    		n += 1

    for i in range(11):
    	ap[i] /= n

    print(ap)

    return render_template('results.html', context=articles, dym=dym)


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def benchmark(articles, query, i):
	ap = [0 for j in range(11)]

	with open("../benchmark/relevant_documents", "r") as file:
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
	art_cont = 0
	rel_cont = 0
	for a in articles:
		art_cont += 1
		for doc in relevant_docs:
			if a['path'][:-1] == doc:
				rel_cont += 1 
				recall += 1
				precision = (rel_cont/art_cont) * 100
				ap[recall] += int(precision)
	
	return ap

if __name__ == "__main__":
    app.run(debug=True)
