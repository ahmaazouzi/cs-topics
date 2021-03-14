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


## Virtual Circuit and Datagram Networks:
## Inside a Router:
## The Internet Protocol: Forwarding and Addressing in the Internet:
## Routing Algorithms:
## Routing in the Internet:
## Broadcast and Multicast Routing: