# From: CLRS, MIT's intro to algorithms OCW
# with slight modifications as CLRS's lists are 1-based.
# Heap size is also a little ambiguous.

def get_parent(index):
	return index / 2

def get_left(index):
	return 2 * index

def get_right(index):
	return (2 * index) + 1

#Repackeging this spaghetti into a heap object will make it less messy
def max_heapify(alist, size, index):
	left = get_left(index)
	right = get_right(index)

	# heap size (to be changed)
	if left < size and alist[left] > alist[index]:
		largest = left
	else:
		largest = index
	if right < size and alist[right] > alist[largest]:
		largest = right

	if largest != index:
		# pythonism can replace this mess
		temp = alist[largest]
		alist[largest] = alist[index]
		alist[index] = temp
		max_heapify(alist, size, largest)

def build_max_heap(alist):
	# Crap to be fixed
	half_size = reversed(range((len(alist))/2))
	for i in half_size:
		max_heapify(alist, len(alist), i)

def heap_sort(alist):
	build_max_heap(alist)
	heap_size = len(alist) - 1
	while heap_size > 0:
		temp = alist[0]
		alist[0] = alist[heap_size]
		alist[heap_size] = temp
		heap_size -= 1
		max_heapify(alist, heap_size, 0)

b = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
heap_sort(b)
print b




