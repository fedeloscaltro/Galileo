from flask import Flask, render_template, url_for, request
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
	articles = processer(query)	# call the processer on the "query"
	# print(articles)
	return render_template('results.html', context=articles)


if __name__ == "__main__":
    app.run(debug=True)
