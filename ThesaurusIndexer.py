import os.path

from whoosh.fields import *
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

import pandas as pd

def create_index():
	schema = Schema(
		key=TEXT(stored=True),
		relationship=TEXT(stored=True),
		related=TEXT(stored=True)
	)

	if not os.path.exists("thesaurus/index"):
		os.mkdir("thesaurus/index")

	ix = create_in("thesaurus/index", schema)
	return ix


def fill_index(ix):
	writer = ix.writer()

	df = pd.read_csv("thesaurus/NASA_Thesaurus_CSV.csv")
	for index, row in df.iterrows():
		writer.add_document(
			key = row["Key Descriptor"],
			relationship = row["Relationship Type"],
			related = row["Related Descriptor"]
		)

	writer.commit()


def test_search():
	ix = open_dir("thesaurus/index")
	parser = QueryParser("key", ix.schema)
	term = parser.parse("2001 mars odyssey")
	parser = QueryParser("relationship", ix.schema)
	rel = parser.parse("RT")

	with ix.searcher() as searcher:
		result = searcher.search(term, filter=rel)
		for r in result:
			print(r['related'])


def main():
	
	# ix = create_index()	
	# fill_index(ix)
	test_search()
	


if __name__ == '__main__':
	main()