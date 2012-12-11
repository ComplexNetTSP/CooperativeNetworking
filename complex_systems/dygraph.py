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

_author__ = """\n""".join(['Vincent Gauthier'])


class DyGraph:

    '''
    DynamicGraph store the time evolution of a graph by saving the snapshot of a graph at a given sampling rate
    
    :Example:
    >>> import networkx as nx
    >>> G = DyGraph()
    >>> G.add_graph(nx.Graph(), 10.0)

    '''

    def __init__(
        self,
        time_stop=None,
        time_step=1.0,
        timeline=None,
        ):
        '''
        Constructor 
        '''

        import numpy as N
        self._slices = {}
        self._index = 0
        self._slice_time = []
        self._nodes_states = {}
        if timeline != None:
            self._slice_time = timeline
            self._time_stop = max(timeline)
            self._time_step = timeline[1] - timeline[0]
            self._generate_empty_slices()
        elif time_stop != None:
            self._time_stop = time_stop
            self._time_step = time_step
            self._slice_time = N.arange(0, time_stop, time_step)
            self._generate_empty_slices()

    def add_graph(self, G, slice_time):
        '''
        Add a new slice or update a slice 
        '''

        G.graph['slice_time'] = slice_time

        if not slice_time in self._slice_time:
            self._slice_time.append(slice_time)
            self._time_stop = max(self._slice_time)
            self._time_start = min(self._slice_time)
            self._slice_time.sort()

        self._slices[int(slice_time)] = {'slice_time': slice_time,
                'graph': G}

    def get_slice(self, time_step=0.0):
        '''
        Return the graph slice at time_step=time
        '''

        return self._slices[int(time_step)]

    def get_slice_time(self):
        '''
        Return the slice time list
        '''

        return list(self._slice_time)

    def get_graph(self, time_step=0.0):
        '''
        Return the graph at time_step=time
        '''

        return self._slices[int(time_step)]['graph']

    def __iter__(self):
        '''
        Iterate through the graph of all the slice in the structure 
        
        :Example:
        >>> G = DyGraph()
        >>> G.add_graph(nx.Graph(), 10.0)
        >>> G.add_graph(nx.Graph(), 10.0)
        >>> for g in G: 
        >>>     print g.graph('slice_time')
        '''

        return self

    def next(self):
        '''
        Iterate through the graph of all the slice in the structure 
        
        :Example:
        >>> G = DyGraph()
        >>> G.add_graph(nx.Graph(), 10.0)
        >>> G.add_graph(nx.Graph(), 10.0)
        >>> for g in G: 
        >>>     print g.graph('slice_time')
        '''

        if self._index > len(self._slice_time) - 1:
            self._index = 0
            raise StopIteration
        else:
            self._index += 1
            idx = self._slice_time[self._index - 1]
            return self._slices[idx]['graph']

    def set_nodes_states(self, nodes_states):
        self._nodes_states = nodes_states

    def get_nodes_states(self):
        return self._nodes_states

    def avg_degree(self):
        import numpy as np
        average_dygraph_degree = []
        for (slice_id, s) in self._slices.iteritems():
            G = s['graph']
            average_dygraph_degree.append(np.mean(G.degree().values()))
        return np.mean(average_dygraph_degree)

    def generate_mobility_levy_walk(
        self,
        alpha,
        beta,
        size_max,
        f_min,
        f_max,
        s_min,
        s_max,
        b_c,
        radius,
        velocity=1.0,
        nb_node=1,
        ):
        '''
        Generate a Levy walk for each node where teh sampling interval are defined as follow : 

        - time_interval = [time_stop:time_step:time_stop]
        - nb_slices = (time_stop-time_start/time_step)  

        :Parameters:
        - `alpha` : float 
            Levy exponent for flight length distribution, 0 < alpha <= 2
        - `beta`  : float 
            Levy exponent for pause time distribution, 0 < beta <= 2
        - `size_max` : int 
            size of simulation area
        - `velocity` : float
            speed in m/s
        - `f_min` : int
            min flight length
        - `f_max` : int
            max flight length
        - `s_min` : int 
            min pause time (second)
        - `s_max` : int  
            max pause time (second)
        - `b_c` : int 
            boundary condition: 
                - wrap-around if b_c=1
                - reflection boundary if b_c=2
        - `nb_node` : int (default 1)
            number of node in the model 
        '''

        from mobility.levy_walk import levy_walk
        import networkx as nx

        # For each node generate a levy_walk

        for node in range(nb_node):
            (un_sampled, A, B, sampled) = levy_walk(
                alpha=alpha,
                beta=beta,
                sample_length=self._time_step,
                size_max=size_max,
                velocity=velocity,
                f_min=f_min,
                f_max=f_max,
                s_min=s_min,
                s_max=s_max,
                duration=self._time_stop,
                b_c=b_c,
                )

            # Position X,Y at time T of a node in his walk

            (X, Y, T) = zip(*sampled)

            # Foreach time step add a new node with pos=(X,Y) in the graph

            for i in range(len(T)):
                self._slices[int(T[i])]['graph'].add_node(node,
                        pos=(X[i], Y[i]))

        # For each slice generate a the edges of the graph

        for (key, val) in self._slices.iteritems():
            pos = nx.get_node_attributes(val['graph'], 'pos')
            G = self._generate_gemetric_graph(nb_node, pos=pos,
                    radius=radius)
            nx.set_node_attributes(G, 'pos', pos)
            self.add_graph(G, key)

    def generate_weights(
        self,
        inner_radius,
        outer_radius,
        alpha,
        ):
        '''Generate weigth  
        '''

        from quasi_unit_disk_graph import gen_quasi_unit_disk_weight
        import networkx as nx
        for t in self._slice_time:
            pos = nx.get_node_attributes(self._slices[int(t)]['graph'],
                    'pos')
            G = gen_quasi_unit_disk_weight(self._slices[int(t)]['graph'
                    ], outer_radius, inner_radius, alpha)
            nx.set_node_attributes(G, 'pos', pos)
            self.add_graph(G, t)

    def diffusion(
        self,
        slice_time,
        synergy,
        states=None,
        time_stamps=None,
        nb_steps=1,
        infected_node=1,
        cooperator_ratio=0.0,
        strategies=None,
        payoffs=None
        ):

        from diffusion import Diffusion
        from pgg import PublicGoodGames
        
        G = self._slices[int(slice_time)]['graph'].copy()

        if states == None or time_stamps == None:
            # Initialize the Public Good Game 
            PGG = PublicGoodGames(G=G,
                    cooperator_ratio=cooperator_ratio, nb_simulation_step=nb_steps, synergy=synergy)

            # Get the startegies list
            strategies = PGG.get_strategies()

            # Initialize the disffusion process with the startegies list
            D = Diffusion(G=G, nb_simulation_step=nb_steps,
                          time_step=self._time_step,
                          initial_time_stamp=slice_time,
                          strategies=strategies)
            
            # Run the diffusion Process
            D.run_steps(infected_node)

            # Run the Game  
            PGG.run_game()

            # Return the strategies list, the payoffs list, the timestamps list and the states list 
            return (D.get_states(), D.get_time_stamps(), PGG.get_strategies(), PGG.get_payoffs())
        elif strategies != None and payoffs != None:

            D = Diffusion(G=G, nb_simulation_step=nb_steps,
                          time_step=self._time_step,
                          initial_time_stamp=slice_time,
                          strategies=strategies)

            PGG = PublicGoodGames(G=G, nb_simulation_step=nb_steps, synergy=synergy)
            
            PGG.set_strategies(strategies)
            PGG.set_payoffs(payoffs)

            D.set_nodes_states(states)
            D.set_node_time_stamps(time_stamps)

            # Run the diffusion Process
            D.run_steps(infected_node)
            # Run the Game  
            PGG.run_game()
            # Return the strategies list, the payoffs list, the timestamps list and the states list 
            return (D.get_states(), D.get_time_stamps(), PGG.get_strategies(), PGG.get_payoffs())

    # ####################
    # Private Methodes
    # ####################

    def _generate_empty_slices(self):
        import networkx as nx
        for t in self._slice_time:
            self.add_graph(nx.Graph(), t)

    def _generate_gemetric_graph(
        self,
        nb_node,
        radius,
        pos,
        ):

        import networkx as nx
        return nx.random_geometric_graph(nb_node, radius, pos=pos)
