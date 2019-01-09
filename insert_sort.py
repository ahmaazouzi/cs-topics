# From Miller and Ranum's "Problem Solving with Algorithms and Data Structures"

def insert_sort(lista):
	for index in range(1,len(lista)):
		pos = index
		current_val = lista[index]

		while pos > 0 and current_val < lista[pos - 1]:
			lista[pos] = lista[pos - 1]
			pos	 = pos - 1

		lista[pos] = current_val

b = [4,5,6,3,6,8,33,2,4,9,2,9]
insert_sort(b)
print b