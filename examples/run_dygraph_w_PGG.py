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
    from complex_systems.pgg import PublicGoodGames
    from complex_systems.quasi_unit_disk_graph import gen_quasi_unit_disk_weight
    from complex_systems.quasi_unit_disk_graph import remove_edges_from_graph
    import networkx as nx
    import pylab as plt

    outer_radius = 75
    inner_radius = 40
    alpha_quasi_unit_disk = 0.9
    synergy = 8
    coop_ratio = 0.5
    noise_var = 1
    nb_node = 400
    time_step = 5.0
    G = DyGraph(time_stop=2000.0, time_step=time_step)
    G.generate_mobility_levy_walk(
        alpha=0.9,
        beta=0.9,
        size_max=1000,
        f_min=10,
        f_max=1000,
        s_min=5,
        s_max=1000.0,
        b_c=2,
        radius=200.0,
        nb_node=nb_node,
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
            nb_coop = PGG.run_game(time_step)
            resultats.append(nb_coop)
            strategies = PGG.get_strategies()
            first_run = False
        else:
            PGG = PublicGoodGames(G=g, synergy=synergy,
                                  cooperator_ratio=coop_ratio,
                                  noise_var=noise_var)
            PGG.set_strategies(strategies)
            nb_coop = PGG.run_game(time_step)
            strategies = PGG.get_strategies()
            resultats.append(nb_coop)
    plt.figure()
    plt.plot(resultats, '-o')
    plt.show()

if __name__ == '__main__':
    main()
