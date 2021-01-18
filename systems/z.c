#include <stdio.h>

int main(){
    float a = 0e128;
    printf("%f\n", a - 0e128);
    return 0;
}
