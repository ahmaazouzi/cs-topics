# Virtual Memory:

## Introduction:
- Multiple processes can share the CPU and memory. When too many processes share a CPU, it is slowed down but when too many	processes share memory, they might run out of the available space and no more processes can use that memory. Processes might also be able to mess with memory "belonging" to other processes, thus corrupting this memory.
- Modern systems use **virtual memory** to address these problems. "*Virtual memory is an elegant interaction of hardware exceptions, hardware address translation, main memory, disk files, and kernel software that provides each process with a large, uniform, and private address space.*" It offers the following three services:
	- It treats main memory as a cache for disk, keeping only active data in memory and moving data back and forth between memory and disk as needed.
	- It simplifies memory management by providing each process with a uniform address space.
	- It provides each process with a private address space that cannot or should not be accessed/corrupted by other processes.
- The system takes care of virtual memory from A to Z without the need of programmer's intervention. Why bother about it then? Reasons for bothering about VM include:
	- *VM is central*: Understanding VM will make one have a better understanding of the system. VM involves all layers and aspects of a system from hardware exceptions, assemblers, files, loaders, processes, etc. 
	- *VM is powerful*: Understanding VM gives applications advanced capabilities and allows for neat tricks (*that we will see later*).
	- *VM is dangerous*: Improper use of VM can lead to weird and dangerous errors and program behavior. Understanding VM might allow me to better understand memory errors surrounding misuse of pointers and what not!
- VM is a difficult subject. This document will try to first go over how it works and then moves on to described how it is used and managed by applications. We might also go over how to manage and control VM in our programs. 

## Physical and Virtual Addressing:
## Address Spaces:
## VM as a Tool for Caching:
## VM as a Tool for Memory Management:
## VM as a Tool for Memory Protection:
## Address Translation:
## Case Study: The Intel Core i7/Linux Memory System
## Memory Mapping:
## Dynamic Memory Allocation:
## Garbage Collection:
## Common Memory Related C Bugs: