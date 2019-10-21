#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Project (1)

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qHE_7uzUuapyvPopHZasglpOhaXCB2EG
"""

import os
import csv
import numpy as np
from numpy.random import choice
import matplotlib.pyplot as plt
import gdown
import networkx as nx
from enum import Enum
import multiprocessing as mp


class State(Enum):
    S = "susceptible"
    E = "exposed"
    I = "infectious"
    R = "recovered"


class Job(Enum):
    S = "student"
    T = "teacher"
    A = "staff"
    O = "other"


class School:
    def __init__(self, edges, people):
        self.G = nx.Graph()
        self.G.add_nodes_from(
            [
                (name, {"state": State.S, "job": str_to_job(job)})
                for name, job in people.items()
            ]
        )
        self.G.add_weighted_edges_from(edges)

        # Keeps a list of people who are sick (exposed or infectious), so
        # we know who to look at during step().
        self.sick_nodes = []

        self.time_offset = None  # Can't step() until we randomly_expose()

    def randomly_expose(self):
        unlucky_one = choice(self.G.nodes)
        # print("Person {} has become exposed to the disease.".format(unlucky_one))
        self.expose(unlucky_one)
        # Also, set the time offset so the infection doesn't always happen on Monday morning
        self.time_offset = choice(
            range(14)
        )  # Perhaps this should be in the constructor?

    def randomly_vaccinate(self, fraction, success_rate=0.4):
        assert 0 <= fraction <= 1
        assert 0 <= success_rate <= 1
        people_to_vaccinate = choice(self.G.nodes, int(fraction * len(self.G.nodes)))
        for person in people_to_vaccinate:
            if np.random.random() < success_rate:
                self.G.node[person]["state"] = State.R

    def transmit_p(self, weight, show_symptoms=False):
        """
        Randomly returns True or False with a probability that models the
        chance of an influenza infection travelling along a link with a
        given weight, measured in CPRs (20s, or 1/3 minutes).
        """
        p = 1 - np.power(1 - 0.003, ((weight / 4) if show_symptoms else weight))
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

    def step(self, time):
        """
        time is the number of half-days since start; it's used to test if it's
        a night or weekend.
        """

        school_in_session = (time + self.time_offset) % 2 == 0 and (
            (time + self.time_offset) // 2
        ) % 7 < 5
        # school_in_session is True iff it's a weekday and not night
        to_expose = set()
        to_infect = set()
        to_recover = set()

        for index in self.sick_nodes:
            sick_node = self.G.node[index]
            state = sick_node["state"]

            if state == State.E:
                sick_node["incubation_period"] -= 1
                if sick_node["incubation_period"] < 0:
                    to_infect.add(index)

            elif state == State.I:
                # Infect neighbors if school is in session
                if school_in_session:
                    for neighbor, weight in self.get_neighbors_weights(index):
                        neighborState = self.G.node[neighbor]["state"]
                        if neighborState == State.S:
                            if self.transmit_p(weight, True):
                                to_expose.add(neighbor)

                # Do we recover?
                if self.recover_p(sick_node["time_infected"]):
                    to_recover.add(index)
                else:
                    sick_node["time_infected"] += 1

        for node in to_expose:
            self.expose(node)

        for node in to_infect:
            self.infect(node)

        for node in to_recover:
            self.recover(node)

    def get_neighbors_weights(self, node):
        # TODO: Can this function be simplified / inlined?
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

    def state_color(self, state):
        if state == State.S:
            return "green"
        elif state == State.E:
            return "yellow"
        elif state == State.I:
            return "red"
        elif state == State.R:
            return "blue"

    def get_colors(self):
        states = list([data["state"] for i, data in self.G.nodes(data=True)])
        return [self.state_color(state) for state in states]

    def get_global_state(self):
        global_state = {state: 0 for state in State}
        for index, attributes in self.G.nodes(data=True):
            state = attributes["state"]
            global_state[state] += 1

        return global_state

    def get_global_state_jobs(self):
        global_state = {group: 0 for group in all_groups}
        for index, attributes in self.G.nodes(data=True):
            state = attributes["state"]
            job = attributes["job"]
            global_state[(state, job)] += 1

        return global_state

    def visualize(self):
        nx.draw_networkx(
            self.G, node_color=self.get_colors(), node_size=5, with_labels=False
        )


def str_to_job(s):
    return {"student": Job.S, "teacher": Job.T, "staff": Job.A, "other": Job.O}[s]


def load_data_from_drive():
    """
    Loads graph data from Google Drive.
    """
    edges = {}
    if not os.path.exists("interactions.txt"):
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
    if not os.path.exists("person_descriptions.txt"):
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


# List of all pairs of state and student/teacher status, e.g. "susceptible teachers'
all_groups = {(s, j): None for s in State for j in Job}

edges, people = load_data_from_drive()


if False:  # Don't graph
    Sch = School(edges, people)

    time = []  # Times of steps, in days
    histories = {
        g: [] for g in all_groups
    }  # How many people in 'group' were in 'state'?

    Sch.randomly_expose()

    for i in range(100):  # Length is capped at that many ticks
        time.append(i / 2)

        global_state = Sch.get_global_state_jobs()

        for group in all_groups:
            histories[group].append(global_state[group])

        # If nobody is exposed or infected, the epidemic is over.
        if all(
            map(
                lambda g: global_state[g] == 0,
                [(s, j) for s in [State.E, State.I] for j in Job],
            )
        ):
            print("The epidemic is over on day {}.".format(i / 2))
            break

        Sch.step(i)

    def plot_all_states(job, ax):
        for s in State:
            ys = histories[(s, job)]
            color = Sch.state_color(s)
            ax.plot(time, ys, color=color, label=s.value)

    f, (axStudent, axTeacher, axStaff, axOther) = plt.subplots(
        1, 4, sharex=True, sharey=False, figsize=(25, 4)
    )

    axStudent.set_title("Students")
    plot_all_states(Job.S, axStudent)

    axTeacher.set_title("Teachers")
    plot_all_states(Job.T, axTeacher)

    axStaff.set_title("Staff")
    plot_all_states(Job.A, axStaff)

    axOther.set_title("Other")
    plot_all_states(Job.O, axOther)

    axStudent.set_xlabel("Time Steps (12 hours)")
    axStudent.set_ylabel("People")

    axOther.legend(loc="best")
    plt.show()


def test_epidemic(
    stop_early=True,
    seed=None,
    vaccination_rate=0,
    epidemic_threshold=0.5,
    max_steps=1000,
):

    np.random.seed(seed)
    school = School(edges, people)

    total_susceptible = school.get_global_state()[State.S]

    school.randomly_vaccinate(vaccination_rate)
    school.randomly_expose()

    times = []
    history = {state: [] for state in State}

    epidemic_happened = False
    took_too_long = True

    for i in range(max_steps):
        school.step(i)  # Move the simulation forward by one tick
        global_state = school.get_global_state()

        # Record data for plotting
        times.append(i / 2)
        for state in State:
            history[state].append(global_state[state])

        current_infected = global_state[State.E] + global_state[State.I]
        current_recovered = global_state[State.R]
        if current_infected == 0:
            epidemic_happened = False
            took_too_long = False
            break
        if (
            epidemic_threshold
            <= (current_infected + current_recovered) / total_susceptible
        ):
            epidemic_happened = True
            took_too_long = False
            if stop_early:
                break

    if took_too_long:
        raise RuntimeError(
            "Epidemic took more than " + str(max_steps) + " steps to fail or succeed"
        )
    else:
        return epidemic_happened, times, history


class EpidemicTester:  # A pickle-able version of test_epidemic so we can parallelize
    def __init__(
        self,
        stop_early=True,
        vaccination_rate=0,
        epidemic_threshold=0.5,
        max_steps=1000,
    ):
        self.stop_early = stop_early
        self.vaccination_rate = vaccination_rate
        self.epidemic_threshold = epidemic_threshold
        self.max_steps = max_steps

    def __call__(self, seed=None):
        return test_epidemic(
            self.stop_early,
            seed,
            self.vaccination_rate,
            self.epidemic_threshold,
            self.max_steps,
        )


def parallel_epidemics(
    n, stop_early=True, vaccination_rate=0, epidemic_threshold=0.5, max_steps=1000
):
    pool = mp.Pool(processes=4)
    return pool.map(
        EpidemicTester(stop_early, vaccination_rate, epidemic_threshold, max_steps),
        range(n),
    )


epidemics = parallel_epidemics(16, False, 0)

histories = [(times, history) for (_, times, history) in epidemics]

for times, history in histories:
    infected = np.array(history[State.E]) + np.array(history[State.I])
    plt.plot(times, infected, color="black", alpha=0.3)

plt.show()


if False:  # Make histogram
    results = []
    for rate in np.arange(0, 1, 0.05):
        results.append(np.mean(parallel_epidemics(32, rate)))
        print(rate, results[-1])
