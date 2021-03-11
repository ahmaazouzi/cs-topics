# System Level IO:
## Table of Content:

## Introduction:
- **Input/Output (IO)** is the process of copying data between main memory and external devices such as networks, displays or storage devices. An **input** operation copies data from an IO device to main memory, while **output** is copying data from main memory to an IO device. 
- All languages provide out-of-the-box higher-level IO packages which include such important functions as `printf`. These higher-level functions themselves are based on the system-level *Unix IO* functions provided by the kernel. The higher-level IO packages do most of what a programmer really needs, so why study the low-level Unix IO? There are a few reasons which include:
	- **Understanding Unix IO is a prerequisite to understanding other systems concepts:** IO concepts are central to systems in general and many other aspects of systems are deeply interdependent with IO. For example, creating a new process does involve one aspect or another of IO. Processes themselves are also fundamental to understanding IO. We have touched in previous documents on a few IO topics when we discussed memory hierarchy, virtual memory and processes. This document will be a deeper treatment of IO and its particular features. 
	- **There are IO services that can only be accessed by raw Unix IO:** There are some IO services that cannot be accessed with language higher-level IO packages such as file metadata (file size or creation date). IO packages also have shortcomings that prevents them from being used safely in network programming. 
- This document will be an introduction to the general concepts of Unix IO and standard IO and how to use them effectively.

## Unix IO:
- A Unix **file** is a sequence of ***m*** bytes:
	- ***B<sub>0</sub>, B<sub>1</sub>, ..., B<sub>k</sub>, ..., B<sub></sub>***
- All IO devices such as networks, disks, displays, keyboards, etc. are modeled as files and all input and output are performed by reading from and writing to these files. This simple mapping between devices and files allows for a simple interface known as the **Unix IO** which allows for all IO operations to be done in a consistent way across different types of devices:
	- **Opening files**: An application indicates that it wants to access an IO device by asking the kernel to **open** its file. The kernel returns a small nonnegative number called a **descriptor**. The descriptor identifies the file in all the following operations. The kernel keeps track of all information about the open file, while the application keeps track of the file descriptor. When you create a process by a Unix shell, the process starts life with 3 open files: **standard input** with descriptor 0, **standard output** with descriptor 1, and **standard error** with descriptor 2. `<unistd.h>` holds constants for these descriptors: **`STDIN_ FILENO`**, **`STDOUT_ FILENO`**, and **`STDERR_FILENO`**.
	- **Changing the current file position**: The **file position** of an open file is a byte offset of a certain value from the beginning of a file. It is initially 0 and is maintained by the kernel. The application can explicitly set the file position with the **seek** operation.
	- **Reading and writing files**: A **read** operation copies ***n > 0*** bytes from a file to memory starting at the current file position, and incrementing the file position by ***n***. If the size of the file is ***m*** bytes, then when the file position is equal to or larger than ***m***, a condition called **edge-of-file (EOF)** is triggered. EOF can be detected by the application. There is no *"EOF character"* at the end of the file! *Thank you!!* The **write** operation follows similar steps with the exception that it copies bytes from memory to the file.   
	- **Closing files**: When the application finishes accessing the file, it tells the kernel to **close** the file. The kernel frees "the data structures it created when the file was opened and restor[es] the descriptor to a pool of available descriptors." If the terminal terminates normally or unexpectedly, the kernel closes all open files and frees their memory resources. 

## Opening and Closing Files:
- The **`open`** function can open an existing file or create a new file:
```c
#include <sys/types.h> 
#include <sys/stat.h> 
#include <fcntl.h>

int open(char *filename, int flags, mode_t mode); // Returns descriptor, or -1 on error
```
- The `open` function "converts" a `filename` to a file descriptor and returns the descriptor number to the calling process. The descriptor returned is the smallest descriptor that is not current opened in the process. 
- The **`flags`** argument tells us how the process wants to access the file:
	- **`O_RDONLY`**: Read only.
	- **`O_WRONLY`**: Write only.
	- **`O_RDWR`**: Write and read.
- The `flags` argument can also be *OR*'d with more instructions for writing:
	- **`O_CREAT`**: If a file with the given name doesn't exist, create a *truncated* version of it. 
	- **`O_TRUNC`**: If the file exists, truncate it (empty it).
	- **`O_APPEND`**: Before writing, set file position to the end of the file.
- The following examples opens a file with the intention of starting to write at the end of it:
```c
fd = open("somefile.txt", O_WRONLY | O_APPEND, 0);
```
- The mode arguments decides the accessing permission bits of a new file. These bits are shown in the following table:

| Mask | Description |
| --- | --- |
| `S_IRUSR` | User (owner) can read this file |
| `S_IWUSR` | User (owner) can write this file |
| `S_IXUSR` | User (owner) can execute this file |
| `S_IRGRP` | Members of the owner's group can read this file |
| `S_IWGRP` | Members of the owner's group can write this file |
| `S_IXGRP` | Members of the owner's group can execute this file |
| `S_IROTH` | Others (anyone) can read this file |
| `S_IWOTH` | Others (anyone) can write this file |
| `S_IXOTH` | Others (anyone) can execute this file |

- The context of each process has a `umask` (whatever that means) which is set by the `umask` function. When a process creates a new file with the `open` function using the `mode` argument, the access permission bits of the file are set to `mode & ~umask`
- The following macros define an example of default `mode` and `umask` you can make:
```c
#define DEF_MODE S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH|S_IWOTH
#define DEF_UMASK S_IWGRP|S_IWOTH
```
- The following code uses the definitions above to create a new file where only the owner has read and write permissions, while everyone else has read permissions only:
```c
umask(DEF_UMASK);
fd = Open("somefile.txt", O_CREAT|O_TRUNC|O_WRONLY, DEF_MODE);
```
- Opened files can be closed with the **`close`** function which takes a file descriptor as an argument. Closing a descriptor that is already closed results in an error:
```c
#include <unistd.h> 

int close(int fd); // Returns 0 if ok, -1 on error
```

## Reading and Writing Files:
- Applications perform input with the **`read`** function and output with the **`write`** function:
```c
#include <unistd.h>

// Returns: number of bytes read if OK, 0 on EOF, −1 on error
ssize_t read(int fd, void *buf, size_t n);

// Returns: number of bytes written if OK, −1 on error
ssize_t write(int fd, const void *buf, size_t n);
```
- The `read` function copies at most `n` bytes from the file pointed to be descriptor `fd` to memory location `buf`. On error, `read` returns -1, and returns 0 on EOF. Normally, it returns the number of bytes that were coppied from `fd` to `byte`. 
- **`write`** does the exact same thing but in reverse: it copies bytes from memory location `buf` to file `fd`.
- The following code copies standard input to standard output one byte at a time:
```c
#include <unistd.h>
#include <stdlib.h>

int main(){
    char c;
    while(read(STDIN_FILENO, &c, 1) != 0)
        write(STDOUT_FILENO, &c, 1);
    exit(0);
}
```
- The current file position can be manipulated with the **`lseek`** function.
- In some cases `read` and `write` transfer less bytes than the application requests. These are called *short counts* they are not necessarily errors, but might occur for some reasons such as:
	- *Encountering EOF on reads*: If the application requests a 100 bytes from a file that has only 20 bytes, the first `read` will return the short count 20 and the next `read` returns the short count 0, coz it encounters EOF.
	- *Reading text lines from a terminal*: If the open file is associated with the terminal (keyboard, display, etc.), `read` can only read one line at a time. If you requests chunks of 100 bytes and a line is shorter than 100, you get a short line.
	- *Reading and wring sockets*: If the open file is a network socket, "then internal buffering constraints and long network delays" can cause short counts. Short counts can also happen due to the Unix *pipe*.
- Short counts are almost never encountered when reading from or writing to disk except on EOF, but to have reliable network applications, we need to overcome short counts caused by network latency and other reasons. 

## Robust Reading and Writing with the Rio Package:
- *This section went over creating a IO package resilient to short counts, but what I thought was interesting is the difference between buffered and unbuffered IO. I understand the general idea, but I'm not sure about the details. Basically, with buffering a whole block of bytes gets written or read at once, instead of reading/writing each byte individually. The block of bytes gets stored somewhere between operations. The common opinion is that buffering reduces overhead because there are not system calls for each byte  and that fewer calls are performed for a whole block than for each byte in the block. One thing that really confused me from the text is a claim that buffered IO is good for text files, while unbuffered IO is good for text files, while binary data is bettered IOed without buffering.I checked online and couldn't find definitive answers to anything about buffering and often some conflicting "opinions", the most confusing of which was that buffering might be bad because we are doing [double buffering](https://www.quora.com/What-is-a-good-explanation-of-buffered-I-O). Even when reading the C programming language book, I was stomped at one of the later chapters that was about Unix IO. Probably, I might have to come back to this subject in the future.*

## Reading File Metadata:
- Information about a file or **metadata** can be got by a call to **`stat`** or **`fstat`**

## Sharing Files:
## IO Redirection:
## Standard I/O:
## Putting It Together: Which I/O Functions Should I Use?