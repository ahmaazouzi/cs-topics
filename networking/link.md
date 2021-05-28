# The Link Layer: Links, Access Networks, and LANs:
## Introduction:
- In the network layer, we saw how a packet travels from a source host to a destination host traversing a series of links (wired or wireless) and packet switches (routers or and switches).
- When thinking about what goes below the network layer at the *link layer*
	- How does a datagram ravel through each one of the *individual links* that make up its end-to-end path?
	- How are network layer datagrams encapsulated in link layer frames for transmission over a link?
	- Do links in a path use different link-layer protocols?
	- How does a switch differ from a router?
	- Does link layer use addressing and how does this addressing interoperate with the network-layer addressing?
- These questions and others will be answered in this document. While trying to answer these questions we will familiarize ourselves with the two fundamental types of link-layer channels:
	- *Broadcast* channels which connect multiple hosts and are used in wireless LANs, satellite networks and hybrid fiber-coaxial cable (HFC). The fact that multiple hosts are connected to the same broadcast channel requires the use of medium access protocols to coordinate frame transmission. 
	- *Point-to-point* links such as a long-distance link connecting two routers or a host and an Ethernet switch. The point-to-point (PPP) is used to coordinate frame transmission in this kinda link.
- Other topics we will touch upon include:
	- Error detection and correction.
	- Multiple access networks especially the famed Ethernet.
	- Virtual LANS.
	- Data center Networks.
- We will not discuss WiFi but leave it to another day when discussing wireless networking.

## Preliminaries:
- Let's start with a few definitions:
	- A **node** in a link-layer context is any device that runs a link-layer protocols. This includes hosts, switches, and WiFi access points. 
	- **Links** are the communication channels connecting adjacent nodes along a communication path. "In order for a datagram to be transferred from source host to destination host, it must be moved over each of the individual links in the end-to-end path." The following figure shows the path of a datagram from a wireless host and a server. It passes through six links:
		1. A WiFi link between the sending hot and a WiFi access point.
		2. An Ethernet link between the WiFi access point and a link-layer switch. 
		3. A link (probably Ethernet) between the link-layer switch and a router.
		4. A link between the aforementioned router and another router.
		5. An Ethernet layer connecting the previous router to a link-layer switch.
		6. An Ethernet link connecting the switch to the server.
![Six link-layer hops](img/linkHops.png)
	- A node encapsulates a datagram into a **link-layer frame** and transmits it into the link. 
- The book provides a nice analogy of the relationship between the link layer and network layer, but you know I hate analogies!

### The Services Provided by the Link Layer:
- The basic role of the link layer is moving a datagram from node to an adjacent node over a single communication link, but the details of what services can be offered vary from one protocol to another. Common services offered by link-layer protocols include:
	- **Framing**: Most link-layer protocols encapsulate datagrams in frames. A frame consists of a data field which contains the datagram and a set of header fields. The structure of a frame differs from one link-layer protocol to the next. We will soon see some link layer protocols and their frame structures. 
	- **Link access**: A **medium access control (MAC)** protocols defines the rules by which a frame is is transmitted into the link. For point-to-point links, the MAC is simple or nonexistent since the link has a single receiver at one end and a single destination at the other. The sender can send frames whenever the link is *idle*.
	- **Reliable delivery**: A link-layer protocol guarantees moving a datagram through a link without error! This is similar to what TCP does at the transport layer, but does it only over a single link and not end-to-end because the link layer only operates over a single link between two adjacent nodes. Reliable delivery is also achieved by acknowledgments and retransmissions just like TCP. Reliable delivery is used in links prone to high error rates such as wireless links, but many wired links don't have these errors so protocols used in some wired links don't bother about reliable delivery. 
	- **Error detection and correction**: *This might seem like a subset of reliable delivery!!* Hardware signal noise can cause bit errors in frames. Many link-layer protocols provide mechanisms for detecting and correcting such errors. This is done by appending error-detection bits by the sender in each frame and having the receiver do error checks. Link-layer error detection is more sophisticated than what we saw in TCP and it's done in hardware. The receiver detects when and exactly where an error occurred in a frame and then corrects this error!! *Wow, interesting! Does this mean there is no reason to retransmit the frame?*

### Where Is the Link Layer Implemented?
- Where do hosts implement the link layer? Is it implemented in software or hardware, and how does it interact with the other components of the computer's hardware and software? The link layer is implemented in a hardware piece called the **network adapter** or the **network interface card (NIC)**. At the heart of the NIC is the *link-layer controller* which is a special-purpose chip that implements link-layer services such as framing and error detection. NICs used to be separate components, but are mostly now integrated into the computer's motherboard. 
- On the sending side, the controller encapsulates a datagram into frame, a possibly adds error bits to the frame, and transmits the frame into the link. On the receiving end, the controller receives the frame, possibly performs error checking and then extracts the datagram from the frame.
- For the computer, the NIC and the controller are an IO device. Most of the of link layer functionality is implemented in the NIC hardware, but some is also implemented in software running on the host's CPU. Such functionality includes assembling link-layer addressing :confused:, and activating the controller. On the receiving host, link-layer software in the CPU responds to controller's interrupts,  handles errors and passes the extracted datagram to the network layer. 

## Techniques of Error Detection and Correction:
- **Bit-level error detection and correction** refers to detecting and correcting the corruption of bits in a link-layer frame that has been sent from a node to a physically adjacent node over a link. Both detection and correction are often provided by the link layer but not always. 
- We will only grate the surface of this subject here as there whole books dedicated to it.
- The following figure shows the steps of how link-layer error detection and correction is done:
![Steps of error detection and correction](img/edc.png)
- As the figure shows, before sending the data D (this also include other frame header fields, etc.), the sending node augments it with error-detection and error-detection bits (EDC).
- The receiving node receives a sequence of bits D' and EDC' which might differ from the original D and EDC due to possible link transit bit corruption. The receiver needs to determine whether D' and EDC' are the same as D and EDC'. The receiver can only determine if an error has been detected which is different from determining if the error has or has not occurred. EDC can only sometimes determine if an error has occurred. It cannot always detect an actual error. There can acktchyually be **undetected bit errors**! Wow! This results in some corrupt datagrams. The goal is to have error-detection and correction schemes that keep the probability of undetected bit errors low, but such schemes can lead to larger overhead. 
- The following subsections will give overview of some common error-detection and correction techniques. 

### Parity Checks: 
- The simplest form of error detection can be done with a single **parity bit**. You can either use an even or odd parity bit. In even parity, we add an extra bit to D such that the total number of bits in EDC whose value is 1 is even. The receiving node counts the number of bits whose value is 1, and if they are odd, the node determines there was an error. At least one bit error has occurred, or more precisely: an odd number of errors has occurred. If an even number of errors has occurred, then the errors go undetected. 
- Experience has shown that, rather than occurring independently of each other, bit errors occur in bursts meaning that single bit parity checks are next to useless. 
- The one-bit parity scheme can be generalized into a *two-dimensional parity* scheme for more robustness. The bits in D can be divided into i columns and j rows and a parity value is calculated for each row and each column as the following figure shows:
![Two-dimensional parity](img/2Dparity.png)
- If an error occurs at a given bit, both the row and column where it occurred will be affected. The receiver can detect the error and also locate exactly where it happened and then correct it. 2D-parity matrices can also detect and correct errors in the parity bit themselves although I have no idea how! 
- The ability of the receiver to both detect and correct errors is called **forward error correct (FEC)**. This technique is used in audio storage and playback devices such as CDs. They can be used by themselves or with other techniques such as retransmission in the way we saw with TCP to recover from errors. The good thing about FEC is that it allows for immediate error correction and reduces the number of retransmissions. This is especially useful for real-time applications. 

### Checksumming Methods:
- With checksumming (we've seen it in the transport document), the bits of a packet are treated as a sequence of k-bit integers. These k-bit integers can be added together to produce a sum which is used for error detection. The 1s complement of this sum is sent as a checksum with the data. The receiver takes the 1s complement of the received data (including the checksum). The result should be all 1 bits, but if any of the bits is 0 this means an error has occurred. 
- Checksumming is used in transport layer with TCP, but not in the link layer which uses the more robust cyclic redundancy check (CRC). The latter requires more computations so it is implemented in hardware. 

### Cyclic Redundancy Check(CRC):
- The basic idea of **cyclic redundancy check (CRC)** is follows:
	- The data to be sent can be represented by D. 
	- The sender and receiver agrees on an r + 1 bit pattern called a *generator* which we can represent by G.
	- The sender chooses r bits R and appends them to D such that the resulting d + r bit pattern is exactly divisible by G (The remainder is 0).
	- The receiver divides the received pattern by G. If the result is a nonzero, the receiver detects an error.
- The idea seems fairly basic and clear, but the authors love to waffle on about details.

## Multiple Access Links and Protocols: 
-
### Channel Partitioning Protocols:
-

### Random Access Protocols:
-

### Taking-Turns Protocols:
-

### The Link-Layer Protocol for Cable Internet Access:
-

## Switched Local Area Networks:
-

## Link Virtualization: Network as a Link Layer:
-

## Data Center Networking:
-

## Actual Day in the Life of a Web page Request:
-





