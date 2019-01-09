#From: CLRS, MIT's intro to algorithms OWC.

def get_parent(index):
	return index / 2

def get_left(index):
	return 2 * index

def get_right(index):
	return (2 * index) + 1

def max_heapify(alist, index):
	left = get_left(index)
	right = get_right(index)

	# heap size (to be changed)
	if left <= len(alist) and alist[left] > alist[index]:
		largest = left
	else:
		largest = index
	if right <= len(alist) and alist[right] > alist[largest]:
		largest = right
	if largest != index:
		# pythonism can replace this mess
		temp = alist[largest]
		alist[largest] = alist[index]
		alist[index] = temp
		max_heapify(alist, largest)

a = [1, 16, 14, 10, 8, 7, 9, 3, 2, 4]
print a
max_heapify(a, 0)
print a




