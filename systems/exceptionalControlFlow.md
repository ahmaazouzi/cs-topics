# Exceptional Control Flow:

## Introduction:
- From the time a computer is powered on until it is turned off, the program counter takes a sequence of values where each value is the address of an instruction. Each transition from one PC value to the next is called a **control transfer**. A sequence of control transfers is called **control flow**. A simple control flow involves instructions that are stored in adjacent memory locations. This simple flow is interrupted from time to time leading to situations where the instructions being executed are not in adjacent memory locations. Such situations involve instructions like jumps, calls or returns. They occur as reactions to changes in the program's state. 
- Systems do also react to changes in system state that are not related to internal program variables or the execution of a program. Examples of such reactions include packets arriving at a network adapter and getting stored in memory, or requesting data from disk and sleeping until such data arrived or parent processes being notified when their child processes have terminated.
- Modern systems make these reactions through abrupt changes to control flow called **exceptional control flow (ECF)**. ECF happens at all levels:
	- At the hardware level, "events detected by the hardware trigger abrupt control transfers to exception handlers."
	- At the OS level, the kernel transfers control from once user process to another through context switches.
	- "At the application level, a process can send a signal to another process that abruptly transfers control to a signal handler in the recipient".
	- "An individual program can react to errors by sidestepping the usual stack discipline and making **nonlocal jumps** to arbitrary locations in other functions." *(:confused: A lot of big words).*
- Reasons why ECF is important include:
	- Understanding ECF is an important prerequisite to understanding important systems and OS concepts. ECF is  fundamental building block in IO, processes and virtual memory.
	- Understanding ECF is important to understand how applications interact with the OS. Applications use **traps** (also called **system calls**) to request services from the OS such as writing/retrieving data from disk and network, creating and terminating processes, etc. Such system calls are based on ECF.
	- Understanding ECF allows you to go beyond the basics to create interesting applications that fully exploit the services provided by the OS. Example applications include shell programs and web servers.
	- Understanding ECF allows you understand concurrency.
	- Understanding ECF allows you to have a better understanding of how exceptions in software and higher level languages work. 
- The previous chapters were about application interaction with the hardware, but from now on we will focus more on application interaction with the OS. This chapter will start discussing exceptions which are an application-hardware form of ECF. We then move on to system calls which give apps access to the the OS. We then describe processes and signals, and then wrap up with nonlocal jumps which are app-level exceptions.

## Exceptions:
- An **exception** is an *abrupt* change in control flow in response to a change in the process's state. It is a form of ECF that is implemented partly by the hardware (HW) and partly by the OS. Exception implementations differ from system to system but the general principles of exceptions and exception handling the same. *Warning: exceptions can be a confusing!!!*
- The following image illustrates how an exception works:
![Exception](img/exception.png)
- The processor in the image is executing the current instruction ***I<sub>curr</sub>*** when a change in the processor's *state* occurs. e processor's state is encoded in various bits and signals. This change in state is called an **event**. The event might be directly related to the current instructions; for example, the instruction might incur an arithmetic overflow or tries to divide by zero. The event might also be unrelated to the current instruction such as an IO request or a system timer going off!! :confused: *What!!*
- When the processors detects an event, it makes an *indirect procedure call (the exception)* through a jump table called the **exception table**, to an OS subroutine called the **exception handler** which is designed to handle this kind of event.
- When the exception handler finishes processing, one of 3 things can happen depending on the type of event that caused the exception:
	1. The exception returns control to the current instruction ***I<sub>curr</sub>*** that was executing before the exception occurred.
	2. The exception handler returns control to ***I<sub>next</sub>***, the instruction that was going to execute after ***I<sub>curr</sub>*** if the exception hadn't occurred.
	3. The handler aborts the interrupted program.

### Exception Handling:
- Exception handling can be confusing because it requires a close cooperation between the hardware and the OS and it's not always easy to tell which part is doing what. 
- Each exception is assigned a unique nonnegative integer called an **exception number**. Some exception numbers are assigned by the processor designers such as "divide by zero, page faults, memory access violations, break- points, and arithmetic overflows." Other exception numbers are designed by OS kernel designers such system calls and IO signals. 
- When a system boots, the OS allocates and initializes a jump table called **exception table**. Each entry ***k*** in the exception table contains the address of the handler of exception ***k***. The following image shows the structure and functionality of an exception table:
![Exception table](img/exceptionTable.png)
- At run time (when the system is executing a program), the processor detects an event has occurred and determines the corresponding exception number ***k***. The processor then triggers the exception by making an indirect procedure call, through entry ***k*** from the exception table, to the corresponding handler. The following image shows how the exception table is used to get the memory address of the appropriate exception handler. The exception number ***k*** is an index into the exception table whose starting address (address of what??!!! table or the first address in the table) is in a special CPU address called the **exception table base register**
![Generating exception handler address](img/excepHandAddr.png)
- An exception is similar to a procedure call but with a few differences:
	- The processor pushes a return address on the stack before starting the handler just as in a procedure call, but the return address is either the current instruction or the next instruction depending on the type of the exception. 
	- The processor pushes additional processor stack on the stack that is necessary to restart the interrupted program when the handler returns. For example, IA32 pushes the EFLAGS register which contains current condition codes and other things onto the stack. 
	- If control is being transfered from a user program to the kernel, all of the pushed items are pushed onto the kernel's stack instead of the user's stack. 
	- Exception handlers run in **kernel mode**, meaning they have complete access to all system resources. 
- Once the exception is triggered, the act of exception handling is done in the software by the exception handler. When the handler finishes processing the event, it optionally returns to the interrupted program by executing a special *return from interrupt* instruction. This instruction pops state back onto the processor and data registers and restores the state to **user mode** if the exception has interrupted a user program and yields control back to the interrupted program.

### Classes of Exceptions:
- There are 4 classes of exceptions: **interrupts**, **traps**, **faults**, and **aborts**. The following table summarizes the characteristics of these exceptions:

| Class | Clause | Async/Sync | Return behavior |
| --- | --- | --- | --- |
| Interrupt | Signal from I/O device | Async | Always returns to next instruction |
| Trap | Intentional exception | Sync | Always returns to next instruction |
| Fault | Potentially recoverable error | Sync | Might return to current instruction |
| Abort | Nonrecoverable error | Sync | Never returns |

#### Interrupts:
- **Interrupts** occur **asynchronously** as result of signal from IO devices external to the processor. They are asynchronous because they are not caused by a program instruction but are caused by external signal. Exception handlers for interrupts are called **interrupt handlers**.
- An interrupt occurs as follows:
	- An IO device such as a network adapter or disk controller triggers an interrupt by "signaling a pin on the processor chip" :confused: on the processor and putting into the system bus the exception number identifying the the device that caused the interrupt.
	- The current instruction finishes executing. 
	- The processor notices the "interrupt pin has gone high," gets the exception number from the system bus and transfers control to the interrupt handler.
	- The interrupt handler does it what does and then returns to the next instruction in the running program. The program resumes executing as if the interrupt never happened. 
- The other 3 classes of exceptions are **synchronous** meaning they occur as a result of executing the current instruction. Such an instruction is called a **faulting instruction**. 

#### Traps and System Calls:
- **Traps** are **Intentional** exceptions that occur as a result of an executing instruction and they return control to the next instruction. Traps role in life is to provide a procedure-like interface between user programs and the kernel called **system calls**. 
- User programs sometimes need to request services from the kernel such reading files (`read`), creating a new process (`fork`), loading a new program (`execve`) or terminating the current process(`exit`). Processors provide access to such services through the special **`sycall` *n*** instruction which the user programs can execute when they want to request service ***n***. Executing `sycall` causes a trap to a trap handler which decodes the argument and calls the right kernel function.
- From the programmer's perspective, a system call is identical to a regular function call, but their implementations are different. Regular functions run in ***user mode*** which restricts the type of instructions they can use and access the same stack as other regular functions. System calls run the other hand run in kernel mode.

#### Faults:
- **Faults** occur because of errors that a fault handler might be able to correct. If the fault handler is able to correct the error, it returns control to the faulting instruction and re-executes it. Otherwise, the handler returns control to an **`abort`** routine in the kernel which terminates the program that caused the fault. 
- A *page fault* exception is a good example of a fault. It occurs when a virtual memory address whose physical counterpart is not in memory and must be retrieved from disk. The fault handler loads the page from disk and returns control to the faulting instruction. When the instruction re-executes, it can access the page and run normally to completion.

#### Aborts:
- **Aborts** occur because of unrecoverable fatal errors such as hardware errors where DRAM	or SRAM are corrupted. Abort handlers don't return control to the application program, but return control to an `abort` routine that terminates the application program.

### Exceptions in Linux/IA32:
- There are 256 exception types in both x86-64 and IA32. Numbers in the range 0-31 correspond to exceptions defined by the Intel processor designers, while 32-265 correspond to exceptions defined by the Linux OS.

#### Faults and Aborts in Linux/IA32:
- **Divide error** (exception 0) occurs when attempting to divide by zero, or when the result of a divide is too big for the destination operand. Unix aborts programs causing divide errors while Linux reports them as "Floating exceptions."
- **General protection fault** (exception 13) is common and occurs for many reasons but it usually occurs when trying to reference a undefined virtual memory area or write to a read-only area. Linux doesn't try to recover from such errors and reports them as *segmentation fault*.
- **Page fault** (exception 14). We've described this earlier. 
- **Machine check** (exception 18) occurs when a fatal hardware error is detected while executing the faulting instruction. Machine check handlers never return control to the application program.

#### Linux/IA32 System Calls:
- Linux has hundreds of system calls doing all kinds of things from process management to IO and file access, etc. 
- C programs can invoke any system call directly through the **`int` *n*** function (This is **`syscall`** in x86-64), but this is rarely used because the C standard library provides function wrappers around system calls. "The wrapper functions package up the arguments, trap to the kernel with the appropriate system call number, and then pass the return status of the system call back to the calling program." From now on, we will call system calls and their wrapper functions *system-level functions*.
- By studying how system calls work inn Linux, we might have a better understanding of the inner workings of the system. Arguments are all passed onto registers rather than the stack. "The stack pointer %esp cannot be used because it is overwritten by the kernel when it enters kernel mode." Consider the following program that prints something to standard output, but using the system-level functions `write` instead of the familiar wrapper `println`:
```c
int main(){
    write(1, "Hello, world!\n", 13); // For Some reason new line is not printed
    exit(0);
}
```
```
.section .data
string:
    .ascii "hello, world\n"
string_end:
    .equ len, string_end - string

.section .text
.globl main
main:
    # First, call write(1, "hello, world\n", 13)
    movl     $4, %eax        # System call number 4   
    movl     $1, %ebx        # stdout has descriptor 1
    movl     $string, %ecx   # Hello world string
    movl     $len, %edx      # String length
    int      $0x80           # System call code

    # Next, call exit(0)
    movl     $1, %eax        # System call number 0  
    movl     $0, %ebx        # Argument is 0     
    int      $0x80           # System call code       
```
- The system call `write` has 3 arguments:
	- The first argument `1` sends output to `stdout` (standard output).
	- The second argument is the sequence of bytes to write.
	- The third argument is the number of bytes to write. 
- In the compiled code we see how the system call numbers `$4` for the `write` system call and `$0` for the `exit` system call are pushed into register `%eax`. The system calls themselves are done with `int $0x80`.

## Processes:
- Exceptions are the building blocks allowing operating systems to have **processes**, "one of the most profound and successful ideas in computer science." *I've heard this somewhere before 🤔*.
- Processes are the one abstraction that allows a program to appear as if it is the only one running in a system and having exclusive use of the processor and memory. 
- A **process** is an instance of a program in execution. Each program in the system runs in the context of some process. The context is made of the state that the program needs to run correctly. This state includes the program's data and code stored in memory, its stack, the contents of its general-purpose registers, its program counter, environment variables and open file descriptors. 
- When a user runs a program by typing the name of an executable on the shell, the shell creates a new process and runs the executable file in the context of this process. Any application program can create a process and either run its own code or the code of another application in this newly created process. 
- The implementation of process won't be discussed here! It is the subject of an OS book. This section will be about two abstractions the process offer to applications:
	- An independent *logical control flow* that gives the illusion that the program has exclusive use of the processor.
	- A private address space giving the illusion that the program has exclusive use of memory. 

### Logical Control Flow:
- If you single step the execution of a program with a debugger, you'll see a series of PC values corresponding to instructions contained in the program's executable object file. This sequence of PC values is called **logical control flow** or **logical flow**. 
- The following image shows a system running three processes. The single physical control flow is divided into three logical flows, one for each process. Each one of the vertical lines in the image represents a portion of the logical flow of a process. The three processes are interleaved. Each one runs for some times, then processing jumps another portion of another process, then jumps back, etc. 
![Logical control flow](img/lcf.png)
- The 3 processes in the image take turns in processing. At any point in time a process is either running or is **preempted** (temporarily suspended). A program might seem to have exclusive use of the processor. "The only evidence to the contrary is that if we were to precisely measure the elapsed time of each instruction, we would notice that the CPU appears to periodically stall between the execution of some of the instructions in our program." However, when the processor resumes running a process, it does so without any changes to the memory locations or registers
- A logical flow can be anything from an exception handler, process, signal handler,thread or Java process.  

### Concurrent Control Flow:
- A logical flow that overlaps in time with another logical flow is a **concurrent flow** and the two flows **run concurrently**. 
- The phenomenon of multiple flows running concurrently is called **concurrency** or **multitasking**. Each time period that a process executes a portion of its logical flow is called a **time slice**. Multitasking is also called **time-slicing**.
- Concurrency is independent of the number of processor cores in a system. If two flows overlap in time, they are concurrent regardless of whether they are running in the same processor or multiple processor cores. Concurrent programs that run in different processor cores or different computers are better called **parallel flows** (or they *run in parallel*).

### Private Address Space:
- A processes gives the illusion that a program has exclusive use of the system's address space. In a system with ***n***-bit addresses, the **address space** is set of ***2<sup>n</sup>*** possible addresses. Each process provides a program with its own **private address space**. Other processes cannot read or write bytes into the memory associated with this process. 
- The memory associated with each private address space differs from one process to another but it's generally organized according to the same principles. The following image shows the general organization of a private address space of a process in Linux with x86:
![Process address space](img/processAddressSpace.png)
- The bottom portion of the address space is reserved for the user program, including its text, data, heap and stack portions. "Code segments begin at address `0x08048000` for 32-bit processes, and at address `0x00400000` for 64-bit processes." The top segment of the address space is reserved for the kernel. It includes the code, data and stack that the kernel uses when it executes instructions on behalf of the process (during a system call for example).

### User and Kernel Mode:
- For the OS to provide a correct process abstraction, the processor provides a way to restrict the instructions an application can run and the portions of the address space it can use. 
- The process does this with a **mode bit** stored in a control register. This mode bit determines the privileges a process currently has. When the mode bit is set, the processor is running in **kernel mode** (also called **supervisor mode**). A process in kernel mode can execute any instruction and access any memory location in the system. *Wow, dangerous!!!*
- When the the mode nit is not set, the process is running in **user mode**, meaning it is not allowed to execute **privileged instructions** which do things like halting the processor, changing the mode bit or initiates an IO operation. It also cannot reference data or code in the kernel area of the address space. An attempt to directly access code/data in the kernel area results in a protection fault error. To access stuff in the kernel area, the user program does it through a system call. 
- A process running an application code is usually running in user mode. The only way for a process to change from user to kernel mode is through an exception such as a fault, an interrupt or a trap. When an exception occurs and control is passed from the application program to the exception handler, mode is changed from user mode to kernel mode. The exception handler runs in kernel mode. When the exception is handler and control is passed back to the program, the mode is changed back to user mode.  
- Linux has the **`/proc` filesystem**  which allows user mode processes to access contents of kernel data structures. It exports the contents of the kernel data structures as a hierarchy of text files which can be read by user programs. `/proc/cpuinfo` for example provides information about the CPU. A similar thing is **`sys` filesystem** provides low-level information about the system buses and devices. 

### Context Switches:
- The OS implements multitasking using the higher level type of control flow called a **context switch**. A context switch itself is built on top of lower level control flow exceptions such as traps.
- The context of each process is maintained by the kernel. The context is "the state that the kernel needs to restart a preempted process." It consists of the values of registers, the user's stack, the program counter, the kernel's stack and data structures such as:
	- The *page table* which characterizes the address space.
	- The *process table* which contains information about the process.
	- The *file table* which contains information about files the process has opened.
- At some point while a process is running, the kernel decides to preempt the currently running process and restart another preempted process. This decision is known as **scheduling** and is done by a part of the kernel called the scheduler. When the kernel selects another process to run it, we say it has *scheduled* it. When the kernel schedules a process it preempts the currently running process and moves control to the new process through the use of a context switch which:
	- Saves the context of the current of process.
	- Restores the context of a previously preempted process.
	- Transfers control to the newly restored process.
- A context switch  can happen even while the kernel is executing a system call requested by current process. If the system call blocks for any reason (let's say a system call handling an IO operation) the current process is preempted and the context switch will still occur. 
- I don't know what a *timer interrupt* is, but a context switch can occur as a result of a timer interrupt which would go off every few milliseconds at which point might decide that the current process has run enough time and it's time to switch context. 
- The following image shows an example of a context switch. Process A is running in user mode until it traps to the kernel mode by using the `read` system call. The trap handler requests  data from the disk controller and arranges for the disk to interrupt the processor when the data from the disk is in memory. Fetching data from the disk takes a long time, so instead of waiting for that data the kernel performs a context switch from process A to process B. Notice that during each context switch both process A and process B are executing in kernel mode:
![Context switching](img/contextSwitching.png)
- Hardware cache in general doesn't usually play well with exception control flow and context switching. A context might *pollute cache*, meaning it makes it go cold for the preempted process and when a context is witched for a process, the new process might have a cold cache. 

## System Call Error Handling:
- When a system-level function encounters an error, they return an ***-1*** and update the global integer variable **`errno`** to show what went wrong. It is advisable to check for errors. The following code checks for errors when the Linux function **`fork`** is called:
```c
if ((pid = fork) < 0){
    fprintf(stderr, "fork error: %s\n", strerror(errno));
    exit(0);
}
```
- The **`strerror`** function returns a text string describing the error associated with the given `errno`. This can be repackaged into the following error reporting function:
```c
void unixError(char *msg){
    fprintf(stderr, "%s: %s\n", msg, strerror(errno));
    exit(0);
}
```
- The original code can then be simplified to:
```c
if ((pid = fork()) < 0)
    unixError("fork error");
```
- The code can be simplified further and made more robust with the use of error-handling wrappers. For each function `foo`, you define a function wrapper `Foo` (capitalized) wich runs the original function, checks for errors and terminates with a descriptive error message if an error occurs as the following example shows:
```c
pid_t Fork(void){
    pid_t pid;

    if ((pid = fork()) < 0)
        unixError("Fork error");
    return pid;
}
```
- A robust call to `fork` with error checking becomes:
```c
pid = Fork();
```

## Process Control:
- Unix systems provide a variety of system calls for manipulating processes from C programs. We will go over some of the more important of these functions in this section.

### Obtaining Process IDs:
- Each process has a unique nonzero **process ID (PID)**. The **`getpid`** returns the PID of the calling process.**`getppid`** returns the parent of the calling process. Both functions return an integer value of type `pid_t` which is defined as an int in Linux systems in the header file `types.h`:
```c
#include <sys/types.h>
#include <unistd.h>

pid_t getpid(void);
pid_t getppid(void);
```

### Creating and Terminating Processes:
- For the programmer, a process can be in one of 3 states:
	1. *Running*. It's either executing or waiting to be scheduled.
	2. *Stopped*. The process is *suspended* and will not be scheduled. It's stopped as a result of a "SIGSTOP, SIGTSTP, SIGTTIN, or SIGTTOU signal, and it remains stopped until it receives a SIGCONT signal, at which point it can begin running again." *Signals* are a type of interrupt we will see later.
	3. *Terminated*. The process stops permanently. A processes becomes terminated as a result of:
		- Receiving a termination signal.
		- Returning from the main routine.
		- Calling the `exit` function:
```c
#include <stdlib.h> 
void exit(int status);
```
- A **parent process** can create a new "running" **child process** by calling the function **`fork`**:
```c
#include <sys/types.h>
#include <unistd.h>

pid_t fork();
```
- The child process is almost identical to its parent but with a few differences. Similarities include:
	- The child has an identical but separate copy of the parent's user-level virtual address space, including text, data, heap, user stack, etc. 
	- Identical copies of the parent's open file descriptors, meaning the child can read and write files that were open when the parent called `fork`.
- The main difference between the parent and the child is that they have different PIDs.
- One confusing aspect of `fork` is that it i called once but returns twice, once in the parent and once in the child. In the child, `fork` returns a 0 and in the parent it returns the child's PID. Since the PID of the child is always a nonzero, `fork`'s return value provides a definitive indicator whether the program is running in the parent or child process. 
- The following code example shows a parent process creating a child process with `fork`. `x` is one when `fork` returns, but we increment `x` inside the child and decrements it inside the parent. *This is a nice way of showing how `fork` works:*
```c
int main(){
    pid_t pid;
    int x = 1;

    pid = fork(); 
    if (pid == 0){
        printf("child: x=%d\n", ++x);
        exit(0);
    }

    printf("parent: x=%d\n", --x);
} 


/*
parent: x=0
child: x=2
*/
```
- A few things one notices about this example:
	- *Call once, return twice:* Because fork two processes are running at once, we have two print statements running together. This is straightforward because `fork` was called once, but it can be confusing in programs calling `fork` multiple times.
	- *Concurrent execution:* The parent and child are separate processes that run concurrently. The kernel interleave them in a seemingly random manner. There is no guarantee that the parent `printf` runs first, because of how the kernel does the interleaving in an unpredictable manner. 
	- *Duplicate but separate address spaces:* The two address spaces for the two processes are identical copies of each other. `x` is equal to 1 in both parent and child before the call to `printf`, but the printed values are different after the incrementing and decrement in each of the two processes. They are identical but still separate copies of each other.  
	- *Shared files:* Both parent and child write their output to `stdout`, because the child inherits all parent open files. 
- Using multiple `fork` functions can be confusing, so it's advisable to chart a *process graph* when using this function. Take the following code as an example:
```c
#include <stdio.h>

int main(){
	fork();
	fork();
	fork();
    printf("fafa\n");
    exit(0);
}
```
- The process graph for such a program is as follows:
[Process graph](img/processGraph.png)
- Each horizontal arrow in the graph corresponds to a process that runs from left to right (*Whatever this means!!*), and each vertical arrow corresponds to the execution of a `fork` function. It sounds like if we we call `fork` ***n*** times, then, there will be ***2<sup>n</sup>*** calls to `printf`.

### Reaping Child Processes:
- When a child process is terminated, the kernel doesn't remove it immediately and it is still kept around in a terminated state until it is **reaped** by its parent. When the parent reaps the child process, its exit status is passed to the parent by the kernel is then discarded (it exists no more). Terminated processes that have not been reaped yet are known as *zombies*. 
- If the parent process dies without having reaped its children, the kernel makes the **`init`** process reap them. The `init` process is a special process with PID 1 that gets created during the initialization of the system and one of its jobs is reaping orphaned zombies. Long running processes such as shells must terminate their zombie children because even if a zombie is terminated, it still consumes memory resources.
- A process waits for its children to terminate by calling the function **`waitpid`**. 
```c
#include <sys/types.h> 
#include <sys/wait.h>


pid_t waitpid(pid_t pid, int *status, int options); 
// Returns: PID of child if OK, 0 (if WNOHANG) or −1 on error
```
- By Default (when `options` is 0), `waitpid` suspends the parent until a child (*or all children*) in its **wait set** terminate. If a process in the wait set has already terminated at the time of the call, `waitpid` returns immediately. Anyways, `waitpid` returns the PID of the terminated child and the child process is removed from the system.

#### Determining the Members of the Wait Set:
- *Things are kinda starting to get a little sloppy! What the hell is a wait set?*
- Ad verbatim "the members of the wait set are determined by the `pid` argument":
	- if `pid > 0`, the process is a single child whose process ID is equal to `pid`.
	- if `pid = -1`, then the wait set consists of all the parent's child processes. 

#### Modifying the Default Behavior:
- The default behavior of `waitpid` can be modified by setting `options` to combinations of the *WNOHANG* and *WUNTRACED* constants:
	- **`WNOHANG`**: Returns immediately with a value of 0 if no child processes has terminated. This is as opposed to the default behavior where the parent is suspended until the child terminates which is kinda wasteful. 
	- **`WUNTRACED`**: Suspends the calling process until a process in the wait set is either terminated or stopped, and returns the process PID (default behavior only returns for terminated processes). This allows you to wait for both terminated and stopped processes.
	- **`WNOHANG | WUNTRACED`**: Returns immediately with a 0 if no processes in the wait set is terminated or stopped, or with a terminated or stopped process PID. 

#### Checking the Exit Status of a Reaped Child:
- If the `status` argument is not a NULL, `waitpid` encodes status information about the process that caused the return in the `status` argument. The `wait.h` has macros for interpreting the `status` argument:
	- **`WIFEXITED(status)`**. Returns true if process terminates normally via exit or eturn.
	- **`WEXITSTATUS(status)`**. Returns the exit status of a normally terminated process (Only defined if `WIFEXITED` returned true).
	- **`WIFSIGNALED(status)`**. Returns true if the process was terminated because of a signal that was not caught (we'll see signals later).
	- **`WTERMSIG(status)`**. Returns the number of the signal that caused a process to terminate (defined only if `WIFSIGNALED(status)` returns true).
	- **`WIFSTOPPED(status)`**. Returns true if the process that caused the return is stopped.
	- **`WSTOPSIG(status)`**. Returns the number of signal that caused a process to stop (defined only if `WIFSTOPPED(status)` returns true).

#### Error Conditions:
- If the calling process has no child processes, `waitpid` returns -1 and sets `errno` to `ECHILD`. If `waitpid` was interrupted by a signal, it returns -1 and sets `errno` to `EINTR`.

#### The `wait` Function:
- **`wait`** is a simpler version of `waitpid`, so the call to ` wait(&status)` is equivalent to `waitpid(-1, &status, 0)`:
```c
#include <sys/types.h> 
#include <sys/wait.h>

pid_t wait(int *status); // Returns: PID of child if OK or −1 on error
```

#### Examples of Using `waitpid`:
- The following example illustrates the use and some of the quirky aspects of the complicated `waitpid` function:
```c
#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <errno.h>

#define N 2

int main(){
    int status, i;
    pid_t pid;

    for (i = 0; i < N; i++)
        if ((pid = fork()) == 0)
            exit(100 + i);

    while ((pid = waitpid(-1, &status, 0)) > 0){
        if (WIFEXITED(status))
            printf("child %d terminated normally with exit status=%d\n",
               pid, WEXITSTATUS(status));

        else
            printf("child %d terminated abnormally\n", pid);
    }

    if (errno != ECHILD)
        unix_error("waitpid error");

    exit(0);
}
```

### Putting Processes to Sleep:
### Loading and Running Programs:
### Using `fork` and `execve` to Run Programs:

  
## Signals:
## Nonlocal Jumps:
## Tools for Manipulating Processes:





















