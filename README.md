# [NTU 2021 Fall] Intelligent Vehicles

智慧型汽車導論程式作業

## Homework 2

In the benchmark, the first number is n, the number of messages. The second number is τ . Each of the following lines contains the priority (Pi), the transmission time (Ci), and the period (Ti) of each message. 

Now, you are asked to use the Simulated Annealing to decide the priority of each message.



**The requirements are: ** 

- The objective is to minimize the summation of the worst-case response times of all messages.  
- The priority of each message must be an integer in the range [0, n − 1].  
- The priority of each message must be unique.  
- The worst-case response time of each message must be smaller than or equal to the period of each message.  
- The given priorities are the initial solution in the Simulated Annealing.  
- We expect the total runtime less than 15 seconds.
