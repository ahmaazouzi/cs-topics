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
### HTTP Overview:
- **HTTP (typer-text transfer protocol)** is the de facto protocol of the **web** or the **world wide web**. The web itself is an application, the most popular and successful application that runs on the Internet. 
- Let's start with some basic but crucial terminology:
	+ A **web page** (also a **document**) consists of one or more objects. Objects can be images, video clips, HTML files... etc. 
	+ A web page consists of a **base HTML file** and probably sever referenced objects.
	+ The objects are referenced in the base HTML file with **URLs**. A URL consists of two parts: the **hostname** of the server that houses the object, the object's **path name**. 
	+ The clients in the web are usually the web browsers and **web servers** such as Apache are the servers.
- The HTTP protocol defines how a client requests a web page from a server and how the server sends back the requested document.
- HTTP uses the TCP transport protocol. The client initiates a connection with the server. Once the connection is established, the client and server processes can exchange messages through their sockets. Both processes send HTTP messages into their socket interfaces and receive messages from those same sockets. 
- HTTP is also traditionally a **stateless protocol**, meaning that the server doesn't keep track of the client between any two requests. The server doesn't know if two requests comes from two different clients or the same client.

### Persistent vs Non-Persistent Connections:
- Should each request/response pair have its own TCP connection (i.e. use **persistent connections**), or should all request/response pairs be sent over the same TCP connection (i.e. use **non-persistent connections**)? This is a very important design decision and can have ramifications on your application. 
- HTTP uses persistent connections by default, but you can configure the clients and server to use non-persistent connections.

#### HTTP with Non-Persistent Connections:
- Let's say we have a web page consisting of a base HMTL file and 20 JPEG images. When using non-persistent connections, the client initiates a connection, then the server open the connection, then client sends a request to get the base HTML, then the server receives the request, retrieves the file and sends it back, the server tells the client to close the connection, the client ensures that the file has been received completely intact, the client then closes the connection. This whole process then is repeated for each of the 20 other documents.
- In non-persistent TCP connections, only one request and only one response can be transported. In our example above 21 connections are opened to serve our web page.
- The connections can be opened in parallel (simultaneously) or serially (one connection at a time). Modern browsers allow for certain amount of parallel connections, but users can configure their browsers to change this number or specify an upper limit to the number parallel connections. 
- **Round-trip time (RTT)** is the time it takes for a small packet to travel from client to server and then back to the server. RTT includes all kinds of delay (transmission, propagation, queuing, processing delays... etc.).
- RTT can be used as a measure of how much time it would take to retrieve a file/object. Requesting a file takes two RTTs plus the time necessary to transfer the file as files usually take several packets. This can be done as follows:
	1. **First RTT**: 
		- The client sends a small TCP segment to the server asking for a connection to be opened.
		- The server responds with a small acknowledgment segment.
	2. **Second RTT**:
		- The client sends an acknowledgment that it has been acknowledged by the server. Combined with the acknowledgment is a message requesting the HTML file.
		- The server sends the file to the client after receiving the acknowledgment and request message.

- The first RTT and the first trip of the second RTT are called a **TCP 3-way handshake**. We will cover it later.

#### HTTP with Persistent Connections:
- Non-Persistent connections suffer from several disadvantages:
	- A new connection with all its overhead such as a TCP buffer and a TCP variable. These are costly on resources and a server handling thousands of requests can easily get overwhelmed by these.
	- Each object will suffer a delay of 2 RTTs.
- In a persistent connection, the server leaves the TCP connection open after sending a response. The following requests and responses will be sent over the same connection. Our entire page and its 20 images get sent over the same connection. Even multiple web pages from the same server can be served over the same persistent connection. Other objects can be sent over the same connection even if there are pending requests that haven't be served yet. 
- HTTP servers close connections when they are used for a certain time (timeout).

### HTTP Message Format:
- HTTP defines two types of messages: **request messages** and **response messages**.

#### HTTP Request Messages:
- The following is a simple HTTP request message:

```
GET /cs-topics/networking.html HTTP/1.1
Host: www.ahmaazouzi.io
Connection: close
User-agent: Mozilla/6.0
Accept-language: ar

```
- HTTP messages are written in plain ASCII text.
- The request message in our example has 5 lines but it can have many more and it can also have few as one!
- A Typical request consists of:
	- The first line of the request is called a **request line**. The request line itself consists of:
		+ The request method, such as GET, POST ..etc. A request method dictates how the client communicates with the server. With GET, for example, a client usually fetches data or documents. A google search, for example, asks for search results. 
		+ The **path** which points to the requested resource.
		+ The HTTP **version**. The most common version is http 1.1.
	- **Request headers** are key value pairs. They include the host, user agent..etc. There can be a lot of headers.
	- A request might also have a **body** that contains parameters added to the request. A POST method has a body while GET doesn't. query parameters in a POST method are added to the request's body and are not appended to the URL as in a GET request.
- `POST` and `GET` are the most commonly used HTTP request methods. The following tables shows some of the fundamental differences between the two:

| **`GET`** | **`POST`**
| --- | --- |
| Parameters are placed in URL | Parameters in body
| Used for fetching documents | Updates data in server
| Has a maximum URL length | No max length
| Cachable | Non-cachable
| Not for changing server | supposed to change server

- These fundamental differences between `POST` and `GET` dictate the fact that `GET` is mostly used to retrieve documents (or data) from the server, while `POST` is used to send data to the server and actuate changes
- The following figure shows the general format of an HTTP request:
![Request message format](request.png)

#### HTTP Response Messages:
- A typical HTTP response looks as follow:
```
HTTP/1.1 200 OK 
Connection: close
Date: Mon, 10 Apr 2020 00:00:00 GMT
Server: Apache
Content-Length: 6821
Content-Type: text/html

<h1>Hello, World!</h1>
```
- It has headers and a body just like a request, but it differs from a request in that it has a **status line** instead of a request line. A status line consists of 3 parts:
	+ The HTTP version.
	+ A **status code** which is a number indicating if the request was successful. Codes include 202 for a successful request, 404 for a not found page, 500 for a server error.. etc. 
	+ "A **status message**, a non-authoritative short description of the status code."
- One important header line in the example request is the **connection** line which controls the connection's persistence. This particular request wants the server to close connection after the requested object is received.
- The following figure shows the general format of an HTTP response:
![Response message format](response.png)

### User-Server Interaction: Cookies:
- HTTP is stateless. This simple designed has allowed for the creation of highly performant web servers since these don't have to worry too much about remembering clients. Servers can still remember clients with the infamous **cookies**.
- A cookie consists of 4 parts:
	1. A cookie header on the request message.
	2. A cookie header on the response message.
	3. A cookie file in the client host that is managed by the browser.
	4. A backend database at the server.
- Cookies work as follows:
	+ When a user visits a website for the first time, the server creates a unique identification number and a unique entry in its database. The database entry is indexed by the unique identification number.
	+ The server responds to the user's request by adding the `Set-cookie` header line to the response, for example `Set-cookie: 222222`.
	+ When the browser receives the response it sees the `Set-cookie` header and appends a line to it's cookie file. This line has the hostname of the server and the identification number in the `Set-cookie` header.
	+ In every subsequent request from the user to the server, the browser will consult its cookie file, extracts the identification number from the cookie file and attaches it to the request before sending it to the server. This is achieved with the `Cookie` header. (e.g. `Cookie: 222222`)
- Cookies permit the server to identify the host between different request. Cookies are very useful in that they keep track of logged in user, for example, allow the user to set personal preferences. They are used for recommendations and have many great application.
- Some corporations, however, use cookies in extremely nefarious ways. Cookies are a privacy nightmare!!

### Web Caching:
- "A **web cache**-Also called a **proxy server**- is a network entity that satisfies HTTP requests on behalf of of an origin of a web server." Wow, so academic! The web cache server has its own storage. Browsers can be configured to direct their requests to the web cache first. Basically, the cache stands as a mediator between the client and the actual server. When the client requests an object, the request goes to the proxy server which checks if it has a copy of the object. If it has a copy, it sends it to the client. If it doesn't have a copy, it sends an HTTP request to the reasl server, stores a copy of the object and serves the client's request. 
- Web cache is installed by ISPs and your cache might go through several caches corresponding to different levels of ISPs.
- Using cache servers achieves two goals: increasing the speed of responses and page retrieval on the one hand (in the worse case it would eliminate a lot of propagation delay), and on the other hand caching offloads much of traffic strain on an ISP's access link reducing costs and and frustration. 
- **Content delivery networks (CDN)** are geographically distributed cache servers that play an important role in today's Internet.

### The Conditional `GET`:
- Caching is good and all, but you don't want stale objects from the cache in the ever more dynamic web of today. The **conditional GET** allows the cache server to verify that an object is up to date. A conditional GET is a regular GET request with a **`If-Modified-Since:`** header.
- When the client requests something, the cache server sends a conditional GET request to the actual server. If the requested object hasn't been modified, the server returns a response with an empty body and the status code **`304`** and the status message **`Not Modified`**. An empty body means a very fast transmission.

## FTP:
- **FTP (file transfer protocol)** allows you to transfer files between the local host and remote host. A typical FTP session goes as follows:
	1. The user provides an FTP client with an FTP hostname.
	2. The client opens a TCP connection with the FTP server process.
	3. The user is asked to provide a username and a password.
	4. The user is authorized to use the server.
	5. The user copies files from/to the local host or remote host.
- FTP seems similar to HTTP. They are both used to transfer files. However they are differences between the two. One big difference is that FTP establishes two connections between the local and remote host:
	1. A **control connection** for sending control information to the server such as user identification, password and commands to change the directory and put and get files
	2. A **data connection** that's used exclusively for exchanging data, that is files, between the two hosts.
- *Nerd extra*: protocols which send both data and control information over the same connection are called **in-band** such as HTTP and SMTP. FTP is said to be **out-of-band**.
- The anatomy of an FTP session: The client initiates a control connection with the FTP server on port 21. The client sends the FTP server the username and password over this control connection. The user can send command to change the directory in the remote host over this same control connection. When the server receives a command to transfer a file, it opens a data connection and then a single file is transfered. The connection is closed immediately after one and only one filed has been transferred. If the user wants to transfer another file during the same session, a new data connections is opened for that.
- The control connection is persistent throughout an FTP session while the data connection is non-persistent.
- Unlike HTTP, FTP is **stateful**. It needs to keep track of the user and associate her with an id and a password and keep track of where she is in the directory tree!! This taxing on the FTP server making less capable of having many simultaneous sessions. It's not as amazingly performant as HTTP.

#### FTP Commands and Replies:
- FTP commands are sent in 7-bit ASCII format over the control connection. Each command is made of 4 ASCII characters. Some commands have optional arguments.To delineate successful commands, separate them by a new line. 
- Here are some common FTP commands (thee are many more):

| Command | Role |
| --- | --- |
| USER *username* | send user id to the server |
| PASS *password* | send user password to the server |
| LIST | asks the server to send a list of files in the current directory in the remote host. The list is sent back to the client over a new data non-persistent data connection |
| RETR *filename* | gets a file from the server in the current directory. It opens a data connection over which the file is sent. |
| STOR *filename* | puts a file in the remote host in the current directory in the remote host. |

- Each command is responded to by the server with a **reply** which is a 3 digit code followed by an optional message. replies are similar to HTTP response status codes. The following table lists some of the more common replies:

| Reply | Message |
| --- | --- |
| 331 | Username OK, password required |
| 125 | Data connection already open; transfer starting |
| 425 | Can't open data connection |
| 452 | Error writing file |

## SMTP and Email:
## DNS:
## Peer-to-Peer Applications:
## Socket Programming:






