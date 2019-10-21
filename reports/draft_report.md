# Epidemic Simulation Using Real-World Graph Shape
Erika Lu and Adam Selker


## Abstract
Mathematical graphs, consisting of nodes that represent individuals and edges that represent interactions, are a common tool for simulating disease spread through a population.  The graph structure is usually created using a stochastic algorithm.  In this paper, we replicate an [experiment](https://www.pnas.org/content/pnas/107/51/22020.full.pdf) that uses real-world interaction data instead of an artificial graph, and expand on it by introducing vaccinations to the model. 

## Purpose
The 2018 flu season was categorized as a high severity season by the [United States Center for Disease Control and Prevention](https://www.cdc.gov/flu/about/season/flu-season-2017-2018.htm) and recorded the highest number of pediatric deaths in a regular flu season. About 80% of these deaths were non-vaccinated children. 

Vaccines are a good precaution but not perfect. The effectiveness of the 2018 flu vaccine was an estimated 40%. According to the CDC, this means "the flu vaccine reduced a person’s overall risk of having to seek medical care at a doctor’s office for flu illness by 40%."

Vaccines are also hampered by a lack of knowledge about how infection spreads, moves, and dies. The model we reproduce and extend in this paper could be useful directly, for estimating the impact of vaccination prevalency on epidemics.  It could also be useful indirectly, by informing future models with different goals or greater accuracy.

# Replication

## Prior Work

In "A high-resolution human contact network for infectious disease transmission," Salathé et al (2010) use an SEIR model to simulate infection in a high school.

An SEIR model is an example of a compartmental model, a group of models proposed in "A Contribution to the Mathematical Theory of Epidemics" (Kermack & McKendrick, 1927).  In the model, each individual is in one of four states. A _susceptible_ individual is not immune to the infection, but has not yet been exposed.  An _exposed_ individual has been exposed to the infection, but is not yet contagious.  An _infectious_ individual is capable to transmitting the infection to others.  A _recovered_ individual is immune, or highly resistant to the infection.  

To build a graph for the model, the authors gather data from one day at an actual school, giving students and faculty wearable devices which tracked close interactions.  Using this data, they built a graph representing the school, where nodes represent people and edges represent interactions.  Edges were also weighted according to the lengths of interactions; infection would travel along an edge with a probability defined by the edge's weight.


## Procedure

In this paper, we replicate Salathé et al, and also add vaccinations to their model.  

Using the (NetworkX library)[https://networkx.github.io/], we build the original model using data from Salathé et al. to generate a graph following these rules:
- Nodes represent people and edges represent interactions between the nodes. The edges are weighted with the contact duration between two individuals (1 edge weight = 20 seconds).
- Nodes are initialized with the state, "susceptible".
- The simulation starts by exposing the disease to a random _susceptible_ individual. The individual becomes _exposed_. An _exposed_ person has an incubation period defined by a Weibull distribution, then moves on to the _infectious_ state.  
- At every time step (12 hours), the "infectious" individuals have a chance of probablility p of exposing the disease to their neighboring nodes. The probability of exposure is defined by p = 1 - (1 - 0.003)<sup>(.25 * edgeWeight)</sup>. 
- At every time step (12 hours), previously _infectious_ individuals become _recovered_ and will no longer spread the disease. This simulates the individual leaving school within half a day. 

## Results

[For example graphs, see p. 22023 of the original paper.]

Our reproduction results in data which match absentee rates gathered from the real high school [cite: Salathé, they show it in Fig. 4], and which differ [only slightly] from the results obtained by Salathé et al.  In figure [foo], the fraction of students who are infected rises and falls sharply in a manner which is consistent with real infection.  Also, as in the original paper, we find that the following vaccination strategies caused significant (p < 0.05) decreases in the rates of infection:
* TODO: Which things worked

[ TODO: Results from our extension ]

## Interpretation

The model seems accurate.  Though more research and broader data are needed to confirm its accuracy and test its applicability to different groups and situations, graph-based models that use real-world graph seem a promising tool.  More specifically, we note that vaccinating according to [some strategy] is [23%] more effective than vaccinating at random; if a vaccination campaign is used at a school or similar institution, this could be used to guide the effort.

One limitation of this model is that it requires real-world data.  [ TODO: More on this, and on outside interactions, limitations of SEIR model, computational feasability]

# Extension

To test the effectiveness of vaccination at creating herd immunity, we added random vaccination to the model.  A configurable fraction of the population is randomly selected to be "vaccinated".  In accordance with the CDC's findings [cite], vaccinations are about 40% effective, so 40% of individuals selected to be vaccinated are made immune (placed in the Recovered state).

We ran [some number] simulations with varying fractions infected, and in each simulation tested whether the infection spread to 50% of the susceptible population.  

[ Graph goes here ]

[ TODO: Commentary on results ]


## Source Code

The source code is available at [ref: our Github], and can be run online at [ref: Binder].  
