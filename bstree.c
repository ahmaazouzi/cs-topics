#include <stdio.h>
#include <stdlib.h>

typedef struct node{
	char data;
	struct node *left, *right;
} node;

node *newNode(char data);
node *insert(node *node, char data);
void inorder(node * node);
int main(){
	node *root = NULL; 
	root = insert(root, 'd');
	insert(root, 'z');
	insert(root, 'z');
	insert(root, 'z');
	insert(root, 'z');
	insert(root, 'z');
	insert(root, 'z');
	insert(root, 'a');
	insert(root, 'z');
	insert(root, '#');
	insert(root, 'l');
	inorder(root);
	return 0;
}

node *newNode(char data){
	node *node = (struct node *) malloc(sizeof(struct node));
	node->data = data;
	node->left = node->right = NULL;
	return node;
}

void inorder(node *node){
	if (node != NULL){
		inorder(node->left);
		printf("%c ", node->data);
		inorder(node->right);
	}
}

node *insert(node *node, char data){
	if (node == NULL)
		return newNode(data);
	// if (node->data == data)
	// 	;
	if (data < node->data)
		node->left = insert(node->left, data);
	else if (data > node->data)
		node->right = insert(node->right, data);
	return node;
}