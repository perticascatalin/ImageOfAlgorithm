import numpy as np

def zip_example():
	a1 = [2, 3, 4]
	b1 = [5, 6]
	a2 = [1, 2, 9]
	b2 = [10, 11]

	a = [a1, a2]
	b = [b1, b2]

	for x, y in zip(a, b):
		print x + y

def euclid_dist():
	a = np.array([1.0, 2.3, 1.7, -5.2])
	b = np.array([-1.0, 0.7, 1.3, 3.2])
	print a
	print b
	print np.linalg.norm(a-b)

def colors():
	import colorsys
	N = 5
	HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
	RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
	print RGB_tuples

def casting():
	matrix = np.ones((5, 5), np.float16)
	print matrix
	new_matrix = np.reshape(map(lambda x: np.array([x, x, x]), np.ravel(matrix)), (5,5,3))
	print new_matrix

def product():
	a = np.array([0.5, 0.3, 0.2])
	b = 0.5
	print b*a

def component_min_max():
	a = np.array([[[0.5, 0.2, 0.3], [0.1, 0.4, 1.0], [0.8, 0.9, 1.0]], \
		[[0.1, 0.2, 0.3], [0.3, 0.2, 0.1], [0.4, 0.5, 0.6]], \
		[[0.9, 0.8, 0.7], [0.6, 0.2, 0.3], [0.1, 0.3, 0.5]]])

	print a

	print np.amin(a[:,:,0:1])
	print np.amin(a[:,:,1:2])
	print np.amin(a[:,:,2:3])

component_min_max()