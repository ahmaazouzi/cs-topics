# Virtual Memory:
## Table of Contents:
* [Introduction](#introduction)
* [Physical and Virtual Addressing](#physical-and-virtual-addressing)
* [Address Spaces](#address-spaces)
* [VM as a Tool for Caching](#vm-as-a-tool-for-caching)
	+ [DRAM Cache Organization](#dram-cache-organization)
	+ [Page Tables](#page-tables)
	+ [Page Hits](#page-hits)
	+ [Page Faults](#page-faults)
	+ [Allocating Pages](#allocating-pages)
	+ [Locality to the Rescue Again](#locality-to-the-rescue-again)
* [VM as a Tool for Memory Management](#vm-as-a-tool-for-memory-management)
* [VM as a Tool for Memory Protection](#vm-as-a-tool-for-memory-protection)
* [Address Translation](#address-translation)
	+ [Integrating Caches and VM](#integrating-caches-and-vm)
	+ [Speeding Up Address Translation with TLB](#speeding-up-address-translation-with-tlb)
	+ [Multi-Level Page Tables](#multi-level-page-tables)
* [Linux Virtual Memory System](#linux-virtual-memory-system)
	+ [Linux Virtual Memory Areas](#linux-virtual-memory-areas)
	+ [Linux Page Fault Exception Handling](#linux-page-fault-exception-handling)
* [Memory Mapping](#memory-mapping)
	+ [Shared Objects](#shared-objects)
	+ [`fork`](#fork)
	+ [User-level Memory Mapping with the `mmap` Function](#user-level-memory-mapping-with-the-mmap-function)
* [Dynamic Memory Allocation](#dynamic-memory-allocation)
	+ [The `malloc` and `free` Functions](#the-malloc-and-free-functions)
	+ [Why Dynamic Memory Allocation?](#why-dynamic-memory-allocation)
	+ [Allocator Requirements and Goals](#allocator-requirements-and-goals)
	+ [Fragmentation](#fragmentation)
	+ [Implementation Issues](#implementation-issues)
	+ [Implicit Free Lists](#implicit-free-lists)
	+ [Placing Allocated Blocks](#placing-allocated-blocks)
	+ [Splitting Free Blocks](#splitting-free-blocks)
	+ [Getting Additional Heap Memory](#getting-additional-heap-memory)
	+ [Coalescing Free Blocks](#coalescing-free-blocks)
	+ [Coalescing with Boundary Tags](#coalescing-with-boundary-tags)
	+ [Explicit Free Lists](#explicit-free-lists)
	+ [Segregated Free Lists](#segregated-free-lists)
* [Garbage Collection](#garbage-collection)
	+ [Garbage Collector Basics](#garbage-collector-basics)
	+ [Mark&Sweep Garbage Collectors](#mark&sweep-garbage-collectors)
* [Common Memory-Related Bugs in C Programs](#common-memory-related-bugs-in-c-programs)
	+ [Dereferencing Bad Pointers](#dereferencing-bad-pointers)
	+ [Reading Uninitialized Memory](#reading-uninitialized-memory)
	+ [Allowing Stack Buffer Overflows](#allowing-stack-buffer-overflows)
	+ [Assuming that Pointers and the Objects They Point to Are the Same Size](#assuming-that-pointers-and-the-objects-they-point-to-are-the-same-size)
	+ [Making Off-by-One Errors](#making-off-by-one-errors)
	+ [Referencing a Pointer Instead of the Object It Points to](#referencing-a-pointer-instead-of-the-object-it-points-to)
	+ [Misunderstanding Pointer Arithmetic](#misunderstanding-pointer-arithmetic)
	+ [Referencing Nonexistent Variables](#referencing-nonexistent-variables)
	+ [Referencing Data in Free Heap Blocks](#referencing-data-in-free-heap-blocks)
	+ [Introducing Memory Leaks](#introducing-memory-leaks)

## Introduction:
- Multiple processes can share the CPU and memory. When too many processes share a CPU, it is slowed down but when too many	processes share the finite memory, they might run out of the available space and no more processes can use that memory. Processes might also be able to mess with memory "belonging" to other processes, thus corrupting this memory.
- Modern systems use **virtual memory** to address these problems. "*Virtual memory is an elegant interaction of hardware exceptions, hardware address translation, main memory, disk files, and kernel software that provides each process with a large, uniform, and private address space.*" It offers the following three services:
	- It treats main memory as a cache for disk, keeping only active data in memory and moving data back and forth between memory and disk as needed.
	- It simplifies memory management by providing each process with a uniform address space.
	- It provides each process with a private address space that cannot or should not be accessed/corrupted by other processes.
- The system takes care of virtual memory from A to Z without the need of programmer's intervention. Why bother about it then? Reasons for bothering about VM include:
	- *VM is central*: Understanding VM will make one have a better understanding of the system. VM involves all layers and aspects of a system from hardware exceptions, assemblers, files, loaders, processes, etc. 
	- *VM is powerful*: Understanding VM gives applications advanced capabilities and allows for neat tricks (*that we will see later*).
	- *VM is dangerous*: Improper use of VM can lead to weird and dangerous errors and program behavior. Understanding VM might allow me to better understand memory errors surrounding misuse of pointers and whatnot!
- VM is a difficult subject. This document will try to first go over how it works and then moves on to describe how it is used and managed by applications. We might also go over how to manage and control VM in our programs. 

## Physical and Virtual Addressing:
- Main memory is an array of ***M*** contiguous byte-sized cells each of which has a unique **physical address (PA)**. The first byte has address 0, the second address 1, the third address 2, etc. The CPU is capable of accessing this array of bytes in what is called **physical addressing**.
- The following image shows an example of physical addressing in the context of a load operation. The CPU generates a physical address starting at address 4. This address is sent to main memory over memory bus. The main memory fetches the 4-byte word starting at PA 4 and returns it to the CPU: 
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
- A page table is an array of **page table entries (PTEs)**. Each page in the virtual address space has a PTE at a fixed offset in the page table. We assume that each PTE consists of two parts, a *valid bit* and an *n*-bit address field. The valid bit indicates whether a virtual page is currently cached in DRAM. If the valid bit is set (has value 1), the address field indicates the start of the physical page where the virtual page is cached. If the valid bit is not set and the address field is NULL, then the virtual page has not been allocated. If the valid bit is not set and there is an address, then that address points to the start of the uncached virtual page on disk. 
- To reiterate, any virtual page can be placed in any physical page because DRAM cache is fully associative. 

### Page Hits:
- Referring to the [page table image](img/pageTable.png), let's say the CPU want to access data from virtual memory located in *VP 2*. The translation hardware uses the virtual memory address as an index to locate *PTE 2* (using a mechanism we will see later) and reads it from memory. *VP 2* is cached because the valid bit is set. The address in *PTE* which points to the start of the physical page *PP 1* is then used to form the physical address of the data. 

### Page Faults:
- A DRAM cache miss is called a **page fault**. When the address translation hardware reads a PTE from memory and finds out that its valid bit is not set and it's address field is not NULL, it knows that the corresponding virtual page is not cached so:
	- It triggers a *page fault exception*. 
	- The page fault exception invokes a handler in the kernel which select a victim virtual page stored in physical memory. It first checks if this victim page has been modified it, in which case it copies it back to the disk. It then modifies the PTE for the given virtual page to reflect that page is no longer cached in main memory.
	- The kernel copies the virtual page from disk to the corresponding physical page, updates the corresponding PTE, and returns.
	- After the handler returns, the faulting instruction is restarted. The address translation hardware now handles a page hit normally because the given virtual page is now cached in DRAM.
- Virtual memory has been around since the early 1960s, which is the reason why it has some  different terminology than SRAM that refer to basically the same things:
	- SRAM *blocks* are called *pages*.
	- Transferring pages between disk and memory is called **swapping** (also **paging**). Pages are *swapped in* from disk to DRAM, and *swapped out* from DRAM to disk.
	- Waiting until the last moment to swap in a page is called **demand paging** which is the de facto mode used in virtual memory.

### Allocating Pages:
- A new page of virtual memory gets allocated as a result of say invoking the `malloc` C function. It basically involves creating a virtual page on disk and updating some entry in the PTE to point to this newly created virtual page.

### Locality to the Rescue Again
- Virtual memory might seem inefficient due to the large miss penalties, but is surprisingly efficient because of *locality*. Programs might reference a large number of distinct pages that might exceed the size of physical memory, but at a given moment these programs tend to mostly operate on a small set of *active pages* called the **working set** or **resident set**. After the initial warming when the resident set is paged into memory, subsequent references to that set are fast with no misses. Think of Microsoft Word's sluggish start!
- Good temporal locality produces seamless fast programs, but not all programs have it. If the working set exceeds the size of the physical memory, **thrashing** occurs. Thrashing is a situation where pages continually swapped in and out. 

## VM as a Tool for Memory Management:
- Another use of virtual memory is that it simplifies memory management and "provide[s] a natural way to protect memory."
- So far we've been talking about a single page table that maps a single virtual address space, but in fact, the OS provides a separate page table, and a thus a separate virtual address space for every process as the following image shows:
![Each process has a separate virtual address space](img/processSeparateAddressSpace.png)
- An interesting observation from the previous image is that multiple virtual pages from different process can be mapped to the same shared physical page.
- The combination of demand paging and separate address spaces in a virtual memory system largely simplifies the use and management of memory (*having skipped the linking chapter for now, I basically know nothing about it at the moment and might misrepresent the rest of this section*):
	- *Simplifying linking*: Separate address spaces allow each process to have the same memory image where code starts at a certain point and text and stack have similar layouts regardless of the the particular physical memory where they are stored. Apparently linking is made easier by this predictable layout of each process irrespective of what physical memories they target. 
	- *Simplifying loading*: ?? *I don't know anything about linking might come back to this*
	- *Simplifying sharing*: Each process has its own separate private data, code, stack and heap, but virtual memory allows for easy sharing of some code and data between different processes such as kernel code or the C standard library routines. Instead of having separate copies of kernel code and shared libraries, the operating systems have page tables map virtual pages of this shared code and data to the same physical pages. 
	- *Simplifying memory allocation*: VM also allows for simple allocation of additional memory to user processes. When a user processes requests additional memory, for example when calling `malloc`), the OS allocates the appropriate amount of contiguous virtual memory pages and maps this contiguous chunk to arbitrary physical memory pages located anywhere in DRAM. 

## VM as a Tool for Memory Protection:
- A modern OS is expected to offer protection and control of a memory system. A user process cannot or should not be able to:
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
- This section offers a rough overview of the basics of address translation and the hardware's role in virtual memory. The following tables show the meanings of the symbols that will be used through this section:

*- Basic Parameters:*

| Symbol | Description |
| --- | --- |
| N = 2<sup>n</sup> | Number of addresses in virtual address space |
| M = 2<sup>m</sup> | Number of addresses in physical address space |
| P = 2<sup>p</sup> | Page size in bytes |

*- Components of a virtual address (VA):*

| Symbol | Description |
| --- | --- |
| VPO | Virtual page offset in bytes |
| VPN | Virtual page number |
| TLBI | TLB index |
| TLBT | TLB tag |

- *Components of a physical address (PA):*

| Symbol | Description |
| --- | --- |
| PPO | Physical page offset in bytes |
| PPN | Physical page number |
| CO | Byte offset within cache block |
| CI | TLB index |
| CT | TLB tag |

- **Address translation** is a mapping between the elements of an ***N***-element virtual address space (***VAS***) and an ***M***-element *physical address space* (***PAS***).
![Address translation with a page table](img/addrTranslation.png)
- The image above shows how the MMU uses a page table to perform address translation. A control register in the CPU called the **page table base pointer (PTBR)** points to the current page table. The ***n***-bit virtual address has two components: a ***p***-bit **virtual page offset (VPO)** and a ***(n - p)***-bit **virtual page number (VPN)**. The VPN is used by the MMU to locate the appropriate PTE so VPN 0 selects PTE 0, VPN 1 selects PTE 1, and so on. The corresponding physical page can be found by concatenating the **physical page number (PPN)** to the VPO of the virtual address. Because physical and virtual pages are both P bytes in length, the PPO and VPO are the same. 
![A page hit](img/pageHit.png) 
- The image above traces the steps followed when there is a page hit:
	- *Step 1*: The processor generates a virtual address and sends it to the MMU. 
	- *Step 2*: The MMU produces the PTE address and requests it from main memory.
	- *Step 3*: The MMU constructs the physical address and sends it to main memory.
	- *Step 4*: The main memory returns the requested word to the processor. 
![A page fault](img/pageFault.png)
- The image above shows what happens when a page fault occurs:
	- *Step 1 to 3*: The same steps 1 to 3 in a page hit.
	- *Step 4*: The valid bit in the PTE is 0, so the CPU triggers an exception which transfers control to a page fault exception handler in the kernel.
	- *Step 5*: The fault handler identifies a victim page in physical memory. If that page is modified, it pages it out to disk.
	- *Step 6*: The fault handler pages the new page in and updates the PTE.
	- *Step 7*: The fault handler returns to the process that caused the fault and causes the faulting instruction to restart. The CPU then resends the same address to the MMU and because the page is in physical memory, there is a hit. Steps 1 to 4 from the page hit section are performed and the main memory returns the requested to the processor. 

### Integrating Caches and VM:
- Should we use virtual or physical addresses to access SRAM cache? Most systems use direct physical addresses for SRAM and don't ask me why! It's enough to know that cache wouldn't have memory protection issues because address translation occurs before access, so processes can have blocks in cache at the same time. PTEs can also be cached in SRAM as any other data from main memory.

### Speeding Up Address Translation with TLB:
- Should the MMU refer to a PTE to translate a virtual address into a physical address for every request by the CPU? This can introduce considerable overhead. If the PTE is cashed in L1, referring to it can take  couple extra cycles, if it has to be fetched from main memory then it's a few hundred cycles. 
- Modern systems try to reduce this overhead by having a small cache of PTEs in the MMU called **translation lookaside buffer (TLB)**. A TLB is a small *virtually addressed (:confused:!!!)* cache where each line holds a single PTE. When there is a TLB hit, the whole address translation voodoo happens in the MMU hardware making it extremely fast. A TLB follows these steps:
	- *Step 1*: The CPU generates a virtual address.
	- *Step 2 and 3*: The MMU fetches the PTE from TLB.
	- *Step 4*: The MMU translates the virtual address to physical address and sends to cache or main memory. 
	- *Step 5*: The cache/main memory returns the requested data to the CPU.
- When there is a TLB miss, the PTE is requested from cache/main memory. The fetched PTE is then stored in the TLB and maybe overwriting an existing PTE. The following image shows how TLB hits and misses work:
[TLB hits and misses](img/tlb.png)

### Multi-Level Page Tables: 
- So far, we've been talking about a single page table for each process. In a 32-bit system, having 4KB pages with a 4-byte PTE for each page requires having a 4 MB page table in memory at all time for each process even if the process uses only a small part of the VM. This becomes a bigger problem in 64-bit systems. 
- This problem is mitigated with the use of **multi-level page tables**. There are many details, but the basic idea is that instead of having a single page table, there is a hierarchy of page tables for each process. Imagine we have a 32-bit address space partitioned into 4KB pages with page table entries having 4 bytes each. There are one million pages and for each one of these pages we have one PTE, which would require 4 million bytes (4MB) if we use a single page table. Imagine also that the address space has the following layout: The first 2K pages are for code and data, the next 6K pages are unallocated, the next 1023 pages are also unallocated, and the next page is allocated for the stack. The following image shows how a 2-level page table hierarchy is used to address such a layout:
![2-level page table hierarchy](img/multLevelPageTable.png)
- Each PTE in the first-level table is responsible for mapping a 4MB chunk of virtual address space, with every chunk containing 1024 pages. We need 1024 PTEs to cover the whole 4GB address space, so our level 1 page table is only 4KB in size. 
- As the image above shows, if every page in a given chunk is unallocated, the corresponding PTE is null. In our image, level-1 PTEs 2 to 7 are null because page is allocated in the corresponding chunks. If only one page is allocated in a given chunk, the corresponding level-1 PTE points to a level-2 page table.
- Each PTE in a level-2 page table is responsible for mapping a single 4KB page of virtual memory. Each of these level-2 page tables has a 4 KB size. 
- This scheme reduce the size of page table requirements in two ways:
	- If a PTE in level-1 table is null, the corresponding level-2 table doesn't have to exist. Most memory in a 4GB virtual address space is unallocated, so we save up a lot of space that would've been eaten by a single page table.
	- Only the 4KB level-1 page need be resident in memory at all time. level-2 pages can be created, paged in or paged out based on current needs. Only the mostly used level-2 pages need to be cached in main memory, hence reducing load on the system. 
- The following image shows how address translation is done with multi-level page tables. The virtual address is partitioned into a number of VPNs corresponding to the number of levels in our page table hierarchy and a VPO. Each VPN is an index into a a table in the hierarchy. Each PTE in the lower-level tables contains points to a higher-level table. PTEs in the highest-level table contains PPNs of physical memory or disk blocks:
![Address translation in a multi-level page table](img/multLevelAddrTranslation.png)
- Multi-Level page tables might seem inefficient, but they are not, because TLB caching makes them faster. Generally speaking, they are not that much slower than single page tables and are worth the spare space you get in your memory.

## Linux Virtual Memory System:
- *I skipped the part about Intel's i7's handling of virtual memory as it was too hardwary, and will focus on Linux's handling of the topic*.
- The virtual memory layout of a Linux process (Each process has its separate virtual address space) generally looks as follows:
![The virtual memory of a Linux process](img/linuxVM.png)
- The kernel virtual memory contains code and data structures in the kernel. Some regions of the kernel virtual memory are shared by all processes. Examples of such shared kernel memory regions include the kernel code and global variables. Linux also maps a set of contiguous virtual pages equal to all the system's DRAM pages to the corresponding set of physical pages. This allows the kernel to access any location in physical memory to do such operations as accessing page tables or memory-mapped IO operations, etc. The kernel region also contains data specific to each process such as page tables for each process or the stack that the kernel uses when it's running in the context of the given process.

### Linux Virtual Memory Areas:
- Linux organizes virtual memory as a collection of **areas** (also called **segments**). Areas are contiguous chunks of allocated virtual memory that is related in some way, for example, we have code area, data area, heap area, shared library area,etc. 
- Each existing virtual page is part of an area. A page that doesn't belong to an area does not exist and cannot be referenced. The kernel does not keep track of pages that don't belong to an area, so they don't consume memory or disk or kernel's memory itself. 
- The following image shows the kernel data structures that keep track of the areas of a process:
![How Linux organizes virtual memory](img/linuxVMOrg.png)
- These data structures include:
	- **`task_struct`**: is a task structure that the kernel maintains for each process. Each element in the task structure points to or contains all the data the kernel needs to run the process such as the PID, pointer to the stack, the PC, the name of the executable, etc. 
	- **`mm_struct`**: one of the data contained in a task structure element characterizes the current state of process's VM. It contains two important structures, `pgd` and `mmap`.
	- **`pgd`**: points to the base of the level 1 page table (*page global directory*, from which the structure's name comes). When the kernel runs the process, it stores the `pgd` in in the CR3 control register. 
	- **`mmap`** points to a list of `vm_area_struct`s.
	- **`vm_area_struct`**: (area structure) characterizes an area of the current virtual address space.
- A `vm_area_struct` itself consists of :
	- **`vm_start`**: points to the beginning of the area.
	- **`vm_end`**: points to the end of the area. 
	- **`vm_prot`**: describes the read/write permissions for all the pages in the area.
	- **`vm_flags`**: does various things, including describing if pages in the area are shared with other processes or private to the current process.
	- **`vm_next`**: points to the next area struct.

### Linux Page Fault Exception Handling
![Linux page fault handling](img/linuxPageFaultHandling.png)
- Remember that we talked about how the kernel intervenes when there is a page fault. When an exception occurs while the MMU is trying to translate a virtual address, control is transferred to the kernel fault handler which does the following:
	- The fault handler checks if the address is legal, meaning: is it in an area struct? The fault handler searches the address in the list of area structs by comparing the address with the `vm_start` and `vm_end` in each area. If the address is not legal, the fault handler triggers a segmentation fault and terminates the process. A process can create an arbitrary number of areas, so Linux places the list in a tree structure for speedy search when there are too many areas.
	- Is the attempted memory access legal? If the process is violating access permissions such as trying to write into a read-only area or if a process running in user mode is trying to read from the kernel's virtual memory, then the handler triggers a protection exception which terminates the process. 
	- The kernel knows now that the page fault resulted from a legal operation on a legal area. It selects a victim page from the area, swaps out the victim page if it's dirty, swaps the new page and updates the page table. When the fault handler returns, the CPU reruns the faulting instruction which resends the address to the MMU. This time the address is translated normally and no page fault occurs. s

## Memory Mapping:
- Linux and other Unix systems initialize the contents of virtual memory area with **memory mapping** which is  associating this memory area with an *object* on disk. A memory area can be mapped to one of two types of objects:
	- **Regular file in the Unix file systems**: (:confused:*This kinda doesn't make much sens e to me*:confused:). An area is mapped to a contiguous section of a disk file such as an executable object file. This file section is divided into page sized chunks with each chunk "obtaining the initial contents of a virtual page"!!! Due to demand paging, virtual pages are only swapped into physical memory when the CPU touches them (the CPU issues an address that goes into one of these pages.
	- **Anonymous file**: Anonymous files created by the kernels get swapped into physical addresses directly and no disk is involved (*zero-demand*)!!! 
- In both regular and anonymous files, once a page is created it is swapped back and forth into a **swap file** (also called *swap area* or *swap space*)maintained by the kernel. 

### Shared Objects:
- Memory mapping has resulted from the fact that integrating virtual memory and the file system provides a simple and efficient way of loading code and data into memory.
- While each process has its private virtual address that shouldn't be accessed by other processes, there is also code and data that multiple processes share such functions from the C standard library functions. It would extremely wasteful to include separate copies of this shared data and code in the virtual address space of each process. Luckily, memory mapping comes to the rescue and allows multiple processes to share the same objects. 
- An object can be mapped into an area of virtual memory as either a **shared object** or **private object**. If a shared object is mapped to an area in the private virtual space of a process, then any writes the process makes to that area are visible to all other processes that have have mapped that same shared object to their private virtual address spaces. The changes are also reflect on the original object in disk. 
- Changes made to an area mapped to a private object are not visible to other processes, and writes that the process makes to the area are not reflected back to the object on disk. An area in the private virtual address space to which a shared object has been mapped is called a **shared area**, and the area to which a private object has been mapped is a **private area**. 
- The following image shows how multiple processes map a shared object to their private VASs. Process 1 and process 2 don't have to copy the shared object the same address in their VASs. Because every object has a unique file name, the kernel easily  determines that process 1 has already mapped the shared object so it directs the PTEs of process 2 to point to the known physical addresses. A shared object does not need to have multiple copies in physical memory, even though it is mapped to multiple shared VAS areas:
![Shared object](img/sharedObject.png)
- Private objects are mapped to virtual media using a technique called **copy-on-write**. A private object starts life like a shared object as the following image shows:
![Private copy-on-write object](img/privateCopyOnWrite.png)
- In the processes that map the private object, the PTEs corresponding to the private area are flagged as read-only and the area struct is flagged as *private copy-on-write*. As  long asneither process attempts to write to the private area, the two processes continue to share the copy of the object in physical memory, but as soon as any process attempts to write to some page in the private area, the write triggers a protection fault.
- When the protection fault notices that the exception was caused by an attempt to write to a page in a private copy-on-write area, it creates a new copy of the page in physical memory, updates the PTE to point to the new copy, and then restores write permissions to this new page. When the fault handler returns, the CPU redoes the write on the newly created page. *These freaking nerds!!! Smart as hell!!👍👍*. This is some very efficient use of physical memory. 

### `fork`:
- As far as virtual memory is concerned, when the current process calls `fork`, the kernel creates exact copies of the current process's `mm_struct`, area structs and page tables. It flags each page in both processes as read-only and flags each area struct in both processes as private copy-on-write. When fork returns the new process, it has an exact copy of of the virtual memory as it it existed before the call to `fork`. (*The parent or child virtual memory??!*). Only when wither the parent or child processes make writes that new pages are created using copy-on-write. 

### User-level Memory Mapping with the `mmap` Function:
- Unix processes can use the **`mmap`** function to create new areas of virtual memory and map objects into these areas:
```c
#include <unistd.h> 
#include <sys/mman.h>

void *mmap(void *start, size_t length, int prot, int flags, int fd, off_t offset);
```
- `mmap` asks the kernel to create a new virtual memory area, starting at the address `start` if possible and map a contiguous chunk of the object given by file descriptor `fd` to this newly created area. This contiguous chunks is `length` bytes long and starts at an offset `offset` from the beginning of the file. The start is usually a NULL. The following image visualizes `mmap` argumetns:
![mmap arguments](img/mmapArgs.png )
- The `prot` argument contains access permission bits:
	- **`PROT_EXEC`**: Instructions in pages in the area may be executed.
	- **`PROT_READ`**: Pages may be read.
	- **`PROT_WRITE`**: Pages may be written.
	- **`PROT_NONE`**: Pages in the area cannot be accessed.
- The `flags` argument specifies the type of the mapped object:
	- **`MAP_ANON`**: Anonymous object with zero-demand.
	- **`MAP_PRIVATE`**: Private object with copy-on-write.
	- **`MAP_Shared`**: Shared Object.
- A similar function **`munmap`** does the opposite, deletes areas from regions of virtual memory.

## Dynamic Memory Allocation:
- **Dynamic memory allocators** are thought to be more convenient and more portable the `mmap` and `munmap` to acquire more virtual memory at run time.
- A dynamic memory allocator maintains an area of the process's virtual memory known as the **heap**. The heap is a demand-zero are that starts immediately after the uninitialized bbs area and it grows upwards toward higher addresses. The kernel maintains a variable **`brk`** (break) that points to the top of the heap. The following image shows the heap in the context of a process's virtual memory:
![The heap](img/heap.png)
- An allocator maintains the heap as a collection of various-sized **blocks**. These blocks can be either **allocated** or **free**. A an allocated area has been reserved for use by the application, while a free area is available to be allocated. A free blocks is free until the application explicitly allocates it. An allocated block stays allocated until it is explicitly freed by the application or implicitly freed by the dynamic allocated. (*Looks like we will see later what these implicit/explicit words mean*).
- There are two styles of allocators. They both explicitly allocate blocks, but they differ in how they deallocate blocks:
	- **Explicit allocators**: require the application to explicitly free the allocated blocks. C has the explicit allocator `malloc` for allocating blocks and `free` for freeing allocated blocks.
	- **Implicit allocators**: require the allocator to detect when an allocated block is no longer in use and free the block. Implicit allocators are called **garbage collectors**, and the process of automatically freeing unused allocated blocks is called **garbage collection**. Higher-level languages such as Java rely on garbage collectors to free memory.
- The rest of this section will focus on explicitly memory allocation with a focus on allcators that manage heap memory. Keep in mind that memory allocation is not specific to the heap but is a general idea that applies to other contexts. Garbage collection is deferred to the next [section](#garbage-colelction).

### The `malloc` and `free` Functions:
- The C standard library has an explicit memory allocator called the **`malloc`** package. Heap memory is allocated using the `malloc` function:
```c
#include <stdlib.h>

void *malloc(size_t size); // Returns pointer to allocated block, or NULL on error!
```
- `malloc` returns a pointer to a block of memory that is at least `size` bytes which is aligned to an 8-byte boundary (double word. *From now on in this document words means 4 bytes*).
- If an error is encountered, such as requesting a block larger than available memory, `malloc` returns a NULL and sets `errno`. `malloc` does not initialize the memory it allocates. Initializing memory can be done with a wrapper around `malloc` called **`calloc`** that initializes the allocated memory to 0. **`realloc`** can be used to to resize an allocated block. 
- Dynamic allocators such as `malloc` can also allocate or deallocate heap memory explicitly using `mmap` and `munmap`. They can also use **`sbrk`** (We are talking here about resizing the heap area and not allocating blocks within the heap):
```c
#include <unistd.h>

void *sbrk(intptr_t incr); // Returns: old brk pointer on success, −1 on error
```
- `sbrk` resizes the heap by adding `incr` to the kernel's `brk` pointer. On success, `sbrk` returns the old value of `brk`, but if a problem is encountered, it returns -1 and sets `errno` to `ENOMEM`.
- Allocated memory is freed with the **`free`**:
```c
#include <stdlib.h>

void free(void *ptr);
```
- The `ptr` pointer must point to the beginning of an allocated block that was obtained from `malloc`, `realloc` or `calloc`. If not, the behavior of `free`. Something bad can go wrong and you are not alerted. 
- The following image shows how `malloc` and `free` work on a small 16-word double-world aligned heap where each word is 4-byte long:
![How malloc and free work](img/mallocFree.png)
- This is what is happening in the image above:
	- **a**. The program uses `malloc` to request a 4-word block. `malloc` allocates the specified block from the beginning of the free block and returns a pointer to the beginning of the allocated block. 
	- **b**. The program requests a 5-word block, and `malloc` allocates a 6-word block *padding* the requested 5-word with an extra word to keep the block "aligned to a double-world boundary".
	- **c**. Same as a.
	- **d**. The program frees the 6-word block allocated in b. `p2` still points to a freed block. Reusing it might cause problems until reinitiated by a call to `malloc` or one of its wrappers.
	- **e**. The program requests a two-word block and `malloc` that in a previously freed block and returns a pointer to this block. *What if I wanted the block to be beyond any of the previously allocated blocks, like closer to the heap's head??!!!!*

### Why Dynamic Memory Allocation?
- The main and obvious reason for using dynamic allocation is that the programmer doesn't know the sizes of certain data structures until run time. The naive alternative is to define static data structures such as static arrays with a specific length. The problem with static arrays is that they can be become a maintainability nightmare if they start receiving data that is larger than their fixed lengths. The static array might also be too large and sitting idle handling only small data while most of it goes  unused. With dynamic, you are guaranteed elastic structures that are allocated and freed based on demand. They can be expanded to handle large amounts of data or deallocated when longer needed thus freeing memory the limited memory resource for other parts of the program or other programs in the system. 
- The main problem with dynamic memory allocation is that it is often misunderstood and baffling to novices and sometimes even experts. The rest of the section will try to demystify some aspects of dynamic memory allocation.

### Allocator Requirements and Goals:
- An explicit allocator is must respect the following constraints:
	- **Handling arbitrary request sequences**: An application can make an arbitrary sequence of allocate and free requests with the constraint that a free requests must correspond to a currently allocated block obtained with a previous allocate request. There are not assumptions about the ordering of allocate and free requests: an allocate request is not necessarily followed by a matching free request.
	- **Making immediate responses to requests**: The allocator cannot reorder or buffer requests to improve performance. It must respond immediately to requests. 
	- **Using only the heap**: all non-scalar data structures must be stored in the heap. 
	- **Aligning blocks (alignment requirement)**: In most systems blocks are aligned on an 8-byte boundary, so that the allocated area can hold any type of object. 
	- **Not modifying allocated blocks**: Allocators cannot move or modify blocks that are already allocated. 
- If you are planning to design an allocator, you should achieve the two main goals of maximizing throughput and memory utilization:
	- *Goal 1: Maximizing throughput.* An allocator's **throughput** is the number of requests it completes per unit times. If an allocator can complete 500 allocate and 500 free requests in a second then its throughput is a 1000 requests per second. Allocator's throughput can be maximized by improving the average time to complete free and allocate requests. We can improve throughput to have a worst-case allocate that is linear to the number of free blocks and a constant runtime for free requests.
	- *Goal 2: Maximizing memory utilization.* Virtual memory is a finite resource limited by the swap space on disk. Dynamic memory allocator usually handle very large blocks of memory, so how is memory utilization maximized by dynamic allocators? There are different ways to measure how memory efficient an allocator is such as **peak utilization**. The peak utilization can be defined by the aggregate block payload in bytes of a sequence of requests divided by the total size of the *monotonically nondecreasing (what!!!!? :confused:)* heap. *(Not very sure, hopefully next sections will clarify this)*. There is tension between the maximal throughput and maximal memory utilization, each one of the two can be maximized at the expense of the other. The programmer needs to strike a good balance between the two.

### Fragmentation:
- **Fragmentation** is the main culprit behind poor heap memory utilization. Fragmentation occurs when "otherwise unused memory is not available to satisfy allocate requests". Fragmentation appears in two forms:
	- **Internal fragmentation**: occurs when an allocated block is larger than the payload. This happens usually as a result of alignment constraints (as we've seen earlier) or when the allocator imposes a minimum size of the allocated block and the payload is smaller than that minimum. It can be measured by summing the aggregate difference of allocated blocks and their payloads.
	- **External fragmentation**: occurs when there is enough aggregate free memory to satisfy an allocate request, but these blocks are scattered all over the place and no single free block is able to satisfy the request. External fragmentation is less quantifiable than its internal counterpart, because it depends on previous as well as future requests. External fragmentation is harder to predict, so allocators try to heuristically maintain small numbers of large free blocks.

### Implementation Issues:
- If we are trying to design our own dynamic memory allocator, our heap would be a large array of bytes and we will use pointer `p` that initially points to the first byte of the array. To allocate `size` bytes, our `malloc` increases `p` by `size`, stores the new `p` on the stack and returns the old value of `p` to the calling function. `free` doesn't do anything.
- This design has an excellent throughput, but a terrible memory utilization because there is no reuse of freed blocks (there is no freeing of blocks in the first place). An actually useful allocator that balances between memory utilization and throughput needs to consider the following issues:
	- *Free block organization*: We need a way of keeping track of free blocks.
	- *Placement*: Decide in which free block a newly allocated block must be placed.
	- *splitting*: Deciding what to do with the remaining free space in a block after allocating a new block in that free block. 
	- *coalescing*: What to do with a block that has just been freed. 

### Implicit Free Lists:
- A self respecting memory allocator must have a data structure that keeps track of block boundaries (where a blocks starts and ends) and distinguishes between free and allocated blocks. Most allocators include such information in the blocks themselves as the following images shows:
![Simple heap block format](img/heapBlockFormat.png)
- In the image above, we see that a block consists of three parts: a one-word (4-byte) *header*, the block's *payload*, and optional *padding*. 
- The **header** is used to encode the block size (including the header and padding) and if the block is allocated or free. If a double-word alignment constraint is applied to the block then the block size is always a multiple of 8, making the 3 low-order bits always zero. We need only 29 bits to represent the block size and as a result we have 3 free bits which we can use to encode other information about the block. 
- The least significant bit in the header is called the **allocated bit**. It is used to indicate whether the block is allocated when it is 1, or free (0). An allocated block whose size is 24 (`0x18`) bytes has a the following header:
```
0x00000018 | 0x1 = 0x00000019
```
- A free 40 (`0x28`)-byte block has the following header:
```
0x00000028 | 0x0 = 0x00000028
```
- Using the configuration of a block from the previous image, we can view the heap as a sequence of contiguous free and allocated blocks:
![Organizing the heap with an implicit free list](img/implicitFreeListHeap.png)
- This organization of the heap is called **implicit free list** because "blocks are linked implicitly by the size fields in the headers"???!!! :confused:. To traverse the list of free blocks in the heap, the allocator must traverse all the blocks including allocated ones. In this list, we also having a special terminating block with the allocated bit set and a size of zero. 
- The implicit free list scheme is simple but not very efficient. Any operation, such as allocating a block might require a sequential search through the whole list of blocks.
- The **minimum block size** in this configuration is mainly dictated by the alignment constraint. Even if we need only a single byte, we must allocate a double-word block. 

### Placing Allocated Blocks:
- When the application requests a block, the allocator searches the free list for a free block that is large enough to hold the requested block. The way the allocator does this search is called the **placement policy**. There different placement policies, and they include:
	- **First fit**: Starts searching the list until it finds the first free block that fits. The first fit policy tends to leave large free blocks at the end of the list which is good, but also have the bad side of effect of leaving a bunch of free small free splinters towards the beginning of the list which causes long search times for large blocks.
	- **Next fit**: Similar to first fit but instead of starting at the beginning of the list, it starts where the previous list stopped. Proposed by eminent nerd, D. Knuth, next runs significantly faster than first fit has a worse memory utilization.
	- **Best fit**: examines all the free blocks, and picks the smallest free block that fits. It has the best memory utilization, but using with simple free list organizations such as implicit free list can incur significant throughput penalties due to exhaustive searches for best fit searches. 

### Splitting Free Blocks:
- Once a free block is found, the allocator must decide what it should do with the remaining free portion of the free block. It can either allocate the whole block, or just use what is needs (including padding imposed by alignment and what not) and **split** the block into two parts, a portion for the allocated bytes and a new free block occupying the rest of the block. Using the whole block introduces internal fragmentation. Looks like splitting is the better option.

### Getting Additional Heap Memory:
- What if the allocator can't find a free block large enough to satisfy a request? In this case the allocator can do one of two things:
	- It can either *coalesce* smaller adjacent free blocks to get a block large enough to hold the requested size.
	- If the coalesced blocks don't satisfy the request, the allocator acquires more heap space with a call to `sbrk`. 

### Coalescing Free Blocks:
- When a block is freed, it might be adjacent to one or two free blocks. Now we have 2 or 3 adjacent free blocks. This results in something called **false fragmentation** where there is a bunch of adjacent tiny but unusable free blocks that are good for nothing. 
- To mitigate false fragmentation, we merge small adjacent free blocks in a process called **coalescing**. The allocator, however, has to decide when to perform coalescing so we have two types of coalescing:
	- **Immediate coalescing** where adjacent blocks are coalesced immediately after a block is freed.
	- **Deferred coalescing** where coalescing happens at a later time than freeing, for example when a request fails, at which point the allocator scans the entire heap coalescing all coalesceable blocks.
- Immediate coalescing is simple but it can introduce thrashing where blocks are repeatedly unnecessarily split and coalesced back following allocations/freeings. Self-respecting allocators go for deferred coalescing to cut unnecessary coalescing. The header of the current block checks the header of the next block to see if it is free and if so, the current block simply adds the size of the next block to its own size, but what how would the current block efficiently coalesce the free block before it?

### Coalescing with Boundary Tags:
- How is coalescing done? Assuming we are doing immediate coalescing, let's call the block we want to free the *current block*. After freeing the current block, coalescing the block following it is easy. With an implicit free list of blocks with headers, the only way to check for the previous free block is to scan the whole list to see if the previous block is free. This makes `free` run in linear time which is kinda too much. 
- Super smart D. Knuth invented **boundary tags** which allow for coalescing in constant time. The basic idea is adding a **footer** that is a replica of the header at the end of each block. Now, coalescing the previous block can be done in constant time because the current block can simply examine the footer of the previous block because it is always the word that precedes it. The following image shows the structure  of a block that uses boundary tags:
![The format of a block that uses boundary tags](img/boundaryTag.png)
- Coalescing with boundary tags is a fairly simple business, but requiring each block to have a header and a footer can be taxing on memory if the application allocates and frees many small blocks. The book gives an example of allocating and freeing many graph nodes that are only one or few words long. The header and footer could eat up half the size of a block.
- There is a clever optimization that can eliminate much of the memory overhead introduced by footers. Only free footers really need a footer, while allocated blocks don't, how how can the current block know if the previous block is free? Remember that blocks have 3 low order bits that don't represent size. We use the lowest bit as an allocated bit. We can actually use the second or third bit as the allocate bit of the previous block so the current block 

### Explicit Free Lists:
- Actual general-purpose allocators do not use implicit free lists because searching for a free block requires the traversal of both allocated and free blocks. An alternative and better approach is **explicit free lists** where only free blocks are searched. This arrangement reduces the search time to only the number of free blocks instead of all blocks in the heap.
- One implementation of an explicit free list involves the use of a doubly-linked list with pointers stored in the blocks themselves. Each free block has a predecessor pointer and successor pointer pointing to the closest other free blocks to them. The following image shows how blocks are organized into doubly-linked lists:
![Heap blocks that use doubly-linked free lists](img/blockLinkedList.png)
- The time to find a free block can even be constant based on the ordering of blocks in the list, so we can order blocks based on the recency of their freeing or based on their addresses in the heap and each one has its own advantages and disadvantages. 
- The disadvantage of explicit lists is that they require a large enough minimum block size that accommodate the previous and predecessor pointers (that's 4 words) in addition a header and possibly a footer which results in more internal fragmentation. 

### Segregated Free Lists:
- It might be very costly to traverse all free lists if they are all placed in one long linked lists. An improvement on explicit free lists is based **segregated storage** where the list is divided into different classes of smaller lists that contain blocks of similar sizes. There are different ways of devising these classes. For example, smaller blocks can be assigned to classes of their sizes while larger ones can be powers of 2 as in: 
	- ***{1}, {2}, {3}, . . . , {1023}, {1024}, {1025−2048}, {2049 − 4096}, {4097−∞}***
- The allocator also maintains an array of these lists ordered by increasing size. When the allocator needs a block of a given size, it index searches the array (it's an ordered array, *so efficient!!!*) and if the given size is not there, it searches the next position in the array and so on. 
- One good variant of segregated storage is the so-called *segregated fit* storage. An allocator using segregated fit maintains an array of lists of free lists where each list is organized as an implicit or explicit list of a size class. Each lists can contain multiple sizes belonging to the appropriate size class. To find a free block, we determine the appropriate size class and search its list. If found, we might split the free block and allocate our block. If not found, we scan the next list  and keep scanning next class lists until we find the appropriate size. If not found in the class list, we request additional heap memory from the kernel, use that and place the remainder free space in the appropriate class list. When we free a block, we coalesce free space around it.
- Segregated fit is used in actual high-performance dynamic memory allocators such as the GNU `malloc` because it is both fast and memory efficient. It is fast because, it searches only a portion of the heap blocks instead of the entire heap. It also has maximal memory utilization because it approaches best-fit search.

## Garbage Collection: 
- With explicit allocators such as `malloc`, the application is responsible for allocating new memory blocks and freeing those blocks it no longer it needs. Failing to free allocated memory is a common mistake among programmers. Examine the following code:
```c
void garbage(){
	int *p = (int *) malloc(23454);
	return;
}
```
- The function `garbage` above allocates some memory but never releases it. This useless block will stay allocated for the lifetime of the program, occupying heap space that could've been used for something else.
- A **garbage collector** is a dynamic memory allocator that automatically frees allocator memory blocks that are no longer needed. Allocated but not needed blocks are called **garbage** and **garbage collection** is freeing these unneeded resources. In a system that supports garbage collection, applications explicitly allocate resources but never explicitly frees them. Instead, the garbage collector periodically finds garbage blocks and frees them. 
- Garbage collectors were first used with Lisp in the 1960s by some John McCarthy that I've never heard of. They are an important part of modern languages such as Java and Python. They also remain an important area of research. The rest of this section will focus on the original McCarthy's *Mark&Sweep* algorithm. It can actually be built on top of a `malloc` package to provide garbage collection for C.

### Garbage Collector Basics:
- A garbage collector views memory as a directed *reachability graph* that looks as the following images shows:
![Memory as a directed reachability graph](img/directedReachabilityGraph.png)
- The nodes in this graph are divided into two sets: **root nodes** and **heap nodes**. Each heap node corresponds to a block allocated in the heap. A directed edge ***p → q*** means that a location in block ***p*** points to a location in block ***q***. Root nodes are locations outside the heap containing pointers to locations inside the heap. Root nodes can be registers, variables on the stack or global variables in the read-write area of the VM.
- A node is **reachable** if there is a directed path from any root node to it. *Unreachable* nodes are garbage that can never be reached and used by the application again. The job of a garbage collector is to "maintain some representation of the reachability graph" and periodically free the unreachable nodes.
- Garbage collectors for interpreted languages like Java can keep an exact representation of the reachability graph and thus free all garbage. In C and C++, a garbage collector cannot maintain an exact representation of a reachability graph, so it is called a **conservative garbage collector**. In such a garbage collector, each reachable node is correctly identified as reachable but some unreachable nodes are wrongly identified as reachable. 
- A garbage collector might collect garbage on demand, or run on a separate thread and continually updating the reachability graph and collecting garbage.	 

### Mark&Sweep Garbage Collectors:
- **Mark&Sweep** collectors consist of two phases: 
	- A **mark phase** where all reachable and allocated descendants of the root nodes are marked.
	- A **sweep phase** which frees all unmarked allocated blocks.
- Usually, one of the low order bits of a block's header is used to mark that block.
- Generally speaking, a `mark` phase function would go over all root nodes and start marking all their reachable descendants that are unremarked heap blocks recursively until they are all marked. At the end of marking, any heap blocks that are unmarked are guaranteed to be unreachable. 
- A `sweep` function would go over all the blocks in the heap and free all blocks that are allocated but unmarked.

## Common Memory-Related Bugs in C Programs:
- Managing virtual memory is fraught with errors and bugs. They are scary and often appear far away from their original causes both in time and space. A program would run fine for a long before a memory-related bug crashes it. Bugs can also seem to have little  relevance to the actual cause. This section is a cheat sheet listing some of the more common memory bugs and errors that plague the code of C programmers.

### Dereferencing Bad Pointers:
- Remember from the section on Linux virtual memory layout. We saw the a process's virtual address space is divided into areas and these areas can be separated by holes that the kernel doesn't keep track of. These holes cannot be dereferenced, and any attempt to dereference them results in a termination of the program with a segmentation exception (the so called seg fault).
- Other regions of the process address space are read-only, so attempting to write to such areas also terminates the program with a protection exception.
- One common example of bad pointer dereferencing is the infamous `scanf` bug. `scanf` is used to read a string from `stdin` into a variable by passing to it a format string and the address of the said variable as in `scanf("%d", &val)`. Novice programmers pass the value of the variable itself instead of its address: `scanf("%d", val)`. The program interprets `val` as an address and attempts to write to it. If you are lucky, the program terminates immediately with an exception. If you are unlucky, your program writes to a valid read/write area causing some obscure and probably disastrous problems. 

### Reading Uninitialized Memory:
- bss memory location (*damn it, I should've read the linking chapter!!*) such as global variables are always initialized to something like zeros, but heap memory variables are not initialized. `malloc` allocates memory but does not initialize the block it initialize. This is instead done its wrapper `calloc`.

### Allowing Stack Buffer Overflows:
- A program suffers from a buffer overflow when it writes to a target buffer on the stack without checking the input size. The following function suffers from a buffer overflow bug, because `gets` doesn't check the input size:
```c
void bufferOverflow(){
	char buf[64];

	gets(buf);

	return;
}
```
- Replacing `gets` with `fgets` which checks the input size is the fix. 

### Assuming that Pointers and the Objects They Point to Are the Same Size:
- Pointer syntax is just confusing and pointers in general are the bane of programming in C. Make sure that you don't confuse pointers with data they point to. This  might not be a problem where a pointer type has the same size as the type of object it points to, but this is not always the case.Programmers usually commit this mistakes and often don't get any warnings, although compilers are becoming smarter and usually give you warnings about such errors.

### Making Off-by-One Errors:
- C doesn't check array boundaries or give you a `ArrayIndexOutOfBoundsException` like Java, so if go over the bounds of an array by by 1 index (a very common error), you might corrupt a crucial part of virtual memory that follows your array.

### Referencing a Pointer Instead of the Object It Points to:
- The expression `*val--` is most probably wrong and was meant is `(*size)--`. We are trying to decrement `val`, the content of pointer but `*val--` decrements the address of that value. This is caused by the precedence and associativity rules of the C language. `*` and `--` have the same precedence and associate from right to left. To be on the safe side make sure to always use parentheses to explicitly override the confusing precedence rules. 

### Misunderstanding Pointer Arithmetic:
- Pointer arithmetic is done in units equal to the size of objects they point to and not bytes.

### Referencing Nonexistent Variables:
```c
int *stackref(){
	int val;

	return &val;
}
```
- `val` in the example above only exists during the lifetime of the function `stackref`. `val` lives in the stack which is popped after the function returns. While the pointer still points to a valid memory address, it points to an invalid variable. That same location might be reused by other function stacks, so changing the returned pointer might corrupt a stack variable of that function. This is a little subtle and one those sneaky and dangerous bugs. 

### Referencing Data in Free Heap Blocks:
- It is easy to find oneself in scenarios where one allocates some heap space, frees it, and then tries to access that space. Because that heap region is now free, it might have been allocated by some other part of the program and its values overwritten. This is another silent bug that's hard to track.

### Introducing Memory Leaks:
- **Memory leaks** mean allocating blocks, say in a functions and returning without ever freeing them. If such a function is called frequently, then the unfreed garbage will grow the heap until it eats up the whole virtual memory space. This is especially bad for daemons and servers that never terminate.  
