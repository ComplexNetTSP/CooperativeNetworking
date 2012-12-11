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

from complex_systems.dygraph import DyGraph
import unittest


class test_DyGraph(unittest.TestCase):

    def setUp(self):
        self.dygraph = DyGraph()

    def test_add_graph(self):
        import networkx as nx
        self.dygraph = DyGraph()
        timeStep = 10.0 
        G = nx.Graph()
        G.add_node(1)
        G.add_node(2)
        self.dygraph.add_graph(G, timeStep)
        self.assertDictEqual(G.node,
                             self.dygraph._slices[timeStep]['graph'
                             ].node)
        self.assertEqual(timeStep,
                         self.dygraph._slices[timeStep]['graph'
                         ].graph['slice_time'])

    def test_dygraph(self):
        import numpy as N
        self.dygraph = DyGraph(time_stop=100.0, time_step=10.0)
        self.assertEqual(N.ceil(100.0 / 10.0),
                         len(self.dygraph._slices))

    def test_dygraph_with_timeline(self):
        import numpy as N
        self.dygraph = DyGraph(timeline=N.arange(0,100,10))
        self.assertEqual(N.ceil(100.0 / 10.0),
                         len(self.dygraph._slices))

    def test_iter(self):
        import networkx as nx
        self.dygraph = DyGraph()
        self.dygraph.add_graph(nx.Graph(),10.0)
        self.dygraph.add_graph(nx.Graph(),20.0)
        self.dygraph.add_graph(nx.Graph(),30.0)
        for g in self.dygraph:
            print g.graph['slice_time']
        self.assertEqual([10.0, 20.0, 30], self.dygraph._slice_time)

    def test_gen_mobility(self):
        import numpy as N
        self.dygraph = DyGraph(time_stop=100.0, time_step=10.0)
        self.dygraph.generate_mobility_levy_walk(
            alpha=0.9,
            beta=0.9,
            size_max=100,
            f_min=10,
            f_max=100,
            s_min=1,
            s_max=100,
            b_c=2,
            radius=20.0,
            nb_node=10,
            )
        self.assertEqual(N.ceil(100.0 / 10.0),
                         len(self.dygraph._slices))

if __name__ == '__main__':
    unittest.main()