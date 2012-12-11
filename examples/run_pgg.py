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
	from complex_systems.pgg import PublicGoodGames
	import pylab as plt
	import numpy as np
	
	nb_node = 1000
	edge_prob = 10.0/nb_node
	coop_ratio = 0.5
	synergy = 8
	nb_round = 100
	nb_game_per_round = 10
	nb_def = []
	nb_coop = []
	
	# Generate a Random Graph 
	G = nx.fast_gnp_random_graph(nb_node, edge_prob)
	# initialize the game 
	PGG = PublicGoodGames(G=G, synergy=synergy,nb_simulation_step=nb_game_per_round, cooperator_ratio=coop_ratio)
	for i in range(nb_round):
		PGG.run_game()
		nb_def.append(PGG.defector_counter())
		nb_coop.append(PGG.cooperator_counter())
		#print nb_coop, nb_def
	plt.figure()
	plt.plot(nb_def,'b-*')
	plt.plot(nb_coop,'r-*')
	plt.figure()
	print np.mean([val for key, val in G.degree().iteritems()])
	nx.draw_networkx(G, node_size=20, with_labels = False)
	plt.show()

if __name__ == '__main__':
	main()