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


def main():
    from complex_systems.dygraph import DyGraph
    from complex_systems.quasi_unit_disk_graph import gen_quasi_unit_disk_weight
    from complex_systems.diffusion import Diffusion
    import networkx as nx
    import pylab as plt

    # Variables

    size_of_simulation_area = 1000.0
    inner_radius = 10
    outer_radius = 50
    number_of_node = 100
    simulation_length = 1000.0
    sample_interval = 10.0
    alpha = 0.8

    # Generate a Graph with position

    G = DyGraph(time_stop=simulation_length, time_step=sample_interval)
    G.generate_mobility_levy_walk(
        alpha=0.9,
        beta=0.9,
        size_max=size_of_simulation_area,
        f_min=10,
        f_max=1000,
        s_min=5,
        s_max=1000.0,
        b_c=2,
        radius=outer_radius,
        nb_node=number_of_node,
        )

    G.generate_weights(inner_radius=inner_radius,
                       outer_radius=outer_radius, alpha=alpha)

    slice_time_list = G.get_slice_time()
    i = 1
    for t in slice_time_list:
        if t == 0.0:
            [states, time_stamps, strategies, payoffs] = G.diffusion(t,
                    nb_steps=10, synergy=8.0,
                    cooperator_ratio=0.5)
        else:
            Gslice = G.get_graph(t)
            pos = nx.get_node_attributes(Gslice, 'pos')

            [states, time_stamps, strategies, payoffs] = G.diffusion(
                t,
                nb_steps=10,
                synergy=8.0,
                states=states,
                time_stamps=time_stamps,
                strategies=strategies,
                payoffs=payoffs,
                )
            nbcoops =  [strategy for strategy in strategies if strategy == 'C'].count()


        Gslice = G.get_graph(t)

        pos = nx.get_node_attributes(Gslice, 'pos')
        nodelist_infected = [key for (key, val) in states.iteritems()
                             if val == 'I']
        nodelist_not_infected = [key for (key, val) in
                                 states.iteritems() if val == 'S']

        plt.figure()
        nx.draw_networkx(Gslice, nodelist=nodelist_infected, pos=pos, with_labels=False, node_size=20)
        nx.draw_networkx(Gslice, nodelist=nodelist_not_infected, pos=pos, with_labels=False, node_size=20, node_color='g')
        filename = 'diffusion_' + str("%04d" % i) + '.jpg'
        plt.savefig(filename)

        i += 1

    time_stamps_list = [vals for (key, vals) in time_stamps.iteritems()]

    plt.figure()
    (n, bins, patches) = plt.hist(time_stamps_list, 50, normed=1,
                                  histtype='bar', rwidth=0.8)
    plt.show()


if __name__ == '__main__':
    main()
