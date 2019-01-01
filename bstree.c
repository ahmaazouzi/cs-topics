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
	node *root = newNode('d');
	insert(root, 'j');
	insert(root, '2');
	insert(root, 'f');
	insert(root, 'd');
	insert(root, 'd');
	insert(root, 'd');
	insert(root, 'a');
	insert(root, 'z');
	insert(root, '#');
	insert(root, 'l');
	inorder(root);
	return 0;
}

node *newNode(char data){
	node *newnode = (struct node *) malloc(sizeof(node));
	newnode->data = data;
	newnode->left = newnode->right = NULL;
	return newnode;
}

node *insert(node *node, char data){
	if (node == NULL)
		return newNode(data);

	if (data == node->data)
		return node;
	else if (data < node->data)
		node->left = insert(node->left, data);
	else
		node->right = insert(node->right, data);
	return node;
}

void inorder(node * node){
	if (node != NULL){
		inorder(node->left);
		printf("%c\n", node->data);
		inorder(node->right);
	}
}
