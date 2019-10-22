# Epidemic Simulation Using Real-World Graph Shape
Erika Lu and Adam Selker


## Abstract
Mathematical graphs, consisting of nodes that represent individuals and edges that represent interactions, are a common tool for simulating disease spread through a population.  The graph structure is usually created using a stochastic algorithm.  In this paper, we replicate an [experiment](https://www.pnas.org/content/pnas/107/51/22020.full.pdf) that uses real-world interaction data instead of an artificial graph, and expand on it by introducing vaccinations to the model. 

## Purpose
The 2018 flu season was categorized as a high severity season by the [United States Center for Disease Control and Prevention](https://www.cdc.gov/flu/about/season/flu-season-2017-2018.htm) and recorded the highest number of pediatric deaths in a regular flu season. About 80% of these deaths were non-vaccinated children. 

Vaccines are a good precaution but not perfect. The effectiveness of the 2018 flu vaccine was an estimated 40%. According to the CDC, this means "the flu vaccine reduced a person’s overall risk of having to seek medical care at a doctor’s office for flu illness by 40%."

Vaccines are also hampered by a lack of knowledge about how infection spreads, moves, and dies. The model we reproduce and extend in this paper could be useful directly, for estimating the impact of vaccination prevalency on epidemics.  It could also be useful indirectly, by informing future models with different goals or greater accuracy.


## Prior Work
In "A high-resolution human contact network for infectious disease transmission," Salathé et al (2010) use an SEIR model run on a graph to simulate infection in a high school.

An SEIR model is an example of a compartmental model, a group of models proposed in "A Contribution to the Mathematical Theory of Epidemics" (Kermack & McKendrick, 1927).  In the model, each individual is in one of four states. A _susceptible_ individual is not immune to the infection, but has not yet been exposed.  An _exposed_ individual has been exposed to the infection, but is not yet contagious.  An _infectious_ individual is capable to transmitting the infection to others.  A _recovered_ individual is immune, or highly resistant to the infection.  

A mathematical graph consists of nodes connected by edges.  Each node represents an individual, each edge represents contact between two individuals.  Edges are _weighted_, representing the frequency and duration of contact between the individuals.  The use of graphs with compartmental models to represent disease spread is [not novel to Salathé et al](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3861041/).  However, the graphs are usually built using an algorithm.  Instead, the authors of this paper use real data collected at a school to build the graph directly.

The authors give students and faculty at a high school wearable devices which track close interactions.  Using this data, they build a graph representing the school, where each tracking device is a node and each edge is weighted based on the duration during which two trackers were in close proximity (3 m).


## Procedure

In this paper, we replicate Salathé et al, and also add vaccinations to their model.  

Using the [NetworkX library](https://networkx.github.io/), we build the original model using data from Salathé et al. to generate a graph following these rules:
- Nodes represent people and edges represent interactions between the nodes. The edges are weighted with the contact duration between two individuals (1 edge weight = 20 seconds).
- Nodes are initialized with the state, "susceptible".
- The simulation starts by exposing the disease to a random _susceptible_ individual. The individual becomes _exposed_. An _exposed_ person has an incubation period defined by a Weibull distribution, then moves on to the _infectious_ state.  
- At every time step (12 hours), the "infectious" individuals have a chance of probablility p of exposing the disease to their neighboring nodes. The probability of exposure is defined by p = 1 - (1 - 0.003)<sup>(.25 * edgeWeight)</sup>. 
- At every time step (12 hours), previously _infectious_ individuals become _recovered_ and will no longer spread the disease. This simulates the individual leaving school within half a day. 

## Results

Salathé et al. ran their SEIR model 1000 times and plotted the percentage of infected individuals at every time step. 

![Visualization of infection by Salathé et al](https://github.com/eriakul/Complexity_Science_Project_1/blob/master/reports/TheirPlot.JPG)
Figure 1: Graph from the paper by Salethé et al. The gray lines are infected people per run. The red lines represent absentee data.

We ran our simulation 100 times and plotted our results below (note the truncated Y axis). 

![Our graph](https://github.com/eriakul/Complexity_Science_Project_1/blob/master/reports/ensemble.png)
Figure 2: Our reproduction of the graph by Salethé et al.

While both figures see the fraction of students who are infected rise and fall sharply in a manner that is consistent with real infection, we see that the scale of our graph's x-axis is much larger than Salathé's. Most of our epidemics run to be about 30 days until the last infected individual recovers, while the majority of theirs runs for 10 days. Another difference is that Salathé's epidemics at most affects about 25 percent of the school's population while our model shows an average of 30 percent people getting infected for the majority of the runs. These disparities may be due to differences in certain parameters that weren't specified in the paper. For example, Salathé provides no units in his calculation for the incubation period between the _exposed_ and _infectious_ states.

In terms of the validation of this model's use in simulating real life scenarious, it is clear that there are limitations. As seen with our recreation of the SEIR model, the outcomes of the model differ greatly even when using the same real-world data. There are many assumed parameters (such as the recovery time distribution) that affect the accuracy of the results. Though more research and broader data are needed to confirm its accuracy and test its applicability to different groups and situations, graph-based models that use real-world graph seem a promising tool.

One limitation of this model is that it requires real-world data.  Using this method, unmodified, to simulate a nation- or world-wide epidemic would be infeasible, since it would require millions, or billions, of people to wear transponders.  Some amount of graph generation or approximation could be used, producing a hybrid model which could be more accurate than existing algorithmically-generated graphs but still feasible.

Another, related limitation is that the data is collected over a single day.  Day-to-day interaction patterns vary, and so there will be noise in the data if only one day is analyzed.  Again, doing this perfectly would require an arbitrarily large investment, but approximations could be made.  For instance, transponders could be worn on a few days distributed across a year, and interaction frequencies could be averaged across the different datasets.

# Extension
 
To test the effectiveness of vaccination at creating herd immunity, we added random vaccination to the model.  A configurable fraction of the population is randomly selected to be "vaccinated".  In accordance with the CDC's findings [cite], vaccinations are about 40% effective, so 40% of individuals selected to be vaccinated are made immune by placing them in the Recovered state.
 
We ran 22,528 simulations with varying fractions vaccinated, and in each simulation tested what fraction of the population was infected before the disease died out.  The results of the simulations are presented in figure $n.

[ Vaccine hist goes here ]

Though the trend is clear, the effect is only moderate, and there is no clear cutoff for "herd immunity".  With no immunity, the epidemic usually reaches between 50% and 60% of the population.  With perfect vaccination, it reaches between 30% and 40%.  The limited effect is due to the low effectiveness of the vaccine; see figure $n.

[ Perfect vacc hist goes here ]

About 47% of Americans receive vaccines against influenza each year [cite: http://thenationshealth.aphapublications.org/content/47/9/E45].  According to this model, this should be enough to reduce the impact of the disease, but not prevent its spread entirely.  This seems to be true [cite: 

## Source Code

The source code is available at [ref: our Github], and can be run online at [ref: Binder].  
