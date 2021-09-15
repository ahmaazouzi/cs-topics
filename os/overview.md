# Introduction to Operating Systems:
## Table of Contents:
* [Table of Contents](#table-of-contents)
* [An Operating System Is](#an-operating-system-is)
* [Virtualizing the CPU](#virtualizing-the-cpu)
* [Virtualizing Memory](#virtualizing-memory)
* [Concurrency](#concurrency)
* [Persistence](#persistence)

## An Operating System Is:
- The **Von Neumann** model of computing dictates that a processor **fetches**, **decodes**, and then **executes** instructions. So when you run a program in a computer, this is what happens in fact over and over: a bunch of instructions are fetched from memory, decoded and then executed. Much of this magic happens behind the scenes without you noticing a thing. It is thanks to **operating systems** that such voodoo happens seamlessly. 
- An operating system:
	- Makes it **easy to use programs**. 
	- Allows multiple programs to run simultaneously without clashes. They share the same memory and their data doesn't get scrambled together.
	- Facilitates communication between the computer and devices attached to it.
	- Gives the user an easy interface for interacting with the device's hardware.
- An operating system can alternatively be thought of as a **resource manager**, since it manages how resources such as CPU time, memory and disk space are shared between different running programs.
- An OS can be thought of as doing three major tasks, **virtualization**, **concurrency**, and **persistence**. The rest of this book will explain what these words mean.

## Virtualizing the CPU:
- A typical computer has one or a few CPUs, but it can run a large number of programs simultaneously as if there are many CPUs. This is what we mean by virtualizing the CPU, we give the user the illusion that the computer has many CPUs running at the same time. Our job is understand how the OS achieves this illusion.

## Virtualizing Memory:
- Two programs running simultaneously, have independent address spaces. Two identical memory addresses for two programs would contain different data. How is it possible? How does each running program seem to have the whole memory space to itself? This is again done with memory virtualization where each program has a virtual memory space to itself that is mapped to actual physical memory. This is another way OSs make running programs easy!

## Concurrency:
- Different processes have their own memory spaces each that are not shared with other processes. There is also the concept of **thread**, which can be thought of as a *process lite*. Threads are different lines of execution but they operate on a shared memory. Sharing memory between threads in multi-threaded programs causes a lot of headaches because of the very unpredictable results such programs can give. We will learn in the concurrency section the causes of this problem and how to write correct programs involving concurrency.

## Persistence:
- Persistence is all about storing data safely using so-called **file systems**. A lot of hard work by the OS goes into this!
