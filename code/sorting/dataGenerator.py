import csv
import numpy as np

from creator import getImageSamplesForClassification, getImageSamples
from extractor import IOA

AR_SIZE = 10
AR_SAMPLES = 200

def outputToCSV(header, data):
	with open('./data/IOA_IBHQR_ID/train_200_inc.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerow(header)
		for item in data:
			writer.writerow(item)

def attachLabels(data, no_classes):
	labeled_data = list(data)
	for i in range(len(labeled_data)):
		cur_class = i % no_classes
		labeled_data[i] = np.insert(labeled_data[i], 0, cur_class)
	return labeled_data

def generateData():
	list_of_images = getImageSamples(AR_SIZE, AR_SAMPLES)
	maxIterations = max([len(image) for image in list_of_images])
	print 'Max iterations:', maxIterations
	IOA_List = [IOA(image, maxIterations) for image in list_of_images]
	no_classes = 5
	no_features = len(IOA_List[0])
	L_IOA_List = attachLabels(IOA_List, no_classes)
	header = ['label']
	for i in range(no_features):
		header.append('pixel_' + str(i/AR_SIZE) + '_' + str(i%AR_SIZE))
	outputToCSV(header, L_IOA_List)

generateData()