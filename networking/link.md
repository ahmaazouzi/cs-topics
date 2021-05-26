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

## What's the Link Layer All about?
## Techniques of Error Detection and Correction:
## Multiple Access Links and Protocols: 
## Switched Local Area Networks:
## Link Virtualization: Network as a Link Layer:
## Data Center Networking:
## Actual Day in the Life of a Web page Request: