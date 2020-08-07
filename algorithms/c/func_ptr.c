#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void f(void (*a)(), int b, int s) {
    a(b, s);
}

void add(int b, int s) {
    printf("%d\n", b + s);
}

void subtract(int b, int s) {
    printf("%d\n", b + s);
}

void multiply(int b, int s) {
    printf("%d\n", b + s);
}

void divide(int b, int s) {
    printf("%d\n", b + s);
}

int main(int argc, char const *argv[]) {
	int first = atoi(argv[2]);
	int secind = atoi(argv[3]);

	if ((strcmp(argv[1], "add")) == 0)
     	f(&add, first, secind);
	if ((strcmp(argv[1], "subtract")) == 0)
     	f(&subtract, first, secind);
    if ((strcmp(argv[1], "multiply")) == 0)
     	f(&multiply, first, secind);
	if ((strcmp(argv[1], "divide")) == 0)
     	f(&divide, first, secind);
    return 0;
}
