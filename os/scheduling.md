# Scheduling:
## Table of Contents:

## Intro:
- This chapter will cover the very important OS topic of scheduling. **Scheduling** basically refers to the **high-level policies** used by the OS to manage slices of time it allots to each process. While *Computer Systems, a Programmer's Perspective* went into great detail describing the low-level mechanisms of how processes are created, stopped, etc. It only acknowledged the existence of a scheduling mechanism (or should I say policy/policies?!) and never said what it was, how it worked, etc. Our discussion of scheduling will be divided into 4 major sections with each section roughly corresponding to a chapter from the book:
	- An overview of scheduling.
	- An overview of a popular scheduler (or scheduling policy) called **multi-level feedback queue (MLFQ)**.
	- Covers another popular scheduler: **proportional share**.
	- Discusses scheduling in multiprocessor hardware. 
- Again, I will try to avoid unnecessary waffling and not repeat anything that was covered in CSAPP.

## Scheduling:
### Preliminary Assumptions and Some Useful Metrics:
- Processes running in a system are collectively called the **workload**, and processes can also be called **jobs** (I believe this weird alternative terminology might come from the fact that OS scheduling took much of its inspiration from the field of operations management). To understand scheduling step by step, let's start by making some basic but truly unrealistic assumptions about the workload:
	1. Jobs run for the same amount of time.
	2. Jobs arrive at the same time (to the CPU or scheduler? :confused:).
	3. Jobs run to completion (A job is not interrupted midway to perform another job).
	4. Jobs us the CPU only, and don't perform any IO operations.
	5. The scheduler (or CPU :confused:) knows the run-time of each job.
- The topic of scheduling is heavy on metrics as a self-respecting OS is all about metrics and scheduler play a central role in the performance of an OS. Let's start with a very basic metric: the **turnaround time** metric. It is the amount of time separating when the job first arrives to the system and the moment when it completes running:
	- ***T<sub>turnaround</sub> = T<sub>completion</sub> - T<sub>arrival</sub>***
- Because we are assuming at the moment that all jobs arrive to the system at the same time, ***T<sub>arrival</sub> = 0*** which means ***T<sub>turnaround</sub> = T<sub>completion</sub>***. We will change this assumption later for sure!
- This section focuses on performance metrics, but there are also **fairness** metrics, and performance can be increased at the expense of fairness and vice versa!

## First In, First Out (FIFO):
- A **first in, first out (FIFO)** scheduling scheme dictates the job that arrives first needs to be done first. Imagine 3 jobs A, B and C arriving all at once but each respectively arrives slightly before the other. Imagine that A takes 100 ms to run, and B and C take 10 ms each (we've just relaxed the first assumption: jobs don't run for the same amount of time anymore). The average turnaround for this workload is ***(100 + 110 + 120) / 3  = 110***. Do B and C have to wait such a long time for A to finish executing?! It seems kinda wasteful! This problem is called the **convoy effect**. It is akin to standing in line for a cash register with a soda bottle behind a lady with a cartful of groceries!

## Shortest Job First (SJF):
- The **shortest-job-first (SJF)** scheme tries to answer this specific convoy effect by picking the shortest jobs to run first, so B and C will be run before A. Their turnaround is ***(10 + 20 + 120)/ 3 = 50***. This is a great improvement over the FIFO approach.
- Let's now relax our second assumption and imagine that A arrives at time 0 ms, B arrives at 10 ms, and C arrives at time 20 ms. The three still run respectively for 100, 10 and 10 milliseconds. When B and C arrive, A would have already started running, and B and C won't start running until A finishes. SJF still suffers from the convoy problem.

## Shortest Time-to-Completion First (STCF):
- To address the convoy problem in SJF that arises from jobs arriving at different times, we have to relax the 3rd assumptions. Jobs need not run to completion anymore. A job can be interrupted midway and the context be switched to another job. The scheduler is said to **preempt** a job and run another. Schedulers that do this are called **preemptive schedulers**. They use context switching and timer interrupts to achieve this.
- The **shortest time-to-completion-first (STCF)** scheduler (also called **preemtive shortest job first (PSJF)**) does just that. The long job A starts at 0. Each time timer interrupt occurs control is returned to the kernel which decides whether to continue the job. If the shorter job B is available, it runs and completes, and then the kernel comes back to job A to complete it.

## Response Time, Another Metric:
- **Response time** is defined (at least according to the authors of the book) as:
	***T<sub>response</sub> = T<sub>arrival</sub> - T<sub>firstrun</sub>***
- Others might define response time as distance in time between the arrival of the job and when it first produces as a job.
- Anyways, response time appear particularly in applications requiring interactivity such as shell programs which you expect to respond quickly.
- The problems associated with response time arise when, for example, 3 jobs arrive at the same time. Imagine they all run for equal periods of time. The second job has to wait for the first one to complete, and the third job has to wait for the previous two! The response of the third job is too bad and the average of the three is also bad.

## Round Robin (RR):
- Imagine again that three same-length jobs arrive at the same time. STCF won't work here, because they all have the same time length, and there is no reason why the STCF scheduler would switch to another one. **Round Robin (RR)** scheduler comes to the rescue! It doesn't run jobs to completion, but instead divides time into **time slices** (also called **scheduling quantum**), and then run first program during first slice, then switch to the second job in the second, slice, etc. The length of a time slice must be a multiple of the timer interrupt. 
- To achieve high response-time performance, time slices need to be small; but smaller time slices can incur heavy overhead emanating from constant context switching! Context switching is a heavyweight operation that involves saving and restoring registers and some cache magic and whatever, and abusing can be really bad for overall performance!
- We need to make trade-offs and tweak the size of time slices until we get to a sweet spot between responsiveness and lowering the costs of context switching. We need to ***amortize*** (yeah, whatever) the cost of context switching (the authors say that if it takes fixed 1 millisecond to context switch, this would mean a 10% performance penalty on a 10 millisecond time slice. If we make the time slice 100ms long, the cost of context switching becomes 1 % as per time slice).

## Performance vs. Fairness:
- RR is great for response time but terrible for turnaround. RR favors fairness, but it hurts performance. SOme jobs that could've finished earlier have to share time with others! Systems are all about trade-offs and achieving both performance and fairness is a great example of this need for fairness!

## Adding IO:
- Let's now abandon our 4th assumption. If two jobs arrive to the system and one job makes an IO request, the scheduler should not wait for that job to complete its IO operation and sit idle. It should immediately switch to the second job and run a slice of it before returning to it when the IO operation is done. The book says that a job involving multiple IO requests should break that job into separate jobs and treat each CPU burst other than when the job is blocked during the IO fetch as if it were an independent job. The IO blocked time should be used to run other jobs.

## No ***A Priori*** Knowledge about the Job Run-Time:
- OSs don't know anything about the length of jobs so it cannot tell for how long they can run, so that was a wrong assumption. Smart schedulers, however can make modest predictions about future based what they've seen in the past! We will see this in the next section about MLFQ. 

## Multi-Level Feedback Queue (MLFQ) Scheduler:
- The **multi-level feedback queue (MLFQ)** was first described by a certain Corbato et al. in 1962 and has been a very influential ever since!
- MLFQ tries to achieve two goals: 
	- Minimize *turnaround time*. How can a scheduler minimize turnaround time by running shorter jobs before longer jobs STCFs style without knowing how long a process would run? 
	- Minimize *response time*, but we know that minimizing response time can come at the expense of turnaround time. How can a scheduler do both in a satisfactory manner?!

### MLFQ, the Basics:
- MLFQ has different implementations that differ in details, but the general rules are very similar.
- MLFQ has a number of queues, and each queue has a different **priority level**. At any point in time a queue can have 0 or more jobs. MLFQ uses the priority levels of job's queues to decide which next job to run. A queue can have multiple jobs which would have the same priority. In such case, MLFQ can decide which of these to run by using some algorithm. The authors suggest round-Robin (RR). These rules can be summarized as:
	- **Rule 1**: If ***priority(A) > priority(B), then run A***.
	- **Rule 2**: If ***priority(A) = priority(B), then run A and B in RR***.
- But how does MLFQ set priority? Well, instead of assigning fixed priorities to jobs, MLFQ moves a job up and down the priority scale based on its *observed behavior*. For example, a job that repeatedly let go of the CPU while waiting for a a keyboard input is an interactive application whose priority must be high. An application with intensive use of the CPU for longer times gets a low priority. In this way, MLFQ *learns* from the *history* behavior of processes to predict their *future*.
- The following diagram shows how MLFQ works. Jobs A and B have a high priority, while C and D have lower priorities:
![MLFQ](img/MLFQ.png)
- For the rest of this section, we will try to understand how priority changes over time. We will continue to improve and add on more rules to our MLFQ until we have a complete picture of how it works.

### Changing priority:
- A job doesn't live its entire life inside one queue, but its priority changes dynamically as it lives. Imagine that our workload is a mixed bag of IO-bound interactive short running jobs, and a long running CPU-bound non-interactive jobs. The priorities of such jobs can be changed according to these rules:
	- **Rule 3**: When a job first arrive to the scheduler it is placed in the highest priority queue.
	- **Rule 4a**: If a job uses an entire time slice without letting go of the CPU, its priority is reduced.
	- **Rule 4b**: If a job lets go of the CPU before its time slice is over, the job stays in the same priority queue.
- Following these rules, imagine we have a long-running CPU-bound job arriving at the scheduler. It is first placed at the highest priority queue. It eats through the whole first time slice so it gets downgraded to the next lower priority queue. It keeps doing so until it reaches the bottom of the queue.
- Imagine a second job, but this time a short job enters the system before the first long job is over. The short job is placed in the highest priority queue. This short job might either stay in the highest queue or at worst be downgraded one or queues only because it is short. The scheduler will interrupt the long job, and switch to executing this short job because it still has a higher priority. This way, MLFQ mimics SJF.
- What happens when a highly responsive job that include many successive IO requests enters the scene? Such a job will probably never eats up through a whole time slice, so it will stay at the highest priority queue at all time so it achieves the high performance it deserves. 

#### Problems with our MLFQ Implementation so Far:
- Our configuration of MLFQ so far suffers from several major flaws:
	- The lower priority queues might be **starved** of all CPU time, especially when there are too many interactive applications placed in higher queues. 
	- Malicious actors might optimize their job behavior so it look like a highly interactive job. This makes it monopolize CPU time. Such attacks are especially dangerous in data centers with shred CPUs and memories.
	- A  job might also change its behavior over time, so it can start as CPU-bound application but at some point it becomes an interactive job. This job in urgent need of response time is in a very low priority queue has no way of elevating itself back to where it really belongs.

### Boosting Priority:
- We can periodically **boost** the priority of all jobs, by for example moving all jobs to the topmost priority queue. We can device a new rule now:
	- **Rule 5**: After a time period S, move all jobs to the topmost priority queue.
- This boosting achieves two goals. First, the CPU bound jobs don't get starved of CPU times as they move up the priority hierarchy and compete with higher priority jobs using RR. Second, jobs that have become suddenly interactive can now be treated as they deserve and be given better response time.
- The value S after which a boost needs to happen must be set with care. If S is too large, starvation of lower-queue long running jobs will still be prone to starvation. If S is too small, short-running job might not get the responsiveness they need.

### Better Accounting:
- Now we need to make our MLFQ resilient to schedule gaming. I don't really understand this part. The authors say that even interactive jobs will be downgraded down the priority hierarchy as if a long job that includes interactivity is treated almost exactly as one that is IO-bound :confused:!! They suggest the following rule (which replaces rules 4a and 4b):
	- **Rule 4**: Every job will keep moving down the priority scale regardless of their use of IO and letting go of the CPU time too soon.
- This configuration is not as easy to game, but 
- At least, the SJT principle will be still maintained in this new configuration.

### Additional Issues:
- One important issue to consider when designing an MLFQ scheduler is so-called parameterization which include:
	- Deciding how many queues to use.
	- Should queues have the same time slices? If not, how big a time slice per queue should be?
	- How often should priority be boosted?
- There are no ready answers for these questions. Designers need to fine tune these parameters until they reach satisfactory results.
- An example of MLFQ parameterization is the choice of time slices for queues. Higher priority queues have shorter slices as they'd usually contain shorter jobs, and the slices get larger as you move down to lower-priority queues. Low priority jobs would use more CPU per slice as they are mainly hungry for CPU.
- The Solaris implementation of MLFQ allows system administrator to alter the way priorities and scheduling work to suit her desires.

## Proportional Share Scheduler:
- Another widely used scheduler is the **proportional share** or **fair share** scheduler. Instead of optimizing for turnaround or response time, it tries to guarantee that each job gains a certain percentage of CPU time. An early form of proportional share scheduling was the so-called **lottery scheduling**. In such a type of scheduling, we often run a lottery to determine which process should run next, and processes that should run more often need to be given higher chances of winning.

### Basics, Tickets and Shares:
- Each process has a number of tickets, and the number of tickets a process has corresponds with its share/proportion of CPU time (or whatever resource). If processes A and B have 75 and 25 tickets respectively, then A has a 75% share of CPU time, and B has 25%. Let's suppose that A has tickets 0 through 74, while B has tickets 75 through 99. The scheduler will pick a ticket whose number is between 0 and 99 at random. 7, and 57 for example will belong to A, while 89 will be B's. This probabilistic setup will not guarantee exact proportion but will approximate it over long runs.
- The choice of randomness will at least free the system from the burden of tracking which processes has used how much state. There are other good side effects to choosing randomness but I don't understand them to be honest!

### Implementation:
- I have absolutely no idea what's going on here!!!! Come on!!

### The Linux Completely Fair Scheduler (CFS):
- I don't really see how this scheduler relates to the ones just mentioned, the lottery schedulers, apart from the fact that it is another fair share scheduler. Anyways, this doesn't kinda seem as voodooy as the previous subsection which was all jumbled up!
- The **completely fair scheduler (CFS)** used in Linux divides the CPU between all jobs evenly in a dynamic and scalable fashion (I don't know how this scalability is achieved). What probably sets this scheduler apart is that it does very little work to schedule jobs since time is shared as evenly as possible between different processes. This is a source of great efficiency!
- CFS divides CPU time evenly between different processes through so-called **virtual runtime (`vruntime`)**. This `vruntime` increases evenly for each running process as time progresses. When a scheduling decision need to be made, the scheduler picks the process with the lowest `vruntime`. 
- How does CFS avoid context switching too often or less often? Over-context- switching is bad for performance, while less context switching might mean less fairness in the short time! (really? :confused:). CFS provides a number of parameters to fix this problem. One such parameter is **`sched_latency`** which is used to determine the run time of a job before considering a switch. CFS uses something like 48 ms for `sched_latency` :confused: and divides this by the number of running processes. If we have 4 processes, this means each job gets 12 seconds before switching occurs. Just remember that `vruntime` increases with time, but when does it stop growing? and how about newly arriving processes?
- Another important parameter is the so-called **`min_granularity`** which acts as some kind of minimum threshold for the size of a run time of a process. This is useful when there are way too many processes. If we divide 48, our dear `sched_latency`, by a 100 then we will need to context switch every half millisecond which is really bad! A typical value for `min_granularity` is 6 ms.
- Different processes can be assigned **weights** to indicate different priorities. This can be done by the Unix **nice** processor level, *what??!!* :confused:!! I believe different processes acquire different time slice priorities through this mechanism.
- Instead of using a simple list for tracking running processes, CFS uses a red-black tree which has a very efficient read time of ***O(log n)***. This is how CFS scalability is achieved. This structure only tracks running processes. Processes that go on sleeps during an IO operation for examples are not kept track of.
- A job that goes on a sleep while waiting for an IO response don't get their `vruntime` increased during their sleep which means they get starved of CPU time by their siblings that didn't sleep and now have a much larger `vruntime`. CFS tries to fix this by assigning the just reawaken process a `vruntime` from a process in the tree (probably the one with the smallest `vruntime`). Anywayss, processes waking froma n IO sleep never get a fair share CPU time. 

## Multiprocessor Scheduling: