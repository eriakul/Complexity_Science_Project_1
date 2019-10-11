# Epidemic Simulation Using Real-World Graph Shape
Erika Lu and Adam Selker


## Abstract
Mathematical graphs, consisting of nodes that represent individuals and edges that represent interactions, are a common tool for simulating disease spread through a population.  The graph structure is usually created using a stochastic algorithm.  In this paper, we replicate an experiment that uses real-world interaction data instead of an artificial graph, and expand on it by [doing something].  [TODO: Results]


## Purpose
Infectious disease kills about one in four people [cite: something in https://en.wikipedia.org/wiki/Infection#Epidemiology].  People have developed tools for fighting epidemics, including vaccination; the effectiveness of these tools is often hampered by a lack of knowledge about how infection spreads, moves, and dies.  The model we reproduce and extend in this paper could be useful directly, for estimating the impact of vaccination [and whatever extension we do] on epidemics.  It could also be useful indirectly, by informing future models with different goals or greater accuracy.


## Prior Work
The core of this work is the Susceptible-Exposed-Infectious-Recovered (SEIR) model of disease spread.  The SEIR model is an example of a compartmental model, a group of models proposed in "A Contribution to the Mathematical Theory of Epidemics" (Kermack & McKendrick, 1927).  In the model, each individual is in one of four states. A _susceptible_ individual is not immune to the infection, but has not yet been exposed.  An _exposed_ individual has been exposed to the infection, but is not yet contagious.  An _infectious_ individual is capable to transmitting the infection to others.  A _recovered_ individual is immune, or highly resistant to the infection.  Most individuals begin as susceptible, and one or a few as exposed or infectious; individuals become exposed through some process specific to the model, and then pass through the stages in a fixed amount of time.

One common use of the SEIR model is on graphs, where nodes represent individuals, and edges represent potential interactions which might spread infection.  In order to mimic real-life dynamics, the graph must share certain properties with reality, including clustering and small-world effects [cite].  Some papers, such as [a paper], use stochastic algorithms to build graphs which fit these criteria.

In "A high-resolution human contact network for infectious disease transmission," Salathé et al (2010) use an SEIR model to simulate infection in a high school.  However, instead of using an algorithm to build the graph, the authors gather data from one day at an actual school, giving students and faculty wearable devices which tracked close interactions.  Using this data, they built a graph representing the school, where edges were present when individuals had had interacted for at least X minutes during the day, for varying values of X.  Edges were also weighted according to the lengths of interactions; infection would travel along an edge with a probability defined by the edge's weight.


## Procedure

In this paper, we replicate Salathé et al, and also [do some expansion].  We build a graph using data from Salathé et al. and proceed through fixed timesteps, following these rules:
* TODO: Rewrite rules from Salathé

We implement the model in Python, using the NetworkX library [cite]. 


## Results

[For example graphs, see p. 22023 of the original paper.]

Our reproduction results in data which match absentee rates gathered from the real high school [cite: Salathé, they show it in Fig. 4], and which differ [only slightly] from the results obtained by Salathé et al.  In figure [foo], the fraction of students who are infected rises and falls sharply in a manner which is consistent with real infection.  Also, as in the original paper, we find that the following vaccination strategies caused significant (p < 0.05) decreases in the rates of infection:
* TODO: Which things worked

[ TODO: Results from our extension ]


## Interpretation

The model seems accurate.  Though more research and broader data are needed to confirm its accuracy and test its applicability to different groups and situations, graph-based models that use real-world graph seem a promising tool.  More specifically, we note that vaccinating according to [some strategy] is [23%] more effective than vaccinating at random; if a vaccination campaign is used at a school or similar institution, this could be used to guide the effort.

One limitation of this model is that it requires real-world data.  [ TODO: More on this, and on outside interactions, limitations of SEIR model, computational feasability]


## Source Code

The source code is available at [ref: our Github], and can be run online at [ref: Binder].  
