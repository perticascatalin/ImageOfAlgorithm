import os
import colorsys
import numpy as np
import pandas as pd

from som import SOM
from creator import getImageSamples
from extractor import IOA, FTIP, FTDP
from extractor import D, S, I

from sklearn.metrics import silhouette_score
from skimage import io

# Self-Organizing Map
SOM_LINES = 20
SOM_COLS = 20
SOM_ITERATIONS = 50

def SelfOrganizingMap(Feature_List):
	som = SOM(SOM_LINES, SOM_COLS, len(Feature_List[0]), SOM_ITERATIONS)
	som.train(Feature_List)
	
	image_grid = som.get_centroids()
	mapped = som.map_vects(Feature_List)

	return mapped, image_grid

def Normalize(matrix):
	minimum = np.amin(matrix)
	maximum = np.amax(matrix)
	return (matrix - minimum) / (maximum - minimum)

def UnifiedDistanceMatrix(image_grid):
	no_lines = len(image_grid)
	no_columns = len(image_grid[0])

	moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
	u_matrix = np.zeros((2*no_lines-1, 2*no_columns-1), dtype = np.float16)

	for line in range(no_lines):
		for column in range(no_columns):
			for move in moves:
				new_line = line + move[0]
				new_column = column + move[1]
				if new_line < 0 or new_column < 0:
					continue
				if new_line >= no_lines or new_column >= no_columns:
					continue
				u_mat_line = 2 * line + move[0]
				u_mat_column = 2 * column + move[1]
				u_matrix[u_mat_line][u_mat_column] = \
					np.linalg.norm(image_grid[line][column] - image_grid[new_line][new_column])

	return u_matrix

def ClustersMatrix(mapped, labels):
	cluster_landscape = []
	for i in range(AR_CLUST):
		cluster_landscape.append(np.zeros((SOM_LINES,SOM_COLS), np.float16))

	for i in range(len(mapped)):
		lin = mapped[i][0]
		col = mapped[i][1]
		cluster_landscape[labels[i]][lin][col] += 1.0

	cluster_landscape = map(Normalize, cluster_landscape)

	HSV_tuples = [(x*1.0/AR_CLUST, 0.5, 1.0) for x in range(AR_CLUST)]
	RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
	cluster_colors = map(lambda x: np.array(list(x)), RGB_tuples)

	colored_landscape = []
	for i in range(len(cluster_landscape)):
		cluster_land = cluster_landscape[i]
		colored_values = map(lambda x: x*cluster_colors[i], np.ravel(cluster_land))
		colored_landscape.append(np.reshape(colored_values, (SOM_LINES,SOM_COLS,3)))

	return colored_landscape


def main(input_location, output_location):
	data = pd.read_csv(input_location)

	header = data.iloc[:,1:].columns.values
	images = data.iloc[:,1:].values.astype(np.float)
	labels = data[[0]].values.ravel().astype(np.uint8)

	global AR_SAMPLES, AR_SIZE, AR_ITER, AR_CLUST
	AR_SAMPLES = len(images)
	AR_SIZE = max(map(lambda x: int(x.split('_')[-1]), header)) + 1
	AR_ITER = max(map(lambda x: int(x.split('_')[-2]), header)) + 1
	AR_CLUST = max(labels) + 1

	FTIP_List = map(lambda x: FTIP(np.reshape(x, (AR_ITER, AR_SIZE))), images)
	FTDP_List = map(lambda x: FTDP(np.reshape(x, (AR_ITER, AR_SIZE))), images)
	MNS_List = map(lambda x: S(np.reshape(x, (AR_ITER, AR_SIZE))), images)

	Feature_List = [list(x) + list(y) for x, y in zip(FTIP_List, MNS_List)]
	mapped, image_grid = SelfOrganizingMap(Feature_List)
	print 'FTIP MNS', silhouette_score(mapped, labels)
	u_matrix = UnifiedDistanceMatrix(image_grid)
	u_matrix = Normalize(u_matrix)
	colored_landscape = ClustersMatrix(mapped, labels)

	cluster_map = reduce(lambda x, y: x + y, colored_landscape)
	cluster_map[:,:,0:1] = Normalize(cluster_map[:,:,0:1])
	cluster_map[:,:,1:2] = Normalize(cluster_map[:,:,1:2])
	cluster_map[:,:,2:3] = Normalize(cluster_map[:,:,2:3])

	if not os.path.exists(output_location):
		os.makedirs(output_location)

	image_name = output_location + 'u_matrix.png'
	io.imsave(image_name, u_matrix)
	
	for i in range(len(colored_landscape)):
		colored_land = colored_landscape[i]
		image_name = output_location + 'colored_land_' + str(i) + '.png'
		io.imsave(image_name, colored_land)

	image_name = output_location + 'cluster_map.png'
	io.imsave(image_name, cluster_map)

main('./data/IOA_IBHQR_ID/train_200_inc.csv', './experiments_2/Clustering/')
