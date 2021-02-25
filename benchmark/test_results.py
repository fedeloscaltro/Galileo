import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def AP(m):
	fig, ax = plt.subplots(figsize=(20,10))
	c = 0
	for k,v in results.items():
		if m in k:
			y = v[0][1:]
			plt.plot(x,y,marker='o',color=colors[c])
			c += 1

	plt.title(f"{m} - AP")
	plt.xlabel("recall")
	plt.ylabel("precision")
	plt.xlim([0,10])
	plt.ylim([0,100])
	plt.xticks(x)
	b = mpatches.Patch(color='green', label='boost')
	sb = mpatches.Patch(color='blue', label='full-stemming-boost')
	qsb = mpatches.Patch(color='black', label='query-stemming-boost')
	d = mpatches.Patch(color='red', label='default')
	plt.legend(handles=[d, b, sb, qsb])
	file_name = ax.get_title().replace(' - ','_')
	plt.savefig(f"{file_name}.png")


def bars(m, metric):
	labels = []
	y = []
	fig, ax = plt.subplots(figsize=(20,10))
	width = 0.50
	for k,v in results.items():
		if m in k:
			y.append(v[metric])
			labels.append(k)

	if metric == 1:
		plt.title(f"{m} - MAP")
	elif metric == 2:
		plt.title(f"{m} - NDCG")

	plt.ylim([0,100])
	x = np.arange(len(labels))
	bar = ax.bar(x, y, width)
	ax.set_xticks(x)
	ax.set_xticklabels(labels)
	for b in bar:
		height = b.get_height()
		ax.annotate('{}'.format(height),
					xy=(b.get_x() + b.get_width() / 2, height),
					xytext=(0, 3),
					textcoords="offset points",
					ha='center', va='bottom')

	file_name = ax.get_title().replace(' - ','_')
	plt.savefig(f"{file_name}.png")


if __name__ == "__main__":
	results = {
				"BM25F-boost":
					[
						[0.0, 83, 64, 59, 54, 47, 42,36, 27, 21, 10],
						44,
						43
					],
				"TF_IDF-boost":
					[
						[0.0, 59, 55, 49, 45, 38, 34, 32, 24, 20, 9],
						36,
						34
					],
				"Frequency-boost":
					[
						[0.0, 51, 50, 47, 40, 35, 33, 31, 23, 20, 8],
						34,
						30
					],
				"BM25F-stem-boost":
					[
						[0.0, 84, 66, 62, 56, 49, 44, 35, 31, 21, 10],
						46,
						46
					],
				"TF_IDF-stem-boost":
					[
						[0.0, 54, 52, 46, 43, 40, 36, 34, 27, 21, 9],
						36,
						32
					],
				"Frequency-stem-boost":
					[
						[0.0, 45, 45, 42, 38, 37, 33, 31, 26, 19, 8],
						32,
						27
					],
				"BM25F-stem_query-boost":
					[
						[0.0, 88, 65, 56, 55, 51, 45, 39, 35, 24, 11],
						47,
						42
					],
				"TF_IDF-stem_query-boost":
					[
						[0.0, 56, 55, 51, 48, 42, 37, 36, 30, 21, 10],
						39,
						34
					],
				"Frequency-stem_query-boost":
					[
						[0.0, 50, 51, 49, 41, 38, 35, 33, 29, 21, 9],
						36,
						29
					],
				"BM25F":
					[
						[0.0, 85, 64, 59, 52, 46, 42, 36, 27, 21, 10],
						44,
						42
					],
				"TF_IDF":
					[
						[0.0, 55, 54, 47, 43, 37, 34, 32, 24, 19, 9],
						35,
						33
					],
				"Frequency":
					[
						[0.0, 51, 50, 46, 38, 34, 33, 30, 23, 19, 8],
						33,
						29
					]
	 		}

	plt.rcParams.update({'font.size': 16})
	x = [i for i in range(1,11,1)]
	colors = ['#FF9E44', '#C06EE2', 'black', '#FF4093']
	models = ["BM25F", "TF_IDF", "Frequency"]
	for m in models:
		AP(m)
		bars(m,1)
		bars(m,2)


	plt.show()
