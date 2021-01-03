# Binary Search Trees:
## Binary Search Trees:
- Trees are some of the most versatile
- A search tree supports such varied operations as: *search, minimum, maximum, predecessor, successor, insert* and *delete*.

## Red-Black Trees:
- While a generic binary search tree can, just can  and are supposed to support operations in _O(h)_ time. this is not guaranteed! A tree is useful if its height is not too large, otherwise it becomes just a clunky linked list slugging at a _O(n)_ time. To guarantee an _O(h)_ speed, we need to balance our BST. Several schemes are devised to balance a search tree including the famous AVL trees and **red-black trees**.

### Properties of Red-Black Trees:
- Each node in a red-black tree has an extra bit of storage for the node's *color* which can be either red or black. Coloring a tree in this manner ensures that any path from the root to a leaf is no bigger than twice the length of any other path making the tree approximately balanced. 
- Nodes which don't have parents or children have pointers to NIL values. These are leaves or **external nodes**, while nodes with non-NIL parent and children pointers are considered **internal nodes**
- Generally speaking a red-black tree is a binary tree with the following characteristics:
	1. Every node is either red or black
	2. The root is black.
	3. Every leaf (NIL node) is black.
	4. If a node is red, both its children are black.
	5. For each node, the paths from it to each of its descending leaves contain the same number of black nodes.
- A **sentinel** node can be used to replace the NIL values to better avoid boundary issues. This sentinel will replace all the NIL child values at the leaves and NIL value of the root's parent. This way all the nodes will treated as regular nodes and "null pointer" errors will be avoided.
- The number of black nodes in a simple path from but not including a node _x_ down to a leaf is called the **black height** and is denoted by *bh(x)*. The black height of a tree is the black height of its root. 
- Should you really need to prove that the height of a red-black tree is _2lg(bh(T) + 1)_, give that that _T_ is for tree and _bh(...)_ is for black height as mentioned before. 

### Rotation:
- *Insert* and *delete* operations in a red-black tree with *n* keys take *lg(n)* time. These operations might also violate the red-black tree properties because they modify the tree. To restore the properties of the red-black tree, we need to change the color of some nodes and modify the pointer structure. 
- The pointer structure can be changed with **rotation**. Rotation leads to preserving the properties of a red-black tree. The following diagram shows the two types of rotation that can be performed on a subtree in a red-black tree:
```
                z          Left rotation        x
               / \         <------------       / \
              x    γ                          α   z
             / \           Right rotatation      / \
            α   β          --------------->     β   γ
```
- When we do a **left rotation** around node `x`, it's assumed that its right side `z` is not a NIL. A left rotation can be performed on any node `x` in the tree whose right child is not NIL. `z` replaces `x` as the new root of the subtree. `x` becomes the left child of `z` and `β`	becomes the right side of `x`.
- A right rotation is symmetrical to the left rotation. `x` becomes the root of the subtree and it's assumed the left child of the subtree's root is not NIL. 
- The following snippet shows how left rotation is done:

```py
def leftRotate(tree, x):
	z = x.right
	x.right = z.left
	if z.left is None:
		z.left.p = x
	z.p = x.p
	if x.p is None:
		tree.root = z
	elif x is x.p.left:
		x.p.left = z
	else:
		x.p.right = z
	z.left = x
	x.p = z
```

### Insertions:

```py
def rbInsert(tree, z):
	y = None
	x = tree.root
	

```













