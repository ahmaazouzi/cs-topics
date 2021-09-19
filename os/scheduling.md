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
## Proportional Share Scheduler:
## Multiprocessor Scheduling: