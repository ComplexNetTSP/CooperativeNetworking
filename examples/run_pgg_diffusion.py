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
    import networkx as nx
    from complex_systems.pgg_diffusion import PGG_diffusion
    from complex_systems.quasi_unit_disk_graph import gen_quasi_unit_disk_weight
    from complex_systems.quasi_unit_disk_graph import remove_edges_from_graph
    import pylab as plt
    import numpy as np
    
    nb_node = 400
    xmax = 1000
    ymax = 1000
    coop_ratio = 0.5
    synergy = 2
    nb_round = 100
    nb_game_per_round = 1
    nb_def = []
    nb_coop = []
    inner_radius = 45
    outer_radius = 75
    alpha = 0.3
    nb_seeder = 40

    # Generate a Random Graph 
    p = dict((i,(np.random.uniform(low=0.0, high=xmax),np.random.uniform(low=0.0, high=ymax))) for i in range(nb_node))
    G = nx.random_geometric_graph(nb_node,outer_radius,pos=p)
    G = gen_quasi_unit_disk_weight(G=G, outer_radius=outer_radius, inner_radius=inner_radius, alpha=alpha)
    G = remove_edges_from_graph(G)
    # initialize the game 
    PGG = PGG_diffusion(G=G, synergy=synergy,nb_simulation_step=nb_game_per_round, nb_seeder=nb_seeder, buffer_size = 100, cooperator_ratio=coop_ratio, noise_var=0.0)
    for i in range(nb_round):
        PGG.run_game()
        nb_def.append(PGG.defector_counter())
        nb_coop.append(PGG.cooperator_counter())

    plt.figure()
    plt.plot(nb_def,'b-*')
    plt.plot(nb_coop,'r-*')

    plt.figure()
    nx.draw_networkx(G, node_size=20, pos=p, with_labels = False)

    time_stamps_dist = PGG.get_distribution_time_stamps()
    x = []
    y = []
    for key,val in time_stamps_dist.iteritems():
       x.append(key)
       y.append(val)
    
    plt.figure()
    plt.bar(x,y)
    plt.show()

if __name__ == '__main__':
    main()