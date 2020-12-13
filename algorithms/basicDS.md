## Stacks:
- Stacks are an abstract LIFO data structures where last inserted data are the first to be popped out. They are great for reversing stuff and checking balanced sequences in syntax parsers.. etc. They can be implemented using arrays or linked lists. Linked lists might be a little less intuitive but they are generally more efficient spacewise and timewise.

## Queues:
- Queues are FIFO (first in, first out). They are essential 

## Linked Lists:
- A **linked list** is a linear data structure just like an array where multiple objects can be traversed one after the other, but it's fundamentally different from an array. 
- An array is a contiguous chunk of memory cells where objects can be accessed by indices located between the bounds of the array. The elements of a linked list are accessed through **pointers** (or object references). They are like beads in a rosary (tasbeeh). You can only access it from one or both of its heads. 
- The main **advantage** of a linked list is its dynamic nature as opposed to the fixed nature of an array. A linked list also provides for faster insertions and deletes because there is no need for shifting. The absence of element shifting is all the better if the location of the insert or delete is towards the head of the linked list. 
- The most basic linked list, a **singly linked list** consists of one or more **nodes**, each nodes has *key* (the node's data) and a *pointer* (usually named *next*) that points to the next node. The first element of a linked to which no other list element points is the **head** of the list. The las element whose *next* pointer points to a null is the list's **tail**. When the list's head points to a null, the list is empty! 
- A linked list can be:
	* Either a **singly** or **doubly**. In a **doubly linked list** a node has two pointers one pointing to the next node and another pointing to the previous node.
	* Either **circular** or not. If the next pointer of a singly linked list's tail points to the list's head, the list is said to be circular.
	* Either **sorted** or **sorted**.
- The different types of linked lists offer different advantages to different operations. Theoretically inserting and removing an element from the tail of a doubly LL can be achieved in constant time `O(1)`  as opposed to `O(N)` in a singly LL. 
- Inserting, removing from and searching a linked list should be fairly obvious and can be learned from code examples.
- There is some mumbling about sentinels and I don't get it and I kinda don't care!

## Hash Tables:
- A hash table supports the 3 basic operations: *insert, search *and *delete*. Inserts and deletes are generally `O(1)` in hash tables, and although searches can be as bad as `O(1)` as in linked lists, hash table search do generally approach `O(1)` especially in well constructed tables. 
- In a hash table, the position of a value (or its key) is computed using the value itself. 
- When the number of actual keys is small compared to the possible number of a table's keys, the table becomes effective in guaranteeing a constant time for the 3 operations aforementioned. A less effective has table suffers from *collisions* where more than one keys map to the same index. This can be mitigated using either *chaining* or *open addressing*.
- A good hash table can be achieved with a good *hash function*. A hash function is used to extract a hash table's key from a given value.

### How Hash Tables Work:
- To understand hash tables, it might be wise to first learn about *direct addressing*. Direct addressing is good way to guarantee `O(1)` speed for inserts, deletes and searches and it's practical if the range of possible values to be stored in a table is small. In a *direct-address table*, each slot (or bucket) corresponds to a key in the range of things we want to store. For example, if the range of possible values we are dealing with is 0 to 20, then we have a direct-address table of length 21 where 0 would be stored in position 0, element 3 would be stored in slot 3 ...etc. All the operations in such table have a constant time complexity. The problem is that such tables can only handle small ranges of possible values making them impractical for most applications although they perform well for situations where the possible ranges of values are small and already known.
- Hash tables allow you to efficiently store a small range of values even if the range of possible range of values is so large and still be able to retrieve such values in an average time of `O(1)`. 
- Instead of mapping directly to an array's index as in direct-address tables, a function is used to map value to its slot in a hash map where is the size of the hash map is much much smaller than the universe of possible values than can be mapped into it.
- Because we are mapping from a large universe of possible values to a small range, it possible and common that two values map to the same slot in hash table resulting in a **collision**. Collisions can be resolved by chaining or open addressing but it would be amazing if we could resolve collisions altogether. 
- Avoiding or minimizing collisions can be done through choosing a good hash function. A good hash function appears to be random. Collisions can't be totally avoided but can be minimized by a seemingly-random hash function. 

### Chaining:
- One way to handle collisions is through the use of chaining. When two or more values map to the same bucket in a hash table, a linked list is constructed and the keys are placed into it. The bucket holds a pointer to the linked list head. 
- Insert in a hash table with chaining is `O(1)` while search and delete can have a linear worst case. CLRS claims that if we use a doubly linked list, deletes would have constant worst case but I don't really understand how that's possible. 
- The worst case time of hashing with chaining can be `O(N)` if all the keys hash to the same slot resulting in an n-long linked list. Added to this is the time to compute the hashing function. 
- With a good hash function dictionary operations in a hash table with chaining should take an average `O(1)` time.

### Hash Functions:
- It's all about hash functions, gov'na! A good hash function is one that satisfies the asumption that each key is equally likely to map to any bucket. There is no way however to test such condition. Popular hashing schemes include the heuristic **hashing by division** and **hashing by multiplication** and the randomized **universal hashing**. 

#### 2. Hashing by Division:
- In this method, the hash value is equal to the remainder of dividing the key *k* by the the size of the hash table *m* as in:
				   ***h(k) = k mod m***
- To get useful hash values avoid making *m* a power of 2. It's preferable to make *m* a prime number not close to a power of 2 to avoid many collusions!!!??

#### 1. Hashing by Multiplication:
- Hashing by multiplication is done through two steps:
	1. The key *K* is first multiplied by a constant number *A* where  *0 < A < 1* and the fractional part of this result is extracted.
	2. The fractional part extracted from the previous operations is again multiplied by the size of the hash table *m* and the floor this operation is the hash value. This can be expressed as follows:
					***h(k) =  ⌊m (kA mod 1)⌋***
- The size *m* of the hash table in not important but it's preferable that it be a power of two to make it easier for binary computers!!! And for other arcane and super-nerdy reasons!
- The value of the constant *A* is also unimportant by the legendary Knuth suggests that it be equivalent to***(√5 - 1) / 2*** and God knows why!

#### 3. Universal Hashing:
- In universal hashing, we using a random hashing function from a class of carefully designed hash functions. The randomly selected function is independent of the key to be stored. This generally results in good performance and little collisions. 
- We can construct a class of universal hash functions as follows:
	1. We pick a value *p* which must be a a prime number larger than *m* the size of the wanted hash table and such that every key value *k* is in the range 0 to *p* - 1.
	2. We pick two values *a* such that *0 < a < p -1* and *b* such that *1 < b < p -1*
	3. We now define a function *h<sub>ab</sub>* as follows:
				   ***h<sub>ab</sub>(k) = ((ak + b) mod p) mod m***
- There is talk of number theory and some big words and I have no clue!!! Might come back to this after a course on discrete math!

### Open Addressing:
- In addition to chaining, **open addressing** is used to handle collisions. We use to this technique to store all the elements of a hash table in the array itself without resorting to external (or internal) linked lists. In open addressing, when a collision occurs, the element is placed somewhere else in the table itself hence resulting in filling up the table. ("The load factor *α* can never exceed 1"). I think the load factor means the elements in the table divided by the size *m* of the table. 
- 









