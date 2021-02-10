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
- Data flows between the CPU and main memory through **buses** which are sets of parallel wires that carry address, data and control signals between CPU, main memory and I/O devices. Transfer of data between the CPU and main memory is called a *transaction*. A *read transaction* is movement of data from memory to the CPU and the opposite of that is a *write transaction*.
- Address and data might flow in the same wires or have their own dedicated wires. In all cases, there are also control wires whose signal manages how data is moved through the bus: is it a read or a write? Does data move between memory and the CPU or between the latter and and an I/O device?
- An *I/O bridge*, a chipset that lies between the CPU, main memory and IO is attached to the bus. The bus that connects it to the CPU is *CPU bus* and the one connecting it to the main memory is *memory bus*. The IO bridge also contains memory control.

### Disk Storage:
### Solid State Disks:
### Storage Technology Trends:

## Locality:
## The Memory Hierarchy:
## Cache Memories:
## Writing Cache-Friendly Programs:
## The Impact of Caches on Program Performance: