# Mobile Edge Computing Project #
**Abstruct**

In a three-tier Vehicle to X (V2X) network, a vehicle can offload the computational tasks to the edge computing component at a roadside unit (RSU) or a base station with cloud computing (gNB). Moreover, an RSU can also offload to gNB, forming three offloading paths: vehicle-to-RSU, vehicle-to-gNB, and RSU-to-gNB. This paper aims to minimize the offloaded tasks' average latency while dealing with the network dynamic. Note that the existing works assume the fixed network parameters, hence have failed to address the dynamic.  As a solution, we use the multi-agent multi-armed bandits (MAB) learning for offloading that can adapt to the network dynamic and optimize the latency. More importantly, we propose a new MBA offloading scheme with an exploration mechanism based on the Sigmoid function. We conduct an extensive evaluation to evaluate and show the superiority of our proposal. First, the proposed Sigmoid exploration mechanism reduces the tasks' average latency by 35\% compared to a basic MAB using negative rewarding. Second, the simulation results show our proposed offloading algorithm shortens the task latency by 18.5\% on average and 56.9\% in the best case, compared to the state-of-the-art. 

### What is this repository for? ###

* This repository includes files to build up MEC enviroment simulator
* Version: 
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact
