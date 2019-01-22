# From: CLRS, MIT's intro to algorithms OWC
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
	if left < size and alist[left][0] < alist[index][0]:
		largest = left
	else:
		largest = index
	if right < size and alist[right][0] < alist[largest][0]:
		largest = right

	if largest != index:
		# pythonism can replace this mess
		temp = alist[largest]
		alist[largest] = alist[index]
		alist[index] = temp
		max_heapify(alist, size, largest)

def build_max_heap(alist):
	# Crap to be fixed
	half_size = reversed(range((len(alist) // 2) + 1))
	for i in half_size:
		max_heapify(alist, len(alist), i)

def heap_max(alist):
	if len(alist) > 0:
		return alist[0]
	else:
		print "Empty queue"

def heap_extract_max(alist):
	if len(alist) < 1:
		print "Empty queue"
		return
	maximum = alist[0]
	alist[0] = alist[-1]
	del(alist[-1])
	max_heapify(alist, len(alist), 0)
	return maximum

def heap_increase_key(alist, index, key):
	if (key) < alist[index]:
		print "new key is smaller than current key"
		return

	alist[index] = key
	while index > 0 and alist[get_parent(index)] > alist[index]:
		temp = alist[index]
		alist[index] = alist[get_parent(index)] # to be fixed
		alist[get_parent(index)] = temp
		index = get_parent(index)

def max_heap_insert(alist, key):
	alist.append(-1)
	heap_increase_key(alist, len(alist) - 1, key)

# a = []

# max_heap_insert(a, 77)
# max_heap_insert(a, 100)
# max_heap_insert(a, 1000)
# max_heap_insert(a, 0)
# max_heap_insert(a, 44)
# max_heap_insert(a, 55)
# max_heap_insert(a, 105500)
# max_heap_insert(a, 13300)

# a = [6666, 666, 0, 7773,54,2,2,4,444,5,6,66666]
# build_max_heap(a)

# while a != []:
# 	print heap_extract_max(a)
 
# print a