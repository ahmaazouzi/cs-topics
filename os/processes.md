# Processes
## Table of Contents:
* [Processes](#processes)
	+ [Intro](#intro)
	+ [A Process](#a-process)
	+ [Process API](#process-api)
	+ [Creating a Process](#creating-a-process)
	+ [Process States](#process-states)
	+ [Data Structures](#data-structures)
* [Unix Process API](#unix-process-api)
	+ [`fork()`](#fork())
	+ [`wait()`](#wait())
	+ [`exec()`](#exec())
	+ [Why an API?](#why-an-api)

## Processes:
### Intro:
- How do we get the illusion of having so many CPUs in a computer? This is done mainly through what's often called one of the greatest ideas (abstractions) in all of computer science, namely **processes**. A process is the live running version of a program.
- The OS "wraps" programs in processes and manages these processes making running multiple (many many) programs at the same time an easy task. You don't have to worry about the availability of the CPU or any of that nonsense.
- The CPU is virtualized through the use of processes. The CPU would run a process for some time, stops running it and jumps to another process, then jumps back to the current process and then another continuously and tirelessly. This jumping around is called **time sharing**. Time sharing is one of those nerdy words OS designers like to throw around. 
- CPU virtualization can be achieved through the use of:
	- Low level **mechanisms** such as the so-called **context switching** which refers to the continuous switching between different processes.
	- High-level intelligence referred to usually as **policies** is also used to guide CPU and other kinds of virtualization. For example, **scheduling polices** based past behavior of programs, their performance and other metrics, help the OS decide scheduling priorities for processes, what process to run next and how much time is allocated to a process.

### A Process:
- A process can be thought of in terms of the system components it affects/ accesses during its lifetime which are collectively called its **machine state**. The machine state of a process includes the following:
	- *Memory*, which contains the program's instructions and the data the process reads/writes. This memory is part of the process and is called its **address space**. 
	- *Registers* are also a crucial part of a process including the **program counter (PC)**, **stack pointer**, and **frame pointer** which manage various aspects of the program such as its return address, etc.

### Process API:
- This is not a real process API but generic features/aspects a typical process might or should have:
	- **Create**: An OS needs to offer a way for the user or other programs to start a process. When you double-click a program you're instructing the OS to start a new process to run that program.
	- **Destroy**: A way to kill a process. Some processes might terminate on their own upon the completion of their tasks.
	- **Wait**: ??! Waiting for a process to stop running??!! But why? :confused:.
	- **Control**: A process can be suspended and then resumed.
	- **Status**: The API might need to tell us if the process is running, suspended, etc. General information about the process's current status.

### Creating a Process:
- Turning a program into a process, in other words getting the program to be running involves:
	- **Loading** an executable containing the program's code and static data (such as its initialized data) from disk to the process's address space.
	- Once the program is loaded, the OS allocates a **runtime stack** for the process which will be used for the return address, local variables, function parameters, etc. 
	- Memory is also allocated for the **heap** which is used for dynamically-allocated data for data structures like linked lists and whatnot. Memory is allocated on the heap by calling `malloc()` and freed with `free()`. The OS manages such allocation/freeing of memory.
	- Initialization tasks related mainly to IO devices. Each Unix process, for example, has three open file descriptors: standard input, standard output, and standard error.
- After all the steps listed above take place, the OS can jump to the program's entry point `main()` and transfer execution to the process/program.

### Process States:
- A running process can be in one of three states:
	- **Running**.
	- **Ready**: The process is ready and can be run if the OS chooses to run it.
	- **Blocked**: The process cannot run currently, because it might be waiting for another operation to finish, example: waiting for an I/O operation to finish or return something.
- These states have to do directly with OS **scheduling**. A running program can be either **scheduled**, meaning it is running currently or **de-scheduled**, meaning it is ready when the scheduler decides to give it a slice of time to run. When a process is blocked, it might also be de-scheduled while in this state of blockage.
- There can be other states we didn't mention earlier such as:
	- *Initial* state for when the process has just started.
	- *Final* or *zombie* state before the process is torn down. This for example, allows a parent process to examine the return value of a process for whatever reason.

### Data Structures:
- A process keeps several data structures to track different information about processes, such as a list of running processes, ready processes, and blocked ones. This might be called a **process list**.
- Another important piece of information the OS holds is so-called **register contexts** for de-scheduled processes. They contain snapshots of the register state for processes so when the process is scheduled again, their register state is restored. This is used for **context switching** which we will see later.

## Unix Process API:
- This will be a basic overview of process creation in the UNIX system(s). It studies three very common Unix system calls `fork()`, `exec()` which are used for creating new processes, and `wait()` which allows a process to wait for its child process(es) to finish executing.

### `fork()`:
- **`fork()`** is a weird system call and can be confusing. Check the following example. It shows a function calling `fork()`. It involves the use of `getpid()` function which allows you to get the **process identifier (PID)** for a function, which allows you identify a specific process to, for example, stop it from running or something:
```c
#include <stdio.h>
#include <unistd.h>

int main(int argc, char const *argv[]) {
	int rc = fork();
	printf("Hello, world! I am %d\n", (int) getpid());
	printf("%d\n===========\n", rc);
return 0;
}
```
- The output of the function is as follows:
```
Hello, world! I am 86057
86058
===========
Hello, world! I am 86058
0
===========
```
- Notice that the second print statement is executed twice, and it has echoed two different PIDs. The first print statement was executed only once. It looks like thee are two similar copies of the same function but not exactly. All statements starting with the call to `fork()` get also executed for the child process.
- Notice, though, that although the same instructions are executed for both the parent and child processes (starting with the call to `fork()`), the values are different as every one of the two processes has its own address spaces, registers, and whatnot. `rc` for example is used to denote the PID of the newly created child process. Notice that the `rc` value for the child process is `0` because it hasn't created any children of its own!
- ANother interesting observation, about this program is that the order of execution between child and parent processes is not deterministic. Print statements within the parent process might execute before those of the child or vice-versa. This **non-deterministic** behavior is mainly due to the CPU scheduler and how it works. The following code illustrates the use of `wait()`:

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char const *argv[]) {
	int rc = fork();
	int rc_wait = wait(NULL);

	printf("Hello, world! I am %d\n", (int) getpid());
	printf("rc: %d, rc_wait: %d\n===========\n", rc, rc_wait);
	
	return 0;
}
```
- The output is as follows (The child process with a larger PID will always finish first):
```
Hello, world! I am 86216
rc: 0, rc_wait: -1
===========
Hello, world! I am 86215
rc: 86216, rc_wait: 86216
```

### `wait()`:
- The **`wait()`** (alternatively **`waitpid()`**, which is more complete) allows you the make the order of execution between child and parent more complete. It basically allows the child to finish executing before. 

### `exec()`:
- `wait()` allows you to run copies of the same program as different processes, but you can also run different programs through creating new processes by calling **`exec()`** as in the following example:
```c
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

int main(int argc, char const *argv[]) {
	char *argz[3];
	argz[0] = strdup("vim");
	argz[1] = strdup("os.c");
	argz[2] = NULL;

	execvp(argz[0], argz);

	return 0;
}
```
- The example allows you to call shell programs form your C code. Notice that we are actually calling `execvp()`. There multiple variants of `exec()`.
- `exec()` and its variants don't create new processes, but instead it "it loads code (and static data) from that executable and overwrites its current code segment (and current static data) with it." The heap and stack of the function or program calling `exec()` get reinitialized. `exec()` basically "transforms the currently running program ... into a different running program".

### Why an API?
- The book claims that the existence of these three seemingly convoluted routines for creating new processes instead of just offering a simple way of creating a new process is to make it easier to create shell programs. I am not really convinced! ANwyays, what happens is that the shell is just another program running as a process. When you invoke a shell program such `ls` or `grep`, the shell process fork a child process of its own, calls `wait()` to let the process child finish before returning to it, then calls `exec()` which replaces its code and static data with those of the program it calls. 
- The book claims that easy redirection of input/output is one great example why these routines exist.

	