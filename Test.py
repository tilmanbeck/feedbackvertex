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
vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
edges = [{'a', 'b'}, {'a', 'g'}, {'b', 'g'}, {'b', 'c'},
         {'c', 'e'}, {'g', 'e'}, {'g', 'f'}, {'e', 'f'},
         {'c', 'd'}, {'d', 'e'}]

ecd = TreeDecomposition(None, None, ['e', 'c', 'd'])
efg = TreeDecomposition(None, None, ['e', 'f', 'g'])
abg = TreeDecomposition(None, None, ['a', 'b', 'g'])
ecg = TreeDecomposition(efg, ecd, ['e', 'c', 'g'])
bcg = TreeDecomposition(abg, ecg, ['b', 'c', 'g'])
bc = TreeDecomposition(bcg, None, ['b', 'c'])

#order: join, internalstuff, leaf, root, edge bags
#print('------')
bc = root(bc)
leaf(bc)
join(bc)
addInternalNodes(bc)
edgeBags(bc,edges)
#print_NiceTree_indented(bc)
#print('------')
#
# #saveTreeDecomposition(bc,edges)
gv = GraphVisualization(bc)
gv.createGraph()
# print(containsEdge(['e', 'c', 'g'], ['g','c']))

#vertices = ['a','b','c']
#edges = [{'a','b'}, {'b','c'}]

k = 5
N = 20
weights = {vertices[i]: rnd.randint(0,N) for i in range(0,len(vertices))}
# weights = {'a':1,'b':3,'c':2}
# print(weights)
#
#bc = TreeDecomposition(None,None, ['b', 'c'])
#ab = TreeDecomposition(bc,None,['a','b'])

#ab = root(ab)
#leaf(ab)
#join(ab)
#addInternalNodes(ab)
#edgeBags(ab,edges)
# # v = GraphVisualization(ab)
# # v.createGraph()

def writeToFile(filename,mode,array,fst,stepInfo):
    f = open(filename, mode)
    f.write(stepInfo)
    f.write("\n")
    for i in range(0,fst):
        f.write(str(i))
        f.write("\n")
        f.write(str(array[i]))
        f.write("\n\n")
    f.write("-----------------------------------------------\n")

    # for i in range(0,fst):
    #    for j in range(0,scn):
    #        for k in range(0,thi):
    #            f.write(str(array[i,j,k]))


def count(vertices, edges, niceTreeDecomp,terminals,k,N, weights):
    # in-order traversal
    k = k + 1
    indices = {vertices[i]: i for i in range(0,len(vertices))}
    data = np.zeros((3 ** len(vertices),k,(k-1)*N))
    for i in range(0, len(vertices)**3):
        data[i,0,0] = 1    # leaf initialization
    # we search for a solution with k nodes but the arrays indices start at 0
    result = inorder(niceTreeDecomp, indices, data,k,N,terminals)
    writeToFile('result.txt', 'w', result, 3**7, "result ")
    print(result.shape)
    for j in range(0,(k-1)*N):
        if((result[0,k-1,j] % 2) == 1):
                print("yes there is a solution")
                print(result.shape)


def inorder(node, indices, data, k, N, terminals):
    if(node.getLeft() != None):
        data = inorder(node.getLeft(),indices, data, k, N, terminals)
    if(node.getRight() != None):
        dataright = inorder(node.getRight(),indices, data, k, N, terminals)
    if(node.bagType == BagType.L):
        return data
    if(node.bagType == BagType.R):
        newData = np.zeros((3 ** len(vertices), k, (k - 1) * N))
        forgottenVertex = 'b'

        missingNodes = list(indices.values())
        val = [0 for i in range(0, len(indices))]
        val[indices.get(forgottenVertex)] = 0

        missingNodes.remove(indices.get(forgottenVertex))
        listForForgottenZero = calculateIndices(val, missingNodes)

        val[indices.get(forgottenVertex)] = 1
        listForForgottenOne = calculateIndices(val, missingNodes)

        val[indices.get(forgottenVertex)] = 2
        listForForgottenTwo = calculateIndices(val, missingNodes)

        for x in range(0, len(listForForgottenZero)):
            for y in range(0, k):
                for z in range(0, (k -1) * N):
                    value = data[listForForgottenZero[x], y, z] + data[listForForgottenOne[x], y, z] + data[
                        listForForgottenTwo[x], y, z]
                    newData[listForForgottenZero[x], y, z] = value
                    newData[listForForgottenOne[x], y, z] = value
                    newData[listForForgottenTwo[x], y, z] = value

        # writeToFile('data.txt','a' ,newData,3**3, "after F " +str(forgottenVertex))
        return newData
    if(node.bagType == BagType.IE):
        newData = np.zeros((3 ** len(vertices),k,(k-1)*N))
        firstVertex = node.getLabel().pop()
        scndVertex = node.getLabel().pop()
        # create list for all indices
        listOfAllIndices = [i for i in range(0,len(indices.values())**3)]

        indicesToBeRemoved = getIndicesForIntroduceEdge(indices, firstVertex, scndVertex)

        # remove the indices where one of the two vertices is either 1 or 2 from the
        # list of all indices
        clearedIndices = [x for x in listOfAllIndices if x not in indicesToBeRemoved]
        for x in clearedIndices:
            for y in range(0,k):
                for z in range(0,(k-1)*N):
                    newData[x,y,z] = data[x,y,z]
        for x in indicesToBeRemoved:
            for y in range(0,k):
                for z in range(0,(k-1)*N):
                    newData[x,y,z] = 0
        # writeToFile('data.txt','a',newData,3**3, "after IE " + label)
        return newData
    if(node.bagType == BagType.IV):
        newData = np.zeros((3 ** len(vertices),k,(k-1)*N))
        introducedVertex = node.getLabel()
        indexInArray = indices.get(introducedVertex)
        bla = list(indices.values())
        for j in range(0,len(bla)):
            bla[j] = 0

        rest = list(indices.values())
        rest.remove(indexInArray)
        # okay from here we iterate over colorings (x), i (y) and the weights (z)
        # we simply assume that v_1 is the first terminal in the terminals array
        # if new vertex is colored 0
        bla[indexInArray] = 0
        newIndices = calculateIndices(bla,rest)
        for x in newIndices:
            for y in range(0,k):
                for z in range(0,(k-1)*N):
                    if not(terminals.__contains__(introducedVertex)):
                        newData[x,y,z] = data[x,y,z]
                    else:
                        newData[x,y,z] = 0

        # if new vertex is colored 1
        bla[indexInArray] = 1
        newIndices = calculateIndices(bla,rest)
        for x in newIndices:
            for y in range(0,k):
                for z in range(0,(k-1)*N):
                    if(y - 1  >= 0 and y - 1 < k and (z - weights.get(introducedVertex) >= 0) and (z - weights.get(introducedVertex) < (k-1)*N)):
                        newData[x, y, z] = data[x, y-1, z-weights.get(introducedVertex)]
                    else:
                        newData[x, y, z] = 0

        # if new vertex is colored 2
        bla[indexInArray] = 2
        newIndices = calculateIndices(bla,rest)
        for x in newIndices:
            for y in range(0,k):
                for z in range(0,(k-1)*N):
                    if(terminals[0] != introducedVertex):
                        if (y - 1 >= 0 and y - 1 < k and (z - weights.get(introducedVertex) >= 0) and (z - weights.get(introducedVertex) < (k-1)*N)):
                            newData[x,y,z] = data[x,y-1,z-weights.get(introducedVertex)]
                        else:
                            newData[x,y,z] = 0

        # writeToFile('data.txt','a',newData,3**3, "after IV " +str(introducedVertex))
        return newData
    if(node.bagType == BagType.F):
        newData = np.zeros((3 ** len(vertices), k, (k-1)*N))
        forgottenVertex = node.getLabel()

        missingNodes = list(indices.values())
        val = [0 for i in range(0, len(indices))]
        val[indices.get(forgottenVertex)] = 0

        missingNodes.remove(indices.get(forgottenVertex))
        listForForgottenZero = calculateIndices(val,missingNodes)

        val[indices.get(forgottenVertex)] = 1
        listForForgottenOne = calculateIndices(val, missingNodes)

        val[indices.get(forgottenVertex)] = 2
        listForForgottenTwo = calculateIndices(val, missingNodes)

        for x in range(0,len(listForForgottenZero)):
            for y in range(0,k):
                for z in range(0, (k-1)*N):
                    value = data[listForForgottenZero[x], y, z] + data[listForForgottenOne[x], y, z] + data[listForForgottenTwo[x], y, z]
                    newData[listForForgottenZero[x], y, z] = value
                    newData[listForForgottenOne[x], y, z] = value
                    newData[listForForgottenTwo[x], y, z] = value

        # writeToFile('data.txt','a' ,newData,3**3, "after F " +str(forgottenVertex))
        return newData
    if(node.bagType == BagType.J):
        newData = np.zeros((3 ** len(vertices), k, (k-1)*N))

        for x in range in indices:
            for y in range(0, k):
                for z in range(0, (k - 1) * N):
                    value = 0
                    accumulationBound1 = 1
                    accumulationBound2 = 2
                    for i1 in range(0, accumulationBound1):
                        for w1 in range(0, accumulationBound2):
                            i2 = accumulationBound1 - i1
                            w2 = accumulationBound2 - w1
                            value += (data[x, i1, w1] * dataright[x, i2, w2])
                newData[x,y,z] = value
        return newData

    return data

def getIndicesForIntroduceEdge(indices, firstVertex, scndVertex):
    val = [0 for i in range(0, len(indices))]
    # what are we doing here? we need all indices except those where one of the edges is colored 1 and the other one 2
    # and vice versa. so we take all indices and remove mentioned from all indices

    val[indices.get(firstVertex)] = 1
    val[indices.get(scndVertex)] = 2
    keys = list(indices.keys())
    keys.remove(firstVertex)
    keys.remove(scndVertex)
    missingNodes = []
    for key in keys:
        missingNodes.append(indices.get(key))
    first = calculateIndices(val, missingNodes)

    val[indices.get(firstVertex)] = 2
    val[indices.get(scndVertex)] = 1
    keys = list(indices.keys())
    keys.remove(firstVertex)
    keys.remove(scndVertex)
    missingNodes = []
    for key in keys:
        missingNodes.append(indices. get(key))
    scnd = calculateIndices(val, missingNodes)

    return first+scnd


count(vertices, edges, bc, ['c', 'b', 'e'], k, N, weights)
# count(vertices, edges, ab, ['a', 'b'], k, N, weights)
