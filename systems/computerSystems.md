# An Overview of Computer Systems: 
- **Computer systems** consists of the hardware and systems software that allow application software to work. Computers are very diverse from mainframes to personal computers to smart watches.. etc. However, they all consist of almost the same basic components. 
- Learning about computer systems concepts can make one a power programmer with an eye for performance and security. These concepts are consistent across different implementations and keep resurfacing whether one is dealing with low or high level programs. 
- In this document, we will run a survey of what computer systems are all about using the following program. We will follow the lifetime of this program from the moment its created until it's executed and shows a `Hello, world!` on the terminal:
```c
#include <stdio.h> 

int main(){
    printf("Hello, world!\n");
    return 0;
}
```

## 1. Information is Bits Plus Context:
- The `hello` program starts as a **source program** (also a **source file**), created with an **editor** like Vim or Sublime Text and a saved in a file named, say, *hello.c*. This file is a sequence of bits which can be either a **1** or **zero**. These bits are organized into **bytes** which are chunks of 8 bits. Each character represents a text character. 
- Most computers represents text characters using the ASCII standard which represents each character with a byte-size integer value.
- A file containing exclusively ASCII characters is called a **text file**, while all other files are **binary characters**
- All information in a system consists of a bunch of bits. Only the context in which these bits are viewed determines what they represents. The same sequence of bytes might represent text, an integer, a floating-point value or a machine instruction. 
- The way computers represent numbers is not exactly the way we understand numbers. Machines representations of numbers are approximations that don't always behave as we expect.

## 2. Programs Are Translated by Other Programs into Different Forms:
- Our `hello.c` program can be read by humans but can't be executed by machines! This program needs to be translated into low-level **machine-language instructions**. There are certain programs that can translate this C program into sequences of low-level machine-language instructions and repackage them into a form called an **executable object program** and stored as a binary disk file. Such program is also called an **executable object file**.
- We use a **compiler driver** to translate a source file to an executable object file. Translating a source file to an object file is done with a **preprocessor**, a **compiler**, an **assembler**, and a **linker**. These four programs are known collectively as a **compilation system**. `gcc` is one of the most popular compilation systems. We can use in a Unix-like machine to translate our `hello.c` program into an executable through the following terminal command:
```sh
gcc -o hello hello.c
```
- The command above tells `gcc` to translate our source file into an object file. This translation follows these 4 phases:
	1. **Preprocessing phase**: The preprocessor(`cpp`, short for C preprocessor) modifies the original C file through replacing directives starting with `#` such as `#include <stdio.h>` with the actual contents of the file `stido.h`. The result of preprocessing is another C file with the suffix `.i`: `hello.i`.
	2. **Compilation phase**: The compiler (`cc1`) translate the text file `hello.i` into the text file `hello.s` which contains an **assembly language program**. In assembly, low-level machine instructions are represented in a textual form. They are human readable and different high-level languages can compile to the same assembly language.
	3. **Assembly phase**: The assembler (`as`) translates the text file `hello.s` into machine language instructions, puts that in a form called **relocatable object program** and stores the result in an object file `hello.o`
	4. **Linking phase**: When a function is called from an external file, it needs to be merged with our `hello.o` program. The `printf` function for example resides in an object file called `printf.o` which is part of the *standard C library* provided by `gcc`. The linker (ld) merges `printf.o` into our `hello.o` resulting in an executable object file `hello` (also simply called an **executable**). The executable is ready to be used by the system.

## 3. The Importance of Understanding How Compilation Systems Work:
- The benefits of understanding how compiler systems work include:
	* *Optimizing program Performance*: Compilers have become so smart that they already do a lot of optimization, but we can still do a lot of optimization manually for what the compiler misses. We need to understand how machine code works and which C statements result in machine good with better performance. Examples of performance tweaking includes such as decisions as choosing between `switch` and `if-else` statements and figuring if one is always better than the other. Is a `while` loop faster a `for` loop? What is the cost of a function call? What are the performance cost of using pointer references vs. array indexes? Optimization is done better when you gain some familiarity with machine language and an understanding of how the compiler translates C constructs into machine language instructions. You can also actively choose which constructs to use in a given situation to help the compiler get optimum results. An understanding of memory hierarchy and how for example the compiler stores arrays in memory is also an important step towards getting optimized code.
	* *Understanding linking-time errors*: Linking is an overlooked but fundamental and problematic step in compilation. When working on a large projects perplexing linking errors emerge. Examples of such errors have to do with things like global variable conflicts. There will be more on linking and linking errors in the following sections. 
	* *Avoiding security problems*: **Buffer overflows** have wrecked many a system over the years. Such attacks arise because many programmers are not careful about restricting data they accept from untrusted sources. To avoid security problems one has to understand the program's stack and how it stores the data and control information of the program. In the following sections we will study how the compiler, operating system and the programmer work together to lessen the threats of attacks. 

## 4. Processors Read and Interpret Instructions Stored in Memory:
- Let's now trace the life of the executable file `hello` which is stored somewhere in disk. To run this program we are going to use the so-called *shell* as follows:
```sh
./hello
``` 
- The shell is a command-line interpreter that waits for you to type a command, then it executes it. If the first word you type is not a built-in shell command, the shell assumes it is a an executable file and it loads it and then runs it. You can equally just type `hello` and it works equally fine.

### Hardware Organization of a Systems: 
- To really understand what happens to our `hello` program when it runs in a system, we need to know something about the hardware organization of the system where it runs. The following diagram shows system based around modern Intel processors. All or most other systems are more or less the same:
![Hardware Organization](img/hardware.png)
- **Buses** are electrical conduits that carry bytes between the different components of the system. Buses are designed to transfer fixed-size chunks of bytes called **words**. The **word size** (the number of bytes in a word) is a fundamental parameter of the system. Most systems today have a word size of either 4 bytes (32 bits) or 8 bytes (64 bits).
- **I/O devices** are what connects our system to the external world. The system in our diagram, we have 4 I/O devices: a mouse and a keyboard, a display for output, and a disk for long term storage (the disk is both an input and output device). Before it runs, our `hello` program resides in the disk. I/O devices are connected to I/O bus with either **controllers** or **adapter**. Controllers are chip sets that make part of the motherboard itself, while adapters are cards that plug into a slot in the motherboard. Both are there to transfer information between the I/O bus and I/O devices. 
- **Main memory** is a temporary storage device that holds the program and the data it manipulates while the processor executes the program. Physically, the main memory is a collection **dynamic random access memory** chips. Logically, memory is arranged as a linear array of bytes, each with its unique address (which is an array index) starting with zero. Each machine instruction of a program can consist of a variable number of bytes. This is caused by the fact that data items have different lengths which also depend on the C types they correspond to. 
- **Processor** or the **CPU (central processing unit)** is the brain of a computer system that executes the instructions stored in the main memory.  An important component of the CPU is a **register** (some storage device we will talk about later) called the **program counter (PC)**. At any point in time, the program counter points to (i.e. contains the memory address) to some machine language instruction in the main memory. While a computer is powered on, the processor repeatedly executes the instruction pointed to by the PC, and updates the the PC to point to the next instruction. A processor *appears* to execute instructions according to a simple model defined by the processor's **ISA (instruction set architecture)**. In our model, instructions execute in a strict sequence and each executing each instructions involves a series of steps:
		+ The processors read the instruction from memory pointed at by the PC. 
		+ It then interprets the bits in the instruction.
		+ Performs the operation in the instruction.
		+ Updates the PC to point to the next instruction. The next instruction might or might "contiguous in memory to the instruction that was just executed".
- A processor can only perform a few set of simple operations. These operations revolve around the **register file**, **ALU (arithmetic/logic unit)** and the main memory. The register file is a small storage device consisting of a collection of word-size (mind you, word size of a our 64-bit CPU is 64) registers. Each register has its unique name. Registers themselves are similar to memory cells but much faster. The ALU computes new data and address values. Examples of instructions the CPU carries out include:
	+ **Load**: copies a byte or a word from memory into a register, overwriting the existing contents of the register. 
	+ **Store**: Copies a byte or a word from a register into memory overwriting the existing content at the given memory location.
	+ **Operate**: Copies the content of two registers into the ALU, performs an arithmetic operation on the two words and stores the result into a register, overwriting its preexisting content. 
	+ **Jump**: Extracts a word from the instruction itself and copies that word into the program counter, overwriting the previous value of the PC. 
- A processor only *appears* to be a simple implementation of its instruction set architecture (ISA), but modern processors use complex tricks to speed up execution. While the ISA describes the effects of instructions, a processor's **microarchitecture** describes how the processor is implemented.

### Running the `hello` Program: 
- At a basic level, this is what happens while our `hello` program is being executed:
	+ The shell program is running and waiting for us to type our commands.
	+ As we type each character of our command, each one character is read by the shell program into a register and then stored into memory.
	+ When we hit the `enter` key, the shell knows we have finished typing our command.
	+ The shell then loads the contents of the executable file `hello` into memory by execution a sequence of instructions that copies the code and data in the file from disk to memory. The data include the `Hello, world!\n` string. Through **DMA (direct memory access)**, data passes directly from disk to memory without passing by the processor. We will discuss DMA later.
	+ When the code and data from the `hello` object file are loaded into memory, the processor starts executing the instructions in the `hello` program's `main` routine. These instructions copy bytes in the `Hello, world!\n` string from memory to the register file, and from there to the display device where they get displayed on the screen. 

## 5. Cache is the Shit:
- It is easy to observe that much of a program's execution revolves around moving data from location to another. `hello` is first stored in desk. When the program is loaded it is copied from disk to memory. When the program starts executing, instructions are copied from main memory to the to the processor and data is copied from main memory to the register file then to the display. There is much of this moving of data from one location another. These movements are also costly and present a lot of overhead that drags down the speed of the actual work of the processor. System designers do a lot of work to make such copying from one location to another fast. 
- Larger storage devices are necessarily slower than smaller storage devices. Faster storage devices are also much more expensive and harder to make. It might take the processor 10 million times longer to read directly from disk than from memory.
- The register file can only hold a few hundred bytes large while main memory can hold billions of bytes. However, accessing registers is 100 times faster than main memory. Memory speed does sometimes seem to progress much slower than processor speed. 
![Memory hierarchy](img/memH.png)










