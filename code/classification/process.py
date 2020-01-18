import pickle
import numpy as np
from keras.utils import to_categorical

def processData(padding = '0before', location = 'datasets/20_1000.csv', task = 'GPC'):

	labels = []
	samples = []
	no_features = int(location.split('/')[1].split('_')[0])
	no_samples_per_class = int(location.split('/')[1].split('_')[1].split('.')[0])
	print(no_features)
	print(no_samples_per_class)

	with open (location) as f:
		content = f.readlines()
		for line in content:
			lst = line.split(',')

			label = int(float(lst[0]))
			sample = [float(x) for x in lst[1:]]

			labels.append(label)
			samples.append(sample)

	max_length = max([len(sample) for sample in samples])

	if padding.startswith('0'):
		for i in range(len(samples)):
			sample = samples[i]
			n = max_length - len(sample)
			for _ in range(n):
				if padding == '0before':
					sample.insert(0, 0.0)
				elif padding == '0after':
					sample.append(0.0)
			samples[i] = sample

	X = np.array(samples)
	X = np.reshape(X, (X.shape[0], X.shape[1] // no_features, no_features))
	y = to_categorical(labels)

	X_ploc = 'datasets/X_' + task + '_' + str(no_features) + '_' + str(no_samples_per_class) + '_' + padding + '.p'
	pickle.dump(X, open(X_ploc, 'wb'))
	y_ploc = 'datasets/y_' + task + '_' + str(no_features) + '_' + str(no_samples_per_class) + '_' + padding + '.p'
	pickle.dump(y, open(y_ploc, 'wb'))

#processData(padding = '0after')
processData('0after', 'datasets/2_2.csv')