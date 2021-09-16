# Processes
## Table of Contents:
## Intro:
- How do we get the illusion of having so many CPUs in a computer? This is done mainly through what's often called one of the greatest ideas (abstractions) in all of computer science, namely **processes**. A process is the live running version of a program.
- The OS "wraps" programs in processes and manages these processes making running multiple (many many) programs at the same time an easy task. You don't have to worry about the availability of the CPU or any of that nonsense.
- The CPU is virtualized through the use of processes. The CPU would run a process for some time, stops running it and jumps to another process, then jumps back to the current process and then another continuously and tirelessly. This jumping around is called **time sharing**. Time sharing is one of those nerdy words OS designers like to throw around. 
- CPU virtualization can be achieved through the use of:
	- Low level **mechanisms** such as the so-called **context switching** which refers to the continuous switching between different processes.
	- High-level intelligence referred to usually as **policies** is also used to guide CPU and other kinds of virtualization. For example, **scheduling polices** based past behavior of programs, their performance and other metrics, help the OS decide scheduling priorities for processes, what process to run next and how much time is allocated to a process.

## A Process:
- A process can be thought of in terms of the system components it affects/ accesses during its lifetime which are collectively called its **machine state**. The machine state of a process includes the following:
	- *Memory*, which contains the program's instructions and the data the process reads/writes. This memory is part of the process and is called its **address space**. 
	- *Registers* are also a crucial part of a process including the **program counter (PC)**, **stack pointer**, and **frame pointer** which manage various aspects of the program such as its return address, etc.

## Process API:
- This is not a real process API but generic features/aspects a typical process might or should have:
	- **Create**: An OS needs to offer a way for the user or other programs to start a process. When you double-click a program you're instructing the OS to start a new process to run that program.
	- **Destroy**: A way to kill a process. Some processes might terminate on their own upon the completion of their tasks.
	- **Wait**: ??! Waiting for a process to stop running??!! But why? :confused:.
	- **Control**: A process can be suspended and then resumed.
	- **Status**: The API might need to tell us if the process is running, suspended, etc. General information about the process's current status.

## Creating a Process:
- Turning a program into a process, in other words getting the program to be running involves:
	- **Loading** an executable containing the program's code and static data (such as its initialized data) from disk to the process's address space.
	- Once the program is loaded, the OS allocates a **runtime stack** for the process which will be used for the return address, local variables, function parameters, etc. 
	- Memory is also allocated for the **heap** which is used for dynamically-allocated data for data structures like linked lists and whatnot. Memory is allocated on the heap by calling `malloc()` and freed with `free()`. The OS manages such allocation/freeing of memory.
	- Initialization tasks related mainly to IO devices. Each Unix process, for example, has three open file descriptors: standard input, standard output, and standard error.
- After all the steps listed above take place, the OS can jump to the program's entry point `main()` and transfer execution to the process/program.

## Process States:
- A running process can be in one of three states:
	- **Running**.
	- **Ready**: The process is ready and can be run if the OS chooses to run it.
	- **Blocked**: The process cannot run currently, because it might be waiting for another operation to finish, example: waiting for an I/O operation to finish or return something.
- These states have to do directly with OS **scheduling**. A running program can be either **scheduled**, meaning it is running currently or **de-scheduled**, meaning it is ready when the scheduler decides to give it a slice of time to run. When a process is blocked, it might also be de-scheduled while in this state of blockage.
- There can be other states we didn't mention earlier such as:
	- *Initial* state for when the process has just started.
	- *Final* or *zombie* state before the process is torn down. This for example, allows a parent process to examine the return value of a process for whatever reason.

## Data Structures:
- A process keeps several data structures to track different information about processes, such as a list of running processes, ready processes, and blocked ones. This might be called a **process list**.
- Another important piece of information the OS holds is so-called **register contexts** for de-scheduled processes. They contain snapshots of the register state for processes so when the process is scheduled again, their register state is restored. This is used for **context switching** which we will see later.

	