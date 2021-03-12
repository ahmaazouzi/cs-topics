# Network Programming:
## Table of Content:
## Introduction:
- *A more in depth treatment of networking in general can be found [here](https://github.com/ahmaazouzi/cs-topics/tree/master/networking). I will assume the reader of this document is already familiar with some basic networking concepts such as the client-server model*.
- Network applications are everywhere and most of them rely on the most basic programming model. They also rely on many of the concepts we have seen so far such as processes, signals, byte ordering, memory mapping and dynamic memory allocation. This chapter will revolve around how a basic web server works and networking from a systems perspective.
- "Internet clients and servers communicate using a mix of sockets interface functions and Unix I/O functions [...] The sockets functions are typically implemented as system calls that trap into the kernel and call various kernel-mode functions in TCP/IP."

## The Client-Server Model:
- A *server* serves *responses* to *requests* from *clients*. Clients and servers are not machines, but they are processes. The client and server processes might reside in the same machine, which is called a *host* in networking lingo. 

## Networks:
- You can find most of this section's content and more [here](https://github.com/ahmaazouzi/cs-topics/blob/master/networking/lowlevel.md).

## The Global IP Internet:
- The whole Internet can be thought of as a collection of hosts with the following properties:
	- The set of hosts is mapped to a set of 32-bit *IP addresses*.
	- The set of IP numbers is mapped to a set of names called *Internet Domain Names*.
	- A process on one Internet host can communicate with a process on any other Internet host over a *connection*.

### IP Addresses:
- An IP address is a 32-bit unsigned integer. 

### Internet Domain Names:
### Internet Connections:



## The Socket Interface:
## Web Servers: