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
int main(){
	node *root = NULL;
	root = insert(root, 100);
	insert(root, 101);
	insert(root, 99);
	insert(root, 98);
	insert(root, 119);
	inorder(root);
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
		printf("%c\n", node->data);
		inorder(node->right);
	}
}

node *delete(node *node){
	return *node;
}
