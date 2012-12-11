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


def main():
    from complex_systems.dygraph import DyGraph
    import networkx as nx
    import pylab as plt

    G = DyGraph(time_stop=400.0, time_step=5.0)
    G.generate_mobility_levy_walk(
        alpha=0.9,
        beta=0.9,
        size_max=1000,
        f_min=1,
        f_max=100,
        s_min=1,
        s_max=100.0,
        b_c=2,
        radius=200.0,
        nb_node=2,
        velocity=float(1.0/60), 
        )
    time_step = 10.0
    graph = G.get_graph(time_step)
    i = 1
    for g in G:
        print "print graph of the slice ", g.graph['slice_time']
        pos = nx.get_node_attributes(g, 'pos')
        plt.figure()
        plt.title('Time = ' + str(g.graph['slice_time']*5.0) + ' seconds')
        limits=plt.axis('off')
        plt.draw() 
        nx.draw(g, pos=pos,with_labels=False, node_size=20)
        filename = 'graph_' + str("%04d" % i) + '.jpg'
        plt.savefig(filename)
        i += 1 


if __name__ == '__main__':
    main()
