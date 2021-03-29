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
![Virtual circuit network](img/VCNetwork.png)
- In the figure above, we see a host A and host B, and 4 routers. Routers R1 and R2 have 3 link interfaces each. Imagine host A wants to establish a virtual circuit between itself and host B at the path A-R1-R2-B, and also assigns VC numbers 12, 22, 32 to the three links in the path for this VC. 
- How does the router determine the replacement VC number of a packet going through the router? Well, Each router's forwarding table has a *VC number translation* which looks something like the following table (for R1):

| Incoming interface | Incoming VC # | Outgoing interface | Outgoing VC # |
| --- | --- | --- | --- |
| 1 | 12 | 2 | 22 |
| 2 | 63 | 1 | 18 |
| 3 | 7 | 2 | 17 |
| 1 | 97 | 3 | 44 |
| ... | ... | ... | ... |

- Whenever a new VC is established across a router, a corresponding entry is added to the forwarding able. When the VC terminates, entries in each router's forwarding table in the path are removed. 
- Why complicate things by changing a packet's header for each link it crosses? There are two reasons for this:
	- 1. It reduces the length of the VC field in the packet's header.
	- 2. It also greatly simplifies the *VC setup* (whatever this :confused:). With multiple VC numbers for each packet, each link in the path can choose a VC number independent of VC numbers chosen at other links along the path. If we have one common VC for all links along a certain path, routers in that path need to communicate and make sure that number is not being in use by another connection at these routers. 
- Being connection-oriented, a VC network's routers must maintain **connection state information** for current connections. Each time a connection is established through a router, a connection entry must be added to that router's forwarding table, and each time a connection is disbanded, the corresponding connection entry in the router's forwarding table must be removed. maintaining state information about the VC connection might be the most important feature of such type of network. 
- The life cycle of a VC connection goes through 4 phases:
	- **VC setup**: The sending transport layer contacts the network layer, giving it the receiver's address. The network determines the path between the sender and receiver, gives each link along the path a VC number, and adds an entry in the forwarding table of each router along the path. The network layer might also reserve resources such as bandwidth along the path.
	- **Data transfer**: Once a VC is established, packets can start flowing through the circuit as the figure blow shows.
	- **VC teardown**: Once the sender or receiver wishes to terminate the connection, it tells the network to tear the VC down. The network informs the other end system of this wish to terminate and updates the forwarding tables in routers along the path to show that the VC doesn't exist anymore.
![VC setup](img/VCSetup.png)
- One important difference between VC setup and transport layer connection setup is only the two end systems are aware of and involved in the set up of a transport layer connection, while in a VC, every router in the VC path is aware of all the VC passing through it.
- Messages that end systems send to setup and teardown a VC and the messages exchanged between routers to setup this connection are called **signaling messages** and are governed by **signaling protocols** and we will not cover them here. 

### Datagram Networks:
- In a **datagram network**, a packet is given an address of the destination end system and is placed in the network where the address will be used by routers to get it get the packet to the desired destination.
Datagram networks are connectionless, so they don't need a VC setup, and routers don't have to maintain VC state information as the following image shows:
![A datagram network](img/datagramNetwork.png)
- As a packet traverses the network, it passes through  a series of routers which use the packet's address to forward it. Each router has a forwarding table that maps destination addresses to link interfaces. A router uses the destination address of a packet to lookup the right link interface in the forwarding table. The router, then, forwards the packet to that link interface. 
- How does the lookup operation works in datagram networks. Let's say that a destination address is 32-bit long. A naive implementation of a forwarding table in such a system would have an entry for every possible address. Such a table would have over 4 billion entries which is extremely inefficient. 
- Let's also suppose we have a router with 4 links numbered 0 through 3, and that packets are to be forwarded as follows:

| Destination range | Link interface |
| --- | --- |
| 11001000 00010111 00010000 00000000<br>through<br>11001000 00010111 00010111 11111111 | 0 |
| 11001000 00010111 00011000 00000000<br>through<br>11001000 00010111 00011000 11111111 | 1 |
| 11001000 00010111 00011001 00000000<br>through<br>11001000 00010111 00011111 11111111 | 2 |
| otherwise | 3 |

- For such an arrangement we don't really need all 4 billion address but we need only a 4-entry table:

| Prefix match | Link interface |
| --- | --- |
| 11001000 00010111 00010 | 0 |
| 11001000 00010111 00011000 | 1 |
| 11001000 00010111 00011 | 2 |
| Otherwise | 3 |

- In this type of forwarding tables, a router matches the **prefix** of a destinations address with a entry in the table. If there is a match, the router forwards the packet to the corresponding link interface. Let's say the destination address of a given packet is ***11001000 00010111 00010110 10100001***. We see that the first 21-bits of the address matches the first entry in the table, so the packet will be forwarded to the link interface 0, or would it?? If you examine the whole table, you'd notice the address matches all 3 entries? So how would the router decide which link to forward the packet to? In fact, when there are multiple matches, the router uses the **longest prefix matching rule**. The router finds the longest matching entry in the table and forwards the packet to the link interface associated with the matching entry. 
- Although datagram networks don't maintain information about connection state, they keep forwarding state information in their tables. However, the rate at which datagram network forwarding tables are updated is very slow. These tables are updated by forwarding tables every one to five minutes. VC forwarding tables are updated whenever a connection is established or torn down.. This can literally happen in microseconds!
- Because forwarding tables in datagram networks can be updated at any time, the paths that packets sent from one system to another can follow different paths and arrive out of order!

### Origins of VC and Datagram Networks:
- THe VC network has its origins in telephony systems which actually use real circuits instead of virtual circuits. It is much more complex than the datagram network because it connects dumb end systems so the network is burdened with maintaining a connection.
- Datagram networks were designed from the get go to connect complex computers. Networks were made as simple as possible. Upper layers of the network stack that reside in the sophisticated end system take care of functions that make the network usable such as packet reordering, reliability and congestion control. Datagram networks are inversion of VC networks. 
- This simple design of datagram networks demands little requirements from the networks which leads to fact that such a network can interconnect networks relying on different link-layer technologies that use different media such as radio, Ethernet, fiber, etc.
- Complex functionality that depends on datagram networks is all implemented in end systems and is not hindered by complex network constraints. It's easy to develop complex applications on the edge on the network without having it mixed with complexities of the network's core.

## Inside a Router:
- How do routers **forward** packets? i.e. How do they transfer packets from their incoming links to their outgoing links? The terms *forwarding* and *switching* are often used interchangeably and it looks like we'll be doing the same from now on.
- The following figure shows a high-level generic view of router architecture:
![Router architecture](img/routerArch.png)
- Your generic router generally consists of:
	- **Input ports**: perform several functions:
		- At the physical layer, the input port *terminates* the incoming physical link.
		- At the link layer, the lookup function is performed at the input port. "It is here that the for- warding table is consulted to determine the router output port to which an arriving packet will be forwarded via the switching fabric", Control packets, *whattt :confused:!!* such as those carrying routing information get forwarded from the input ports to the routing processor. 
	- **Switching fabric**: connects the input ports to output ports. It is completely contained within the router. It is a network inside the network's router.
	- **Output ports**: stores packets received from the switching fabric and transmits these packets on the outgoing link by performing the physical and link layer functions we've touched on for input ports. With bidirectional links which transmit data in both directions, an output port is paired with an input port "on the same line card (a printed circuit board containing one or more input ports, which is connected to the switching fabric)".
	- **Routing processor**: executes the *routing protocols*,  maintains *routing tables* (what :confused:!!) and attached link information. It also computes the forwarding table of the router and performs network management which we will not talk about in this chapter. 
- As we've seen earlier, a router perform two functions: routing and forwarding. The image above showing router's architecture illustrates this distinction where we can see how the router is divided into a **router forwarding plane** and a **router control plane**.
- The router's input ports, output ports and switching fabric are part of the forwarding plane and are almost always implemented in hardware. Implementing the forwarding plane in hardware rather than software is due to the fact that a typical router needs to forward large amounts of packets in a few nanoseconds. Implementing the forwarding functionality in software would make it slower.
- Unlike the forwarding plane, the router control plane which executes router protocols executes at a scale of milliseconds and seconds. They are implemented in software that runs on the routing processor which a typical CPU.
- There are many things to consider when designing a self-respecting router! how do routers handle packet jams? What if many packets all want to go through a specific output port? Are there priorities governing the flow of packets? We will see some answers to these questions in the following more detailed subsections about the internals of routers.

### Input Processing:
- The following diagram shows a detailed description of how input ports work:
![Input port processing](img/inputPortProcessing.png)
- An input port implements the physical-layer and link-layer for an individual input link. The lookup function is executed at the input port. It is in the input port that the router uses the forwarding table to decide which output port to forward a packet to via the switching fabric. The router processor computes and updates the forwarding table but a *shadow copy* of the forwarding table is usually stored in each input port. The forwarding table is copied to the "line cards" (*whatever these are!!*) over a separate bus. The shadow copies of the forwarding table in each port allow each port to make forwarding decisions locally without referring to the routing processor for each packet.
- The ports don't just search the forwarding table linearly as they can receive several Gbps of data which they need to process in mere nanoseconds. The lookup is done in hardware and specialized algorithms are used to do such lookup. Embedded on-chip DRAM and SRAM memories are also used to speedup lookup. There is talk of a certain *ternary content address memories (TCAMs)* which returns a forwarding table entry in constant time. Each input port has its CAM or TCAM.
- Once the lookup determines which output port the packet needs to be forwarded to, it sends the packet to the switching fabric. Sometimes, a packet might be blocked temporarily from entering the switching fabric because packets from another input port are passing through the fabric. Blocked packets are queued and scheduled to be passed to the switching fabric at a later time. Queuing can be done in both input and output processors as we will see later. A few other operations are performed at the input router such as checking packet checksum, version number and time-to-live, etc.
- Input port processing which involves looking up an address (*match*) and sending a packet into the switching fabric (*action*) is a specific case of general abstraction called *match plus action*. Other network components also use this abstraction such as link-layer switches which do destination addresses lookup before sending frames to the switching fabric, and firewalls which would filter packets that don't match certain criteria such as a combination of source/destination IP addresses and transport-layer port numbers.

### Switching:
![Three switching techniques](img/switchingTechniques.png)
- The switching fabric is a fundamental component of the router which uses it to switch (forward) packets from input ports to output ports. As the image above depicts, switching can be done in one of 3 ways:
	- **Switching via memory**: Earlier routers were simple and acted like traditional computers. Switching was done directly by the CPU (routing processor). Input and output ports acted as IO devices. When an input port received a packet, it signaled the routing processor with an interrupt, which copied the packet to main memory, extracted its destination addresses, looked up the output port in the forwarding table, and then copied it to the output port's buffer. Memory acted as a bottleneck in this system and only one packet could be forwarded at a time because only one memory read/write operation could be done over the shared system bus. Routers still perform switching via memory, but instead of doing it in the routing CPU, the lookup and storage in appropriate memory locations is done by processing on the *input line cards*. I believe in this scheme multiple packets can be written read concurrently, but don't take my word for it. 
	- **Switching via a bus** involves moving a packet directly from the input port to the appropriate output port through a shared bus by prepending the packet with a header that indicates the destination output port. All the output ports will receive the packet, but only the port with the matching label keeps the packet while others discard it. The label is then stripped from the packet because that label is only used within the switch. If multiple packets arrive at the router input at the same time (even when targeting different input ports), they all must wait but one packet because only one packet can pass through the shared bus at a time. The switching speed in such switches is bottlenecked by the speed of the bus. Such routers are OK for small local networks and enterprise networks. 
	- **Switching via an interconnection network**: The limitations of a single shared bus can be replaced by the use of an interconnection network. In a router with ***N*** input ports and ***N*** output ports, there are ***2N*** buses connecting the two types of ports. These buses have switches that get opened and closed by the switching fabric controller. Multiple packets arriving at multiple different input ports and destined for multiple different output ports can be forwarded simultaneously.

### Output Processing:
![Output port processing](img/outputPortProcessing.png)
- The image above shows a how output port's processing is done. It takes packets stored in the output port's memory and transmits them to the output link after it selects them and dequeues them for transmission. 

### Where Does Queuing Occur?
- 

### Routing Control Plane:



## The Internet Protocol: Forwarding and Addressing in the Internet:
## Routing Algorithms:
## Routing in the Internet:
## Broadcast and Multicast Routing: