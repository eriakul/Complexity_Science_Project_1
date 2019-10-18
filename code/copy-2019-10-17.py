#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Project (1)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qHE_7uzUuapyvPopHZasglpOhaXCB2EG
"""

# TODO:
# Make sure the 75% and 100% drops in connections are handled properly

import matplotlib.pyplot as plt
import gdown
import csv
import networkx as nx
import numpy as np
from enum import Enum
from numpy.random import choice


def load_data_from_drive():
    """
    Loads graph data from Google Drive.
    """
    edges = {}
    gdown.download(
        "https://drive.google.com/uc?id=1vBUOcQVh1EDY91xtW4fZjowbN8RFQ5Br",
        "interactions.txt",
        quiet=True,
    )
    with open("interactions.txt") as f:
        c = csv.reader(f, delimiter="\t")
        for row in c:
            pair = (int(row[0]), int(row[1]))
            edges[pair] = edges.get(pair, 0) + (float(row[2]) / 3)

    people = {}
    gdown.download(
        "https://drive.google.com/uc?id=10e8tFloUoUpV8UUf863blJBk8eTrSUih",
        "person_descriptions.txt",
        quiet=True,
    )
    with open("person_descriptions.txt") as f:
        c = csv.reader(f, delimiter="\t")
        for row in c:
            people[int(row[0])] = row[1]

    edges_list = [(key[0], key[1], value) for key, value in edges.items()]
    return edges_list, people


edges, people = load_data_from_drive()


class State(Enum):
    S = "susceptible"
    E = "exposed"
    I = "infectious"
    R = "recovered"


def state_color(state):
    if state == State.S:
        return "green"
    elif state == State.E:
        return "yellow"
    elif state == State.I:
        return "red"
    elif state == State.R:
        return "blue"


class School:
    def __init__(self, edges, people):
        self.G = nx.Graph()
        self.G.add_nodes_from(
            [(name, {"state": State.S, "job": job}) for name, job in people.items()]
        )
        self.G.add_weighted_edges_from(edges)

        # Keeps a list of people who are sick (exposed or infectious), so
        # we know who to look at during step().
        self.sick_nodes = []

    def randomly_expose(self):
        unlucky_one = choice(self.G.nodes)
        print("Person {} has become exposed to the disease.".format(unlucky_one))
        self.expose(unlucky_one)

    def transmit_p(self, weight, showSymptoms=False):
        """
        Randomly returns True or False with a probability that models the
        chance of an influenza infection travelling along a link with a
        given weight, measured in CPRs (20s, or 1/3 minutes).
        """
        p = 1 - np.power(1 - 0.003, ((weight / 4) if showSymptoms else weight))
        return np.random.random() < p

    def get_incubation_period(self):
        """
        From the paper:
            The incubation period distribution is modeled by
            a right-shifted Weibull distribution with a
            fixed offset of half a day [power
            parameter = 2.21, scale parameter = 1.10]
        """
        # TODO: Is this in half-days?
        return 1 + (1.10 * np.random.weibull(2.21))

    def recover_p(self, time_infected):
        """
        From the paper:
            Once an individual is infectious,
            recovery occurs withaprobability of
            1−0.95^t per time step, where t represents
            the number of timesteps spent in the infectious state [...]
            After 12 d in the infectiousclass, an individual will recover 
            if recovery has not occurred before that time.
        """
        if time_infected >= 12:
            return True
        p = 1.0 - np.power(0.95, time_infected)
        return np.random.random() < p

    def step(self):
        toExpose = set()
        toInfect = set()
        toRecover = set()

        for index in self.sick_nodes:
            sick_node = self.G.node[index]
            state = sick_node["state"]

            for neighbor, weight in self.get_neighbors_weights(index):
                neighborState = self.G.node[neighbor]["state"]
                if neighborState == State.S:
                    if self.transmit_p(weight, showSymptoms=state == State.I):
                        toExpose.add(neighbor)

            if state == State.E:
                sick_node["incubation_period"] -= 1
                if sick_node["incubation_period"] < 0:
                    toInfect.add(index)
            elif state == State.I:
                if self.recover_p(sick_node["time_infected"]):
                    toRecover.add(index)
                else:
                    sick_node["time_infected"] += 1

        for node in toExpose:
            self.expose(node)

        for node in toInfect:
            self.infect(node)

        for node in toRecover:
            self.recover(node)

    def get_neighbors_weights(self, node):
        arr = []
        for n in self.G.neighbors(node):
            arr.append((n, self.G.edges[(node, n)]["weight"]))
        return arr

    def expose(self, index):
        self.G.node[index]["state"] = State.E
        self.G.node[index]["incubation_period"] = self.get_incubation_period()
        self.sick_nodes.append(index)

    def infect(self, index):
        self.G.node[index]["state"] = State.I
        self.G.node[index]["time_infected"] = 0

    def recover(self, index):
        self.G.node[index]["state"] = State.R
        self.sick_nodes.remove(index)

    def get_colors(self):
        states = list([data["state"] for i, data in self.G.nodes(data=True)])
        return [state_color(state) for state in states]

    def get_global_state(self):
        globalState = {}
        for index, attributes in self.G.nodes(data=True):
            state = attributes["state"]
            globalState[State] = globalState.get(state, 0) + 1

        return globalState

    def get_global_state_jobs(self):
        globalState = {}
        for index, attributes in self.G.nodes(data=True):
            state = attributes["state"]
            job = attributes["job"]
            globalState[(state, job)] = globalState.get((state, job), 0) + 1

        return globalState

    def visualize(self):
        nx.draw_networkx(
            self.G, node_color=self.get_colors(), node_size=5, with_labels=False
        )


steps = 30
time = range(steps)
Sch = School(edges, people)
Sch.randomly_expose()

histories = {}
for state in [State.S, State.E, State.I, State.R]:
    for group in ["student", "teacher"]:
        histories[(state, group)] = []


for i in time:
    global_state = Sch.get_global_state_jobs()

    for state in [State.S, State.E, State.I, State.R]:
        for group in ["student", "teacher"]:
            histories[(state, group)].append(global_state.get((state, group), 0))

    Sch.step()

fig, ax = plt.subplots()

lines = []
for state in [State.S, State.E, State.I, State.R]:
    for group in ["student", "teacher"]:
        ys = histories[(state, group)]
        color = state_color(state)
        style = "-" if group == "student" else ":"
        ax.plot(
            np.array(time) / 2, ys, style, color=color, label=state
        )  # Half-time so it's days.  TODO: make state names nicer and label groups


ax.legend()
plt.title("SEIR High School Model - Instantaneous Time Steps")
plt.xlabel("Time (days)")
plt.ylabel("People")

plt.show()