from ultralytics import YOLO
import matplotlib.pyplot as plt

def predict(filename):
	model = YOLO("best.pt")
	results = model([filename])

	classTop5 = [results[0].names[i] for i in results[0].probs.top5]
	probsTop5 = results[0].probs.top5conf.numpy()

	'''
	bars = plt.barh(classTop5, probsTop5)
	plt.title(filename)
	plt.ylabel('class')
	plt.xlabel('probability')
	plt.bar_label(bars)
	plt.tight_layout()
	plt.savefig('./static/images/bar.png')
	plt.close('all')
	'''

	res = {}
	for i in range(5):
		if f'{probsTop5[i]:.2f}' > f'0.00':
			res[classTop5[i]] = str(probsTop5[i])
	return res