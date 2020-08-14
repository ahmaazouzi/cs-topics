# The Application Layer:
- The application layer is where it's all at. One thing to keep in mind is that the application layer is confined to end systems. Core devices such as switches and routers don't understand anything about application and are confined to the 3 bottom layers of our 5-layer Internet stack!

## Principles of Network Applications:
### Network Application Architecture:
- There are very common application architectures:
1. **Client-Server Architecture**: It consists of two types of host. A ***server***, which is an *always-on* host with a fixed IP address. This fixed big machine is connected to a bunch of ***clients*** (*client* is the other type of host in this architecture). The server is a central dependable machine that receives ***requests*** for data or objects from the client a serves back a ***response*** with the requested data/object. A single server might not be able to server a very large amount of requests, that's why multiple servers can be clustered together into a **data center** to create a powerful virtual server. Protocols that use this architecture includes: HTTP, FTM, SMTP... etc.
2. **P2P (Peer-to-Peer) Architecture**: In P2P, hosts (called **peers** here) share data directly without having to pass by a server. Sample applications include file sharing through with BitTorrent, peer-assisted download accelerators like Xunlei, Internet telephony like Skype. Hybrid architectures combining P2P with Client-Server architectures are also in common use. The advantages of P2P are immense as it is **self-scalable** architecture since peers distribute files to other peers reducing the workload of the network. It is also cost-effective as no dedicated servers are required. P2P suffers from security problems, lack of economic incentives to Silicon valley mafias and asymmetric way ISPs treat download vs. upload traffic.

### Inter-Process Communication:
- In the application layer, the protocols allow applications or more precisely **processes** to communicate with each other. A process in OS lingo is a program running in a host. When communication is done between processes in the same host, this communication is governed by the operating system. When processes reside in different hosts, the communication is governed by application layer protocols.
- Process exchange **messages**. The sending process creates and sends a message and the receiving host receives the message and possibly responds to it with a message of its own.

#### Client and Server Processes:
- A better definition of a network application is that it "consists of pairs of processes that send messages to each other over a network."
- Like hosts, processes can also be labeled as a **client** and a **server**. To be more precise, in a *communication session*, the process that initiates the communication is the client and the process that wait to be contacted for that session is the server. This is the same in both P2P and client-server architectures. While in client-server architectures, the client process usually resides in a client host such as a web browser and the server process (web app) resides in a server host, in P2P this role gets reversed based on which process initiates the communication session. 

#### The Interface between the Process and Computer Network:
- Processes send and receive messages from the network using an Interface called a **socket**. If a process were a door, a socket would be its door.
- A socket is the interface between the application layer and the transport layer. The developer has full control on the application side of the socket while the transport layer is controlled by the operating system. The developer can only choose the protocol to be used on the transport layer (TCP or UDP) and tweak a few parameters such as the maximum buffer size and maximum segment size. 

### Addressing Processes:
- When a process is ready to send a message to another process residing in another host, it needs to identify where that process is. This is done with two pieces of information, the IP address of the receiving host and the socket (or process)'s port number. 

### Transport Services available to Applications:
- Picking a a certain transport layer service to use for transporting our application message depends on the following four dimensions:
	1. **Data Transfer Reliability**: packets can get lost due to it being corrupted in transit or an overflowing router... etc. In an application like email where the data must be transferred reliably, you use a **reliable data transfer** protocol like TCP. Some applications can be **loss-tolerant** such as video/voice chatting. These can use data transfer transport with less reliability like UDP. Lost data results in glitches but the overall messages get through. 
	2. **Throughput**: Throughput almost always suffers from pressure. **bandwidth-sensitive applications** need to have their throughput at a minimum rate (bits per second) to be usable. The transport provides a service that can guarantees the delivery of the specified throughput. If it can't guarantee that throughput, it gives up and the application can't work until that throughput is available again. **Elastic applications** on the other hand can work with as little or as much throughput. This include web and email.
	3. **Timing**: The transport layer can also guarantees that data be received no less than a specified time (say a 100 msec). This is especially important in real time applications like telephone or live games.
	4. **Security**: Security is another great service offered by the transport layer. Things like encryption, end-to-end authentication, data integrity... etc. 

#### TCP vs UDP:
- **TCP** and **UDP** are the chief transport protocols on top of which network applications are built. Choosing one over the other depends on a several criteria. 
- TCP is connection-oriented and is all about reliable data transfer. It also adds a congestion control mechanism. These features add overhead which makes TCP no ideal for real time applications that are sensitive about throughput and time. It's great for elastic applications such as email and web.
- TCP also comes coupled with **SSL/TLS** for security purposes. SSL is an enhancement of TCP that is implemented on the application layer. The client and server must implement SSL to use it. SSL has its own socket. The process passes cleartext data to the SSL socket and SSL encrypts the data and passes the encrypted output to the TCP socket. On the other host, the TCP socket receives the encrypted data, passes it to SSL which decrypts it and then passes it to the process.
- UDP on the other hand is connectionless, and doesn't offer transfer reliability or congestion control, thus making it a lightweight protocol great for real-time applications, even if a packet is lost here or there or if some packets arrived out of order.
- While the transport layer can offer security and reliability with the TCP transport and its SSL enhancement, it can't offer any guarantees concerning timing and throughput. There are programming tricks the programmer can add to her application, but these have their limitations.

### Application Layer Protocols:
- An application layer protocol defines how messages between different processes in different host machines are exchanged. An application-layer	protocol should define the following:
	- The type of messages exchanged (request and response messages).
	- The syntax of message types such as fields and how they are delineated.
	- The semantics (meanings) of fields.
	- Rules for how and when processes send or respond to messages.
- Some protocols are in the public domain and specified in RFCs such as HTTP and FTP. If you implement the protocol correctly, you can create an application that can download web pages or files. Other protocols are proprietary like those used by Skype.
- Protocols are only one part of the applications that are based on them. HTTP is only one part of the Web. The Web has many other components such as servers, the HTML language... etc. 

## HTTP:
- **HTTP (typer-text transfer protocol)** is the de facto protocol of the **web** or the **world wide web**. The web itself is an application, the most popular and successful application that runs on the Internet. 

## FTP:
## SMTP and Email:
## DNS:
## Peer-to-Peer Applications:
## Socket Programming:






