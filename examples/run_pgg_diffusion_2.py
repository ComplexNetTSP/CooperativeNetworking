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



def main(parameters):
    import networkx as nx
    from complex_systems.dygraph import DyGraph
    from complex_systems.pgg_diffusion import PGG_diffusion
    from complex_systems.quasi_unit_disk_graph import gen_quasi_unit_disk_weight
    from complex_systems.quasi_unit_disk_graph import remove_edges_from_graph
    import pylab as plt
    import numpy as np
    
    nb_node = 400
    xmax = 1000
    ymax = 1000
    coop_ratio = 0.5
    synergy = 9
    nb_game_per_round = 1
    nb_def = []
    nb_coop = []
    number_of_node = parameters['number_of_node']
    nb_seeder = parameters['number_of_seeder']
    size_of_simulation_area = parameters['size_of_simulation_area']
    buffer_size = parameters['buffer_size']
    outer_radius = parameters['outer_radius']
    inner_radius = parameters['inner_radius']
    alpha_quasi_unit_disk = parameters['alpha_quasi_unit_disk']
    coop_ratio = parameters['initial_cooperator_ratio']
    simulation_length = parameters['simulation_length']
    sampling_interval = parameters['sampling_interval']
    alpha_levy = parameters['alpha_levy']
    #noise_var = parameters['noise_variance']
    noise_var = 0.1
    beta = parameters['beta']
    f_min = parameters['f_min']
    f_max = parameters['f_max']
    s_min = parameters['s_min']
    s_max = parameters['s_max']
    velocity = parameters['velocity']


    G = DyGraph(time_stop=simulation_length,
                time_step=sampling_interval)
    G.generate_mobility_levy_walk(
        alpha=alpha_levy,
        beta=beta,
        size_max=xmax,
        f_min=f_min,
        f_max=f_max,
        s_min=s_min,
        s_max=s_max,
        b_c=2,
        radius=outer_radius,
        nb_node=nb_node,
        velocity=velocity,
        )

    first_run = True
    for g in G:
        g = gen_quasi_unit_disk_weight(G=g, outer_radius=outer_radius,
                inner_radius=inner_radius, alpha=alpha_quasi_unit_disk)
        g = remove_edges_from_graph(g)
        if first_run == True:

            PGG = PGG_diffusion(G=g, synergy=synergy,
                                cooperator_ratio=coop_ratio,
                                noise_var=noise_var,
                                buffer_size=buffer_size,
                                nb_seeder=int(nb_seeder))

            PGG.run_game()
            nb_def.append(PGG.defector_counter())
            nb_coop.append(PGG.cooperator_counter())
            strategies = PGG.get_strategies()
            time_stamps = PGG.get_time_stamps()
            states = PGG.get_states()
            #sent_update = PGG.get_sent_update()
            seeder = PGG.get_seeder()
            #print time_stamps[0]
            #print sent_update
            #print strategies
            #print states
            first_run = False
        else:
            PGG = PGG_diffusion(G=g, synergy=synergy,
                                cooperator_ratio=coop_ratio,
                                buffer_size=buffer_size,
                                noise_var=noise_var)
            PGG.set_strategies(strategies)
            PGG.set_time_stamps(time_stamps)
            PGG.set_nodes_states(states)
            #PGG.set_sent_update(sent_update)
            PGG.set_seeder(seeder)
            res = PGG.run_game()
            nb_def.append(PGG.defector_counter())
            nb_coop.append(PGG.cooperator_counter())
            strategies = PGG.get_strategies()
            time_stamps = PGG.get_time_stamps()
            states = PGG.get_states()
            #print states
            #print strategies
            #print time_stamps[0]
            #sent_update = PGG.get_sent_update()
            #seeder = PGG.get_seeder()
            #print seeder
    print synergy, res, np.mean(G.avg_degree())
    plt.figure()
    plt.plot(nb_def,'b-*')
    plt.plot(nb_coop,'r-*')

    #plt.figure()
    #print np.mean([val for key, val in G.degree().iteritems()])
    #nx.draw_networkx(G, node_size=20, pos=p, with_labels = False)

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
    import sys
    from sumatra.parameters import build_parameters
    parameter_file = sys.argv[1]
    parameters = build_parameters(parameter_file)
    main(parameters)