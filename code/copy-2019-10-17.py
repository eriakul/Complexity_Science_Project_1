#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Project (1)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qHE_7uzUuapyvPopHZasglpOhaXCB2EG
"""

import gdown
import csv
import networkx as nx
import numpy as np
from enum import Enum
from random import choice


def load_data_from_drive():
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


from numpy.random import choice

edges, people = load_data_from_drive()


class Status(Enum):
    S = "susceptible"
    E = "exposed"
    I = "infectious"
    R = "recovered"


class School(Graphs):
    def __init__(self, edges, people):
        self.G = nx.Graph()
        G.add_nodes_from(
            [(name, dict(state=Status.S, job=job)) for name, job in people.items()]
        )
        G.add_weighted_edges_from(edges)
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

    def start_showing_symptoms_p(self):
        p = 0.5
        return np.random.random() < p

    def step(self):
        toExpose = set()
        toInfect = set()
        toRecover = set()

        for sickNode in self.sick_nodes:
            state = self.G.node[sickNode]["state"]
            for neighbor, weight in self.get_neighbors_weights(sickNode):
                neighborState = self.G.node[neighbor]["state"]
                if neighborState == Status.S:
                    if self.transmit_p(weight, showSymptoms=state == Status.I):
                        toExpose.add(neighbor)
            if state == Status.E:
                if self.start_showing_symptoms_p():
                    toInfect.add(sickNode)
            if state == Status.I:
                toRecover.add(sickNode)

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
        self.G.node[index]["state"] = Status.E
        self.sick_nodes.append(index)

    def infect(self, index):
        self.G.node[index]["state"] = Status.I

    def recover(self, index):
        self.G.node[index]["state"] = Status.R
        self.sick_nodes.remove(index)

    def get_colors(self):
        def color(state):
            if state == "susceptible":
                return "green"
            elif state == "exposed":
                return "yellow"
            if state == "infectious":
                return "red"
            if state == "recovered":
                return "blue"

        states = list([data["state"] for i, data in self.G.nodes(data=True)])
        return list(map(color, states))

    def get_global_state(self):
        globalState = {}
        for index, attributes in self.G.nodes(data=True):
            state = attributes["state"]
            globalState[state] = globalState.get(state, 0) + 1

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
        print(self.get_global_state())


S = School(edges, people)
S.randomly_expose()

print(S.get_global_state_jobs())
S.step()
# S.visualize()

import matplotlib.pyplot as plt

steps = 15
time = range(steps)
Sch = School(edges, people)
Sch.randomly_expose()

S = []
E = []
I = []
R = []

St = []
Et = []
It = []
Rt = []


for i in time:
    state = Sch.get_global_state_jobs()

    S.append(state.get(("susceptible", "student"), 0))
    E.append(state.get(("exposed", "student"), 0))
    I.append(state.get(("infectious", "student"), 0))
    R.append(state.get(("recovered", "student"), 0))

    St.append(state.get(("susceptible", "teacher"), 0))
    Et.append(state.get(("exposed", "teacher"), 0))
    It.append(state.get(("infectious", "teacher"), 0))
    Rt.append(state.get(("recovered", "teacher"), 0))

    Sch.step()

fig, ax = plt.subplots()

sLine = ax.plot(time, S, "g", label="Susceptible")
eLine = ax.plot(time, E, "y", label="Exposed")
iLine = ax.plot(time, I, "r", label="Infectious")
rLine = ax.plot(time, R, "c", label="Recovered")


sLinet = ax.plot(time, St, "g:")
eLinet = ax.plot(time, Et, "y:")
iLinet = ax.plot(time, It, "r:")
rLinet = ax.plot(time, Rt, "c:")


ax.legend()
plt.title("SEIR High School Model - Instantaneous Time Steps")
plt.xlabel("Time Steps - 12 hr Each")
plt.ylabel("People")

plt.show()

import matplotlib.pyplot as plt

steps = 10

time = range(steps)
argAnts = []
carpAnts = []

Sch = School(edges, people)
Sch.randomly_expose()

for i in time:
    state = Sch.get_global_state()
    S.append(state.get("susceptible", 0))
    E.append(state.get("exposed", 0))
    I.append(state.get("infectious", 0))
    R.append(state.get("recovered", 0))
    Sch.step()


fig, ax = plt.subplots()

sLine = ax.plot(time, S, label="Susceptible")
eLine = ax.plot(time, E, label="Exposed")
iLine = ax.plot(time, I, label="Infectious")
rLine = ax.plot(time, R, label="Recovered")


ax.legend()
plt.title("SEIR High School Model - Instantaneous Time Steps")
plt.xlabel("Time Steps - 12 hr Each")
plt.ylabel("People")

plt.show()

Sch.visualize()
