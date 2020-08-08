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
	2. **Ethernet** frames are kinda more elaborate. They are separated by a silent gap of zeros (no signal) which is required to be at least 96 bits in length. This is called an **IFG (Inter-frame Gap)**. Following the IFG is a **preamble** of 56 bits which is the start of a frame it's a pattern of ones each followed by a zero**`10101010101010101010101010101010101010101010101010101010`**. The preamble is followed by the **SFD (Start of Frame Delimiter)**. THe SFD is one byte that has alternating 1s and 0s just like the preamble except for the last bit which is a one instead of a 0: **`10101011`**. Following the SFD comes the data which is a combination of payload and meta-data which we will see later. The size of a frame tends to be between 64 and 1500 bytes. It's not recommended to have very large frames because errors are always a possibility and in the case of an error we don't want to resend a very large frame. In the case of reasonably sized frames we might only need to resent a small amount of data to recover from an error. There are situation where large frames (called **jumbo frames** of 9000 bytes are used).
- Frames are a **data link layer** concept. There two main data link types, **PTP (point to point)** and **multi-point** or **broadcast** data links. PTP is where to computers talk directly to each other. A computer simply put data into frames and send them directly to another. This is mainly used by ISPs where networking equipment in different cities are linked through PTP and where fiber glass might usually be used. They cover large distances. Multipoint data link is where data is broadcast to the whole network where each computer in the network can receive the data sent by our computer. Examples of a multi-point data link include a wireless network where all computers can communicate directly with each other, a cable residential broadband network, and Ethernet network.
- An Ethernet frame generally follows this format (called **Ethernet Logical Link Control (LLC)**):
```
+----------------+---------------+-----------+----------+--------------/ /--+-----------------+
|  Preamble/SFD  |  Destination  |  Source   |   Ether  |    Payload      	|  Frame Check 	  |
|                | 	  Address    |  Address  |   Type   |    Payload      	|    Sequence     |
+----------------+---------------+-----------+----------+--------------/ /--+-----------------+
	8B(7B/1B)           6B            6B          2B		Varies                   4B
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
- 
