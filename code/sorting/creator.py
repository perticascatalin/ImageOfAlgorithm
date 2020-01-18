import random
from algorithms import OrganizeArray

# The generated arrays should have values between 0.0 and 1.0
sampleList = [0.81, 0.97, 0.33, 0.28, 0.32, 0.34, 0.12, 0.13, 0.14, 0.15, 0.89, 0.76, 0.23, 0.69, 0.11, 0.31]

def insertionSortImage(aList, order):
	#print 'Sorting', aList
	insertionSort = OrganizeArray(arr = list(aList), method = 'insertionsort', order = order)
	insertionSort.run()
	if insertionSort.isSorted():
		#print 'Insertion Sorted!'
		#print insertionSort.arr
		#insertionSort.saveSwapArrImage('insertion.jpg')
		return insertionSort.swapArrImage
	else:
		print '!!! Insertionsort did not work properly', insertionSort.arr

def bubbleSortImage(aList, order):
	#print 'Sorting', aList
	bubbleSort = OrganizeArray(arr = list(aList), method = 'bubblesort', order = order)
	bubbleSort.run()
	if bubbleSort.isSorted():
		#print 'Bubble Sorted!'
		#print bubbleSort.arr
		#bubbleSort.saveSwapArrImage('bubble.jpg')
		return bubbleSort.swapArrImage
	else:
		print '!!! Bubblesort did not work properly', bubbleSort.arr

def heapSortImage(aList, order):
	#print 'Sorting', aList
	heapSort = OrganizeArray(arr = list(aList), method = 'heapsort', order = order)
	heapSort.run()
	if heapSort.isSorted():
		#print 'Heap Sorted!'
		#print heapSort.arr
		#heapSort.saveSwapArrImage('heap.jpg')
		return heapSort.swapArrImage
	else:
		print '!!! Heapsort did not work properly', heapSort.arr

def quickSortImage(aList, order):
	#print 'Sorting', aList
	quickSort = OrganizeArray(arr = list(aList), method = 'quicksort', order = order)
	quickSort.run()
	if quickSort.isSorted():
		#print 'Quick Sorted!'
		#print quickSort.arr
		#quickSort.saveSwapArrImage('quick.jpg')
		return quickSort.swapArrImage
	else:
		print '!!! Quicksort did not work properly', quickSort.arr

def randomSortImage(aList, order):
	#print 'Sorting', aList
	randomSort = OrganizeArray(arr = list(aList), method = 'randomsort', order = order)
	randomSort.run()
	if randomSort.isSorted():
		#print 'Random Sorted!'
		#print randomSort.arr
		#randomSort.saveSwapArrImage('random.jpg')
		return randomSort.swapArrImage
	else:
		print '!!! Randomsort did not work properly', randomSort.arr

def lReverseImage(aList, L):
	lReverse = OrganizeArray(arr = list(aList), method = 'reverse', order = L)
	lReverse.run()
	return lReverse.swapArrImage

def lIntervalSwapImage(aList, L):
	lIntervalSwap = OrganizeArray(arr = list(aList), method = 'intervalswap', order = L)
	lIntervalSwap.run()
	return lIntervalSwap.swapArrImage

def bstFollowCyclesImage(aList):
	bstFollowCycles = OrganizeArray(arr = list(aList), method = 'bstfollowcycles')
	bstFollowCycles.run()
	return bstFollowCycles.swapArrImage

# Creates sample images of algorithms execution
def getImageSamples(arr_size, num_samples):
	list_of_images = []
	inc = 'increasing'
	dec = 'decreasing'
	for i in range(num_samples):
		generatedList = [round(random.uniform(0.0, 1.0),4) for i in xrange(arr_size)]
		#print generatedList
		list_of_images.append(insertionSortImage(generatedList, inc))
		list_of_images.append(bubbleSortImage(generatedList, inc))
		list_of_images.append(heapSortImage(generatedList, inc))
		list_of_images.append(quickSortImage(generatedList, inc))
		list_of_images.append(randomSortImage(generatedList, inc))
	return list_of_images

# Creates samples of non-sorting algorithms execution
def getNonSortingSamples(arr_size, num_samples):
	list_of_images = []
	for i in range(num_samples):
		generatedList = [round(random.uniform(0.0, 1.0),4) for i in xrange(arr_size)]
		#print generatedList
		list_of_images.append(lReverseImage(sorted(generatedList), arr_size))
		list_of_images.append(lReverseImage(sorted(generatedList), arr_size/2))
		list_of_images.append(lIntervalSwapImage(sorted(generatedList), arr_size))
		list_of_images.append(lIntervalSwapImage(sorted(generatedList), arr_size/2))
		list_of_images.append(lReverseImage(generatedList, arr_size))
		list_of_images.append(lReverseImage(generatedList, arr_size/2))
		list_of_images.append(lIntervalSwapImage(generatedList, arr_size))
		list_of_images.append(lIntervalSwapImage(generatedList, arr_size/2))	
	return list_of_images

def getImageSamplesForClassification(arr_size, num_samples):
	list_of_images = []
	inc = 'increasing'
	dec = 'decreasing'
	for i in range(num_samples):
		generatedList = [round(random.uniform(0.0, 1.0),4) for i in xrange(arr_size)]
		#print generatedList
		list_of_images.append(insertionSortImage(generatedList, inc))
		list_of_images.append(insertionSortImage(generatedList, dec))
		list_of_images.append(bubbleSortImage(generatedList, inc))
		list_of_images.append(bubbleSortImage(generatedList, dec))
		list_of_images.append(heapSortImage(generatedList, inc))
		list_of_images.append(heapSortImage(generatedList, dec))
		list_of_images.append(quickSortImage(generatedList, inc))
		list_of_images.append(quickSortImage(generatedList, dec))
		list_of_images.append(randomSortImage(generatedList, inc))
		list_of_images.append(randomSortImage(generatedList, dec))
	return list_of_images