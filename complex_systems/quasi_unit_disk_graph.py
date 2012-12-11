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


def gen_quasi_unit_disk_weight(
    G,
    outer_radius,
    inner_radius,
    alpha,
    ):

    import numpy as N
    
    for edge in G.edges():
        (node_s, node_d) = edge
        (x_s, y_s) = G.node[node_s]['pos']
        (x_d, y_d) = G.node[node_d]['pos']
        D = N.sqrt((x_s - x_d) ** 2 + (y_s - y_d) ** 2)
        if D <= inner_radius:
            weight = 1
        elif D >= outer_radius:
            weight = 0
        else:
            weight = ((outer_radius - D) / (outer_radius
                      - inner_radius)) ** alpha
        G.edge[node_s][node_d]['weight'] = weight
    return G

def remove_edges_from_graph(G):
    from random import random
    H = G.copy()
    for edge in H.edges():
        (node_s, node_d) = edge
        if H.edge[node_s][node_d]['weight'] < random():
            H.remove_edge(*edge)
    return H 