# Limited Direct Execution:
## Intro:
- The authors came up with the term **limited direct execution** to describe how processes are controlled by a modern regular OS. Processes need to be both *performant*, and also be *controlled* by the OS. Performance means its instructions run natively on the CPU, and controls refer to the requirement that a process shouldn't access resources it is not supposed to access or run longer than the time allotted to it.

## Direct but Limited Execution:
- Direct execution means the process runs directly on the CPU. This is why C, for example, is faster than Java (or why x86 instructions are faster than Java bytecode as the former run directly on the metal, while the latter run on a intermediate machine which translates it to x86 instructions). The problem with direct execution is that process code can do anything it wishes. Process instructions are identical to the instructions used to make the OS itself, so the processes might change and access data it's not meant to access, or might run forever and take over the system's resources.
- We know that an OS manages computer resources, so it allows certain operations and restrict others. It gives users different levels of control over the system, etc. If processes are not limited, they can do anything, so the OS becomes less usable. 
- To make the instructions of a process less dangerous, we limit their capabilities. Certain operations such as accessing IO devices, creating and destroying other processes, etc. cannot be done directly by processes, but are done through indirectly, through system calls and whatnot!
- But how can processes be limited? This is done by having processes run in two modes:
	- **User mode** in which the process is limited in what it can do. It cannot, for example, perform an IO operation.
	- **Kernel mode** in which the kernel code runs. It can do anything it want
- If the user process wishes to execute certain restricted operations, it needs to do so through a system call. These system calls are done by the OS itself on behalf of the user process. When the user process wants to perform a restricted operation, it executes a special **trap** instruction. This instruction jumps into the kernel raising privilege to the kernel mode. The system performs the restricted operation, and the OS calls a **return-from-trap** instruction which returns to the calling user and lowers privileges.

### Exception!!
- *It turned out that much what I've been reading so far of this book has already been already detailed in Computer Systems, a Programmer's Perspective!! That book didn't discuss "policies", and the "whys" of things, but did thoroughly described much of OS functionality, especially Unix*. I will continue reading this book but will mostly focus on stuff not covered yet in the systems book. I will also spend more times on they whys and design aspects of OSs and why certain aspects were in certain ways in Unix or whatever OS. At least, I am glad that spending a few months reading the systems book was so far really really worth it!


