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

from sumatra.decorators import capture

@capture
def parameters_sweep(parameters):
    import networkx as nx
    from complex_systems.pgg import PublicGoodGames
    import numpy as np
    import csv
    import itertools
    from IPython.parallel import Client

    ####### Init the variables #######
    synergy_step = parameters['synergy_step']
    synergy_max = parameters['synergy_max']
    synergy_min = parameters['synergy_min']
    filename_txt = parameters['filename'] + '_%s.dat' \
        % parameters['sumatra_label']
    filename_jpg = parameters['filename'] + '_%s.jpg' \
        % parameters['sumatra_label']
    nb_batch = parameters['nb_batch']
    synergy_range = np.arange(synergy_min, synergy_max, synergy_step)
    job_id_list = []
    resultats_raw = dict()
    X = []
    Y = []
    Z = []

    # Init Dictionary
    for entry in synergy_range:
        resultats_raw[entry] = []

    ####### Init the Multiprocessing Pool #######
    rc = Client(packer='pickle')
    #rc = Client()
    dview = rc[:]
    lbview = rc.load_balanced_view()
    # Print the number of engine ready
    print 'Run with ', rc.ids, ' Ipython Engines'

    ####### Start the Batch of simualtion #######
    for synergy in synergy_range:
        # Run the Game
        jobid = [lbview.apply_async(run_simu, parameters, synergy) for i in range(nb_batch)]
        job_id_list.append(jobid)
    print 'Job list submited to the scheduler'

    ####### Gather the simulations results #######
    for batch in job_id_list:
        for job in batch:
            resultat = job.get()
            print 'Number of job still runing:', len(rc.outstanding)
            map_id, val1, val2 = resultat
            resultats_raw[map_id].append((val1,val2))
        print 'Finish the batch of simulation for synergy=', map_id
    items = resultats_raw.items()
    items.sort()
    ####### Reduce the results #######
    for key,val in items:
        x, y, z  = reduceR(key, val)
        X.append(x)
        Y.append(y)
        Z.append(z)

    ####### Save the Result in csv file  #######
    with open(filename_txt, 'wb') as f:
        writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
        for row_id in xrange(len(X)):
            row = [X[row_id], Y[row_id], Z[row_id]]
            writer.writerow(row)

def reduceR(key, val):
    import numpy as np
    val1, val2 = zip(*val)
    print 'Reducer:', val1
    return key, np.mean(val1), np.mean(val2)

def run_simu(parameters, synergy):
    import numpy as np
    import networkx as nx
    from complex_systems.dygraph import DyGraph
    from complex_systems.pgg import PublicGoodGames
    from complex_systems.quasi_unit_disk_graph import gen_quasi_unit_disk_weight
    from complex_systems.quasi_unit_disk_graph import remove_edges_from_graph


    number_of_node = parameters['number_of_node']
    size_of_simulation_area = parameters['size_of_simulation_area']
    outer_radius = parameters['outer_radius']
    inner_radius = parameters['inner_radius']
    alpha_quasi_unit_disk = parameters['alpha_quasi_unit_disk']
    coop_ratio = parameters['initial_cooperator_ratio']
    simulation_length = parameters['simulation_length']
    sampling_interval = parameters['sampling_interval']
    alpha_levy = parameters['alpha_levy']
    noise_var = parameters['noise_variance']
    beta = parameters['beta']
    f_min = parameters['f_min']
    f_max = parameters['f_max']
    s_min = parameters['s_min']
    s_max = parameters['s_max']
    velocity = parameters['velocity']

    G = DyGraph(time_stop=simulation_length, time_step=sampling_interval)
    G.generate_mobility_levy_walk(
        alpha=alpha_levy,
        beta=beta,
        size_max=size_of_simulation_area,
        f_min=f_min,
        f_max=f_max,
        s_min=s_min,
        s_max=s_max,
        b_c=2,
        radius=outer_radius,
        nb_node=number_of_node,
        velocity=velocity,
        )

    first_run = True
    resultats = []
    for g in G:
        g = gen_quasi_unit_disk_weight(G=g, outer_radius=outer_radius,
                inner_radius=inner_radius, alpha=alpha_quasi_unit_disk)
        g = remove_edges_from_graph(g)
        if first_run == True:
            PGG = PublicGoodGames(G=g, synergy=synergy,
                                  cooperator_ratio=coop_ratio,
                                  noise_var=noise_var)
            nb_coop = PGG.run_game(sampling_interval)
            resultats.append(nb_coop)
            strategies = PGG.get_strategies()
            first_run = False
        else:
            PGG = PublicGoodGames(G=g, synergy=synergy,
                                  cooperator_ratio=coop_ratio,
                                  noise_var=noise_var)
            PGG.set_strategies(strategies)
            nb_coop = PGG.run_game(sampling_interval)
            strategies = PGG.get_strategies()
            resultats.append(nb_coop)

    return (synergy, nb_coop, np.mean(G.avg_degree()))

if __name__ == '__main__':
    import sys
    from sumatra.parameters import build_parameters

    sys.path.append('../..')

    parameter_file = sys.argv[1]
    parameters = build_parameters(parameter_file)
    parameters_sweep(parameters)
