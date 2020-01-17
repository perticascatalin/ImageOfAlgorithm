# It's best to assume that all elements are different because otherwise equal elements might be swapped

import numpy as np
import random
from skimage import io
from random import randint
from extractor import Permutation, Cycles

# A generic class for organizing elements in an array
class OrganizeArray:
	def __init__(self, arr = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0], method = 'bubblesort', order = 'same'):
		# order describes the order for a family of elements
		# precedInOrder functions can be applied to elements and families of elements
		# Singular values are intended for variables which have in-built comparison operators

		self.arr = arr
		self.method = method
		self.order = order
		# The image of arr tracked for swaps
		self.iterations = 1
		self.swapArrImage = np.zeros((0,len(arr)), dtype = np.float16)

		line = np.reshape(np.array(self.arr), (1,len(self.arr)))
		self.swapArrImage = np.append(self.swapArrImage, line, axis = 0)

	# Keeps the elements in the given order
	def asIs(self, element1, element2):
		return True

	# Converges towards increasing order
	def singularIncreasing(self, element1, element2):
		if element1 < element2:
			return True
		return False

	# Converges towards decreasing order 
	def singularDecreasing(self, element1, element2):
		if element1 > element2:
			return True
		return False

	# Doesn't converge
	def singularEqual(self, element1, element2):
		if element1 == element2:
			return True
		return False

	# Swaps elements in the array to organize
	def swap(self, position1, position2, drawLine = True, iterLimit = 1000):
		if position1 == position2:
			return
		thirdHand = self.arr[position1]
		self.arr[position1] = self.arr[position2]
		self.arr[position2] = thirdHand
		if drawLine and self.iterations < iterLimit:
			line = np.reshape(np.array(self.arr), (1,len(self.arr)))
			self.swapArrImage = np.append(self.swapArrImage, line, axis = 0)
		self.iterations += 1

	def randomSort(self, precedInOrder = singularIncreasing):

		n = len(self.arr)*len(self.arr)*len(self.arr)
		for i in range(n):
			a = randint(0,len(self.arr) - 1)
			b = randint(0,len(self.arr) - 1)
			if a > b:
				a, b = b, a
			if precedInOrder(self.arr[b], self.arr[a]):
				self.swap(a, b)

	def insertionSort(self, precedInOrder = singularIncreasing):

		for i in range(len(self.arr)):
			pos = i - 1
			while pos >= 0:
				if not precedInOrder(self.arr[i], self.arr[pos]):
					break
				pos -= 1
			if pos + 1 != i:
				for j in range(i, pos + 1, -1):
					self.swap(j, j-1)

	def bubbleSort(self, precedInOrder = singularIncreasing):

		isSorted = False
		while isSorted != True:
			isSorted = True
			for i in range(len(self.arr) - 1):
				if precedInOrder(self.arr[i + 1], self.arr[i]):
					self.swap(i + 1, i)
					isSorted = False
	
	def heapSort(self, precedInOrder = singularIncreasing):

		def father(pos):
			return (pos - 1) / 2
		def leftSon(pos):
			return 2 * pos + 1
		def rightSon(pos):
			return 2 * pos + 2

		def rearrangeAsHeap(precedInOrder):
			heapLen = len(self.arr)
			for i in range(0, len(self.arr)):
				pos = i
				while pos != 0 and precedInOrder(self.arr[pos], self.arr[father(pos)]):
					self.swap(pos, father(pos))
					pos = father(pos)

		rearrangeAsHeap(precedInOrder = precedInOrder)
		heapLen = len(self.arr)
		while heapLen > 0:
			pos = 0
			self.swap(pos, heapLen-1)
			heapLen -= 1
			while True:
				swapPos = pos
				if leftSon(pos) < heapLen and precedInOrder(self.arr[leftSon(pos)], self.arr[swapPos]):
					swapPos = leftSon(pos)
				if rightSon(pos) < heapLen and precedInOrder(self.arr[rightSon(pos)], self.arr[swapPos]):
					swapPos = rightSon(pos)
				if swapPos == pos:
					break
				self.swap(swapPos, pos)
				pos = swapPos

	def minheap(self):

		def father(pos):
			return (pos - 1) / 2
		def leftSon(pos):
			return 2 * pos + 1
		def rightSon(pos):
			return 2 * pos + 2

		heapLen = len(self.arr)
		for i in range(0, len(self.arr)):
			pos = i
			while pos != 0 and self.singularIncreasing(self.arr[pos], self.arr[father(pos)]):
				self.swap(pos, father(pos))
				pos = father(pos)

	def maxheap(self):

		def father(pos):
			return (pos - 1) / 2
		def leftSon(pos):
			return 2 * pos + 1
		def rightSon(pos):
			return 2 * pos + 2

		heapLen = len(self.arr)
		for i in range(0, len(self.arr)):
			pos = i
			while pos != 0 and self.singularDecreasing(self.arr[pos], self.arr[father(pos)]):
				self.swap(pos, father(pos))
				pos = father(pos)
			
	def quickSort(self, precedInOrder = singularIncreasing, left = 0, right = None):

		def partition(precedInOrder, left, right):
			leftmark = left + 1
			rightmark = right
			pivotvalue = self.arr[left]

			done = False
			while not done:
				while leftmark <= rightmark and (precedInOrder(self.arr[leftmark], pivotvalue) or self.singularEqual(self.arr[leftmark], pivotvalue)):
					leftmark += 1
				while rightmark >= leftmark and not precedInOrder(self.arr[rightmark], pivotvalue):
					rightmark -= 1
				if rightmark < leftmark:
					done = True
				else:
					self.swap(leftmark, rightmark)
			self.swap(left, rightmark)
			return rightmark

		if right == None:
			right = len(self.arr) - 1
		if left >= right:
			return

		splitPos = partition(precedInOrder, left, right)
		self.quickSort(precedInOrder, left, splitPos - 1)
		self.quickSort(precedInOrder, splitPos + 1, right)

	# Reverses elements in intervals of size L
	def LReverse(self, L):
		start = 0
		end = L - 1
		while start < len(self.arr):
			left = start
			right = end
			while left < right:
				self.swap(left, right)
				left += 1
				right -= 1
			start += L
			end += L
			end = min(end, len(self.arr) - 1)

	# Swaps half intervals (of size L/2)
	def LIntervalSwap(self, L):
		start = 0
		end = L - 1
		while start < len(self.arr):
			left = start
			right = start + L/2
			while right <= end:
				self.swap(left, right)
				left += 1
				right += 1
			start += L
			end += L
			end = min(end, len(self.arr) - 1)

	def LRandomSwap(self, L):
		for i in range(L):
			a = randint(0,len(self.arr) - 1)
			b = randint(0,len(self.arr) - 1)
			if a > b:
				a, b = b, a
			self.swap(a, b)

	def BST(self):
		n = len(self.arr)
		l_nodes = [-1 for i in range(n)]
		r_nodes = [-1 for i in range(n)]
		target_perm = [i for i in range(n)]

		def father(pos):
			return (pos - 1) / 2
		def leftSon(pos):
			return 2 * pos + 1
		def rightSon(pos):
			return 2 * pos + 2

		def computeLRNodes(node):
			if l_nodes[node] != -1 and r_nodes[node] != -1:
				return
			else:
				l_nodes[node] = 0
				r_nodes[node] = 0
				ls = leftSon(node)
				rs = rightSon(node)
				if ls < n:
					computeLRNodes(ls)
					l_nodes[node] = (l_nodes[ls] + r_nodes[ls] + 1)
				if rs < n:
					computeLRNodes(rs)
					r_nodes[node] = (l_nodes[rs] + r_nodes[rs] + 1)

		def computeBSTPerm(node, value):
			target_perm[node] = value + l_nodes[node]
			ls = leftSon(node)
			rs = rightSon(node)
			if ls < n:
				computeBSTPerm(ls, value)
			if rs < n:
				computeBSTPerm(rs, target_perm[node] + 1)

		perm = Permutation(self.arr)
		#print self.arr
		#print perm
		computeLRNodes(0)
		#print l_nodes
		#print r_nodes
		computeBSTPerm(0, 0)
		#print target_perm

		where_in_perm = [0 for _ in range(n)]
		for i in range(n):
			where_in_perm[perm[i]] = i
		for i in range(n):
			if perm[i] != target_perm[i]:
				j = where_in_perm[target_perm[i]]
				self.swap(i, j)
				was_here = perm[i]
				perm[j] = perm[i]
				perm[i] = target_perm[i]
				where_in_perm[perm[i]] = i
				where_in_perm[was_here] = j

		#print perm

	def ComplementaryPerm(self):
		n = len(self.arr)
		perm = Permutation(self.arr)
		target_perm = [n - i - 1 for i in perm]
		where_in_perm = [0 for _ in range(n)]
		for i in range(n):
			where_in_perm[perm[i]] = i
		for i in range(n):
			if perm[i] != target_perm[i]:
				j = where_in_perm[target_perm[i]]
				self.swap(i, j)
				was_here = perm[i]
				perm[j] = perm[i]
				perm[i] = target_perm[i]
				where_in_perm[perm[i]] = i
				where_in_perm[was_here] = j

	def Scrambler(self, L):
		n = len(self.arr)
		swaps = 0
		for i in range(n-2):
			if self.arr[i] < self.arr[i+1] and self.arr[i+1] < self.arr[i+2]:
				self.swap(i, i+1)
				swaps += 1
				if swaps >= L:
					break

	# Saving and showing the 2D image of 
	# element swaps in the array arr throughout the execution of entire algorithm

	def saveSwapArrImage(self, name):
		io.imsave(name, self.swapArrImage)
	def showSwapArrImage(self, name):
		io.imshow(self.swapArrImage)
	def isSorted(self):
		return True
		#return all(self.arr[i] <= self.arr[i+1] for i in xrange(len(self.arr) - 1))

	def run(self):

		# when we want to keep the elements in the same order
		# does not work as expected
		precedInOrder = self.asIs

		if self.order == 'increasing':
			precedInOrder = self.singularIncreasing
		elif self.order == 'decreasing':
			precedInOrder = self.singularDecreasing

		if self.method == 'insertionsort':

			self.insertionSort(precedInOrder = precedInOrder)

		elif self.method == 'bubblesort':

			self.bubbleSort(precedInOrder = precedInOrder)

		# MaxHeap for Increasing, MinHeap for Decreasing, etc.
		elif self.method == 'heapsort':
			heapOrder = self.asIs
			if precedInOrder == self.singularIncreasing:
				heapOrder = self.singularDecreasing
			elif precedInOrder == self.singularDecreasing:
				heapOrder = self.singularIncreasing

			self.heapSort(precedInOrder = heapOrder)

		elif self.method == 'quicksort':

			self.quickSort(precedInOrder = precedInOrder)

		elif self.method == 'randomsort':

			self.randomSort(precedInOrder = precedInOrder)

		elif self.method == 'reverse':

			self.LReverse(self.order)

		elif self.method == 'intervalswap':

			self.LIntervalSwap(self.order)

		elif self.method == 'randomswap':

			self.LRandomSwap(self.order)

		elif self.method == 'bst':

			self.BST()

		elif self.method == 'minheap':

			self.minheap()

		elif self.method == 'maxheap':

			self.maxheap()

		elif self.method == 'scrambler':

			self.Scrambler(self.order)

		elif self.method == 'complementary':

			self.ComplementaryPerm()
