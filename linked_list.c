#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

struct item {
    int data;
    struct item *next;
};
void printReverse(struct item *);
struct item *createList(void);
struct item *recsearch(struct item *, int);
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
    struct item *l = recsearch(list, 4);
    printf("number %d found in list\n", l->data);
    printList(list);
    printList(list);
    return 0;
}

struct item *createList(void){
    struct item *tail;
    tail = (struct item *) malloc(sizeof(struct item));
    tail->next = NULL;
    return tail;
}

struct item *recsearch(struct item *list, int data){
    if (list == NULL)
        return(NULL);
    if (list->data == data)
        return list;
    else
        return(recsearch(list->next, data));
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
    for (itemo = list; itemo->next != NULL; temp = itemo, itemo = itemo->next)
        if (itemo->data == data)
            temp->next = itemo->next;
}

void printReverse(struct item *list){
    if(list->next != NULL) {
        printReverse(list->next);
        printf("%d ", list->data);
    }
}

void printList(struct item *list){
    struct item *itemo;
    itemo = (struct item *) malloc(sizeof(struct item));
    putchar('\n');
    for (itemo = list; itemo->next != NULL; itemo = itemo->next)
        printf("%d ", itemo->data);
    printf("\n");
}