#include<stdio.h>

int main(){
    int x = 12340;
    int k = 8;
    int a = (x + (1<< k) - 1) >>k;
    printf("%d\n", a);
    return 0;
}
