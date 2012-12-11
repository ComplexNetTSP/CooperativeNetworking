#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Copyright (c) 2012 Vincent Gauthier.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# -------------------------------------------------------------------------------


__author__ = """\n""".join(['Vincent Gauthier'])

import networkx as nx
import random as RD
import pylab as P
import numpy as N

class Diffusion(object):

    """docstring for Diffusion"""

    def __init__(
        self,
        G,
        time_step,
        nb_simulation_step,
        initial_infection_rate=0.0,
        initial_time_stamp=0.0, 
        strategies = None,
        ):

        super(Diffusion, self).__init__()
        
        self._G = G
        self._initial_infection_rate = initial_infection_rate
        self._initial_time_stamp = initial_time_stamp
        self._nb_simulation_step = nb_simulation_step
        self._time_step = float(time_step) / nb_simulation_step
        self.set_strategies(strategies)

        for node in self._G.nodes():
            if RD.random() < initial_infection_rate:
                self._G.node[node]['state'] = 'I'
                self._G.node[node]['time_stamp'] = initial_time_stamp
            else:
                self._G.node[node]['state'] = 'S'
                self._G.node[node]['time_stamp'] = initial_time_stamp

    def run_steps(self, infected_node):
        self.set_infected(infected_node)
        for i in range(self._nb_simulation_step):
            self.diffusion_step()
            self.set_time_stamp(infected_node, self._initial_time_stamp
                                + i * self._nb_simulation_step)

    def diffusion_step(self):
        H = self._G.copy()
        node_list = H.nodes()
        RD.shuffle(node_list)
        for node in node_list:
            if H.node[node]['state'] == 'I' and H.node[node]['strategy'] == 'C':
                neighbors = H.neighbors(node)
                for neighbor in neighbors:
                    if RD.random() \
                        < H.edge[node][neighbor]['weight']:
                        if H.node[neighbor]['state'] == 'S':
                            H.node[neighbor]['state'] = 'I'
                            H.node[neighbor]['time_stamp'] = \
                                H.node[node]['time_stamp']
                        else:
                            max_time_stamp = \
                                max(H.node[neighbor]['time_stamp'
                                    ], H.node[node]['time_stamp'])
                            H.node[neighbor]['time_stamp'] = \
                                max_time_stamp
                            H.node[node]['time_stamp'] = \
                                max_time_stamp
        self._G = H.copy()

    #
    # Set
    #
    def set_nodes_states(self, nodes_states):
        for (key, val) in nodes_states.iteritems():
            self._G.node[key]['state'] = val

    def set_node_time_stamps(self, time_stamps):
        for (key, val) in time_stamps.iteritems():
            self._G.node[key]['time_stamp'] = val 

    def set_time_stamp(self, node_id, time_stamp):
        self._G.node[node_id]['state'] = 'I'
        self._G.node[node_id]['time_stamp'] = time_stamp

    def set_weight(self, weights):
        for (item, val) in weights.iteritems():
            (node_s, node_d) = item
            self._G.edge[node_s][node_d]['weight'] = val

    def set_strategies(self, strategies):
        '''
        initialize the strategy of a node in the graph
        '''
        if strategies != None:
            for node in self._G.nodes():
                self._G.node[node]['strategy'] = strategies[node]
        else:
            for node in self._G.nodes():
                self._G.node[node]['strategy'] = 'C'

    def set_infected(self, infected_node):
        '''
        initialize the infected node in the graph 
        '''
        time_stamp = self._initial_time_stamp
        if type(infected_node) == list:
            for node in infected_node.iteritems():
                self._G.node[node]['state'] = 'I'
                self._G.node[node]['time_stamp'] = time_stamp
        else:
            self._G.node[infected_node]['state'] = 'I'
            self._G.node[infected_node]['time_stamp'] = time_stamp

    #
    # Get 
    #
    def get_number_infected(self):
        infected = 0
        for node in self._G.nodes():
            if self._G.node[node]['state'] == 'I':
                infected += 1
        return infected

    def get_time_stamps(self):
        time_stamps = {}
        for node in self._G.nodes():
            time_stamps[node] = self._G.node[node]['time_stamp']
        return time_stamps

    def get_states(self):
        states = {}
        for node in self._G.nodes():
            states[node] = self._G.node[node]['state']
        return states