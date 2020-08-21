# Transport Layer:
- This article will be on the **transport layer** which is responsible for transmitting data between different processes in the layered network architecture. It will discuss the principles of transport and how these are implemented in actual protocols (specifically **UDP** and **TCP**).
- The article will discuss the following topics in order:
	+ The relationship between the network and transport layer and how the transport layer extends network layer's function of connection different hosts to actually connecting different processes running on these hosts. This part will also include a discussion of UDP as a basic transport protocol.
	+ This part will discuss how can data be transferred reliably between different processes residing in different hosts. A deep discussion of TCP will supplement the topic of data transfer reliability.
	+ A discussion of congestion, it's causes and ways to control it. This discussion will also involves TCP's specific techniques of congestion control. 

## Transport-Layer Services, an Intro:
- The transport layer provides *logical communication* between processes running on different end systems: this enables "connecting" the two processes even though they are running in different that might be geographically distant from each other. Thanks to the transport layer protocols, the processes communicate with each other without having to worry about the physical realities of the network or the hosts they run on. 
- How does the transport layer relate to the layers immediately surrounding it? When a process in the application layer pushes a messages down to the transport layer, the messages get sliced into small chunks to which transport headers are added to create transport layer **segments**. The segments themselves are passed down to the network layer where network headers are added to them to create **datagrams**. The datagrams are transported through the network from the current host. Before reaching the destination host, the datagrams are examined by routers which direct them toward their final destination. Routers don't understand transport segments but are only concerned with datagram headers where they have information for routing packets. Once a datagram arrives to the destination host, segments are extracted and pushed up to the transport layer. The transport layer processes the segments, probably reassembles back into messages, and pushes them up to the destination process.

### Relationship Between the Transport and Network Layers:
- While the transport layer provides logical communication between processes, the network layer provides logical communication between hosts. The difference between the two layer as in as far as being mechanisms from transmitting data from one end to the other is subtle but crucial. If the network is the mail service that move letters and packages between different buildings, let's just say the transport is some kinda secretary who also distributes mail within a building.
- The transport layer is constrained by the network layer. The bandwidth and delay guarantees that transport can provide to applications are constrained by the bandwidth and delay guarantees provided to it by the network layer. 
- The transport layer can, however, provide services that make up for the shortcomings of the network layer's services. The transport layer can provide the ability to transfer data reliably between different processes even though the network layer usually corrupts, drops and duplicates packets. The transport layer can also provide encryption which the network layer can't do.

### Transport Layer in the Internet, an Overview:
- The Internet and any typical TCP/IP network provide two main transport protocols: **UDP**, an unreliable, connectionless protocol and **TCP**, a reliable connection-oriented protocol. 

#### IP:
- The Internet's network layer's protocol is called **IP (Internet Protocol)**. IP is the protocol that provides logical communication between hosts connected to the Internet. It is a **best-effort delivery service**. IP tries its best to deliver packets but it *makes no guarantees*. IP might:
	* Lose segments.
	* Fail to provide orderly delivery of segments.
	* Fail to guarantee the integrity of the data in the segments. 
- IP is an **unreliable service**. 
- Every host must have a *unique IP addresss*. 

#### Internet Transport Protocols:
- The most important service provided by UDP and TCP is to extend IP's delivery service between two hosts into a a delivery service between processes. Elevating the host-to-host delivery to a process-to-process delivery is called **transport-layer multiplexing/demultiplexing**. 
- Another important service TCP and UDP provide is *integrity checking* which is done by including error checking fields in segment headers. 
- TCP, unlike, UDP goes further to provide **reliable data transfer**. TCP ensures data is delivered from the sending process to the receiving process correctly and in order. 
- TCP also provides **congestion control**.

## Multiplexing and Demultiplexing:
- Multiplexing/demultiplexing basically refers to extending the network's host-to-host communication to the transport's process-to-process communication. How does the transport layer sort the segments it receives from the network layer and direct each one to the appropriate process? 
- The transport layer doesn't deliver data to a process directly but uses an intermediary *socket*. Each socket has a unique identifier. When the transport layer receives a segment from the network layer, it examines the segment's header fields to identify the receiving socket. **Demultiplexing** refers to delivering a segment to the correct socket. **Multiplexing**, on the other hand, refers to the process of gathering data packets from different sockets, wrapping them with transport headers to create segments, and sending them down the stack to the network layer. 
- The **source port number field** and **destination port number field** are the unique identifiers which indicate which socket a segment is to be delivered to. A port number is a 16-bit value whose value could be between 0 and 65535. Port numbers between 0 and 1023 are **well-known port numbers** which are reserved for well-known application protocols such HTTP, FTP, etc. 
- Each socket has a port number assigned to it. When the transport layer receives a segment, it checks its designation port number and directs it to the socket with the same port number. The segment data is then passed up to the socket's process. This is roughly how it's down in UDP but TCP is kinda more complex. The following subsections will discuss how multiplexing/demultiplexing in UDP vs TCP.

### Connectionless Multiplexing and Demultiplexing:
### Connection-Oriented Multiplexing and Demultiplexing: 

## Connectionless Transport with UDP:
## Principles of Reliable Data Transfer:
## Connection-Oriented Transport with TCP:
## Principles of Congestion Control:
## Congestion Control with TCP: