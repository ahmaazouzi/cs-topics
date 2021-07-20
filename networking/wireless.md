# Wireless and Mobile Networks:

## Table of Contents:

## Introduction:
- Wireless is king in our days. The reason a separate chapter was dedicated to to wireless networking is that it poses challenges that are different from the challenges encountered in traditional wired networks at both the data link and network layers. 
- This chapter will try to tackle the wireless networking and the issue of mobility and how wireless networking relates and compares to traditional wired networking. 
- Specific topics we will see include:
	- How a device connects to the network through a wireless link.
	- How multiple access is done in wireless links, with a focus on CDMA.
	- How wireless LANs work at the link level with such protocols as IEEE 802.11 (WiFi), Bluetooth, etc.
	- How cellular Internet works with 3G and 4G technologies.
	- The issue of mobility and networking and how it's tackled with mobile IP and GSM.
	- The effect of wireless links and mobility on transport-layer protocols and networked applications. 
- *I will just skim over these topics and not spend to much time trying to summarize the material*.

## Components of a Wireless Network:
- A wireless network (regardless of whether it covers a large area such as a cellular network or a smaller one like WiFi) generally consists of:
	- **Wireless hosts**.
	- **Wireless communication links** that connect wireless hosts and base stations. Communication links differ mainly in their *transmission rates* and *coverage areas*. WiFi for example covers a small area of a few dozen meters, but has a high transmission rate, as opposed to to some cellular network (2G)links which cover areas with radii of several kilometers but has a lower transmission rates. These characteristics are not static, however, as WiFi and cellular technologies evolve over time and acquire higher transmission rates and might cover larger areas. 
	- **Base station** is the point in a wireless network that is responsible for sending and receiving data from wireless hosts. The base station coordinates transmission between hosts, and connects the hosts to the larger network infrastructure. The base point basically acts as a link-layer relay between the hosts and the larger "Internet" infrastructure. Examples of base stations include *cell towers* in cellular networks and *access points* in 802.11 wireless LANs. 
- The presence or absence of a base station external to hosts that controls the wireless network where these hosts exist means there are two types of networks:
	- **Infrastructure mode**: where the base station controls network services such as routing and IP address assignment to wireless hosts.
	- **Ad hoc mode**: where the wireless hosts themselves control such services.
- The mobility issue rises mainly in cellular networks. How would an IP connection be handled while you're driving and your connection in handed off from one cell tower to another? How are you located in the network? This is one aspect of the mobility issue that will talk about later. 
- Generally speaking, experts divide networks into 4 types depending on two factors: (1) whether a wireless network runs in infrastructure or ad hoc mode, and whether a packet crosses one or multiple wireless hops. These types are:
	1. *Single-hop, infrastructure-based*: which has a base station  connected to the Internet, and all communication in such network is between each host and the base station. Examples include 802.11 LANs and 3G cellular networks.
	2. *Single-hop, infrastructureless*: lacks a base station connected to the Internet. One of the hosts participating in this network may coordinate the communication between devices. Examples include Bluetooth and 802.11 running in ad hoc mode.
	3. *Multi-hop, infrastructure-based*: Includes a base station connected to the Internet, but nodes can be used as relay packets from and to the base station. Examples include *wireless mesh networks* :confused:.
	4. *Multi-hop, infrastructureless*: has no base station and nodes can be used as relays. Nodes might also be mobile. Examples include *mobile ad hock networks (MANETS)* and *vehicular ad hoc networks (VANET)*.
	- The rest of this chapter will focus on single hop infrastructure-based networks. 

## Wireless Links and Network Characteristics:
- Differences between a wired and a wireless network lie obviously in the physical and link layers while the upper layers such as the network layer are the same. Some of the more important differences include: 
	- **Decreasing signal strength**: Radio signal gets weaker as it passes through thick matter such as WiFi passing through some thick walls. It also decreases even in free space as the distance between the sender and receiver gets larger. 
	- **Interference from other sources**: Radio signal sources transmitting in the same band interfere with each other. 2.4 GHz wireless phones for example interfere with 802.11 wireless LANs. Electromagnetic noise from nearby sources such as a microwave or a motor is a larger problem in wireless than wired networks.
	- **Multipath propagation**: This is caused by signal reflecting off objects. It arrives blurred to the receiver :confused:.
- These characteristics mean that wireless channels are more prone to errors. To mitigate these errors, wireless protocols such 802.11 provide strong error detection. It even provides *link-level reliable data transfer* which retransmits corrupted frames.
- The signal that arrives at the receiving host is not as clean and nice as when it was sent. It undergoes all the side effects we've just mentioned (decreasing signal strength, interference and multipath propagation), so the receiver receives distorted signal mixed with background noise. This requires the wireless protocols to employ strong CRC error detection and link-layer reliable data transfer techniques to retransmit corrupt frames.
- The received signal then is a mix of a degraded version of the original signal (degraded due to multipath propagation and interference with other signal) and background noise. The degradation and background noise might be too high that the strength of the original signal is severely reduced. How can we measure the strength of this signal? **Signal-to-noise ratio (SNR)** is one indicator used by engineers to measure the strength of the received signal. There is technical voodoo involved in this SNR that my feeble brain and can't and probably shouldn't even try to understand. Anyways, higher SNR means stronger signal which also means it's easier for the receiver to extract the transmitted signal from the background noise.
- Another measure of signal strength is **bit error rate (BER)** which measures the probability that a transmitted bit is in error. There is also another thing called modulation and I have no idea what it is, but let's just say that different modulation schemes have different transmission rates.
- Considering these three physical-layer factors (SNR, BER, modulation technique transmission rate), we can say that the physical layer of wireless networking have the following characteristics:
	- *"For a given modulation scheme, the higher the SNR, the lower the BER."* Increasing SNR requires higher transmission power (e.g phone battery). It might be wasteful to keep increasing SNR beyond a certain threshold because you are using more energy and not getting any lower BER. Even worse, very unnecessarily high SNR of a sender might interfere with other senders.
	- *"For a given SNR, a modulation technique with a higher bit transmission rate (whether in error or not) will have a higher BER"*
	- *"Dynamic selection of the physical-layer modulation technique can be used to adapt the modulation technique to channel conditions."* SNR (and as a result BER) change due to mobility. We need a higher transmission rate with the least possible BER. Wireless protocols use what is called adaptive modulation where modulation techniques are selected dynamically while a device is moving around signal sources. The device tries to use the modulation technique with the highest transmission rate and the lowest BER. 
- Another characteristic or problem that wireless networks suffer from is the so-called **hidden terminal problem** where two stations A and B cannot communicate with each other due to fading (long distance between the two stations) or due to a physical barrier, but there is a third station C which is visible to both. The signal from A and B interfere at station C and have undetected collisions. This can make multiple access in wireless networks more challenging than wired ones.s

## WiFi: 802.11 Wireless LANs:
## Cellular Internet Access:
## Mobility Management, Principles:
## Mobile IP:
## Managing Mobility in Cellular Networks:
## Wireless Mobility, Impacts on Higher-Layer Protocols: