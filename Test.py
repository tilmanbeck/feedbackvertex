from TreeDecomposition import TreeDecomposition
from TreeDecomposition import print_NiceTree_indented
from TreeDecomposition import leaf
from TreeDecomposition import root
from TreeDecomposition import join
from TreeDecomposition import addInternalNodes
from TreeDecomposition import saveTreeDecomposition
from TreeDecomposition import edgeBags
from TreeDecomposition import containsEdge
from BagType import BagType
from Graphviz import GraphVisualization
import numpy as np
import random as rnd

#value zB [0,1,2,2,0]
#missingNodes zB [0,4]
#indices []
#indices of the missingNodes in value have to be zero!d
def calculateIndices(value, missingNodes):
    indices = calculateIndicesRec(value, missingNodes, [])
    return list(set(indices))

def calculateIndicesRec(value, missingNodes, indices):
    if not missingNodes:
        return indices
    else:
        # Honorshema
        startPoint = 0
        for i in range(0,len(value)):
            startPoint = startPoint +  3**i * value[i]

        i1 = startPoint + 3**missingNodes[0] * 0
        i2 = startPoint + 3**missingNodes[0] * 1
        i3 = startPoint + 3**missingNodes[0] * 2

        indices = indices + [i1,i2,i3]

        value1 = list(value)
        value1[missingNodes[0]] = 0
        value2 = list(value)
        value2[missingNodes[0]] = 1
        value3 = list(value)
        value3[missingNodes[0]] = 2


        return indices + calculateIndicesRec(value1,missingNodes[1:], indices) +  calculateIndicesRec(value2,missingNodes[1:], indices) + calculateIndicesRec(value3,missingNodes[1:],indices)


# https://www.researchgate.net/figure/221426649_fig1_Fig-1-An-example-of-an-H-coloring-of-G-is-the-mapping-A-a-A-d-A-f-1
# example graph G
# vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# edges = [{'a', 'b'}, {'a', 'g'}, {'b', 'g'}, {'b', 'c'},
#          {'c', 'e'}, {'g', 'e'}, {'g', 'f'}, {'e', 'f'},
#          {'c', 'd'}, {'d', 'e'}]
#
# ecd = TreeDecomposition(None, None, ['e', 'c', 'd'])
# efg = TreeDecomposition(None, None, ['e', 'f', 'g'])
# abg = TreeDecomposition(None, None, ['a', 'b', 'g'])
# ecg = TreeDecomposition(efg, ecd, ['e', 'c', 'g'])
# bcg = TreeDecomposition(abg, ecg, ['b', 'c', 'g'])
# bc = TreeDecomposition(bcg, None, ['b', 'c'])

#order: join, internalstuff, leaf, root, edge bags
# print('------')
# bc = root(bc)
# leaf(bc)
# join(bc)
# addInternalNodes(bc)
# edgeBags(bc,edges)
# print_NiceTree_indented(bc)
# print('------')
#
# #saveTreeDecomposition(bc,edges)
# gv = GraphVisualization(bc)
# gv.createGraph()
# print(containsEdge(['e', 'c', 'g'], ['g','c']))

vertices = ['a','b','c']
edges = [{'a','b'}, {'b','c'}]
k = 3
N = 5
weights = {vertices[i]: rnd.randint(0,N) for i in range(0,len(vertices))}
print(weights)

bc = TreeDecomposition(None,None, ['b', 'c'])
ab = TreeDecomposition(bc,None,['a','b'])

ab = root(ab)
leaf(ab)
join(ab)
addInternalNodes(ab)
edgeBags(ab,edges)
gv = GraphVisualization(ab)
gv.createGraph()

def count(vertices, edges, niceTreeDecomp,terminals,k,N, weights):
    #in-order traversal
    indices = {vertices[i]: i for i in range(0,len(vertices))}
    print(indices)

    data = np.zeros((len(vertices)**3,k,k*N))
    for i in range(0, len(vertices)**3):
        data[i,0,0] = 1    # leaf initialization
    result = inorder(niceTreeDecomp, indices, data,k,N,terminals)

def inorder(node, indices, data, k, N, terminals):
    if(node.getLeft() != None):
        inorder(node.getLeft(),indices, data, k, N, terminals)
    if(node.getRight() != None):
        inorder(node.getRight(),indices, data, k, N, terminals)
    if(node.bagType == BagType.L):
        return
    if(node.bagType == BagType.IV):
        introducedVertex = node.getLabel()

        indexInArray = indices.get(introducedVertex)
        bla = list(indices.values())
        for j in range(0,len(bla)):
            bla[j] = 0

        rest = list(indices.values())
        rest.remove(indexInArray)
        # okay from here we iterate over colorings (x), i (y) and the weights (z)
        # we simply assume that v_1 is the first terminal in the terminals array
        #if new vertex is colored 0
        bla[indexInArray] = 0
        newIndices = calculateIndices(bla,rest)
        for x in newIndices:
            for y in range(0,k):
                for z in range(0,k*N):
                    if(terminals.__contains__(introducedVertex)):
                        data[x,y,z] = 0
        #if new vertex is colored 1
        bla[indexInArray] = 1
        newIndices = calculateIndices(bla,rest)
        for x in newIndices:
            for y in range(0,k):
                for z in range(0,k*N):
                    if(y - 1  >= 0 and y - 1 < k and (z - weights.get(introducedVertex) >= 0) and (z - weights.get(introducedVertex) < k*N)):
                        data[x,y,z] = data[x,y-1,z-weights.get(introducedVertex)]
                    else:
                        data[x,y,z] = 0
        print("indices for coloring new vertex 1: " + str(newIndices))
        #if new vertex is colored 2
        bla[indexInArray] = 2
        newIndices = calculateIndices(bla,rest)
        for x in newIndices:
            for y in range(0,k):
                for z in range(0,k*N):
                    if(terminals[0] != introducedVertex):
                        data[x,y,z] = data[x,y-1,z-weights.get(introducedVertex)]
                    else:
                        data[x,y,z] = 0
        print("indices for coloring new vertex 2: " + str(newIndices))

        return
    return


count(vertices,edges,ab,['a','b'],k,N,weights)






