# The Memory Hierarchy:

## Table of Content:
* [Introduction](#introduction)
* [Storage Technologies](#storage-technologies)
	+ [Random-Access Memory](#random-access-memory)
		+ [SRAM](#sram)
		+ [DRAM](#dram)
		+ [Enhanced DRAMs](#enhanced-drams)
		+ [Non-Volatile Memories](#non-volatile-memories)
		+ [Accessing Main Memory](#accessing-main-memory)
	+ [Disk Storage](#disk-storage)
		+ [Disk Geometry](#disk-geometry)
		+ [Disk Capacity](#disk-capacity)
		+ [Disk Operation](#disk-operation)
		+ [Logical Disk Blocks](#logical-disk-blocks)
		+ [Connecting IO Devices](#connecting-io-devices)
		+ [Accessing Disks](#accessing-disks)
	+ [Solid State Disks](#solid-state-disks)
* [Locality](#locality)
* [The Memory Hierarchy](#the-memory-hierarchy)
	+ [Caching in the Memory Hierarchy](#caching-in-the-memory-hierarchy)
		+ [Cache Hits](#cache-hits)
		+ [Cache Misses](#cache-misses)
		+ [Kinds of Cache Misses](#kinds-of-cache-misses)
		+ [Cache Management](#cache-management)
	+ [Summary of Memory Hierarchy Concepts](#summary-of-memory-hierarchy-concepts)
* [Cache Memories](#cache-memories)
	+ [Generic Cache Memory Organization](#generic-cache-memory-organization)
	+ [Direct-Mapped Caches](#direct-mapped-caches)
		+ [Set Selection in Direct-Mapped Caches](#set-selection-in-direct-mapped-caches)
		+ [Line Matching in Direct-Mapped Caches](#line-matching-in-direct-mapped-caches)
		+ [Word Selection in Direct-Mapped Caches](#word-selection-in-direct-mapped-caches)
		+ [Line Replacement on Misses in Direct-Mapped Caches](#line-replacement-on-misses-in-direct-mapped-caches)
		+ [Putting It Together A Direct-Mapped Cache in Action](#putting-it-together-a-direct-mapped-cache-in-action)
		+ [Conflict Misses in Direct-Mapped Caches](#conflict-misses-in-direct-mapped-caches)
	+ [Set Associative Caches](#set-associative-caches)
	+ [Fully Associative Caches](#fully-associative-caches)
	+ [Issues with Writes](#issues-with-writes)
	+ [Anatomy of a Real Cache Hierarchy](#anatomy-of-a-real-cache-hierarchy)
	+ [Performance Impact of Cache Parameters](#performance-impact-of-cache-parameters)
* [Cache-Friendly Programs](#cache-friendly-programs)

## Introduction:
- *Virtual memory*, an OS abstraction, gives the illusion that memory is just a long linear byte-array that holds instructions and data for the CPU which can access different parts of this memory at a constant time, but the reality is much more complicated. 
- The actual hardware that constitutes a system's memory is divided up into a hierarchy of different storage devices that differ in their speed and cost, and each one of these storage devices acts as a caching facility for the device that lies under it in this hierarchy. The CPU registers hold most used data, while *cache memories* act as a staging area for main memory. Main memory act as a staging area for storage disk and the latter is a cache for the network. 
- This hierarchical setup allows well-written programs to both exploit the high speed of the costly small memories and have access to the vast cheap memories. To have a 'well-written' program that makes use of this hierarchy, you need understand how a system moves data up and down this hierarchy (this is what we will be doing here)!
- A fundamental concept we will be dealing with in this document is *locality*, a feature of programs that tend to access the same data over and over again and access nearby data and usually from the upper levels of the memory hierarchy. In a way this document is an extension of the previous document about optimization. We want to have faster programs and memory is often a bottleneck that needs to be broken.
- We will look at different memory and storage technologies: stuff like *SRAM*, *DRAM*, *ROM*, *rotating* and *solid state* disks. We will also look at cache memories and their impact on program efficiency. We will analyze programs' locality. 

## Storage Technologies:
### Random-Access Memory:
- Random-access memory (RAM) exists in two forms: **static RAM (SRAM)** which is faster and much more expensive and used for caching in the CPU and outside of it, and **dynamic RAM (DRAM)** which is used for main memory and the *frame buffer for graphics* :confused:! The system used to type this document has a couple megabytes of SRAM and sever gigabytes of DRAM. 

#### SRAM:
- SRAM stores data in a *bistable* cells where a cell can only be stable in one of two states. Any intermediate state is unstable and will quickly change to one of the two stable states which makes it a persistent type of memory holding its state as long as the power is on. An SRAM cell is made of a 6-transistor circuit. It has fast access and is resilient to electric disturbances.

#### DRAM:
- Dynamic RAM is inferior to SRAM. It stores a bit as charge on a capacitor that is connected to one transistor. This simple setup allows for storing a bunch of DRAM cells in a small area. The inferiority of DRAM stems from its hyper sensitivity to electric disturbances  and even light rays (for your info, a digital camera's sensor are arrays of DRAM cells).
- Even worse, DRAM leaks voltage like crazy every 10 to 100 milliseconds, but processors work at at nanosecond rates so they shouldn't be affected by this type of data loss. To tackle this data loss, memory systems refresh data by reading it out and writing it back in and some systems have special mechanisms to detect and correct errors caused by these leakages. 
- The following tables illustrates the differences between SRAM and DRAM and justifies the cost difference:

|  | Transistors per bit | Relative Access Time | Persistent | Sensitive | Relative cost | Applications |
| --- | --- | --- | --- | --- | --- | --- |
| SRAM | 6 | 1x | Yes | No | 100x | Cache Memory |
| DRAM | 1 | 10x | No | Yes | 1x | Main memory, frame buffers |

- Cells in a DRAM chip are packaged into *supercells* (Some call supercells words). The chip itself is made of a rectangular array of supercells that are organized into rows and columns. Each supercells cell has an address of the form ***(i, j)*** where ***i*** denotes the row and ***j*** denotes the column. 
- Examine the following figure. It shows a 124-bit 16 x 8 DRAM chip consisting of 16 supercells each of which has 8 cells. It has 4 rows and 4 columns. The shaded supercells has address ***(2, 1)***. Data flow in and out of the chip through **pins**. Each pin carries one bit of data. In this figure there are two sets of pins: an 8-pin set that carries one byte of data and a 2-bit set that carries 2 bits of address, I believe one for row and the other for column (control pins are not shown in the diagram):
![DRAM chip](img/dram.png)
- Attached to the chip is the **memory controller** which controls data movement into and out of the chip. It can move a supercell worth of bits. To read data at address ***(i, j)***, the controller sends the row address ***i*** and follows it by that of the column ***j***. A row address is called **RAS (row access strobe request)** and a column address is called **CAS (column access strobe request)**. The chip responds to the request to read data at a particular address by first copy a whole row to the area called *internal row buffer* and then sending the column part to the controller. 
- Multiple DRAM chips can and are usually packaged into so-called *memory modules* which can be plugged into expansion slots of a motherboard. 

#### Enhanced DRAMs
- You might see and be confused by the many types of DRAM in different computer hardware specifications. This is caused by manufacturers' quest to catch up with the increasingly faster processors. These DRAMs are based on the conventional cell model we've discussed in the previous section, but they differ in the different optimizations they apply to DRAM to get faster data access:
	- *Fast page mode (FPM DRAM)*: Conventional DRAM copies a whole row into the internal row buffer for every request even if consecutive address requests come from the same row. This means that if 4 requests of supercells all come from the same row, there will be 4 RAS/CAS requests, but in FPM DRAM only the initial request will be RAS/CAS! The following 3 requests will be only CAS requests. Only one copying of the row to the internal row buffer is performed for all 4 addresses. This makes this type of DRAM faster. 
	- *Extended data out (EDO DRAM)*: This is a faster variety of FPM DRAM that spaces CAS requests closer together in time. 
	- *Synchronous (SDRAM)*: I have no idea what I've just read but this is faster than the previous types. 
- There are other faster types of DRAM and I don't care. 

#### Non-Volatile Memories:
- DRAM and SRAM are **volatile**: they lose information when cut off from electricity. There are also **non-volatile memories** that retain information even when off!! They are generally, somehow incorrectly, called *read-only memories (ROMs)*. Some of can be written! There are different types of ROMs and they differ mainly by how often they can be reprogrammed (written to) and how they get programmed. They include:
	- *Programmable ROM (PROM)*: is programmable exactly once.
	- *Erasable programmable ROM (EPROM)*: uses light and ultraviolet and what not to write data. Can be erased and rewritten in the order of a 1000 times. *Electric erasable programmable ROM (EEPROM)* can be reprogrammed a 100,000 times and doesn't require special tools to write.
	- *Flash memory*: is based on EEPROM and is everywhere today from server computers to watches to flash thumbnails and SD cards. The flash-based SSD cards are replacing rotating disks in many applications. 
- Programs stored in ROMs are what is called *firmware*. Some systems offer some basic IO functionality in the firmware which is the first programs to run when a a computer starts up such BIOS (basic input output system)  

#### Accessing Main Memory:
![Computer system](img/computerSystems/hardware.png)
- Data flows between the CPU and main memory through **buses** which are sets of parallel wires that carry address, data and control signals between CPU, main memory and I/O devices. Transfer of data between the CPU and main memory is called a *transaction*. A *read transaction* is movement of data from memory to the CPU and the opposite of that is a *write transaction*.
- Address and data might flow in the same wires or have their own dedicated wires. In all cases, there are also control wires whose signal manages how data is moved through the bus: is it a read or a write? Does data move between memory and the CPU or between the latter and and an I/O device?
- An *I/O bridge*, a chipset that lies between the CPU, main memory and IO is attached to the bus. The bus that connects it to the CPU is *system bus* (which is connected to the rest of the CPU by a *bus interface*) and the one connecting it to the main memory is *memory bus*. The IO bridge also contains memory control.
- What happens we *load* data from memory to a register through the following instruction?
```
movl     A, %eax
```
- The bus interface chip on the CPU initiates a read transaction on the bus. The read transaction consists of 3 steps:
	- CPU places address A on the system bus.
	- The IO bridge passes the address to the memory bus.
	- The main memory receives the read transaction signal through the memory bus, fetches the data at the given address from DRAM and writes it on the memory bus. The data follows the same path backward until it is written up on the register.
- Writing register data to memory involves a write transaction and it follows the same path.

### Disk Storage:
- Disks are a cheap storage technology which can store huge amounts of data, but they are very slow. THey can access data in the order of milliseconds which is millions of times slower than SRAM.

#### Disk Geometry:
- A typical disk consists of one or two *platters*, each with two *surfaces* coated with magnetic recording material. A spindle in the middle of platters spins at a fixed rotation rate that is a few thousand *revolutions per minutes (RPM)*. 
- A platter surface is divided into eccentric rings called *tracks*. Each track is cut in length into *sectors*. Each sector contains an equal amount of data bits encoded in its magnetic coating. Sectors are separated from each other by little gaps that don't store data, but store information identifying sectors. 
- *Cylinders* refer to  tracks that are equidistant from the center of the disk: a cylinder on 1-platter disk is the two overlapping tracks on the two surfaces of the platter. On a 2-platter disk, a cylinder contains 4 tracks.

#### Disk Capacity:
- The *capacity* of a disk refers to how much data can be stored in a disk. It is determined by the following factors:
	- *Recording density (bits/in)*: the number f bits that can be squeezed into a 1-inch segment of a track.
	- *Track density (tracks/in)*: The number of tracks that can be squeezed into an inch of the disk's radius. 
	- *Areal Density (bits/in<sup>2</sup>)*: equal to product of recording density but track density.

#### Disk Operation:
- Bits on the surface of a platter are read and written using a *read/write head* placed at the end of an *actuator arm*. The arm moves back and forth over the surface (performing a *seek*) while the disk rotates around to the spindle allowing the arm head to reach any spot on the disk surface. When the head is over the desired track it can either alter bits during a *write* or read the bits during a *read*. Disks usually have multiple platters and hence multiple arms and read/write heads. 
- "The read/write head at the end of the arm flies (literally) on a thin cushion of air over the disk surface at a height of about 0.1 microns and a speed of about 80 km/h. This is analogous to placing the Sears Tower on its side and flying it around the world at a height of 2.5 cm (1 inch) above the ground, with each orbit of the earth taking only 8 seconds!"
- Data is read and written into sector-sized blocks. The **access time** of a sector has 3 components:
	- **Seek time**: the time it takes an arm to move over the disk before hitting the track containing the target sector. It depends on the arm's speed and the head's previous position. It is usually between 3 and 9 ms and can be as high as 20 ms.  
	- **Rotational latency**: the time the head spends on the track containing the right sector before the first bit of that sector is read or written. This depends on the position of the surface before the head arrives at the track and the rotational speed of the disk. 
	- **Transfer time**: from when the head starts reading or writing the first bit of the sector until the end of the sector. It depends on two factors: the rotational speed of the disk, and the number of sectors on a track. 
- The total access time of a disk is the sum of the average times of the 3 factors above. The seek time and rotational latency dominate the access time and are almost the same so we can safely say that ***access time =  2 x  seek time***. 

#### Logical Disk Blocks:
- Disks have complex geometries. They have multiple surfaces with tracks and sectors, etc. They are just too complex!! They hide this complexity from the OS by showing it a a simpler geometry that is a sequence of ***B*** sector-sized **logical blocks** numbered ***1, 2, ..., B - 1***. The **disk controller**, a hardware/firmware mechanism in the disk translates between logical blocks and the actual physical sectors in the disk.
- When the OS wants to load certain data from the disk to RAM, it sends a command to the disk controller asking it for data in a certain logical block. The controller translates the lgical block into a (surface, track, sector) triplet that identify the given sector. The disk hardware uses this triplet to move the head to that sector and put its content into a buffer in the disk controller which then sends it back up to memory. 

#### Connecting IO Devices:
- Some waffling about IO bus! One important component that is connected to the IO bus is the *host bus adapter* which is used to connect one or more disks to the system. It is controlled by a communication protocol *host bus interface*. There are two famous host bus interfaces: *SCSI* (:speaker: 'scuzzy') and *SATA* (:speaker: 'sat-uh').SCSI is more expensive, faster and can connect more disks to the system. SATA can only connect one disk to the system. 

#### Accessing Disks:
- The CPU in a typical system manages IO devices through a technique called **memory-mapped IO**. In such a system, a block of addresses is reserved for communicating with IO devices. Each IO devices is mapped to one or more of these addresses (called **IO ports**) when it's attached to the IO bus. 
- If the disk were mapped to address `0x44`, the CPU sends 3 instructions to that address. The first instruction tells the disk to initiate a read, the second instruction tells the disk the logical block that needs to be read, and the third instruction indicates where in memory the content should be placed. The disk controller does its thing and sends the data directly to memory. By the way, the process whereby an IO device reads or writes into memory without CPU involvement is called **direct memory access (DMA)**. This transfer of data is called a **DMA transfer**. After the transfer is completed, the disk controller might send an interrupt signal to the CPU notifying it of the transfer completion (we will see interrupts later). 

### Solid State Disks:
- Solid state disks (SSD) is based on the non-volatile flash memory we saw [earlier](#non-volatile-memories) that can be a better alternative to rotting disks. An SSD can be attached to a slot on the system's IO bus (USB or SATA mostly) and acts like a normal disk. SSD storage comes in SSD packages which consists of one or more flash chips and *flash translation layers* which translate requests for logical blocks into flash physical voodoo. 
- Sequential reads and writes to an SSD are relatively fast. Random reads are also comparably fast, but random writes are much slower. 
- *I don't even know what a sequential vs. random access are as far as SSDs go*. Anyways, the reason why random writes are slow lies in how SSDs are built and work. An SSD consists of a sequence of **blocks** and each block is made of a sequence of **pages**. The reading and writing in SSD are expressed in units of pages. Before data can be written to a page, the whole block it belongs to must be first erased by setting all its bits to 1. Once erased, data can be written to the block's pages with no further erasing. Knowing that SSDs are ROMs, blocks do wear out after 100k writes. 
- Two factors make random SSD writes slower:
	- Erasing a block is a slow operation! It takes an average of 1ms.
	- If the write occurs in a page that contains other useful data, then all pages in that block must be copied to another erased block before data can be written (*this is a little probaly misworded! What if I write to an erased page in a block containing pages with useful data? adn Should this block also be erased before we can start writing into it?*). 
- SSDs beat rotating in disks in that they use semiconductor memory which uses less power, is much faster and much rugged (doesn't get affected by shocks like moving disks). The big disadvantage of SSD is that they wear out of many writes. Manufacturers implement logic in SSDs to achieve *wear leveling*, meaning that erasures are spread evenly over all blocks to maximize of lives of these blocks. SSDs are also more expansive than rotating disks, but this gaps has been getting smaller over the last decades. 

## Locality:
- The fundamental principle of **locality** refers to the tendency of a program to:
	+ Reference data near other data that has been recently referenced.
	+ Reference data that has been recently referenced. 
- Locality appears in two forms: **temporal locality** and **spatial locality**. In a program with good temporal locality, a memory location that is referenced once is likely to referenced again maybe multiple times in near future. In a program with good spatial locality, if a memory location is referenced once, then a nearby memory location is likely to be referenced soon. 
- Programs with good locality are by definition faster than those with poor locality. The programmer needs to understand the mechanics of locality because hardware, OS and applications are designed in such a way as to make best use of it:
	- At the hardware level, the faster cache memories store the most recently accessed data and instructions from main memory.
	- The OS uses the main memory as a cache for recently accessed disk blocks and also as a cache for recently accessed virtual address space.
	- At the application level, examples of temporal locality exploitation include web browsers caching recently accessed pages and web servers using front-end servers that cache recently accessed documents. 
- Examine the following code:
```c
int sumvec(int v[N]){
	int i, sum = 0;

	for (i = 0; i < N; i++)
		sum += v[i];

	return sum;
}
```
- The `sum` variable has good temporal locality because it's referenced many times inside the loop, but it has no spatial locality.
- The elements of `v`, however, exhibit good spatial locality because they are in adjacent locations in memory but have bad temporal locality because they are accessed only once. 
- The loop in the function above has a **stride-1 reference pattern** because it iterates of the elements of an array one adjacent element at a time. We can have a **stride-k reference pattern**, but the larger the ***k*** the poorer spatial locality we have because the programs have to hop around memory away from data that have been recently accessed. 
- Spatial locality can be an even bigger issue in multidimensional arrays. If we iterate over the rows (inner arrays, which we usually do and I thought that's the only way to do it) we have good spatial locality because we are accessing adjacent memory locations. If we instead columns first (read all first elements from all inner arrays, then all second elements from each array, etc.), then we have a poorer locality.
- Instruction fetches can also enjoy locality. the instruction inside the loop body in the code above has both temporal and spatial locality because it is called repeatedly. Keep in mind that the smaller the loop body and the larger the number of iteration, the better the locality.
- We haven't discussed why a better locality produces faster programs. This has to do with caches which we will see later. It's good, however, to assess the locality of a program by simply looking at the code. 

## The Memory Hierarchy:
- Locality along with the availability of multiple storage mechanisms with varying speeds and costs in a system gave rise to **memory hierarchy**, an approach to organizing storage that is used in most modern systems.The following figure gives a high-level view of memory hierarchy in a typical modern system:
![Memory hierarchy](img/computerSystems/memH.png)
- Generally speaking, such a hierarchy starts at the highest level (L0) with a handful of registers that can be accessed in a single clock cycle. These are followed by larger SRAM that can be accessed in a few clock cycles, then comes the much larger DRAM which can be accessed in a few tens to hundreds of clock cycles, and then comes the huge and much slower disks. Beyond the disk are files in remote machines that can be accessed through the network which include the *World Wide Web* and distributed file systems such as *Andrew File System (AFS)* and *Network File System (NFS)*.

### Caching in the Memory Hierarchy:
![Principles of memory hierarchy](img/princMemHier.png)
- The image above illustrates how memory caching works. The storage at level ***k + 1*** is divided into contiguous chunks of data called **blocks**. Blocks mostly have the same size, but can also be of varied sized such as HTML documents on the Web. The image shows 16 fixed-size blocks numbered 0 to 15. Level ***k*** also contains a smaller set of similar fixed-size blocks. At any point of time, level ***k*** contains copies of a subset of blocks from level ***k + 1***. The image can contain 4 blocks and it has copies of blocks 4, 9, 14 and 3. 
- Data is always copied back and forth between levels ***k*** and ***k + 1*** in block-sized **transfer-units**. The block size is the same between any two adjacent levels, but different pairs of levels can have different block sizes. Block size between **L0** and **L1** is one-word, between **L1** and **L2** (and **L3** and **L2**, and **L4** and **L3**) is several words, and between **L4** and **L5** it is hundreds of thousands of bytes. Lower access time in lower levels is countered by transferring data in larger blocks. 

#### Cache Hits:
- When a program needs a data object ***d*** from level ***k + 1***, it first looks for it in one of the blocks currently stored in ***k***. If ***d*** is in level ***k*** then this is a **cache hit**. The program reads ***d*** from level ***k*** which is faster then if **d**, were read from ***k + 1***. Trying to access block 14 from level ***k*** in the image will result in a cache hit.

#### Cache Misses:
- If ***d*** is not in level ***k*** then the search results in a **cache miss**. When a miss occurs, ***k*** fetches the block containing ***d*** in ***k + 1*** and copies it to itself, overwriting existing data if it is full.
- Overwriting existing data in the cache is called **evicting** or **replacing** the block. The evicted block is called the **victim block**. The cache's **replacement policy** decides which block to evict. Example replacement policies include: **random replacement policy** and **least-recently used (LRU)** replacement which picks the block that "was last accessed the furthest in the past." The block will stay in and be accessed from ***k*** in the next reads.

#### Kinds of Cache Misses:
- There are different kinds of cache misses:
	- **Cold miss** or **compulsory miss**: happens when ***k*** is empty (is a **cold cache**). Every access attempt results in a miss until the cache is filled again (*warmed up*) after repeated accesses.
	- **Conflict miss**: When a miss occurs, a **placement policy** is needed to place the block retrieved from ***k + 1*** at the cache ***k***. This can be done at random where any block from ***k + 1*** can be placed anywhere in ***k***. This is will result in expensive lookups in the cache level. Instead a restricted placement policy is adopted such as ***(i mod j)*** where ***i*** is the block position or address :confused: and ***j*** is the number of blocks in ***k***. This arrangement will cause a type of misses called ***conflict miss*** which is similar to hash map collisions. Blocks which have such collisions will always suffer from them. Every time you ask the cache for a result you will have a conflict miss. 
	- **Capacity misses** happens when the data being cached is larger than the cache itself.. Something like the *working set* of an inner loop 🙃.

#### Cache Management
- So what logic manages all this mess? The system contains is operated by a form of logic that:
	- Partitions cache into blocks
	- Transfers blocks between levels. 
	- Decides when there are hits and misses and handles them.
- This logic can be done in the hardware, software or a combination of the two! For example:
	- Registers (L0 cache) are managed by the compiler which decides when loads occur, when there are misses and what data go to what registers.
	- L1, L2 and L3 are managed entirely by the hardware. 
	- In systems that have virtual memory, DRAM is managed by a combination of the OS and address translation software on the CPU.
	- In distributed file systems such as AFS, an AFS client processes running on the local machine manages the local disk as a cache for the distributed system.
- Most cache operates automatically and requires no intervention from the program or programmer. 

### Summary of Memory Hierarchy Concepts:
- Demystification time:
	- Good *temporal locality* makes your program faster because data recently used has been cached.
	- *Spatial locality* speeds our programs because a cached block contains multiple data objects and accessing the next data object is very likely to be from this cached block. 
- Cache is everywhere! It is a crucial part of modern systems especially in distributed networked systems which are the present and future of computing. The following tables gives a summary of different levels of caches (some terms in the table we haven't covered yet):

| Type | What cached | Where cached | Latency (cycles) | Managed by |
| --- | --- | --- | --- | --- |
| CPU Registers | 4-byte or 8-byte word | On-chip CPU registers | 0 | Compiler |
| TLB | Address translations | On-chip TLB | 0 | Hardware MMU |
| L1 cache | 64-byte block | On-chip L1 cache | 1 | Hardware |
| L2 cache | 64-byte block | On/off-chip L2 cache | 10 | Hardware |
| L3 cache | 64-byte block | On/off-chip L3 cache | 30 | Hardware |
| Virtual memory | 4-KB page | Main memory | 100 | Hardware + OS |
| Buffer cache | Parts of files | Main memory | 100 | OS |
| Disk cache | Disk sectors | Disk controller | 100,000 | Controller firmware |
| Network cache | Parts of files | Local disk | 10,000,000 | AFS/NFS client |
| Browser cache | Web pages | Local disk | 1,000,000,000 | Web browser |
| Web cache | Web pages | Remote server disk | 1,000,000,000 | Web proxy server |

## Cache Memories:
- Traditional computer systems consisted of only 3 cache levels: CPU registers, main memory and disk. Due to the ever-widening gap between CPU registers and main memory speeds, designers thought of mitigating the problem by inserting tiny SRAMs into CPUS as a cache for main memory called **L1 cache memory**. L1 is almost as fast as registers at a rate of 2 to 4 clocks cycles: 
![L1 cache](img/L1.png)
- Designers later supplemented computer systems with **L2** which sits between L1 and main memory and has an access time of about 10 cycles. Later an **L3** was inserted between L2 and main memory. L3 has an access time of 30 to 40 cycles. Caching systems are generally based on the same principles.
- The next section will discuss the principles governing cache memories but will assume the existence of a single L1 cache between the CPU and main memory (these same principles apply in other systems with more cache layers). 

### Generic Cache Memory Organization:
- Examine the following image showing how cache memory is organized:
![General cache organization](img/cacheorg.png)
- In a computer system where each memory address has ***m*** bits that form ***M = 2<sup>m</sup>*** unique addresses, a cache's organization can be represented by a tuple ***(S, E, B, m)*** where:
	- The cache for such a machine is an array of ***S = 2<sup>s</sup>*** *cache sets*.
	- Each cache set consists of ***E** cache lines*.
	- Each line consists of:
		+ Data block of ***B = 2<sup>b</sup>** bytes*.
		+ A *valid bit* indicating if the line contains meaningful information. For this stuff to make sense, let's call ***m*** the minimum number of bits needed to represent the given address. 
		+ ***t = m - (s + b)** tag bits* which is a subset of the bits from the current block's memory address that uniquely identify the block stored in the line.
- The size of this cache ***C*** is the aggregate size of the all the blocks, ***C = S · E · B***. Tag bits and valid bits are not included in the cache size.
- When the CPU receive a load instruction to read a word from address ***A*** from main memory, it sends the address ***A*** to the cache. If the cache has the given word at address ***A***, it sends it to the CPU. The cache examines the bits of address ***A*** and does a lookup similar to searches in a hashmap with a simple hash function. Parameters ***B*** and ***S*** of the tuple representing the cache are the reason the ***m*** bits (as shown in part (b) of the image above) of ***A*** address are partitioned into 3 parts:
	- The *s set index bits*: is an index into the array of ***S*** sets of the cache. The first set is 0, the next 1, etc. 
	- The *t* tag bits: tells us in which line within the set the address ***A*** is located. A line in the set contains the address only if the valid bit is set and the tag bits in the line match tag bit in the address.  
	- The *b block offset bits*: gives us the offset of the word in the ***B***-byte data block. 
- The previous paragraphs had too much confusing information. The following two tables kinda summarize these information. The first table illustrates the fundamental parameters of a cache memory, and the second one shows quantities derived from these parameters:

| Parameter | Description |
| --- | --- |
| S = 2<sup>s</sup> | Number of sets |
| E | Number of lines per set |
| B = 2<sup>b</sup> | Block size (bytes) |
| m = log<sub>2</sub>(M) | Number of physical (main memory) address bits |

| Parameter | Description |
| --- | --- |
| M = 2<sup>m</sup> | Maximum number of unique memory addresses |
| s = log<sub>2</sub>(S) | Number of set index bits |
| b = log<sub>2</sub>(B) | Number of block offset bits |
| t = m - (s + b) | Number of tag bits |
| C = B · E · S | Cache size (bytes) not including overhead such as the valid and tag bits |

### Direct-Mapped Caches:
- There are different types of caches based on ***E*** (the number of lines in a set). A cache with one line per set (***E = 1***) is a **direct-mapped cache**. We will use it to explain general concepts of caching because it is simple to implement and easy to understand.
- Let's say we have system with a CPU, register file, an L1 cache and a main memory. When the CPU wants a word ***w***, it requests it from L1 cache. If L1 has the word, the request results in a cache hit; otherwise we have a cache miss and the CPU has to wait until L1 requests a copy of the block contains ***w***, it places it in one of its lines, extracts ***w*** and returns it to the CPU. To determine if a request is a hit or a miss and then request the requested word is done by the cache in 3 steps: **set selection**, **line matching**, and **word extraction**.

#### Set Selection in Direct-Mapped Caches:
- In this step, the cache extracts the ***s*** set index bits from the middle of the address of word ***w***. These bits are read as an unsigned number which is a set number. Our cache is an array of sets. This number is an index into this array:
![Set selection in direct-mapped caches](img/setSelection.png)

#### Line Matching in Direct-Mapped Caches:
- After selecting a set ***i***, we need to find if a copy of the word ***w*** is in a line in the set. We only have one line per set in our setup. We know that the word is in the line only if the valid bit is set and the tag in the cache line matches the tag in the address of the word ***w***. If the valid bit is set (has value 1) and the tag bits of the ***w*** address match those of the line's tag, we have a cache hit. Otherwise, we have cache miss!

#### Word Selection in Direct-Mapped Caches:
- Once we match our line, we know that the word ***w*** is somewhere in the block contained in the line. This step determines with the ***w*** word start (knowing that the block contains multiple words). The offset bits in the word tells us where the first byte of the word starts in the block. The block can be thought of as an array of bytes and block offset as an index into that array. The definition of a word here must be clear, is it a 4-byte or 8-byte word?!  The following image shows how line matching and word selection are done:
![Line matching and word Selection](img/lineMatchwordSel.png) 

#### Line Replacement on Misses in Direct-Mapped Caches:
- What if a cache miss occurs? The cache then will retrieve the given block from the lower memory layer and store the new block in the appropriate line. If the cache is full of valid cache lines, one of them has to be evicted. The replacement policy for a direct-mapped cache where each set has one line is simple, replace the old line with the new one. 

#### Putting It Together: A Direct-Mapped Cache in Action:
- *At least the authors admit that this can be confusing!!!*, but whatever, dude! This is an example-based recounting of the previous voodoo!
- Suppose we have a direct-mapped cache described by ***(S, E, B, m) = (4, 1, 2, 4)***, meaning it has 4 sets, 1 line per set, 2 bytes per block and 4-bit addresses. In this system, each word is one byte long. The following table shows the entire address space for this cache and its bits partitioning:

| Address<br>(decimal) | Tag bits<br>(t = 1) | Index bits<br>(s = 2) | Offset bits<br>(b = 1) | Block number<br>(decimal) |
| --- | --- | --- | --- | --- |
| 0 | 0 | 00 | 0 | 0 |
| 1 | 0 | 00 | 1 | 0 |
| 2 | 0 | 01 | 0 | 1 |
| 3 | 0 | 01 | 1 | 1 |
| 4 | 0 | 10 | 0 | 2 |
| 5 | 0 | 10 | 1 | 2 |
| 6 | 0 | 11 | 0 | 3 |
| 7 | 0 | 11 | 1 | 3 |
| 8 | 1 | 00 | 0 | 4 |
| 9 | 1 | 00 | 1 | 4 |
| 10 | 1 | 01 | 0 | 5 |
| 11 | 1 | 01 | 1 | 5 |
| 12 | 1 | 10 | 0 | 6 |
| 13 | 1 | 10 | 1 | 6 |
| 14 | 1 | 11 | 0 | 7 |
| 15 | 1 | 11 | 1 | 7 |

- A few things that jump at one from examining the table above:
	- Concatonating the tag bit and index bits uniquely identifies each block in memory.
	- Since there are 8 memory blocks, but only 4 cache sets, multiple blocks are placed in the same cache set.
	- Blocks that map to the same set are uniquely identified by their tag. 
- *I feel a little relieved the authors admit students might trip when it comes to this caching voodoo!* They suggest that we go through a sequence of reads that our hypothetical CPU performs and track the behavior of our cache to really understand how it works. In the following tables, each row represents one of the 4 cache lines. The first column is not really part of a cache line be is used here just to make things easy. T:
	- **0. Initially our cache looks as follows:**

	| Set | Valid | Tag | block[0] | block[1] |
	| --- | --- | --- | --- | --- |
	| 0 | 0 |  |  |  |
	| 1 | 0 |  |  |  |
	| 2 | 0 |  |  |  |
	| 3 | 0 |  |  |  |

	- **1. Read word at address 0**. The valid is not set. This is a cache miss. The cache retrieves block 0 from memory and stores it in set 0. The cache reaturns to the CPU m[0] from block[0] of the newly fetched line.

	| Set | Valid | Tag | block[0] | block[1] |
	| --- | --- | --- | --- | --- |
	| 0 | 1 | 0 | m[0] | m[1] |
	| 1 | 0 |  |  |  |
	| 2 | 0 |  |  |  |
	| 3 | 0 |  |  |  |

	- **2. Read word at address 1**. This is a cache hit (block 0 has this as its second word). m[1] from block[1] is immediately return from cache. This request doesn't change the cache state. 
	- **3. Read word at address 13**. This results in a miss because the cache line in set 2 is not valid. Block 6 is loaded into set 2. m[13] of block[1] of the new cache line is returned to the CPU.

	| Set | Valid | Tag | block[0] | block[1] |
	| --- | --- | --- | --- | --- |
	| 0 | 1 | 0 | m[0] | m[1] |
	| 1 | 0 |  |  |  |
	| 2 | 1 | 1 | m[12] | m[13] |
	| 3 | 0 |  |  |  |

	- **4. Read word at address 8**. This is a cache miss. Even though the cache line 0 is valid, the tag doesn't match. The cache loads block 4 into line 0 (replacing the older one we got when reading address 0). It then returns m[8] from block[0] of the new cache line.

	| Set | Valid | Tag | block[0] | block[1] |
	| --- | --- | --- | --- | --- |
	| 0 | 1 | 1 | m[8] | m[9] |
	| 1 | 0 |  |  |  |
	| 2 | 1 | 1 | m[12] | m[13] |
	| 3 | 0 |  |  |  |

	- **5. Read word at address 0**. This is a miss because of the previous request. This is a conflict miss. The cache might still have more room for more values, but we keep alternating values in certain lines.

	| Set | Valid | Tag | block[0] | block[1] |
	| --- | --- | --- | --- | --- |
	| 0 | 1 | 0 | m[0] | m[1] |
	| 1 | 0 |  |  |  |
	| 2 | 0 |  |  |  |
	| 3 | 0 |  |  |  |

#### Conflict Misses in Direct-Mapped Caches:
- Situations where you can never exploit caching and every request would result in a conflict miss are possible. This can be especially more likely when trying to access arrays whose sizes are powers of 2 with direct-mapped caches. Chunks of such arrays that map to the same cache sets will keep overwriting each other in a process called *thrashing*. This will be really bad for performance and reduce it by a factor of 2 or 3. Having a good spatial locality will not help here.
- The authors suggest pad arrays where such a problem by a number of bytes to make the two arrays map to different sets. 

### Set Associative Caches:
- The reason behind the common conflict misses in direct-mapped caching is that each set has exactly one line meaning that ***E = 1***. In **set associative caches** a set can have multiple lines which (maybe) reduces conflict misses. Caches with ***1 < E < (C / B)*** are called **E-way set associate caches**, meaning such a cache can be *2-way*, or 3-way, etc. 
- Searching an E-way associative cache is similar to a direct-mapped one but differs form it in the line matching step. The tags and valid bits of multiple lines have to be checked "in order to determine if the requested word is in the set." 
- A conventional memory is an array of values that takes an address as an input and returns a value indexed by the memory address. An *associative memory* is an array of key-value pairs that takes the key as an input and returns the value paired with it. Each set in a set associative cache can be thought of as a small associative memory "where the keys are the concatenation of the tag and valid bits, and the values are the contents of a block." Any line in the matching set might contain the given value, so each line of that set must be searched for valid line containing the matching concatenation of the valid bit and tag bits. 
- If the requested word is not in any of the set lines, we have a cache miss and the cache must retrieve the appropriate blocks from memory, but which line will it replace? Replacement policy in a set associative cache is kinda complicated. The simplest policy to replace a random line in the set, but the more ambitious policies use the principle of locality and vie to minimize the chances of replacing a line that might be used in the near future. Examples of such policies include:
	- The **least-frequently used (LFU)** policy which replaces a lines that has been used the fewest times over a past window. 
	- The **least-recently used (LRU)** policy replaces a line that has been last referenced the furthest in the past. 

### Fully Associative Caches:
- A **fully associative cache** is one giant set containing all the lines (***E = C / B***). It looks as follows:
![Fully associative cache](img/fullyasoc.png)
- In this set up, lines don't have set index bits. There is only one set and no need to search for one. The line and word matching in fully associative cache are the same as set associative cache but on a bigger scale! 
- Fully associative caches can be expensive and slow if they get too large, so they are used in limited situations for small caches.

### Issues with Writes:
- Cache reads are simple. We search the cache and if we get a hit, we return the value. If a miss occurs, we retrieve the block containing the address from the lower memory level, etc., and replace a possibly valid line and get the value back to the CPU.
- Writes are more complicated. If we write an already cached word (*write hit*), how does the cache update lower memory levels?
	- The most straightforward way is a **write-through** where the cache updates the memory level under it. The downside of this approach is that it incurs a *bus traffic* with every write.
	- A **write-back** defers writes updating the lower level of memory as long as possible until it is time for the block to be evicted by the replacement policy. This approach reduces bus traffic significantly, but has the downside of added complexity. Each line must also have a *dirty bit* which indicates if the block has been modified (so that it gets used to replace lower memory when it's about being evicted).
- When it comes to *write misses* approaches used include:
	- **Write-allocate** loads the corresponding memory block every time a write miss occurs. It exploits spatial locality, but suffers from having to perform a block transfer from memory for every miss.
	- **No-write-allocate** bypasses the cache and wries directly to the lower memory level. Write-through caches are usually no-write-allocate, while write-back caches are write-allocate.
- How modern cache designs works is proprietary and poorly documented, but it might be safe to assume that they use write-backs instead of write-through.

### Anatomy of a Real Cache Hierarchy:
- We've been assuming that cache holds only data, but in a real system it holds both data and instructions. A cache that only holds data is called **d-cache** while cache holding only instructions is called **i-cache**. Cache that holds both data and instructions is called **unified cache**. Modern systems tend to use separate specialized d-caches and i-caches. Reasons for this split include:
	- The processor can read an instruction word and a data word at the same time.
	- I-caches are read-only making them simpler, meaning they can have their own ways of optimization based on their access patterns.
- The following diagram shows one the Intel i7 processors and the organization of its cache (notice the separation of i-cache and d-cache):
![i7 cache](img/i7cache.png)

### Performance Impact of Cache Parameters:
- Cache performance is evaluated with the following metrics:
	- *Miss rate* = ***1 - references***.
	- *Hit rate* = ***hits / references***
	- *Hit time* is the time it takes to deliver word in cache to the CPU. It includes time for set selection, line matching and word selection. It is a few clock cycles for L1.
	- *Miss penalty* is the additional time caused by a cache miss. The penalty for misses from L2 to L1 is about 10 clock cycles.
- Cache performance is generally affected by cache parameters in different ways:
	- A larger **cache size** increase the hit rate of the cache but decreases its speed. It generally increases the hit time which is bad.
	- Larger **block sizes** is good for spatial locality, but might mean fewer lines which is bad for temporal locality. Larger blocks might also increase miss penalty because it takes longer to transfer a larger block. Modern caches have 32 to 64 byte blocks.
	- **Associativity** refers to *E*, the number of lines per set. Higher associativity means less vulnerability to thrashing because of conflict misses, but it's costly to implement and hard to make fast. it has increased complexity that might contribute to increased miss penalty. 
	- L1 prefers a write-through **writing strategy** for its simplicity and the fact that it includes faster reads because a read wouldn't trigger an update of lower memory. Lower cache layers prefer write-back that triggers less transfers because data movement is slower. 

## Cache-Friendly Programs:
- *Cache-friendly* code is code with good locality. To ensure your code is cache-friendly:
	- *Make the common case go fast*. Programs spend most time on a few core functions and such core functions might revolve about some loops. The programmer should focus and optimize such loops and especially if they were inner loops and "ignore the rest". Loops with better miss rates always run faster!
	- *Minimize the number of cache misses in each inner loop*
- Consider the following function which we've seen before:
```c
int sumvec(int v[N]){
	int i, sum = 0;

	for (i = 0; i < N; i++)
		sum += v[i];

	return sum;
}
```
- Local variables `i` and `sum` have excellent temporal locality. The compiler optimize these and puts them in the register file, the highest caching level. Repeated references to local variables result in excellent cache-friendliness!
- Stride-1 references in loop are very cache friendly. In a cache with 4-words per block and where z word is 4 bytes, referencing words would on average result in one 1 miss and 3 hits. Stride-1 references are good because caches store data in contiguous blocks. 
- Spatial locality is even more important in nested arrays.Iterating over the rows of an array first has better locality. 