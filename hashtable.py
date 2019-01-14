# From Miller and Ranum's "Problem Solving with Algorithms and Data Structures"

class HashMap:
	def __init__(self):
		self.size = 11
		self.slots = [None] * self.size
		self.data = [None] * self.size

	def put(self, key, data):
		hashvalue = self.hashFunction(key, len(self.slots))

		if self.slots[hashvalue] == None:
			self.slots[hashvalue] = key
			self.data[hashvalue] = data
		else:
			if self.slots[hashvalue] == key:
				self.data[hashvalue] = data
			else:
				nextslot = self.rehash(hashvalue, len(self.slots))
				while self.slots[nextslot] != None and self.slots[nextslot] != key:
					nextslot = self.rehash(nextslot, len(self.slots))

				if self.slots[nextslot] == None:
					self.slots[nextslot] = key
					self.slots[nextslot] = data
				else:
					self.data[nextslot] = data

	def get(self, key):
		startslot = self.hashFunction(key, len(self.slots))

		data = None
		stop = False
		found = False
		position = startslot
		while self.slots[position] != None and not found and not stop:
			if self.slots[position] == key:
				found = True
				data = self.data[position]
			else:
				position = self.rehash(position, len(self.slots))
				if position == startslot:
					stop = True
		return data

	def __getitem__(self, key):
		return self.get(key)

	def __setitem__(self, key):
		return self.set(key)

	def hashFunction(self, key, size):
		return key % size

	def rehash(self, oldhash, size):
		return (oldhash + 1) % size


a = HashMap()
a.put(0, "baba")
a.put(0, "nana")
print a.slots

