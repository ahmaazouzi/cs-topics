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
