# Limited Direct Execution:
## Table of Contents:
## Intro:
- The authors came up with the term **limited direct execution** to describe how processes are controlled by a modern regular OS. Processes need to be both *performant*, and also be *controlled* by the OS. Performance means its instructions run natively on the CPU, and controls refer to the requirement that a process shouldn't access resources it is not supposed to access or run longer than the time allotted to it.

## Direct but Limited Execution:
- Direct execution means the process runs directly on the CPU. This is why C, for example, is faster than Java (or why x86 instructions are faster than Java bytecode as the former run directly on the metal, while the latter run on a intermediate machine which translates it to x86 instructions). The problem with direct execution is that process code can do anything it wishes. Process instructions are identical to the instructions used to make the OS itself, so the processes might change and access data it's not meant to access, or might run forever and take over the system's resources.
- We know that an OS manages computer resources, so it allows certain operations and restrict others. It gives users different levels of control over the system, etc. If processes are not limited, they can do anything, so the OS becomes less usable. 
- To make the instructions of a process less dangerous, we limit their capabilities. Certain operations such as accessing IO devices, creating and destroying other processes, etc. cannot be done directly by processes, but are done through indirectly, through system calls and whatnot!
- But how can processes be limited? This is done by having processes run in two modes:
	- A **user **


