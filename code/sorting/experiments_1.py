import os
import random
import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from sklearn import cluster

from som import SOM
from creator import getImageSamples, getImageSamplesForClassification, getNonSortingSamples
from extractor import save_IOA_Images, save_FTIP_IOA_Images, save_FTDP_IOA_Images, save_FTIP_FTDP_IOA_Images
from extractor import average_Images, save_Average_Images
from extractor import Permutation, Inversions, Cycles, Distance, MinimumNumberOfSwaps
from extractor import FTIP, FTDP, IOA, D, S, I

# Global constants
AR_SAMPLES = 150
AR_SIZE = 15
OUTPUT_DIR = './output/'

# Clustering constants
NUM_CLUST = 5

# Self-Organizing Map
SOM_LINES = 15
SOM_COLS = 15
NUM_ITERATIONS = 40

SS_LINES = 1
SS_COLS = 30

# Performs a Self-Organizing Map clustering for a given Feature List
def SelfOrganizingMap(Feature_List, where):
	if not os.path.exists(where):
		os.makedirs(where)

	som = SOM(SOM_LINES, SOM_COLS, len(Feature_List[0]), NUM_ITERATIONS)
	som.train(Feature_List)
	# Get output grid
	image_grid = som.get_centroids()
	#print 'Image grid shows weights for all the input features'
	#print image_grid
	# Get vector mappings
	mapped = som.map_vects(Feature_List)
	#print 'Mapping', mapped

	# Visualization part
	# Needs to be refactored to produce output for any number of clusters
	avg_line = []
	for i in range(NUM_CLUST):
		avg_line.append(0)
	avg_column = []
	for i in range(NUM_CLUST):
		avg_column.append(0)

	for i in range(0, len(mapped), NUM_CLUST):
		for j in range(NUM_CLUST):
			avg_line[(i+j) % NUM_CLUST] += mapped[i+j][0]
			avg_column[(i+j) % NUM_CLUST] += mapped[i+j][1]

	for i in range(len(avg_line)):
		avg_line[i] = avg_line[i]/(len(mapped)/NUM_CLUST)

	for i in range(len(avg_column)):
		avg_column[i] = avg_column[i]/(len(mapped)/NUM_CLUST)

	'Average location'
	print avg_line, avg_column

	# Grayscale landscape
	sorting_landscape = []
	for i in range(NUM_CLUST):
		sorting_landscape.append(np.zeros((SOM_LINES,SOM_COLS), np.float16))

	for i in range(len(mapped)):
		lin = mapped[i][0]
		col = mapped[i][1]
		sorting_landscape[i%NUM_CLUST][lin][col] += 0.05
		if sorting_landscape[i%NUM_CLUST][lin][col] > 1.0:
			sorting_landscape[i%NUM_CLUST][lin][col] = 1.0

	for i in range(NUM_CLUST):
		sorting_landscape[i][avg_line[i]][avg_column[i]] = 1.0

	for i in range(NUM_CLUST):
		io.imsave(where + str(i) + '_sorting_cluster.png', sorting_landscape[i])

	# Colored landscape
	colored_landscape = np.zeros((SOM_LINES,SOM_COLS,3), np.float16)
	white = np.array([1.0, 1.0, 1.0])

	# sorting
	insertion_color = np.array([0.0, 0.0, 1.0]) # blue
	bubble_color = np.array([0.0, 1.0, 0.0]) # green
	heap_color = np.array([1.0, 0.0, 0.0]) # red
	quick_color = np.array([1.0, 0.0, 1.0]) # magenta
	random_color = np.array([1.0, 1.0, 0.0]) # yellow

	# non-sorting
	reverseSorted_color = np.array([0.0, 1.0, 1.0]) # cyan
	intervalSwapSorted_color = np.array([1.0, 0.5, 0.0]) # orange
	reverse_color = np.array([0.5, 1.0, 0.0]) # lime-green
	intervalSwap_color = np.array([1.0, 0.0, 0.5]) # fuchsia

	colored = [insertion_color, bubble_color, heap_color, quick_color, random_color]
	#add_colored = [reverseSorted_color, intervalSwapSorted_color, reverse_color, intervalSwap_color]
	#colored.extend(add_colored)

	grad = 0.005
	for i in range(len(mapped)):
		lin = mapped[i][0]
		col = mapped[i][1]
		colored_landscape[lin][col] += grad*colored[i%NUM_CLUST]
		#if colored_landscape[lin][col].any() > 1.0:
		#	colored_landscape[lin][col] -= 0.05*colored[i%NUM_CLUST]

	for i in range(NUM_CLUST):
		colored_landscape[avg_line[i]][avg_column[i]] = 0.3 * white + 0.7 * colored[i]

	io.imsave(where + 'all_sorting_clusters.png', colored_landscape)

# Performs standard KMeans for a given Feature List
def KMeans(Feature_List):
	k_means = cluster.KMeans(n_clusters = NUM_CLUST)
	k_means.fit(Feature_List)
	#print 'K Means labels', k_means.labels_

	clusters = []
	for i in range(NUM_CLUST):
		clust= []
		for j in range(NUM_CLUST):
			clust.append(0)
		clusters.append(clust)

	labels = k_means.labels_
	for i in range(0, len(labels), NUM_CLUST):
		for j in range(NUM_CLUST):
			clusters[j][labels[i+j]] += 1

	print 'Insertion Cluster:', clusters[0]
	print 'Bubble Cluster:', clusters[1]
	print 'Heap Cluster', clusters[2]
	print 'Quick Cluster:', clusters[3]
	print 'Random Cluster:', clusters[4]

# Performs standard SpectralClustering for a given Feature List
def SpectralClustering(Feature_List):
	spectral = cluster.SpectralClustering(n_clusters = NUM_CLUST)
	spectral.fit(Feature_List)
	#print 'Spectral labels', spectral.labels_

	clusters = []
	for i in range(NUM_CLUST):
		clust= []
		for j in range(NUM_CLUST):
			clust.append(0)
		clusters.append(clust)

	labels = spectral.labels_
	for i in range(0, len(labels), NUM_CLUST):
		for j in range(NUM_CLUST):
			clusters[j][labels[i+j]] += 1

	print 'Insertion Cluster:', clusters[0]
	print 'Bubble Cluster:', clusters[1]
	print 'Heap Cluster:', clusters[2]
	print 'Quick Cluster:', clusters[3]
	print 'Random Cluster:', clusters[4]

# Experiment for sorting an array using a clustering technique
def SortingSelfOrganizingMap(Feature_List):
	# Train a SS_LINES x SS_COLS self-organizing map using NUM_ITERATIONS iterations
	som = SOM(SS_LINES, SS_COLS, len(Feature_List[0]), NUM_ITERATIONS)
	som.train(Feature_List)
	mapped = som.map_vects(Feature_List)

	# Grayscale landscape
	sorting_landscape = np.zeros((SS_LINES,SS_COLS), np.float16)

	for i in range(len(mapped)):
		lin = mapped[i][0]
		col = mapped[i][1]
		sorting_landscape[lin][col] = Feature_List[i][0]

	io.imsave('sorted_landscape.png', sorting_landscape)

def SOMSorting():
	generatedList = [round(random.uniform(0.1, 1.0),4) for i in xrange(AR_SIZE)]
	Feature_List = [np.array([element]) for element in generatedList]
	SortingSelfOrganizingMap(Feature_List)

# CLUSTERING

def normalizeSpatialFeature(feat, maxIterations):
	for i in range(maxIterations - len(feat)):
		#feat = np.append(feat, np.array([0]), axis = 0)
		feat.append(0)
	return feat

# Find the longest length and make all images the same length
def getIOAList(list_of_images):
	maxIterations = max([len(image) for image in list_of_images])
	print 'maxIterations', maxIterations
	IOA_List = [IOA(image, maxIterations) for image in list_of_images]
	return IOA_List, maxIterations

# Generate inputs, extract all features and cluster using all implemented algorithms
def clusteringExperiments():
	list_of_images = getImageSamples(AR_SIZE, AR_SAMPLES)
	IOA_List, maxIterations = getIOAList(list_of_images)

	# temporal and spatial features extraction
	FTIP_List = [FTIP(image) for image in list_of_images]
	FTDP_List = [FTDP(image) for image in list_of_images]
	DCF_List = [D(image) for image in list_of_images]
	MNS_List = [S(image) for image in list_of_images]
	NI_List = [I(image) for image in list_of_images]

	# normalize spatial features
	DCF_List = [normalizeSpatialFeature(feat, maxIterations) for feat in DCF_List]
	MNS_List = [normalizeSpatialFeature(feat, maxIterations) for feat in MNS_List]
	NI_List = [normalizeSpatialFeature(feat, maxIterations) for feat in NI_List]

	# clustering
	SelfOrganizingMap(FTIP_List, OUTPUT_DIR + 'FTIP_Clustering/')
	SelfOrganizingMap(FTDP_List, OUTPUT_DIR + 'FTDP_Clustering/')
	SelfOrganizingMap(DCF_List, OUTPUT_DIR + 'DCF_Clustering/')
	SelfOrganizingMap(MNS_List, OUTPUT_DIR + 'MNS_Clustering/')
	SelfOrganizingMap(NI_List, OUTPUT_DIR + 'NI_Clustering/')
	KMeans(IOA_List)
	KMeans(FTIP_List)
	SpectralClustering(IOA_List)
	SpectralClustering(FTIP_List)

def dimensionalityReductionExperiments():
	print AR_SIZE, AR_SAMPLES
	list_of_images = getImageSamples(AR_SIZE, AR_SAMPLES)
	IOA_List, maxIterations = getIOAList(list_of_images)

	from sklearn.decomposition import PCA
	pca = PCA(n_components=20)
	PCA_List = pca.fit_transform(IOA_List)
	print pca.explained_variance_ratio_
	print PCA_List
	SelfOrganizingMap(PCA_List, OUTPUT_DIR + 'PCA_Clustering/')

	# comparison with best clustering method so far
	#FTIP_List = [FTIP(image) for image in list_of_images]
	#SelfOrganizingMap(FTIP_List, OUTPUT_DIR + 'FTIP_Clustering/')

def autoClustering():
	list_of_images = getImageSamples(AR_SIZE, AR_SAMPLES)
	IOA_List, maxIterations = getIOAList(list_of_images)
	SelfOrganizingMap(IOA_List, OUTPUT_DIR + 'IOA_Clustering/')

def combinedFeaturesClustering():
	list_of_images = getImageSamples(AR_SIZE, AR_SAMPLES)
	IOA_List, maxIterations = getIOAList(list_of_images)
	FTIP_List = [FTIP(image) for image in list_of_images]
	FTDP_List = [FTDP(image) for iamge in list_of_images]
	MNS_List = [S(image) for image in list_of_images]
	MNS_List = [normalizeSpatialFeature(feat, maxIterations) for feat in MNS_List]

	FTIP_MNS_List = [list(x) + list(y) for x, y in zip(FTIP_List, MNS_List)]
	FTDP_MNS_List = [list(x) + list(y) for x, y in zip(FTDP_List, MNS_List)]

	SelfOrganizingMap(FTDP_MNS_List, OUTPUT_DIR + 'FTDP_MNS_Clustering/')

#dimensionalityReductionExperiments()
#autoClustering()
combinedFeaturesClustering()

# View Average Images
def averageImages():
	list_of_images = getImageSamples(AR_SIZE, AR_SAMPLES)
	IOA_List, maxIterations = getIOAList(list_of_images)
	average_images = average_Images(IOA_List, 5, AR_SIZE)
	save_Average_Images(average_images, OUTPUT_DIR + 'average_images/')

# Used for saving visualizations of program executions and their patterns
def patternExperiments():
	list_of_images = getImageSamples(AR_SIZE, AR_SAMPLES)

	FTIP_List = [FTIP(image) for image in list_of_images]
	#DistanceMatrix(FTIP_List)

	# Temporal features on IOA
	save_FTIP_IOA_Images(list_of_images, where = OUTPUT_DIR + 'FTIP_IOA_samples/')
	save_FTDP_IOA_Images(list_of_images, where = OUTPUT_DIR + 'FTDP_IOA_samples/')
	save_FTIP_FTDP_IOA_Images(list_of_images, where = OUTPUT_DIR  + 'FTIP_FTDP_IOA_samples/')

	# IOA Non-sorting samples
	list_of_images = getNonSortingSamples(AR_SIZE, AR_SAMPLES)
	save_IOA_Images(list_of_images, where = OUTPUT_DIR + 'IOA_nonsort_samples/')

	# IOA Sorting sample
	list_of_images = getImageSamples(AR_SIZE, AR_SAMPLES)
	save_IOA_Images(list_of_images, where = OUTPUT_DIR + 'IOA_samples/')


# Performs clustering with different techniques on different features
#clusteringExperiments()
#patternExperiments()
#averageImages()
#SOMSorting()

# SORTING METRICS

def generateSortingMetrics():

	list_of_images = getImageSamples(AR_SIZE, AR_SAMPLES)

	D_List = [D(image) for image in list_of_images]
	S_List = [S(image) for image in list_of_images]
	I_List = [I(image) for image in list_of_images]

	for i in range(len(list_of_images)):
		print 'Image', i
		#print list_of_images[i]
		#print 'Distance'
		#print D_List[i]
		#print 'Swaps'
		#print S_List[i]
		#print 'Inversions'
		#print I_List[i]

		x_range = []
		for j in range(len(D_List[i])):
			x_range.append(j)

		#print len(x_range)
		#print len(D_List[i]), len(S_List[i]), len(I_List[i])

		plot_title = ''
		where = OUTPUT_DIR + 'SpatialFeatures/'

		ind = i % 5
		if ind == 0:
			plot_title = 'InsertionSort'
		elif ind == 1:
			plot_title = 'BubbleSort'
		elif ind == 2:
			plot_title = 'HeapSort'
		elif ind == 3:
			plot_title = 'QuickSort'
		elif ind == 4:
			plot_title = 'RandomSort'

		dcf = plt.plot(x_range, D_List[i], '-b', label = 'DCF')
		mns = plt.plot(x_range, S_List[i], '-g', label = 'MNS')
		ni = plt.plot(x_range, I_List[i], '-r', label = 'NI')
		plt.setp(dcf, linewidth = 2.0)
		plt.setp(mns, linewidth = 2.0)
		plt.setp(ni, linewidth = 2.0)
		plt.legend(loc='upper right', frameon=False, prop={'size':20})
		#plt.ylim(ymax = 1.1, ymin = 0.7)
		plt.ylabel('Value', fontsize=20)
		plt.xlabel('Step', fontsize=20)
		#plt.title(plot_title)
		plt.savefig(where + str(i) + '_' + plot_title + '.png')
		plt.clf()

#generateSortingMetrics()