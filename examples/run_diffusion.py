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
from complex_systems.diffusion import Diffusion

def main():
    nb_node = 1000
    Pb_edge = 3.0 / nb_node
    weights = 0.1
    edges_weights = {}

    # Define the Graph

    G = nx.fast_gnp_random_graph(nb_node, Pb_edge)

    # Instantiate the diffusion Process

    D = Diffusion(G)

    # define the weights on the edges

    for edges in G.edges():
        edges_weights[edges] = weights

    # Set the weights on the edge of the graph

    D.set_weight(edges_weights)

    # Run the diffusion Process

    D.run_steps(1000, 1)

    # Stats

    print D.get_number_infected()
    time_stamps = D.get_time_stamps()
    print time_stamps


    time_stamps_list = [vals for key,vals in time_stamps.iteritems()]

    nx.draw(G, pos=nx.spring_layout(G), node_size=20, with_labels=False)

    # the histogram of the data with histtype='step'

    P.figure()
    (n, bins, patches) = P.hist(time_stamps_list, 50, normed=1,
                                histtype='bar', rwidth=0.8)

    # l = P.plot(bins,'k--', linewidth=1.5)

    P.show()


if __name__ == '__main__':
    main()
