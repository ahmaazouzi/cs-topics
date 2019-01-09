#From: CLRS, MIT's intro to algorithms OWC.

def get_parent(index):
	return index / 2

def get_left(index):
	return 2 * index

def get_right(index):
	return (2 * index) + 1

#Repackeging this spaghetti into a heap object will make it less messy
def max_heapify(alist, index):
	left = get_left(index)
	right = get_right(index)

	# heap size (to be changed)
	if left < len(alist) and alist[left] > alist[index]:
		largest = left
	else:
		largest = index
	if right < len(alist)  and alist[right] > alist[largest]:
		largest = right

	if largest != index:
		# pythonism can replace this mess
		temp = alist[largest]
		alist[largest] = alist[index]
		alist[index] = temp
		max_heapify(alist, largest)

def build_max_heap(alist):
	# Crap to be fixed
	half_size = reversed(range((len(alist))/2))
	for i in half_size:
		max_heapify(alist, i)
		

a = [1, 16, 14, 10, 8, 7, 9, 3, 2, 4, 1]
print "1 is unheaped: ", a
max_heapify(a, 0)
print "1 is heaped: ", a
print

b = [4, 1, 3, 2, 16, 9, 10, 14, 8]
print "unheapified list: ", b
build_max_heap(b)
print "heapified list: ", b




