from flask import Flask, render_template, url_for, request
from QueryProcesser import processer

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/results", methods=['GET', 'POST'])
def results():
	articles = processer(request.args.get('query'))
	print(articles)
	return render_template('results.html', context=articles)


if __name__ == "__main__":
    app.run(debug=True)
