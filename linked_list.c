#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

struct item {
    int data;
    struct item *next;
};

struct item *createList(void);
void addItem(struct item **, int);
void printList(struct item *);
void deleteItem(struct item *, int);
int main(){
    struct item *list = createList();
    addItem(&list, 4);
    addItem(&list, 3);
    addItem(&list, 2);
    addItem(&list, 1);
    addItem(&list, 0);
    deleteItem(list, 0);
    printList(list);
    return 0;
}

struct item *createList(void){
    struct item *tail;
    tail = (struct item *) malloc(sizeof(struct item));
    tail->next = NULL;
    return tail;
}

void addItem(struct item **list, int data){
    struct item *itemo;
    itemo = (struct item *) malloc(sizeof(struct item));
    itemo->data = data;
    itemo->next = *list;
    *list = itemo;
}

void deleteItem(struct item *list, int data){
    struct item *itemo, *temp;
    itemo = (struct item *) malloc(sizeof(struct item));
    temp = (struct item *) malloc(sizeof(struct item));
    itemo = list;
    if (itemo->data == data)
            itemo = itemo->next;
    else
        for (itemo = list; itemo->next != NULL; temp = itemo, itemo = itemo->next)
            if (itemo->data == data)
                temp->next = itemo->next;
}

void printList(struct item *list){
    struct item *itemo;
    itemo = (struct item *) malloc(sizeof(struct item));
    for (itemo = list; itemo->next != NULL; itemo = itemo->next)
        printf("%d ", itemo->data);
    printf("\n");
}