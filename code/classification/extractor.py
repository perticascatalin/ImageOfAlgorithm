import os
import numpy as np
from skimage import io
from skimage.color import gray2rgb

# Computes image of an algorithm feature
def IOA(image, maxIterations):
	for i in xrange(maxIterations - len(image)):
		line = np.reshape(image[len(image) - 1], (1,len(image[len(image) - 1])))
		image = np.append(image, line, axis = 0)
	return image.ravel()

# Computes first time in place feature
def FTIP(image):
	firstTimeInPlace = np.zeros((len(image[0])), np.int16)
	stopped = np.zeros((len(image[0])), np.int16)
	for i in xrange(len(firstTimeInPlace)):
		firstTimeInPlace[i] = len(image) - 1

	for i in range(len(image) - 1, 0, -1):
		for j in xrange(len(image[i])):
			if stopped[j] == 0 and image[i][j] == image[i-1][j]:
				firstTimeInPlace[j] = i - 1
			else:
				stopped[j] = 1
	return firstTimeInPlace

# Computes first time displaced feature
def FTDP(image):
	firstTimeDisplaced = np.zeros((len(image[0])), np.int16)
	moved = np.zeros((len(image[0])), np.int16)
	for i in xrange(len(firstTimeDisplaced)):
		firstTimeDisplaced[i] = 0

	for i in range(len(image) - 1):
		for j in xrange(len(image[i])):
			if moved[j] == 0 and image[i][j] == image[i+1][j]:
				firstTimeDisplaced[j] = i + 1
			else:
				moved[j] = 1
	return firstTimeDisplaced

# Computes the representation of the FTIP feature onto IOA
def FTIP_Image(image):
	ftip = FTIP(image)
	ftip_image = gray2rgb(image)
	red = np.array([1.0, 0.0, 0.0]) #red
	for i in range(len(ftip)):
		ftip_image[ftip[i]][i] = red
	return ftip_image

# Computes the representation of the FTDP feature onto IOA
def FTDP_Image(image):
	ftdp = FTDP(image)
	ftdp_image = gray2rgb(image)
	red = np.array([1.0, 0.0, 0.0]) #red
	for i in range(len(ftdp)):
		ftdp_image[ftdp[i]][i] = red
	return ftdp_image

# Computes the representation of the FTDP feature onto IOA
def FTIP_FTDP_Image(image):
	ftip = FTIP(image)
	ftdp = FTDP(image)
	ftip_ftdp_image = gray2rgb(image)

	blue = np.array([0.0, 0.0, 1.0]) #blue
	red = np.array([1.0, 0.0, 0.0]) #red

	for i in range(len(ftdp)):
		ftip_ftdp_image[ftdp[i]][i] = blue

	for i in range(len(ftip)):
		ftip_ftdp_image[ftip[i]][i] = red

	return ftip_ftdp_image

# Save IOA images
def save_IOA_Images(list_of_images, where):
	if not os.path.exists(where):
		os.makedirs(where)
	for i in range(len(list_of_images)):
		io.imsave(where + str(i) + '_ioa_image.png', list_of_images[i])

# Save FTIP, IOA images
def save_FTIP_IOA_Images(list_of_images, where):
	if not os.path.exists(where):
		os.makedirs(where)

	FTIP_Image_List = [FTIP_Image(image) for image in list_of_images]
	for i in range(len(FTIP_Image_List)):
		ftip_image = FTIP_Image_List[i]
		io.imsave(where + str(i) + '_ftip_ioa_image.png', ftip_image)

# Save FTDP, IOA images
def save_FTDP_IOA_Images(list_of_images, where):
	if not os.path.exists(where):
		os.makedirs(where)

	FTDP_Image_List = [FTDP_Image(image) for image in list_of_images]
	for i in range(len(FTDP_Image_List)):
		ftdp_image = FTDP_Image_List[i]
		io.imsave(where + str(i) + '_ftdp_ioa_image.png', ftdp_image)

def save_FTIP_FTDP_IOA_Images(list_of_images, where):
	if not os.path.exists(where):
		os.makedirs(where)

	FTIP_FTDP_Image_List = [FTIP_FTDP_Image(image) for image in list_of_images]
	for i in range(len(FTIP_FTDP_Image_List)):
		ftip_ftdp_image = FTIP_FTDP_Image_List[i]
		io.imsave(where + str(i) + '_ftip_ftdp_ioa_image.png', ftip_ftdp_image)

def save_Average_Images(list_of_images, where):
	if not os.path.exists(where):
		os.makedirs(where)

	for i in range(len(list_of_images)):
		io.imsave(where + str(i) + '_average_image.png', list_of_images[i])

def average_Images(list_of_images, period, image_width):

	list_of_averages = []
	for p in range(period):
		average = list_of_images[p]
		list_of_averages.append(average)

	for i in range(period, len(list_of_images)):
		p = i % period
		list_of_averages[p] = np.add(list_of_averages[p], list_of_images[i])

	for p in range(period):
		list_of_averages[p] = np.divide(list_of_averages[p], len(list_of_images)/period)

	the_shape = len(list_of_averages[0])
	list_of_averages = [np.reshape(image, ((the_shape/image_width), image_width)) for image in list_of_averages]
	return list_of_averages

# Compute the distance matrix for a feature list
def DistanceMatrix(Feature_List):
	dstMatrix = np.zeros((len(Feature_List), len(Feature_List)), np.int16)
	for i in range(len(Feature_List)):
		for j in range(len(Feature_List)):
			subSqrt = math.sqrt(np.sum((Feature_List[i] - Feature_List[j])**2))
			sub = np.sum((Feature_List[i] - Feature_List[j])**2)
			dstMatrix[i][j] = subSqrt
			#print sub
	print dstMatrix

# Computes the corresponding permutation given an array with unique elements
# Returns an array
def Permutation(arr):
	srt_arr = list(arr)
	srt_arr.sort()
	perm_map = {}
	for i in range(len(srt_arr)):
		perm_map[srt_arr[i]] = i
	perm = []
	for i in range(len(arr)):
		perm.append(perm_map[arr[i]])
	return perm

# Computes the inversions in a permutation
# Returns an array of tuples with the inversed elements
def Inversions(perm):
	inv = []
	for i in range(len(perm)):
		for j in range(i+1, len(perm)):
			if perm[i] > perm[j]:
				inv.append((perm[i],perm[j]))
	return inv

# Computes the cycles in a permutation
# Returns an array of arrays representing the cycles in the permutation
def Cycles(perm):
	cycles = []
	used = []
	for i in range(len(perm)):
		used.append(False)
	for i in range(len(perm)):
		if used[i] == True:
			continue
		pos = i
		cur_cycle = []
		while used[pos] == False:
			cur_cycle.append(pos)
			used[pos] = True
			pos = perm[pos]
		cycles.append(cur_cycle)
	return cycles

# Computes the sum of distances between current position to desired poition in a permutation
def Distance(perm):
	dst = 0
	for i in range(len(perm)):
		dst += abs(i - perm[i])
	return dst

# Returns the minimum number of swaps necessary to sort an array with distinct elements
def MinimumNumberOfSwaps(arr):
	perm = Permutation(arr)
	cycles = Cycles(perm)
	swapCount = 0
	for cycle in cycles:
		swapCount += (len(cycle) - 1)
	return swapCount

# Returns the distance feature as an array where 
# each element corresponds to one line in the image
def D(image):
	d_ft = []
	for i in range(len(image)):
		perm = Permutation(image[i])
		dst = Distance(perm)
		d_ft.append(dst)
	return d_ft

# Returns the minimum number of swaps in order to sort
def S(image):
	s_ft = []
	for i in range(len(image)):
		perm = Permutation(image[i])
		swapCount = MinimumNumberOfSwaps(perm)
		s_ft.append(swapCount)
	return s_ft

# Returns the number of inversions
def I(image):
	i_ft = []
	for i in range(len(image)):
		perm = Permutation(image[i])
		inv = len(Inversions(perm))
		i_ft.append(inv)
	return i_ft