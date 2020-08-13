# Networking and Internet: an Overview:
## "I heard there is rumors on the Internets":
- Let's just say that the Internet is a gigantic network that connects millions or billions of **end systems** or **hosts**. The network itself is made of many **communication links** which intersect at **packed switches** which can be either **routers** or **link-layer switches**. The data itself is encapsulated into **packets** which are smallest discrete quantities of data that can be transported through a network at a certain abstraction level.
- The Internet is provided by **Internet Service Providers (ISPs)** which of which is "in itself a network of packet switches and communication links". ISPs are organized in some sort of a hierarchy. You have international and national ISPs and under those are residential ISPs, cable ISPs, university ISPs ...etc.
- Communication in the Internet and in any kind of network indeed is controlled and regulated with **protocols** and there is a ton of these. Networking is all about the protocols, baby! Internet Standards are developed by the **Internet Engineering Task Force(IETF)** through so-called **Requests for Comments (RFCs)** which define the different Internet protocols.
- From a programmer's perspective, the Internet is the infrastructure that allow **distributed applications** to exist. This type of application is not tied to a single computer. Instead it uses other computers to do its job. 

## Network Edge:
- We can think of the Internet and any network in general as consisting of an **edge** and a **core**. The edge is where end systems and hosts are. The computer on which this is being typed is part of the edge of the Internet and the home network it is connected to.
- At the edge of the Internet are so-called **access networks**. An access network is one that connects an end system to the first router in the Internet. It sounds like home routers are not part of such routers.
- Residential Networks get access to the Internet through several methods:
	+ **Digital Subscriber Line (DSL)**: in a DSL both telephone data and Internet data are transmitted between the home network modem and the **DSLAM (DSL Access Multiplexer)**. This DSLAM combines signal from telephone lines and from data allows both to pass to the home network. This data is encoded in different frequencies. At home, they get split by a splitter and  the modem extracts Internet data while phone data passes to the phone and there is no interference between the two as they are transmitted on different frequencies. DSL speed degrades as a function of distance from the DSLAM because it was optimized to work best in relatively short distances.
	+ In **Cable** the Internet is transmitted through cable television lines. It usually employs a combination of fiber optics and coaxial cables. The **cable modem termination system (CMTS)** plays the same role in cable access as in DSLAM in DSL.
	+ **Satellite** Internet.
	+ **Dial up**:  this one is especially painfully slow!
- **Local Area Networks (LAN)** were restricted to corporates and universities but have gradually become used in home networks where DSL or Cable are combined with LAN technologies to create wired or wireless LAN networks.

### A Primer on Physical Media Used in Networking:
- When a bit of information is sent from one end system to another it might morph into different forms as electrons moving through a wire or radio waves propagated in the air or as optic pulses in fiber-optic cable. These physical media can be divided into two types: **guided media** where bits are transmitted through solid media such as copper wire and **unguided media** where the data is propagated/broadcast in the air as waves for other systems to capture its signal.
- Some of the popular physical media used in networking including:
	1. **Twisted-Pair Copper:** These are used mainly for land line telephone. They consist of a pair of shielded copper wires twisted together to reduce interference from close-by electrical fields. Each pair is a single line of communication. These are popularly called Ethernet wires. One of form of these**Unshielded Twisted Pairs (UTP)** are used for computer networking. These are popularly called Ethernet cables. These usually have multiple pairs of wire. They can transmit data at a rate between 10 Mbps and 10Gbps. This rate is affected by the thickness of the wire and distance between the transmitter and receiver. This medium is inferior to fiber optics, but it is still in use and it's the de facto medium for LAN networks.
	2. **Coaxial Cable:** is a pair of concentric shielded copper wires. The inner wire is a thick wire while the outer one is a mesh of shorts. They are used in television and cable and can achieve high transmission rates.
	3. **Fiber Optics:** The data in these is transmitted through pulses of light. They result in very high bit rates and might not need any amplification for up to a 100 km. They are excellent for long distance links but are not very practical for LANs because the optical devices such as transmitters, switches and receivers are expansive.
	4. **Terrestrial Radio Channels:** These are convenient for users as they require no wiring and are divided into 3 categories: those that operate over 1 or 2 meters (I can't think of an example), those that operate within a short distance such as wifi and those that operate over a long distance such as cell phone towers..etc. 
	5. **Satellite Radio Channels**: These can provide relatively high speed internet where there is no cable/DSL.

## Network Core:
- The Internet core is the gigantic mesh of links and packet switches that connects end systems.
- There are two ways data can be moved through communication links: **packet switching** and **circuit switching**.

### Packet Switching:
- In packet switching messages are broken into packets, something like discrete amounts of bits, over communication links and packet switches (this can be either routers or link-layers switches). Transmitting such packets through multiple kinks and routers/switches involves so-called **store-and-forward**. Before a packet switch starts outputting the first bit of packet it receives, it must first receive the whole packet. After all, a switch/router must receive, store and process a packet before forwarding it. This results in some delay which is proportional to the number of links separating the communicating end-systems.
- A packet switch usually have multiple links attached to it. For each link, the packet switch has an **output queue (or output buffer)**. The output queue is used to store packets if the link is too busy or congested with other packets (this link might have a slower rate or it might be targeted by multiple links at the same time). The time a packet might spend in this buffer is called **queuing delay**. The queuing buffer is of a finite size and if the number of packets exceeds that size, some packets will be dropped (**packet loss**). Packet loss might occur to either packets already in the buffer or new coming packets. 
- The way a router/switch decides what link to forward a packet to is done with **forwarding tables**. **Routing protocols** are used to dynamically populate forwarding tables.

### Circuit Switching:
- This type of switching is based on reserving a path for exchanging bits. We mention it here only to tout the fact that packet switching is superior and much more scalable than circuit switching. It allows of a large number of simultaneous users of the network.

## Delay, Loss and Throughput in a Packet-Switched Network:
- The finite physical nature of the Internet and networks in general constrains the **throughput** (he amount of data per second that can be transferred through the network) leading to delay and packet loss.

### Delay:
- We've seen a couple types of delay earlier, but there are others which we will cover here in more detail. All these types of delay accumulate to produce what we called **total nodal delay**. The effects of delay can be clearly seen in real time systems such as in video chatting. Types of delay include (Remember that only one packet can be transmitted on a link at a time.):
	1. **Nodal processing delay**: Routers do to main types of processing that cause delay in the order of microseconds or less. These are deciding which link to direct a packet to and checking if the packet has any errors. After that the packet is directed to the queue preceding the appropriate link.
	2. **Queuing delay**: This is the delay a packet experiences while in a links queue. IF the queue is empty this delay is practically zero, but it is high if the queue is full.
	3. **Transmission delay**: A packet can only be transmitted after all the packets that went before it have been transmitted. Transmission delay is equivalent to the transmission rate of a link (10Mbps, 1Mbps ... etc.) This can be in the order of microseconds and even milliseconds. 
	4. **Propagation delay**: This is related to the propagation speed of links. Some media might be faster than others. For example, fiber optics are much faster than copper wires. The propagation delay is tied the distance of a link divided by the propagation rate of the link's medium. 
- Propagation delay might be confused with transmission delay, but they are different. Propagation is more related to the distance of the link while propagation is related to how much data is being transmitted through the link (packet size and how data a link can transmit at a time).

### Packet Loss:
- Queuing delay is an interesting beast and many PHDs and books were written about. It's mired in uncertainty as it depends on multiple factors such as packet sizes. Different packets will suffer from different queuing delay. Statistics and probability rules are used to measure queuing delay. The main side effects of queuing delays is packet loss. The size of a queue is finite and if a packet arrives at a full queue it gets dropped and lost in the core abyss! 

### End-to-End Delay and Others:
- **End-to-end** refers to the total delay between end systems. What we have looked at earlier was nodal delay which is delay in a single node between a computer and a router or between two routers. This type of delay can be examined using the famous **traceroute** utility.
- Other types of delay include delays caused by end systems themselves. End systems might throttle the rate at which they send data to a shared network to not congest it. Some applications such those using the VoIO protocol for video/voice chatting might take a very long time packetizing data hence causing so called packetization delay.


### Throughput:
- Throughput is generally the amount of data per second that can b transmitted between two end systems. Through can be subdivided into two types: **instantaneous throughput** which we can use to describe for example the right at which a file is being downloaded at a specific moment in time. The **average throughput** is the rate in bits per seconds at which an entire file is downloaded.
- Throughput seems very similar to transmission rate, but throughput is a combination of all overhead and other rates, not just the pure transmission rate of the link.
- Throughput might not be so obvious in a multi-link network where links have different throughput. Generally speaking the throughput in an end-to-end path is capped by the rate of the **bottleneck link** (the link with the lowest throughput).
- Today access networks are the real bottleneck! The core of the Internet operates at a very high speed.
- Another important consideration about throughput is when a link is linked to many links whose total throughput is larger than that link, then the throughput of that common link average throughput of all the links that feeds the common link. I hope that makes sense!! 

## Protocol Layers and Models:
- Networks are extremely complicated. Fortunately we have we use models to organize and simplify our knowledge about the structure and many components, protocols and technologies of networking.
- One great way of describing networking is the so-called layered architecture. Networking in general and networks are described into terms of layers of things. These layered models allow for modularity as parts of a complex system can be changed without affecting the overall system. They also allow us to discuss specific parts of a system without having to bother or be confused by what lies in other layers.
- Networking protocols are organized in simple layered models that do a great job at simplifying the dizzying nature of networks and allowing for easy understanding of how protocols (be they hardware or software protocols) do their job and interact with other protocols in other layers.
- One very popular layered networking model is the **seven-layer ISO OSI reference model**:

<table>
	<tr>
		<td>Application</td>
	</tr>
		</tr>
		<tr>
		<td>Presentation</td>
	</tr>
		</tr>
		<tr>
		<td>Session</td>
	</tr>
		<tr>
		<td>Transport</td>
	</tr>
		<tr>
		<td>Network</td>
	</tr>
		<tr>
		<td>Link</td>
	</tr>
		<tr>
		<td>Physical</td>
	</tr>
</table> 

- Another popular model which today's de facto model is the **five-layer Internet protocol stack**:

<table>
	<tr>
		<td>Application</td>
	</tr>
		<tr>
		<td>Transport</td>
	</tr>
		<tr>
		<td>Network</td>
	</tr>
		<tr>
		<td>Link</td>
	</tr>
		<tr>
		<td>Physical</td>
	</tr>
</table>

- Some people are opposed to protocol layering arguing that it introduces repetition such as the fact that indeed multiple protocols on different layers check for errors while this checking could have been done in just one layer. Interdependence between protocols from different layers kinda beats the purpose of layering which seems contrived and artificial.
- Layers be layering:
	+ **Application**: This is where protocols of specific applications exist. Here you have HTTP for web page applications, SMTP for email, DNS for website names, FTP for file transfer..etc. You can define your own protocols for your applications here use use the existing protocols. This layer's packets are called **messages**.
	+ **Transport**: packets here are called **segments** and this layer is all about transport. It breaks large application messages into manageable segments to transport them through the network. It has the two famous protocols **TCP** and **UDP**. TCP provides and connection-oriented type of transport and strives to establish reliability and recovery of lost segments and prevention of congestion. UDP just sends segments and doesn't care about too much control.
	+ **Network**: Packets are called **datagrams**. This layer acts like a postal service. The transport layer passes it information about the destination of the transport segment and this takes care of carrying the segment to the appropriate end-system. It includes the **IP** protocols which tells it where to forward the datagram and many types of **routing protocols** which guide the journey of a datagram.
	+ **Link**: The network needs the assistance of the link layer to move the datagram (which gets wrapped in a link layer **frame**) through a link. There are several link layer protocols such as Ethernet, WiFi, cable's DOCSIS and PPP. The same frame might be handled by different protocols before it reaches its final destination.
	+ **Physical**: Here individual bits move in the form of electrons, light pulses or radio waves through coaxial cable, UTP, fiber optics or air/the void. This layer's protocols are tied to the link layer's protocols, for example, Ethernet is both a link layer and physical layer protocol. 

- The **OSI** model is old and respected. It's mostly the same as the 5-layer Internet stack, except for two layers: the **presentation layer** which deal with application specific features such as compression and encryption, and the **session layer** which handles data synchronization and delimiting between applications. The Internet stack removes these two layers and delegates the responsibility of implementing them the app developer if she sees need for them. 

### Encapsulation in Networking:
- when you send a piece of data through the Internet or any other network, it moves up and down the network stack depending on multiple circumstances. This movement up and down the stack happens at different depths depending on the node: They can move through the whole 5 layers in an end system but can only travel through the 3 bottom layers in a router because those are all the layers a router needs to be useful. In a link-layer switch data moves up and own only the first 2 bottom layers. The following figure shows the steps of such a journey:
![End-to-end data journey (with and up and down the stack travel)](stack.png)
- An important concept that allows for this interlayer interaction **encapsulation**. Upper layer data is encapsulated in lower layer packets: meaning that a layer receives a packet from the layer above it, adds its **header** information to the received packet, thus constructing a packet of its kind.
- In the 5-layer Internet stack, an application layer message is passed down to the transport layer which adds transport layer header information to the application message thus turning it into an application layer segment. The transport header information allows the packet to be directed to the right application in the end system and checks for errors and maybe allows for reliability in the case of TCP. The segment is then passed to the network layer where it becomes the payload of a an IP datagram. It receives source and destination information which allows it to be routed to its final destination. The datagram is then encapsulated into a link layer frame which allow it to move through the a link the appropriate next node. Frames themselves are carefully arranged bit patterns that move through the underlying hardware. When the frames  are received by the application in the destination end system, they are reassembled and reconstructed back into the original messages that were sent by the original end system.
- This was a very brief and simplified overview of how a message moves through the network. In reality, there is much more to this process. One important process that take place in data's journey through the network is splitting large messages into smaller chunks that can be fitted inside a segment and breaking a segment up to parts that can be encapsulated inside datagrams... etc.
- The following figures is a better illustration of encapsulation:
<div>
![data journey 2](fivelayer.svg)
</div>

## Network Security:
## Networking History:
