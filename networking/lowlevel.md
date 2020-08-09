# Notes on Low Level Networking:
##  Physical Layer:
- Messages are send through a wire using a signal of some sort, maybe an alternation of different voltage levels (let's say between 0V and 5V). The trick is in timing. You can have 2 seconds of 5V, 1 second of 0V, 5 seconds of 5V, 4 seconds of 0V. Your 5V and 0V are called **symbols**; they are used to represent information of sorts: 1 bit for example can be represented by 5V and 0Vs is used to represent a 0 bit.
- The rate at which the symbols are sent is called the **symbol rate**. Symbol rate of 1 signal per second is a 1 **baud** symbol rate. 10 symbols per second is 0.1 baud.
- Information can be shared in network using a variety of ways including **copper wire**, **fiber optics** where a beam of light keeps getting reflected through two layers of fiber glass until it reaches the other end. **RF** (radio frequency) uses something similar which I don't understand, but generally speaking you alternate between two symbols which get converted by the machine to a binary format??!!
- It common for computers to have different clock rates which means they can't communicate correctly. Communication between the two results in **clock slips** if the sending computer is faster than the receiving machine or extra bits vice-versa. Multiple ways are used to achieve a **synchronized clock** between different computers in order to communicate correctly: they include **GPS antennas** (GPS satellites have atomic clocks that can be used to synchronize machines), the machines themselves can have **atomic clocks**, but these are expansive and largely unpractical solutions. You might also have two wires one for the data and the other for clock rate so that the sending computer's clock rate is used by the receiver to read the data accurately, but this technique is also mired with problems.
- A smarter workaround combines both the data and the clock rate, but uses different symbols. Instead of having 0V represent 0 and 5V represent 1, a 0 is represented by a transition from 5V to 0V and a 1 is represented by a transition from 0V to 5V. This is called **Manchester coding**.

## Framing:
- The data a machine sends or receives is just a string of 1s and 0s and there is no way for machine to know exactly how start reading it. Where does a letter or number start or end? Does a binary string represent one small number or two? To solve this problem we use **framing** which a way of delimiting data before it's sent. There are several framing schemes that divide data into **frames** (which usually are around 1000-bite long). There are different framing protocols such as:
	1. **HDLC (High Level-Data Link Control)**: In this protocol each frame starts with a **flag** which follows the pattern **`01111110`**. There are cases where a sequence of bits are similar to the flag even though they are not meant to signal the beginning of a new frame. In such cases the protocol stuffs an extra zero after each string of 5 ones in what's called **bit stuffing**. The receiver will ignore every zero that follows 5 one bits. THis way, it knows exactly that a flag is the start of a new frame.
	2. **Ethernet** frames are kinda more elaborate. They are separated by a silent gap of zeros (no signal) which is required to be at least 96 bits in length. This is called an **IFG (Inter-frame Gap)**. Following the IFG is a **preamble** of 56 bits which is the start of a frame it's a pattern of ones each followed by a zero **`10101010101010101010101010101010101010101010101010101010`**. The preamble is followed by the **SFD (Start of Frame Delimiter)**. THe SFD is one byte that has alternating 1s and 0s just like the preamble except for the last bit which is a one instead of a 0: **`10101011`**. Following the SFD comes the data which is a combination of payload and meta-data which we will see later. The size of a frame tends to be between 64 and 1500 bytes. It's not recommended to have very large frames because errors are always a possibility and in the case of an error we don't want to resend a very large frame. In the case of reasonably sized frames we might only need to resent a small amount of data to recover from an error. There are situation where large frames (called **jumbo frames** of 9000 bytes are used).
- Frames are a **data link layer** concept. There two main data link types, **PTP (point to point)** and **multi-point** or **broadcast** data links. PTP is where to computers talk directly to each other. A computer simply put data into frames and send them directly to another. This is mainly used by ISPs where networking equipment in different cities are linked through PTP and where fiber glass might usually be used. They cover large distances. Multipoint data link is where data is broadcast to the whole network where each computer in the network can receive the data sent by our computer. Examples of a multi-point data link include a wireless network where all computers can communicate directly with each other, a cable residential broadband network, and Ethernet network.
- An Ethernet frame generally follows this format (called **Ethernet Logical Link Control (LLC)**):
```
+----------------+---------------+-----------+----------+--------------/ /--+-----------------+
|  Preamble/SFD  |  Destination  |  Source   |   Ether  |    Payload        |  Frame Check    |
|                |    Address    |  Address  |   Type   |    Payload        |    Sequence     |
+----------------+---------------+-----------+----------+--------------/ /--+-----------------+
     8B(7B/1B)           6B            6B          2B         Varies                   4B
```
- The **destination address** and **source address** are called Ethernet Addresses or **Mac Addresses**. These are unique addresses built into the hardware of a computer. They look as follows: **`01:0D:F2:23:AA:0E`**. To send a message to another computer in the same Ethernet network, the destination address of the computer you wanna send to is placed in the destination address of the frame and the source in source address. The data is then sent to the Ethernet switch of the network which will forward it to the destination computer if it has its address. If doesn't have that address, it sends it to all computers in the network. The computer whose address matches the message's destination address will read it and other computers just ignore it. To send the data to all other computers in the network the destination address should have the address **`FF:FF:FF:FF:FF:FF`**.
- The **`Ether type`** is a 2 byte field that gives information on the format of the payload of the frame. The most common Ether type is IP (an Internet packet) that has the value **`0800`**.
- The **payload** is the content itself and other stuff. Its size has a usual upper limit of 1500 bytes but can be as big as 9000 bytes as in the case of the aforementioned jumbo frames.
- The **Frame check sequence** (4 bytes) is a number computed based on the content of the frame (from the destination source to the payload). The receiving computer recomputes this number and if it doesn't match the received number it detects an error. 
- Other data link protocols have different frame formats such the PPP format which we will not cover here!

## Layers:
- In the last two sections we touched on the bottom two networking layers (in both the **OSI** and **TCP/IP** models).
- The **physical layer** has to do with the physical properties of networks and how signal is transmitted through these. These include copper wire, fiber optics and radio frequency. We also covered methods of synchronizing clocks and data encoding between computers in what is called Manchester code. There are equivalent methods in other media such as **QAM** and **NRZ**.
- The **data link** is all about framing and data format. We covered two widely used data links protocols Ethernet which uses preambles and SFDs to delimit frames and HDLC which uses flags instead. We also covered the Ethernet frame format (called Ethernet LLC (logical link control)) and mentioned the PPP LLC. 

## The Internet Protocol:
- How would a computer in an Ethernet network in Bangalore communicate with another computer in an Ethernet network in Lucknow?
- Most probably Lucknow is connected to Bangalore through multiple PPP links. A PPP node can only send data to another PPP node that is directly connected to it. How can data be forwarded between the different PPP links?
- Let's call our source computer host A and our destination host B. When host A sends data, none of the computers in the Bangalore network will receive it because none of them has the destination address specified in the frames sent by host A. Another problem is that the PPP links don't understand mac addresses. To solve this problem we need a universal address that is not specific to a certain type of link. The solution is the **Internet Protocol (IP)** which is a protocol used to connect multiple networks. 
- The PPP nodes are also **IP routers**. The IP router connected to the Bangalore network will receive a packet containing a destination IP address and then decides which route it forwards to. When the routing decision is made the message is encapsulated into a PPP frame that will be send to the specified PPP node.
- Routers serve two purposes:
	1. **Routing** which is the process of building **routing tables** which map IP addresses to routes.
	2. **Forwarding** is the actual transfer of the packet from one router to another until the packet reaches its destination.
- An IP address is a 32-bit value. There are 2<sup>32</sup> possible IP addresses (about 4 billion). The protocol geeks were afraid we'd run out of IP addresses so they add another IP address scheme called IPv6 to mitigate their fears. This one has 2<sup>128</sup> possible IP addresses.
- The router does a lot of hard work but it doesn't have to store all 4 billion IP addresses in its routing table. It can just store the first 2 bytes of IP ranges and the first 3 IP address ranges which correspond to other routers. It might store the actual addresses that are directly linked to it. The router will search its table and match the IP address it receives to the longest matching entry in its table.

## The Journey of a Packet over the Internet:
- When trying to send data to Lucknow, the IP packet makes part of the the Ethernet frame payload. The destination address of this frame, however, is not the final destination but is the first router the message needs to go to. The sender doesn't automatically know the MAC address of this router. The computer has to somehow be configured to know the IP address of the router. The sender will first check if destination IP against the subnet mask (the 24-bit significant range of an IP address) and if it is not there, the packet will be sent to the router.
- Before sending the frame to the router, however, host A needs to discover the router. The host broadcasts to all other computers in the network asking if they have the router's IP address and if so send back a response containing the mac address of the router. This is called **Address Resolution Protocol (ARP)**. ARP is the payload of the Ethernet frame (whose Ether type is **`0806`** meaning that the payload is of type ARP) and it looks as follows:
```
+------------+-----------+----------+----------+-----+--------------+---------------+---------------+---------------+
| HW Address | Protocol  |  HW Addr | Protocol | Op  | Hardware Addr| Protocol Addr | Hardware Addr | Protocol Addr |
|  Type      | Addr Type |  Length  | Addr Len | Code|   of Sender  |   Of Sender   |   Of Target   |   Of Target   |
+------------+-----------+----------+----------+-----+--------------+---------------+---------------+---------------+
```
- The different segments of the ARP packet have the following meanings:
	* **HW address Type**: this is usually **`1`** because we are using Ethernet (The protocol we want to map to).
	* **Protocol address Type**: most probably **`0800`** since we are trying to map hardware address to the IP protocol.
	* **HW address Length**: most probably **`6`** for Ethernet (Mac Addresses are 6 bytes in length).
	* **Protocol address Length**: matches IP address length which is **`4`** bytes (for IPv4).
	* **Op Code**: can be either a **`1`** or **`2`**. 1 for a broadcast question when host A is searching for the router, and 2 when the host A receives a response from the router telling it that it has the given hadrware address.
	* **HW address of Sender**: Mac Address of the sender
	* **Protocol address of Sender** IP Address of the sender.
	* **HW address of Target** ... 
	* **Protocol address of Target** ...
- Basically, if the IP address is not in the subnet mask, host A broadcasts an Ethernet frame whose payload is an ARP packet. The ARP asks "who owns the router's IP?". The router responds with a frame that also containing an ARP packet where it gives its MAC address to the host A. Now that host A has the MAC address of the router it can send it what it wants.
- Now that host A has successfully located the router, it sends it a frame with Ether type **0800** meaning it is a frame of type IP. The payload of this frame contains an IP packet which consists of a an **IP header**  which has some information about the IP packet and some of kid of body or payload.
- The header of an IP packet is usually made of 5 or 6 32-bit words which contain information on how the IP packet should behave in the network. Important information in the header include the IP version (IPv4 or IPv6), the time to live (to prevent the packets from looping forever in the Internet), the source and destination addresses, the header checksum for error checking, the protocol field which indicates the type of the protocol inside the IP's body ... etc.
- Once our packet reaches the first router it will hop from one router to another following a path set to it by the routing tables of each router until it reaches the final router where the destination IP address is detected. Now this router will do some ARP voodoo and asks for the Mac address of the computer that has that IP address and then it goes there.

## TCP:
- There is only so much data you can fit inside a data link frame which means you have to split that data into multiple packets which you stuff inside the frames. Data sent in chunks stuffed inside multiple frames are not always guaranteed to arrived safe to the destination IP address. There is a very high chance many of these packets get lost in the way due to multiple reasons in the physical or other layers such routers or links between routers becoming congested. Losing packets means we might get incomplete garbage data on the other end of the communication line. Packets might also arrive not in the order they were sent because they might have taken different routes. **Transmission Control Protocol (TCP)** is the savior here. It provides a **byte stream service** that is **connection oriented** and **reliable**. It kinda mimics a phone call. It involves a **handshaking** which establishes that two computers can talk to each other before they can send data to each other.
- The TCP segment itself is encapsulated inside an IP datagram. It, too, has a header which contains important data about how it travels through the network. The IP protocol number for TCP is **`6`**. 
- The **source port** and **destination port** are important TCP headers. A computer can connect to the rest of the world through multiple **ports**. These two headers tell ports apart. TCP connections are also bidirectional. TCP also provides its own **checksum** to account for errors.
- When two computers are communication using TCP, the computer that initiates the connection is called the client and the other is the server but once the connection is established data starts flowing in both directions. TCP needs two pieces of information, the IP address and the port number as in **`127.0.0.1:3000`**.
- I will cover more of TCP in other articles.













