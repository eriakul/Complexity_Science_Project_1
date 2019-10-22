# Epidemic Simulation Using Real-World Interaction Data
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

A mathematical graph consists of nodes connected by edges.  Each node represents an individual, each edge represents contact between two individuals.  Edges are _weighted_, representing the frequency and duration of contact between the individuals.  The use of graphs with compartmental models to represent disease spread is not novel to Salathé [TODO: Cite].  However, the graphs are usually built using an algorithm.  Instead, the author of this paper uses real data collected at a school to build the graph directly.

The author gives students and faculty at a high school wearable devices which track close interactions.  Using this data, they build a graph representing the school, where each tracking device is a node and each edge is weighted based on the duration during which two trackers were in close proximity (3 m).


## Procedure

In this paper, we replicate Salathé et al, and also add vaccinations to their model.  

Using the [NetworkX library](https://networkx.github.io/), we build the original model using data from Salathé et al. to generate a graph following these rules:
- Nodes represent people and edges represent interactions between the nodes. The edges are weighted with the contact duration between two individuals (1 edge weight = 20 seconds).
- Nodes are initialized with the state, "susceptible".
- The simulation starts by exposing the disease to a random _susceptible_ individual. The individual becomes _exposed_. An _exposed_ person has an incubation period defined by a Weibull distribution, then moves on to the _infectious_ state.  
- At every time step (12 hours), the "infectious" individuals have a chance of probablility p of exposing the disease to their neighboring nodes. The probability of exposure is defined by p = 1 - (1 - 0.003)<sup>(.25 * edgeWeight)</sup>. 
- At every time step (12 hours), previously _infectious_ individuals become _recovered_ and will no longer spread the disease. This simulates the individual leaving school within half a day. 

## Results

Salathé ran their SEIR model 1000 times and plotted the the percentage of infected individuals at every time step. 

![Visualization of infection by Salathé et al](https://github.com/eriakul/Complexity_Science_Project_1/blob/master/reports/TheirPlot.JPG)

We ran our simulation 100 times and plotted our results below. 

![Our graph](https://github.com/eriakul/Complexity_Science_Project_1/blob/master/reports/OurPlot.JPG)

While both figures see the fraction of students who are infected rise and fall sharply in a manner that is consistent with real infection, we see that the scale of our graph's x-axis is much larger than Salathé's. Most of our epidemics run to be about 30 days until the last infected individual recovers, while the majority of theirs runs for 10 days. Another difference is that Salathé's epidemics only affect .25 percent of the school's population while our model usually shows an average of x people getting infected for the majority of the runs. This may be due to differences in certain parameters that weren't specified in the paper. For example, Salathé provides no units in his calculation for the incubation period between the _exposed_ and _infectious_ states.

## Interpretation

The model seems accurate.  Though more research and broader data are needed to confirm its accuracy and test its applicability to different groups and situations, graph-based models that use real-world graph seem a promising tool.  More specifically, we note that vaccinating according to [some strategy] is [23%] more effective than vaccinating at random; if a vaccination campaign is used at a school or similar institution, this could be used to guide the effort.

One limitation of this model is that it requires real-world data.  [ TODO: More on this, and on outside interactions, limitations of SEIR model, computational feasability]


# Extension
 
To test the effectiveness of vaccination at creating herd immunity, we added random vaccination to the model.  A configurable fraction of the population is randomly selected to be "vaccinated".  In accordance with the CDC's findings [cite], vaccinations are about 40% effective, so 40% of individuals selected to be vaccinated are made immune by placing them in the Recovered state.
 
We ran 22,528 simulations with varying fractions vaccinated, and in each simulation tested whether the infection spread to 50% of the susceptible population before it died out.  The results of the simulations are presented in figure $n (note the truncated Y axis).

[ Graph goes here ]

Though the trend is clear (r = -0.97, p < 10<sup>6</sup>), the effect is surprisingly small.  With perfect vaccination, the likelihood of an epidemic that reaches most of the susceptible population drops from about 75% to about 61%.  Herd immunity has not been reached, due to the low effectiveness of the vaccine.  When the vaccine is perfectly effective, herd immunity is reached with about X% coverage; see figure $n.

[ Graph goes here ]

[TODO: Is this consistent with IRL?]


## Source Code

The source code is available at [ref: our Github], and can be run online at [ref: Binder].  
