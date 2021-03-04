# Virtual Memory:

## Introduction:
- Multiple processes can share the CPU and memory. When too many processes share a CPU, it is slowed down but when too many	processes share memory, they might run out of the available space and no more processes can use that memory. Processes might also be able to mess with memory "belonging" to other processes, thus corrupting this memory.
- Modern systems use **virtual memory** to address these problems. "*Virtual memory is an elegant interaction of hardware exceptions, hardware address translation, main memory, disk files, and kernel software that provides each process with a large, uniform, and private address space.*" It offers the following three services:
	- It treats main memory as a cache for disk, keeping only active data in memory and moving data back and forth between memory and disk as needed.
	- It simplifies memory management by providing each process with a uniform address space.
	- It provides each process with a private address space that cannot or should not be accessed/corrupted by other processes.
- The system takes care of virtual memory from A to Z without the need of programmer's intervention. Why bother about it then? Reasons for bothering about VM include:
	- *VM is central*: Understanding VM will make one have a better understanding of the system. VM involves all layers and aspects of a system from hardware exceptions, assemblers, files, loaders, processes, etc. 
	- *VM is powerful*: Understanding VM gives applications advanced capabilities and allows for neat tricks (*that we will see later*).
	- *VM is dangerous*: Improper use of VM can lead to weird and dangerous errors and program behavior. Understanding VM might allow me to better understand memory errors surrounding misuse of pointers and what not!
- VM is a difficult subject. This document will try to first go over how it works and then moves on to described how it is used and managed by applications. We might also go over how to manage and control VM in our programs. 

## Physical and Virtual Addressing:
- Main memory is an array of ***M*** contiguous byte-sized cells each of which has a unique **physical address (PA)**. The first byte has address 0, the second address 1, the third address 2, etc. The CPU is capable of accessing this array of bytes in what is called **physical addressing**.
- The following images shows an example of physical addressing in the context of a load operation. The CPU generates a physical address starting at address 4. This address is sent to main memory over memory bus. The main memory fetches the 4-byte word starting at PA 4 and returns it to the CPU: 
![Physical addressing](img/pa.png)
- Physical addressing was common in earlier computers. Embedded microcontrollers, digital signal processors, etc. continue to use raw physical addressing. 
- Modern processors use **virtual addressing (VA)** instead. With virtual addressing, the CPU accesses main memory by issuing virtual addresses which are converted to physical addresses before being sent to memory. The act of converting a virtual address into a physical address is called **address translation**. Virtual addressing requires a close cooperation between the CPU hardware and the operating system. The CPU chip has a piece of hardware dedicated to translating virtual addresses. It is called **memory management unit (MMU)**. It translates virtual addresses on the fly using a look-up table stored in main memory whose contents are managed by the OS. The following image shows how VA works:
![Virtual addressing](img/va.png)

## Address Spaces:
- An **address space** is an ordered set of nonnegative integer addresses:
	* ***{0, 1, 2, ...}***
- A **linear address space** is one where the integers are consecutive. We will assume all address spaces are linear. 
- In a system with virtual memory, the CPU generates virtual addresses from an address space of ***N = 2<sup>n</sup>*** addresses called the **virtual address space**:
	* ***{0, 1, 2, ..., N - 1}***
- The size of an address space is determined by the number of bits needed to represent the largest address. A virtual address space with ***N = 2<sup>n</sup>*** is an *n-bit* address space. Modern systems have either a 32-bit or 64-bit virtual address space. 
- A system also has a **physical address space** corresponding to the ***M*** bytes of its physical memory:
	* ***{0, 1, 2, ..., M - 1}***
- ***M*** doesn't have to be a power of 2, but for the sake of simplification we will assume ***M = 2<sup>m</sup>***. 
- The address space concept can help us make distinction between data objects (bytes) and their attributes (addresses). This distinction allows us to have multiple addresses from different address spaces for each data object. 
- The basic idea of virtual memory is that each byte of main memory has a virtual address from the virtual address space and a physical address from the physical address space. 

## VM as a Tool for Caching:
- In theory, a virtual memory is an array of ***N*** contiguous byte-sized cells stored in disk. Each byte has a unique virtual address acting as an index into this array. The contents of the array in disk are cached in main memory. As with other cache in memory hierarchy, the virtual array in disk is segmented into blocks that are used as transfer units between disk and main memory. The VM system is responsible for this partitioning. It partitions virtual memory into fixed-sized blocks called **virtual pages (VPs)**. Each virtual page is ***P = 2<sup>p</sup>*** bytes in size. 
- Physical memory is also partitioned into blocks called **physical pages (PP)** which are called **page frames**. 
- The set of virtual pages is partitioned into 3 disjointed subsets:
	- **Unallocated**: pages are not yet created (allocated) by the VM system. They have no data associated with them and don't occupy space on disk.
	- **Cached**: Allocated pages that are cached in physical memory.
	- **Uncached**: Allocated pages that are not cached in physical memory.
- The following image shows a virtual memory with 8 pages accommodating a 6-page physical memory. You can see in the image the different subsets of virtual memory, i.e. unallocated, cached and uncached:
![VM for caching](img/vmAsCache.png)

### DRAM Cache Organization:
- From now on we will use *SRAM cache* to denote three caching layers L1, L2 and L3, and *DRAM cache* to denote the VM system's cache which caches virtual pages in main memory. 
- The position of a caching level in the memory hierarchy decides how the cache is organized. DRAM is only 10 times slower than SRAM, but disk is 100,000 times slower than DRAM. DRAM cache misses are extremely costly.
- To mitigate the large miss penalties and the costly retrieval of data from disk:
	- Virtual pages are between 4KB and 2MB large. These large page sizes can help . 
	- DRAM caches are also fully associative: a virtual page can be placed in any physical page.
	- Operating systems also use sophisticated implementations of replacement policies for DRAM caches.
	- DRAM caches also use write-back instead of write-through. 

### Page Tables:
- The VM system must have a way of finding if and where a virtual page is cached in DRAM. If the virtual page is cached, the system must know in which physical page it's cached. If not, the system must know where the virtual page is stored in disk. It must also select a victim page in DRAM and replace it with the appropriate virtual page.
- These capabilities are provided by a combination of OS software, address translation hardware in the MMU and an important data structure stored in physical memory called **page table**. Page table maps virtual pages to physical pages. The address translation hardware reads the page table each time it translates a virtual address to a physical address. The OS is responsible for maintaining the contents of the page table and moving pages between the DRAM and disk.
- The following image shows the organization of the page table and how it works:
![Page table](img/pageTable.png)
- A page table is an array of **page table entries (PTEs)**. Each page in the virtual address space has a PTE at a flexible offset in the page table. We assume that each PTE consists of two parts, a *valid bit* and an *n*-bit address field. The valid bit indicates whether a virtual page is currently cached in DRAM. If the valid bit is set (has value 1), the address field indicates the start of the physical page where the virtual page is cached. If the valid bit is not set and the address field is NULL, then the virtual page has not been allocated. If the valid bit is not set and there is an address, then that address points to the start of the uncached virtual page on disk. 
- To reiterate, any virtual page can be placed in any physical page because DRAM cache is fully associative. 

### Page Hits:
- Referring to the [page table image](img/pageTable.png), let's say the CPU want to access data from virtual memory located in *VP 2*. The translation hardware uses the virtual memory address as an index to locate *PTE 2* (using a mechanism we will see later) and reads it from memory. *VP 2* is cached because the valid bit is set. The address in *PTE* which points to the start of the physical page *PP 1*is then used to form the physical address of the data. 

### Page Faults:
- A DRAM cache miss is called a **page fault**. When the address translation hardware reads a PTE from memory and finds out that its valid bit is not set and it's address field is not NULL. it knows that the corresponding virtual page is not cached so:
	- It triggers a *page fault exception*. 
	- The page fault exception invokes a handler in the kernel which select a victim virtual page stored in physical memory. It first checks if this victim page has been modified it, in which case it copies it back to the disk. It then modifies the PTE for the given virtual page to reflect that page is no longer cached in main memory.
	- The kernel copies the virtual page from disk to the corresponding physical page, updates the corresponding PTE, and returns.
	- After the handler returns, the faulting instruction is restarted. The address translation hardware now handles a page hit normally because the given virtual page is now cached in DRAM.
- Virtual memory has been around since the early 1960s, which is the reason why it has some  different terminology than SRAM that refer the basically the same things:
	- SRAM *blocks* are called *pages*.
	- Transferring pages between disk and memory is called **swapping** (also **paging**). Pages are *swapped in* from disk to DRAM, and *swapped out* from DRAM to disk.
	- Waiting until the last moment to swap in a page is called **demand paging** which is the de facto mode used in virtual memory.

### Allocating Pages:
- A new page of virtual gets allocated as a result of say the `malloc` C function. It basically involves creating a virtual page on disk and updating some entry in the PTE to point to this newly created virtual page.

### Locality to the Rescue Again
- Virtual memory might seem inefficient due to the large miss penalties, but is surprisingly efficient because of *locality*. Programs might reference a large number of distinct pages that might exceed the size of physical memory, but a given moment these programs tend to mostly operate on a small set of *active pages* called the **working set** or **resident set**. After the initial warming when the resident set is paged into memory, subsequent references to that set are fast with no misses. Think of Microsoft Word's sluggish start!
- Good temporal locality produces seamless fast programs, but not all programs have it. If the working set exceeds the size of the physical memory, **thrashing** occurs. Thrashing is a situation where pages continually swapped in and out. 

## VM as a Tool for Memory Management:
- Another use of virtual memory is that it simplifies memory management and "provide[s] a natural way to protect memory."
- So far we've been talking about a single page table that maps a single virtual address space, but in fact, the OS provides a separate page table, and a thus a separate virtual address space for every process as the following image shows:
![Each process has a separate virtual address space](img/processSeparateAddressSpace.png)
- An interesting observation from the previous image is that multiple virtual pages from different process can be mapped to the same shared physical page.
- The combination of demand paging and separate address spaces in a virtual memory system largely simplifies the use and management of memory (*having skipped the linking chapter for now, I basically know nothing about it at the moment and might misrepresent the rest of this section*):
	- *Simplifying linking*: Separate address spaces allow each process to have the same memory image where code starts a certain point and text and stack have similar layouts regardless of the the particular physical memory where they are stored. Apparently linking is made easier by this predictable layout of each process irrespective of what physical memories they target. 
	- *Simplifying loading*: ?? *I don't know anything about linking might come back to this*
	- *Simplifying sharing*: Each process has its own separate private data, code, stack and heap, but virtual memory allows for easy sharing of some code and data between different processes such as kernel code or the C standard library routines. Instead of having separate copies of kernel code and shared libraries, the operating systems have page tables map virtual pages of this shared code and data to the same physical pages. 
	- *Simplifying memory allocation*: VM also allows for simple allocation of additional memory to user processes. When a user processes requests additional memory, for example when calling `malloc`), the OS allocates the appropriate amount of contiguous virtual memory pages and maps this contiguous chunk to arbitrary physical memory pages located anywhere in DRAM. 

## VM as a Tool for Memory Protection:
- A modern OS is expected to offer protection and control of memory system. A user process cannot or should not be able to:
	- Modify its read-only text region. 
	- Read or modify kernel's data and code.
	- Read or write private memory of other processes.
	- Modify virtual pages shared with other processes (unless explicitly allowed to do so through interprocess system calls).
- By providing processes with separate address spaces, VM makes it easy to isolate the private memories of these processes.  
- The address translation mechanism of a VM system goes further to offer a finger form of memory protection at the page-level. Every time the CPU wants to access information at a given address, the address translation hardware reads a PTE. By adding permission bits to PTEs, it becomes easy to control access to the contents of the corresponding virtual page as the following image shows:
![Page-level memory protection](img/pageLevelMemProtection.png)
- PTEs in this example now have 3 additional bits for access control:
	- The ***SUP*** bit indicates whether the process must be running in kernel (supervisor) mode to able to access the page. Processes running in kernel mode can access any page, but user mode processes can only access pages whose SUP bit is 0.
	- The ***READ*** bit controls the read access to the page.
	- The ***WRITE*** bit controls the write access to the page.
- If a process violates any of these permissions, the CPU triggers a protection fault and transfers control to an exception handler in the kernel. This is reported as the famous or infamous *segmentation fault*!! Ahha, that's what it is!!

## Address Translation:
## Case Study: The Intel Core i7/Linux Memory System
## Memory Mapping:
## Dynamic Memory Allocation:
## Garbage Collection:
## Common Memory Related C Bugs:
















