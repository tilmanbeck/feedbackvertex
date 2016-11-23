import TreeDecomposition as td
from Graphviz import GraphVisualization
import random as rnd
import time
import DynamicProgramm as dp

# https://www.researchgate.net/figure/221426649_fig1_Fig-1-An-example-of-an-H-coloring-of-G-is-the-mapping-A-a-A-d-A-f-1
# example graph G

#############################################################
######################### BIG EXAMPLE #######################
#############################################################
# k = 3
# vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# N = 2 * len(vertices)
# edges = [{'a', 'b'}, {'a', 'g'}, {'b', 'g'}, {'b', 'c'},
#          {'c', 'e'}, {'g', 'e'}, {'g', 'f'}, {'e', 'f'},
#          {'c', 'd'}, {'d', 'e'}]
# weights = {vertices[i]: rnd.randint(1, N) for i in range(0, len(vertices))}
#
# ecd = td.TreeDecomposition(None, None, ['e', 'c', 'd'])
# efg = td.TreeDecomposition(None, None, ['e', 'f', 'g'])
# abg = td.TreeDecomposition(None, None, ['a', 'b', 'g'])
# ecg = td.TreeDecomposition(efg, ecd, ['e', 'c', 'g'])
# bcg = td.TreeDecomposition(abg, ecg, ['b', 'c', 'g'])
# bc = td.TreeDecomposition(bcg, None, ['b', 'c'])
#
# bc = td.root(bc)
# td.leaf(bc)
# td.join(bc)
# td.add_internal_nodes(bc)
# td.edge_bags(bc, edges)

# gv = GraphVisualization(bc)
# gv.createGraph()

# dp.count(vertices, bc, ['d','c','e'], k, N, weights)

# k = 3
# vertices = ['a', 'b', 'c', 'd', 'e']
# N = 2 * len(vertices)
# edges = [{'a', 'b'}, {'a', 'd'}, {'b', 'd'}, {'b', 'c'},
#          {'c', 'e'}, {'d', 'e'}]
# weights = {vertices[i]: rnd.randint(1, N) for i in range(0, len(vertices))}
#
# abg = td.TreeDecomposition(None, None, ['a', 'b', 'd'])
# ecg = td.TreeDecomposition(None, None, ['e', 'c', 'd'])
# bcg = td.TreeDecomposition(abg, ecg, ['b', 'c', 'd'])
# bc = td.TreeDecomposition(bcg, None, ['b', 'c'])
# bc = td.td.root(bc)
# td.td.leaf(bc)
# td.join(bc)
# td.add_internal_nodes(bc)
# td.edge_bags(bc, edges)
#
# gv = GraphVisualization(bc)
# gv.createGraph()

#############################################################
######################### SMALL EXAMPLE #####################
#############################################################
# vertices = ['a','b','c']
# edges = [{'a','b'}, {'b','c'}]
#
# k = 2
# N = 5
# weights = {vertices[i]: rnd.randint(1,N) for i in range(0,len(vertices))}
# bc = td.TreeDecomposition(None, None, ['b', 'c'])
# ab = td.TreeDecomposition(bc, None, ['a', 'b'])
#
# ab = td.root(ab)
# td.leaf(ab)
# td.join(ab)
# td.add_internal_nodes(ab)
# td.edge_bags(ab,edges)
# # v = GraphVisualization(ab)
# # v.createGraph()
# #
# # dp.count(vertices, ab, ['a', 'c'], k, N, weights)
# #


#############################################################
######################### LARGE EXAMPLE #####################
#############################################################
#UNSER GEHIRNSCHMALZ
#
vertices = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p']

edges = [{'a', 'b'}, {'a', 'g'}, {'b', 'g'}, {'b', 'c'},
         {'c', 'e'}, {'g', 'e'}, {'g', 'f'}, {'e', 'f'},
         {'c', 'd'}, {'d', 'e'}, {'h', 'g'}, {'h', 'f'},
         {'h', 'i'}, {'i', 'f'}, {'i', 'j'}, {'j', 'f'},
         {'k', 'l'}, {'k', 'o'}, {'k', 'm'}, {'o', 'l'},
         {'m', 'n'}, {'m', 'p'}, {'n', 'p'}, {'e', 'k'},
         {'d', 'k'}]
k = 4
N = 2 * len(vertices)


weights = {vertices[i]: rnd.randint(1, N) for i in range(0, len(vertices))}


mnp = td.TreeDecomposition(None, None, ['m', 'n', 'p'])

fij = td.TreeDecomposition(None, None, ['f', 'i', 'j'])
klo = td.TreeDecomposition(None, None, ['k', 'l', 'o'])
kmn = td.TreeDecomposition(mnp, None, ['k', 'm', 'n'])

hfi = td.TreeDecomposition(fij, None, ['h', 'f', 'i'])
ekl = td.TreeDecomposition(klo, None, ['e', 'k', 'l'])
dmk = td.TreeDecomposition(kmn, None, ['d', 'm', 'k'])

ghf = td.TreeDecomposition(hfi, None, ['g', 'h', 'f'])
edk = td.TreeDecomposition(ekl, dmk, ['e', 'd', 'k'])

ecd = td.TreeDecomposition(edk, None, ['e', 'c', 'd'])
gfe = td.TreeDecomposition(ghf, None, ['g', 'f', 'e'])

cge = td.TreeDecomposition(gfe, ecd, ['c', 'g', 'e'])
bga = td.TreeDecomposition(None, None, ['b', 'g', 'a'])

bcg = td.TreeDecomposition(bga, cge, ['b', 'c', 'g'])

bc = td.TreeDecomposition(bcg, None, ['b', 'c'])

bc = td.root(bc)
td.leaf(bc)
td.join(bc)
td.add_internal_nodes(bc)
td.edge_bags(bc, edges)

gv = GraphVisualization(bc)
gv.createGraph()

# runs = 25
# t = [0] * runs
# for i in range(0, runs):
#     vertices = ['a', 'b', 'c']
#     edges = [{'a', 'b'}, {'b', 'c'}]
#
#     k = 2
#     N = 6
#     weights = {vertices[i]: rnd.randint(1, N) for i in range(0, len(vertices))}
#     bc = td.TreeDecomposition(None, None, ['b', 'c'])
#     ab = td.TreeDecomposition(bc, None, ['a', 'b'])
#
#     ab = td.root(ab)
#     td.leaf(ab)
#     td.join(ab)
#     td.add_internal_nodes(ab)
#     td.edge_bags(ab, edges)
#
#     s = time.time()
#     dp.count(vertices, ab, ['b','c'], k, N, weights)
#     e = time.time()
#     t[i] = (e-s)
#
# avg = 0
# for i in range(0, runs):
#     avg += t[i]
#
# avg /= runs
#
# print("Execution Time: " + str(avg)+"s")