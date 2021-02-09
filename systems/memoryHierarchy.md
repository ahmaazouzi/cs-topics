# The Memory Hierarchy:
- *Virtual memory*, an OS abstraction, gives the illusion that memory is just a long linear byte-array that holds instructions and data for the CPU which can access different parts of this memory at a constant time, but the reality is much more complicated. 
- The actual hardware that constitutes a system's memory is divided up into a hierarchy of different storage devices that differ in their speed and cost, and each one of these storage devices acts as a caching facility for the device that lies under it in this hierarchy. The CPU registers hold most used data, while *cache memories* act as a staging area for main memory. Main memory act as a staging area for storage disk and the latter is a cache for the network. 
- This hierarchical setup allows well-written programs to both exploit the high speed of the costly small memories and have access to the vast cheap memories. To have a 'well-written' program that makes use of this hierarchy, you need understand how a system moves data up and down this hierarchy (this is what we will be doing here)!
- A fundamental concept we will be dealing with in this document is *locality*, a feature of programs that tend to access the same data over and over again and access nearby data and usually from the upper levels of the memory hierarchy. In a way this document is an extension of the previous document about optimization. We want to have faster programs and memory is often a bottleneck that needs to be broken.
- We will look at different memory and storage technologies: stuff like *SRAM*, *DRAM*, *ROM*, *rotating* and *solid state* disks. We will also look at cache memories and their impact on program efficiency. We will analyze programs' locality. 

## Storage Technologies:
### Random-Access Memory:
- Random-access memory (RAM) exists in two types: **static RAM (SRAM)** which is faster and much more expensive and used for caching in the CPU and outside of it, and **dynamic RAM (DRAM)** which is used for main memory and the *frame buffer for graphics* :confused:! The system used to type this document has a couple megabytes of SRAM and sever gigabytes of DRAM. 

#### SRAM:
|  | Transistors per bit | Relative Access Time | Persistent | Sensitive | Relative cost | Applications |
| --- | --- | --- | --- | --- | --- |
| SRAM | 6 | 1x | Yes | No | 100x | Cache Memory |
| DRAM | 1 | 10x | No | Yes | 1x | Main memory, frame buffers |


#### DRAM:
#### Conventional DRAMs:
#### Memory Modules:
#### Enhanced DRAMs
#### Non-Volatile Memories:
#### Accessing Main Memory:


### Disk Storage:
### Solid State Disks:
### Storage Technology Trends:

## Locality:
## The Memory Hierarchy:
## Cache Memories:
## Writing Cache-Friendly Programs:
## The Impact of Caches on Program Performance: