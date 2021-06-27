# Wireless and Mobile Networks:

## Table of Contents:

## Introduction:
- Wireless is king in our days. The reason a separate chapter was dedicated to to wireless networking is that poses challenges that are different challenged encountered in traditional wired networks at both the data link and network layers. 
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
## WiFi: 802.11 Wireless LANs:
## Cellular Internet Access:
## Mobility Management, Principles:
## Mobile IP:
## Managing Mobility in Cellular Networks:
## Wireless Mobility, Impacts on Higher-Layer Protocols: