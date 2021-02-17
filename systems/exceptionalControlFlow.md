# Exceptional Control Flow:

## Introduction:
- From the time a computer is powered on until it is turned off, the program counter takes a sequence of values where each value is the address of an instruction. Each transition from one PC value to the next is called a **control transfer**. A sequence of control transfers is called **control flow**. A simple control flow involves instructions that are stored in adjacent memory locations. This simple flow is interrupted from time to time leading to situations where the instructions being executed are not in adjacent memory locations. Such situations involve instructions like jumps, calls or returns. They occur as reactions to changes in the program's state. 
- Systems do also react to changes in system state that are not related to internal program variables or the execution of a program. Examples of such reactions include packets arriving at a network adapter and getting stored in memory, or requesting data from disk and sleeping until such data arrived or parent processes being notified when their child processes have terminated.
- Modern systems make these reactions through abrupt changes to control flow called **exceptional control flow (ECF)**. ECF happens at all levels:
	- At the hardware level, "events detected by the hardware trigger abrupt control transfers to exception handlers."
	- At the OS level, the kernel transfers control from once user process to another through context switches.
	- "At the application level, a process can send a signal to another process that abruptly transfers control to a signal handler in the recipient".
	- "An individual program can react to errors by sidestepping the usual stack discipline and making nonlocal jumps to arbitrary locations in other functions." *(:confused: A lot of big words).*
- Reasons why ECF is important include:
	- Understanding ECF is an important prerequisite to understanding important systems and OS concepts. ECF is  fundamental building block in IO, processes and virtual memory.
	- Understanding ECF is important to understand how applications interact with the OS. Applications use **traps** (also called **system calls**) to request services from the OS such as writing/retrieving data from disk and network, creating and terminating processes, etc. Such system calls are based on ECF.
	- Understanding ECF allows you to go beyond the basics to create interesting applications that fully exploit the services provided by the OS. Example applications include shell programs and web servers.
	- Understanding ECF allows you understand concurrency.
	- Understanding ECF allows you to have a better understanding of how exceptions in software and higher level languages work. 
- The previous chapters were about application interaction with the hardware, but from now on we will focus more on application interaction with the OS. This chapter will start discussing exceptions which are an application-hardware form of ECF. We then move on to system calls which give apps access to the the OS. We then describe processes and signals, and then wrap up with nonlocal jumps which are app-level exceptions.

## Exceptions:
## Processes:
## System Call Error Handling:
## Process Control:
## Signals:
## Nonlocal Jumps:
## Tools for Manipulating Processes:
