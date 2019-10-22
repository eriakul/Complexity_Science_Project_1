# Epidemic Simulation Using Real-World Interaction Data
Erika Lu and Adam Selker


## Abstract
Mathematical graphs, consisting of nodes that represent individuals and edges that represent interactions, are a common tool for simulating disease spread through a population.  The graph structure is usually created using a stochastic algorithm.  In this paper, we replicate Salathé et al. (2010), which uses real-world interaction data instead of an artificial graph, and expand on it by introducing vaccinations to the model to see how different frequencies of vaccination affect the probability of an epidemic. 

## Purpose
The 2018 flu season was categorized as a high severity season by the United States Center for Disease Control and Prevention (Center for Disease Control, 2019) and recorded the highest number of pediatric deaths in a regular flu season. About 80% of these deaths were non-vaccinated children. 

Vaccines are a good precaution but not perfect. The effectiveness of the 2018 flu vaccine was an estimated 40%. According to the CDC, this means "the flu vaccine reduced a person’s overall risk of having to seek medical care at a doctor’s office for flu illness by 40%."

Vaccines are also hampered by a lack of knowledge about how infection spreads, moves, and dies. The model we reproduce and extend in this paper could be useful directly, for estimating the impact of vaccination prevalency on epidemics.  It could also be useful indirectly, by informing future models with different goals or greater accuracy.


## Prior Work
In "A high-resolution human contact network for infectious disease transmission," Salathé et al. (2010) use an SEIR model run on a graph to simulate infection in a high school.

An SEIR model is an example of a compartmental model, a group of models proposed in "A Contribution to the Mathematical Theory of Epidemics" (Kermack & McKendrick, 1927).  In the model, each individual is in one of four states. A _susceptible_ individual is not immune to the infection, but has not yet been exposed.  An _exposed_ individual has been exposed to the infection, but is not yet contagious.  An _infectious_ individual is capable to transmitting the infection to others.  A _recovered_ individual is immune, or highly resistant to the infection.  

A mathematical graph consists of nodes connected by edges.  Each node represents an individual, each edge represents contact between two individuals.  Edges are _weighted_, representing the frequency and duration of contact between the individuals.  The use of graphs with compartmental models to represent disease spread is not novel to Salathé et al. (Kamp, Moslonka-Lefebvre, & Alizon, 2013).  However, the graphs are usually built using an algorithm.  Instead, the authors of this paper use real data collected at a school to build the graph directly.

The authors give students and faculty at a high school wearable devices which track close interactions.  Using this data, they build a graph representing the school, where each tracking device is a node and each edge is weighted based on the duration during which two trackers were in close proximity (3 m).


## Procedure

In this paper, we replicate Salathé et al, and also add vaccinations to their model.  

Using the [NetworkX library](https://networkx.github.io/), we build the original model using data from Salathé et al. to generate a graph following these rules:
- Nodes represent people and edges represent interactions between the nodes. The edges are weighted with the contact duration between two individuals (1 edge weight = 20 seconds).
- Nodes are initialized in the _susceptible_ state.
- The simulation starts by exposing the disease to a random _susceptible_ individual. The individual becomes _exposed_. An _exposed_ person goes through an incubation period defined by a Weibull distribution (power parameter 2.21, scale factor 1.10), and then moves on to the _infectious_ state.  
- At every time step (12 hours), the _infectious_ individuals have a chance of probability p of exposing the disease to their neighboring nodes. The probability of exposure is defined by p = 1 - (1 - 0.003)<sup>(.25 * edge\_weight)</sup>. 
- Also at every time step, previously _infectious_ individuals become _recovered_ with probability p = 1 - 0.95<sup>t</sup>, where t is the number of time steps the individual has been _infectious_.

## Results

Salathé et al. ran their SEIR model 1000 times and plotted the percentage of infected individuals at every time step (note the truncated Y axis). 

![Visualization of infection by Salathé et al](https://github.com/eriakul/Complexity_Science_Project_1/blob/master/reports/TheirPlot.JPG)
Figure 1: Graph from the paper by Salethé et al. The gray lines are infected people per run. The red lines represent absentee data.

We ran our simulation 100 times and plotted our results below (note the truncated Y axis). 

![Visualization of infection in our model](https://github.com/eriakul/Complexity_Science_Project_1/blob/master/reports/ensemble.png)

Figure 2: Our reproduction of the graph by Salethé et al.

While both figures see the fraction of students who are infected rise and fall sharply in a manner that is consistent with real infection, our epidemics infect more people, and run longer, than Salathé's.  Most of our epidemics run to be about 30 days until the last infected individual recovers, while the majority of theirs runs for 10 days. At their peaks, Salathé's epidemics affect about 15% of the school's population; ours affect about 30%. These disparities may be due to differences in certain parameters that weren't specified in the paper. For example, Salathé et al. provide no units for the incubation period between the _exposed_ and _infectious_ states; we assumed the units were time steps, but they may be hours or days.

One limitation of this model is that it requires real-world data.  Using this method, unmodified, to simulate a nation- or world-wide epidemic would be infeasible, since it would require millions, or billions, of people to wear transponders.  Some amount of graph generation or approximation could be used, producing a hybrid model which could be more accurate than existing algorithmically-generated graphs but still feasible.

Another, related limitation is that the data is collected over a single day.  Day-to-day interaction patterns vary, and so there will be noise in the data if only one day is analyzed.  Again, doing this perfectly would require an arbitrarily large investment, but approximations could be made.  For instance, transponders could be worn on a few days distributed across a year, and interaction frequencies could be averaged across the different datasets.

## Vaccinations
 
To test the effectiveness of vaccination at creating herd immunity, we added random vaccination to the model.  A configurable fraction of the population is randomly selected to be "vaccinated".  Influenza vaccines are about 40% effective (Center for Disease Control, 2019), so 40% of individuals selected to be vaccinated are made immune by placing them in the Recovered state.
 
We ran 22,528 simulations with varying fractions vaccinated, and in each simulation tested what fraction of the population was infected before the disease died out.  The results of the simulations are presented in Figure 3.

![Epidemic size frequencies varying with vaccination rates](https://github.com/eriakul/Complexity_Science_Project_1/blob/master/reports/vacc_hist.png)  
Figure 3: Epidemic size frequencies varying with vaccination rates

Though the trend is clear, the effect is only moderate, and there is no clear cutoff for "herd immunity".  With no immunity, the epidemic usually reaches between 50% and 60% of the population.  With perfect vaccination, it reaches between 30% and 40%.  The limited effect is due to the low effectiveness of the vaccine; see Figure 4, which visualizes the same model but with 100%-effective vaccines.

![Vaccination impact when vaccines are perfectly effective](https://github.com/eriakul/Complexity_Science_Project_1/blob/master/reports/vacc_hist_perfect_vaccine.png)
Figure 4: Vaccination impact when vaccines are perfectly effective

When the vaccine is perfectly effective, there is still no distinct threshold for herd immunity, but epidemic sizes drop more sharply.  At 60% vaccination rate, most epidemics do not affect more than 20% of the population.

In reality, about 47% of Americans receive vaccines against influenza each year (Bergman, 2017).  According to this model, this should be enough to reduce the impact of the disease, but not prevent its spread entirely.  Qualitatively, this seems to be true (Simonsen et al., 2005), but given the model's limited scope, it is difficult to evaluate quantitative accuracy.

## Source Code

The source code is available on GitHub at https://github.com/eriakul/Complexity_Science_Project_1/blob/master/code/model.py.

Jupyter notebook versions are available [on NBViewer](https://nbviewer.jupyter.org/github/eriakul/Complexity_Science_Project_1/blob/master/code/Epidemic%20Simulation%20Using%20Real-World%20Interaction%20Data.ipynb) (static), and [on Binder](https://mybinder.org/v2/gh/eriakul/Complexity_Science_Project_1/master) (runnable).

## References

Salathé, M., Kazandjieva, M., Lee, J. W., Levis, P., Feldman, M. W., & Jones, J. H. (2010). A high-resolution human contact network for infectious disease transmission. _Proceedings for the National Academy of Sciences, 107(51)_, pp. 22020-22025.

Center for Disease Control. (Last reviewed 2019, Sep. 5). Summary of the 2017-2018 Influenza Season. https://www.cdc.gov/flu/about/season/flu-season-2017-2018.htm

Kermack, W.O. & McKendrick, A. G. (1927). A contribution to the mathematical theory of epidemics. _Proceedings of the Royal Society of London, 115_(772), pp. 700-721.

Kamp, C., Moslonka-Lefebvre, M., & Alizon, S. (2013). Epidemic spread on weighted networks. _PLoS computational biology, 9_(12), e1003352. doi:10.1371/journal.pcbi.1003352

Bergman, R. (2017). CDC: Fewer than half of Americans get flu vaccine. http://thenationshealth.aphapublications.org/content/47/9/E45

Simonsen L, Reichert TA, Viboud C, Blackwelder WC, Taylor RJ, Miller MA. (2005). Impact of Influenza Vaccination on Seasonal Mortality in the US Elderly Population. _Arch Intern Med. 165_(3), pp. 265-272. doi:10.1001/archinte.165.3.265
