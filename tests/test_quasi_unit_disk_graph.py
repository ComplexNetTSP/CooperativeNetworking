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

from complex_systems.quasi_unit_disk_graph import gen_quasi_unit_disk_weight
import unittest


class test_QuasiUnitDiskGraph(unittest.TestCase):

    def setUp(self):
        import networkx as nx

        self.G = nx.Graph()
        self.G.add_node(1, pos=(1, 1))
        self.G.add_node(2, pos=(1, 2))
        self.G.add_node(3, pos=(1, 3))
        self.G.add_edge(1, 2)
        self.G.add_edge(1, 3)
        self.G.add_edge(2, 3)

    def test_gen_weight(self):
        G1 = gen_quasi_unit_disk_weight(self.G, inner_radius=1,
                outer_radius=3, alpha=1)
        val = [d['weight'] for (u, v, d) in G1.edges(data=True)]
        self.assertEqual(val, [1, 0.5, 1])


if __name__ == '__main__':
    unittest.main()
