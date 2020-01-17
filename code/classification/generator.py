import random
import csv
import os
import pickle
import numpy as np
from algorithms import *

def generate_data(num_samples, arr_size):
	X = []
	Y = []
	for i in range(num_samples):
		if i % 100 == 0:
			print ('Iteration ', str(i))
		aList = [round(random.uniform(0.0, 1.0),3) for i in xrange(arr_size)]

		# INSERTION SORT (increasing)
		algo = OrganizeArray(arr = list(aList), method = 'insertionsort', order = 'increasing')
		algo.run()
		item = np.array(algo.swapArrImage)
		X.append(item.reshape(item.shape[0] * item.shape[1]))
		Y.append(0)

		# INSERTION SORT (decreasing)
		algo = OrganizeArray(arr = list(aList), method = 'insertionsort', order = 'decreasing')
		algo.run()
		item = np.array(algo.swapArrImage)
		X.append(item.reshape(item.shape[0] * item.shape[1]))
		Y.append(1)

	n_patterns = len(X)
	print ('Number of generated patterns:', n_patterns)
	return X, Y


num_samples = 1
arr_size = 10

X, Y = generate_data(num_samples, arr_size)
print X[0]
print Y[0]

f = open("sample.csv","w+")

s = str(Y[0])
for x in X[0]:
	s += ("," + str(x))
s += '\n'
f.write(s)

s = str(Y[1])
for x in X[1]:
	s += ("," + str(x))
s += '\n'
f.write(s)

f.close()