# The Network Layer:
## Introduction:
- The process-to-process communication in the transport layer depends on services provided by the layer under it, the *network layer* which is responsible for host-to-host communication. This is probably the most important and interesting layer in the networking stack. While the application and transport layers are implemented only in the end systems, the network layer is implemented across the whole network, so every router in the network has to process it. 
- The network layer is both complex and interesting and in this document we will try to capture some of this complexity by covering various topics which include:
	- An overview of the network layer and the services it provides.
	- The two main approaches to network-layer packet delivery: the datagram and virtual-circuit model.
	- The role of addressing in packet delivery.
	- Forwarding and routing, how they differ and what their role in packet delivery.
	- Looking inside a router and how it's used in packet delivery. 
	- Diving deep in the Internet Protocol (IP) and such things as IPv4, NAT, ICMP, IPv6, etc. 
	- Routing algorithms and how they are used to make the network efficient.
	- Different routing protocols such as RIP, OSPF, etc.
	- Multicast and broadcast routing.

## The Network Layer:
### Forwarding and Routing:
- The role of the network layer is deceptively simple: moving packets from host A to host B. This involves two important network layer functions:
	- **Forwarding**: is basically moving a packet from an input link to the appropriate output link. 
	- **Routing**: is determining the route/path that a packet needs to take to get from a sending host to a receiving host. These paths are calculated by **routing algorithms**.
- Some people might use the terms forwarding and routing interchangeably, but these terms are totally different. If we use the analogy of driving between two distant cities, forwarding is passing through each interchange in the route, and routing is planning the trip using a map. 
- Every router has a **forwarding table**. The router forwards a packet, through examining some value in the header of the packet and using this value as an index into the forwarding table. The value stored in the corresponding entry in the forwarding table indicates the output link interface to which the packet is to be forwarded. Depending on the network-layer protocol, the packet header value could be either the destination address of the packet or an "indication of the connection to which the packet belongs". 
- The following figure shows how a packet is forwarded by the router. A packet with the header value ***0111*** arrives to the router which uses the that value as an index in its forwarding table.  It determines that the outgoing link interface is 2. It then forwards the packet to interface 2. 
![How routers use forwarding tables](img/routingAlgoForwardingTable.png)
- How does the router build the forwarding table? The figure above shows a **routing algorithm** which determines the values that are inserted into the router forwarding table. The routing algorithm can be either centralized where it's processed in one place and then routing information is downloaded to routers. It might also be decentralized where multiple routers would process different pieces of the algorithms. In both the centralized and decentralized cases, a router receives *routing protocol messages* :confused:, which are used to configure the forwarding table in that router. 
- Don't mix **link-layer switches** with routers. Switches work at the link-layer and base their forwarding on link-layer frame headers. Some might call routers layer 3 switches which is just confusing!! Anyways, routers must implemented layer 2 protocols because the network layer depends on the services provided by the link-layer. This document will also use the term *router* to refer to packet switches in virtual-circuit networks.

#### Connection Setup:
- In addition to routing and forwarding, some network-layer architectures also provide **connection setup**. These architectures, e.g. *ATM*, require routers in the chosen path to handshake to establish state before data can start flowing between source and destination. 

### Network Service Models:
- When it comes to the services provided by the network layer to the transport layer, what kinds of services can the transport layer expect from the network layer, namely:
	- Can the transport layer expect the network layer to deliver a packet to the destination host?
	- Can packets arrive in the order they were sent?
	- Is the time between the sending of two packets the same as time between the receiving of these two packets?
	- Does the network layer offer any mechanism of congestion monitoring or control?
- Answers to these questions are determined by the *network service model*, which defines the characteristics of end-to-end transport of packets between the sending and receiving systems. Possible services that the network layer might provide include:
	- *Guaranteed delivery* of the packet to the destination.
	- *Guaranteed delivery with bounded delay*, in say a 100 milliseconds. 
	- *In-order packet delivery*. 
	- *Guaranteed minimal bandwidth*. The network layer can guarantee a minimal bit rate similar to that found in transmission links (such as 1 Mbps). As long as the host sends bits at a rate smaller than this bandwidth, no packets are dropped. 
	- *Guaranteed maximum jitter* guarantees that time separating the sending of two packets is equal to the time separating the receiving of those two packets (or equal within a time window).
	- *Security services*: The network layer can use a secret session key known only by the source and destination hosts, so the payloads of packets can be encrypted by the sender and decrypted by the receiver. 
- This is just a glimpse of the services that the network can possibly provide.
- The Internet's network layer provides a single service called **best-effort service** which basically means none of the services we mentioned earlier such as security, guaranteed delivery, in-order delivery, etc. are provided as the following table shows:

| Network<br>architecture | Service<br>model | Bandwidth<br>guarantee | No-loss<br>guarantee | Ordering | Timing | Congestion<br>indication |
| --- | --- | --- | --- | --- | --- | --- |
| Internet | Best effort | None | None | Any order<br>possible | Not<br>maintained | None |
| ATM | CBR | Guaranteed<br>constant rate | yes | In order | Maintained | Congestion<br>won't occur |
| ATM | ABR | Guaranteed<br>minimum | None | In order | Not maintained | Congestion<br>indication provided |

- The best-effort service model seems useless, but there are some great reasons why it works and dominates the world!! 
- Some other network-layer architecture go beyond the best-effort service model and offer other models with more services. The ATM architecture offers service models that are less bare-bone than the Internet network, which we will look at briefly just to illustrate that there are alternatives to best-effort:
	- **Constant bit rate (CBR) ATM network service**: has the goal of "to pro- vide a flow of packets (known as cells in ATM terminology) with a virtual pipe whose properties are the same as if a dedicated fixed-bandwidth transmission link existed between sending and receiving hosts." It is kinda similar to telephone
	- **Available bit rate (ABR) ATM network service** is a slightly better than best-effort service. Packets can be lost but are never reordered. A minimum packets transmission rate (MCR) is also guaranteed. If the network has excess resources at a given time, it sends packets at a rate higher than MCR. ATM ABR can also notify the sender of the existence of congestion and maybe tells it to adjust its sending rate according to the level of congestion. 

## Virtual Circuit and Datagram Networks:
- Just like the transport layer, the network layer can offer a connection-oriented service and a connectionless service, but the similarities between the transport and network layers connectionwise is only skin-deep, and there are some fundamental differences between the two:
	- In the network layer connection(-less) services are host-to-host services provided by the network to the transport layer, while the transport connection(-less) services are process-to-process services offered to application by the transport layer.
	- A network architecture can only offer a connectionless host-to-host service or a connection host-to-host service but can never offer both. Networks providing only connection services at the network layer are called **virtual circuits (VCs)**, and those offering connectionless services only are called **datagram networks**.
	- Transport connection facilities are implemented in the edge at the end-systems, while network connection is implemented at the core in routers as well as the edge in end-systems.

### Virtual-Circuit Networks:
- We all know and interact daily with the Internet network which is a datagram network, but there are other networks which belong to the virtual-circuit architecture such as the ATM and *frame relay* networks. 
- A VC consists of:
	- 1. A *path* consisting of a series of links and routers connecting the source to the destination. 
	- 2. *VC numbers*, one for each link along the path.
	- 3. Entries in the *forwarding table* of each router along the path.
- A VC packet carries a VC number in its header. Each VC router along the packet's path changes the VC number of the packet using the router's forwarding table.
- Consider the following virtual circuit network:
![Virtual circuit network](VCNetwork.png)
- In the figure above, we see a host A and host B, and 4 routers. Routers R1 and R2 have 3 link interfaces each. Imagine host A wants to establish a virtual circuit between itself and host B at the path A-R1-R2-B, and also assigns VC numbers 12, 22, 32 to the three links in the path for this VC. 
- How does the router determine the replacement VC number of a packet going through the router? Well, Each router's forwarding table has a *VC number translation* which looks something like the following table (for R1):

| Incoming interface | Incoming VC # | Outgoing interface | Outgoing VC # |
| --- | --- | --- |
| 1 | 12 | 2 | 22 |
| 2 | 63 | 1 | 18 |
| 3 | 7 | 2 | 17 |
| 1 | 97 | 3 | 44 |
| ... | ... | ... | ... |

- Whenever a new VC is established across a router, a corresponding entry is added to the forwarding able. When the VC terminates, entries in each router's forwarding table in the path are removed. 



### Datagram Networks:
### Origins of VC and Datagram Networks:

## Inside a Router:
## The Internet Protocol: Forwarding and Addressing in the Internet:
## Routing Algorithms:
## Routing in the Internet:
## Broadcast and Multicast Routing: