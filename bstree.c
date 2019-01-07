#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct node {
	char data;
	struct node *left, *right;
} node;

node *newNode(char data);
node *insert(node *, char);
void inorder(node *);
struct node * minValueNode(struct node*);
node *delete(node *, char);
int main(){
	node *root = NULL;
	root = insert(root, 100);
	insert(root, 101);
	insert(root, 99);
	insert(root, 98);
	insert(root, 119);
	inorder(root);
	putchar('\n');
	delete(root, 99);
	inorder(root);
	putchar('\n');
	return 0;
}

node *newNode(char data){
	node *node = (struct node *) malloc(sizeof(struct node));
	node->data = data;
	node->left = node->right = NULL;
	return node;
}

node *insert(node * node, char data){
	if (node == NULL)
		return newNode(data);
	if (data < node->data)
		node->left = insert(node->left, data);
	else if(data > node->data)
		node->right = insert(node->right, data);
	return node;
}

void inorder(node *node){
	if(node != NULL){
		inorder(node->left);
		printf("%c ", node->data);
		inorder(node->right);
	}
}

struct node * minValueNode(struct node* node) { 
    struct node* current = node; 
    while (current->left != NULL) 
        current = current->left; 
    return current; 
} 

node *delete(node *node, char data){
	if (node == NULL)
		return node;

	if (data < node->data)
		node->left = delete(node->left, data);
	else if(data > node->data)
		node->right = delete(node->right, data);

	else {
		if (node->left == NULL){
			struct node *temp = node->right;
			free(node);
			return temp;
		} else if (node->right == NULL){
			struct node *temp = node->left;
			free(node);
			return temp;
		}

		struct node* temp = minValueNode(node->right); 
		node->data = temp->data;
		node->right = delete(node->right, temp->data);

	}

	return node;
}

node* search(struct node* root, int key) { 
    if (root == NULL || root->key == key) 
       return root; 

    if (root->key < key) 
       return search(root->right, key); 
    return search(root->left, key);
}
