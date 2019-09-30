# A Graph-Based Look at the Spread of Infectious Disease

## Abstract
A graph-based model of a social network can simulate the spread of disease by representing people as nodes, and encounters as edges. Our project intends to observe how disease spreads across populations. We plan to observe the rate at which disease spread across an SEIR model while varying the rate of infection along the encounter edges. 

## Model Overview
For our project, we plan to reproduce the experiment carried out in the paper “A high-resolution human contact network for infectious disease transmission” (Salathé et al, 2010).  In the paper, the authors gather data on close-proximity interactions (CPI’s) in a high school, and use the data to build a graph-based model of potential disease spread.  We plan to reproduce the graph-based segment of this, using their algorithm to build the graph and then running a time-step-based SEIR model using their constants.  Next, we can improve on the model; we will find a potentially-useful improvement while we analyze the paper and reproduce the original model.

## Graph Mock-Up
![Graph Mock-Up]( https://github.com/eriakul/Complexity_Science_Project_1/blob/master/reports/graph-mockup-cropped.png)

## Analysis Mock-Up
We find that, in [\_]% of cases, the infection never spreads beyond the first infected person.  In the remaining [\_]% of cases, the infection [almost always] spreads to most of the school, peaking on average at [\_]% infected, and eventually infecting [\_]% of the population.  If 20% of the population is vaccinated (i.e. immune from the beginning), then the infection only spreads [\_]% of the time, and infects [\_]% on average.

## Next Steps
* Find library to create graph
* Decide on size of model
* Extract model parameters from graph
* Implement model
* Graph results
* Brainstorm how to improve model
* Do that
