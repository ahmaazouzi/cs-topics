# Optimizing Program Performance:
- This document is not about effective data structures or algorithms. It's mostly about how to make the compiler generate more optimized code. It also advises you on the general etiquette of optimization. Don't wholesale sacrifice the readability and extendability of your programs, be open to using trial and error and optimize  mostly when necessary, etc. 
- Topics we will discuss in the document include (in no particular order):
	- Identifying and eliminating or reducing *optimization blockers*, aspects of a program that depend largely on the execution environment and the compiler have no idea about.
	- Reducing unnecessary code such as function calls and memory references
	- Exploiting our knowledge of how a processor process instructions and how a certain goal can be achieved through different instructions or combinations of instructions, some of which are more efficient than the others. We can also direct the compiler to make use of so-called *instruction-level parallelism*.
	- We discuss how performance is measured and introduce such tools as *profilers* that are used to identify bottlenecks in the code and parts that require optimization. We will also hand-examine or eye-examine assembly code to identify bottlenecks.

## Capabilities and Limitations of Optimizing Compilers:
- Modern compilers are so smart! They can use the result of a single computations in several places and reduce the number of times computations are done. 
- Compilers such GCC offer us ways to control optimization. The simplest optimization control is to specify the level of optimization with an option like **`-Og`**, **`-O1`**, **`-O2`** or **`-03`**. We will mostly work with level 1 optimization. One side effect of raising the optimization level is that it results in hard to debug code and larger code size. Optimizing our code rationally using the tricks we will learn here can make optimization level 1 vastly better than blindly applying a higher level of optimization to it.
- As there can apparently be unsafe optimization, one must only use **safe optimizations** which result in a code with the exact same behavior for all cases. The following program shows how naive optimizations can result in bad code:
```c
void twiddle1(int *xp, int *yp){
    *xp += *yp;
    *xp += *yp;
}

void twiddle2(int *xp, int *yp){
    *xp += 2 * *yp;
}
```
- This is a case where trying to optimize code involving memory references can get a little murky. `twiddle2` is more efficient than `twiddle1` because the latter uses 3 memory references, while the former uses only 3 (memory references are generally considered as expensive operations).  What if both **`xp`** and **`yp`** reference the same memory location. this will result? There is no reason why they shouldn't. In this case the two operations will have different results. `twiddle1` will result in 3 times the value at **`xp`**, while `twiddle2` will quadruple that value. Normally the compiler would optimize `twiddle1` to a form similar to that of `twiddle2`, because the compiler can't by any means determine if **`xp`** and **`yp`** would point to the same location in memory, it will not optimize `twiddle1` to `twiddle2`. This is called **memory aliasing** where two pointers may point to the same location. Memory aliasing, where multiple pointers might reference the same memory location is a major **optimization blockers**, a situation where the compiler doesn't compile a segment of code because it cannot determine whether memory is aliased or not.
- Function calls are another major optimization blocker. Consider the following code:
```c
int counter = 0;

int f(){
    return counter++;
}

int func1(){
    return f() + f() + f();
}

int func2(){
    return 4 * f();
}
```
- `func2` might seem like an optimized `func1` and it might be in certain cases, but what if it produces side effects? In this example `f()` modifies the global variable `counter` making `func1` function differently from `func2`. 
- A compiler GCC does not try to do this kind of optimization because it assumes a function might cause side effects, this is why it's on the programmer to write more efficient code that leaves to the compiler only cases where there are no optimization blockers.



## Expressing Program Performance:
## Program Example:
## Eliminating Loop Inefficiencies: 
## Reducing Procedure Calls:
## Eliminating Unneeded Memory References:
## Understanding Modern Processors:
## Loop Unrolling:
## Enhancing Parallelism:
