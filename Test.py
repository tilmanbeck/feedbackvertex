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
import math

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


def count(vertices, edges, niceTreeDecomp, terminals, k, N, weights):
    # in-order traversal
    k = k + 1
    indices = {vertices[i]: i for i in range(0,len(vertices))}
    print(str(weights))
    result = inorder(niceTreeDecomp, indices, None, k, N, terminals)
    # we search for a solution with k nodes but the arrays indices start at 0
    sol = 0
    print("is there a solution?")
    for j in range(0,(k-1)*N):
        if((result[0,k-1,j] % 2) == 1):
                print("yes there is a solution")
                sol += 1
    if(sol == 0):
        print("sadly not...")

def inorder(node, indices, data, k, N, terminals):
    if(node.getLeft() != None):
        data = inorder(node.getLeft(),indices, data, k, N, terminals)
    if(node.getRight() != None):
        dataright = inorder(node.getRight(),indices, data, k, N, terminals)
    if(node.bagType == BagType.L):
        newData = np.zeros((1, k, (k-1) * N))
        newData[0,0,0] = 1    # leaf initialization
        writeToFile('test.txt', 'w', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
        return newData
    if(node.bagType == BagType.R):

        newData = np.zeros((1, k, (k - 1) * N))
        for i in range(0, k):
            for w in range(0, (k -1) * N):
                newData[0, i, w] = data[0, i, w] + data[1, i, w] + data[2,  i, w]
        writeToFile('test.txt', 'a', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
        return newData

        #newData = np.zeros((3 ** len(vertices), k, (k - 1) * N))
        # forgottenVertex = node.getLabel()
        #
        # missingNodes = list(indices.values())
        # val = [0 for i in range(0, len(indices))]
        # val[indices.get(forgottenVertex)] = 0
        #
        # missingNodes.remove(indices.get(forgottenVertex))
        # listForForgottenZero = calculateIndices(val, missingNodes)
        #
        # val[indices.get(forgottenVertex)] = 1
        # listForForgottenOne = calculateIndices(val, missingNodes)
        #
        # val[indices.get(forgottenVertex)] = 2
        # listForForgottenTwo = calculateIndices(val, missingNodes)
        #
        # for x in range(0, len(listForForgottenZero)):
        #     for y in range(0, k):
        #         for z in range(0, (k -1) * N):
        #             value = data[listForForgottenZero[x], y, z] + data[listForForgottenOne[x], y, z] + data[
        #                 listForForgottenTwo[x], y, z]
        #             newData[listForForgottenZero[x], y, z] = value
        #             newData[listForForgottenOne[x], y, z] = value
        #             newData[listForForgottenTwo[x], y, z] = value
        #
        # # writeToFile('data.txt','a' ,newData,3**3, "after F " +str(forgottenVertex))
        # return newData
    if(node.bagType == BagType.IE):

        matSize = 3 ** len(node.getBag())
        newData = np.zeros((matSize, k, (k-1)*N))
        firstVertex = node.getLabel().pop()
        scndVertex = node.getLabel().pop()
        posFirstVertex = node.getBag().index(firstVertex)
        posScndVertex = node.getBag().index(scndVertex)
        for s in range(0, matSize):
            coloringFromIndex = getIndexAsList(s, len(node.getBag()))
            firstCol = coloringFromIndex[posFirstVertex]
            scndCol = coloringFromIndex[posScndVertex]
            if(firstCol == 0 or scndCol == 0 or firstCol == scndCol):
                for i in range(0, k):
                    for w in range(0, (k - 1) * N):
                        newData[s, i, w] = data[s, i, w]
        writeToFile('test.txt', 'a', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
        return newData

        # newData = np.zeros((3 ** len(vertices),k,(k-1)*N))
        # firstVertex = node.getLabel().pop()
        # scndVertex = node.getLabel().pop()
        # # create list for all indices
        # listOfAllIndices = [i for i in range(0,len(indices.values())**3)]
        #
        # indicesToBeRemoved = getIndicesForIntroduceEdge(indices, firstVertex, scndVertex)
        #
        # # remove the indices where one of the two vertices is either 1 or 2 from the
        # # list of all indices
        # clearedIndices = [x for x in listOfAllIndices if x not in indicesToBeRemoved]
        # for x in clearedIndices:
        #     for y in range(0,k):
        #         for z in range(0,(k-1)*N):
        #             newData[x,y,z] = data[x,y,z]
        # for x in indicesToBeRemoved:
        #     for y in range(0,k):
        #         for z in range(0,(k-1)*N):
        #             newData[x,y,z] = 0
        # # writeToFile('data.txt','a',newData,3**3, "after IE " + label)
    if(node.bagType == BagType.IV):

        #create new data matrix (one dimension bigger than child)
        newData = np.zeros((3 ** len(node.getBag()), k, (k - 1) * N))
        introducedVertex = node.getLabel()
        childBag = node.getLeft().getBag()
        positionOfIV = node.getBag().index(introducedVertex)
        # we have to iterate over all colorings from child bag
        lengthOfChildColorings = 3 ** len(childBag)

        # okay from here we iterate over colorings (x), i (y) and the weights (z)
        # we simply assume that v_1 is the first terminal in the terminals array
        # if new vertex is colored 0
        for s in range(0, lengthOfChildColorings):
            coloringFromIndex = getIndexAsList(s, len(childBag))
            # this is the special if the child bag is a leaf
            # and there is no coloring
            if(node.getLeft().getBagType() == BagType.L):
                extendedColoring = [positionOfIV]
            else:
                extendedColoring = coloringFromIndex[0:positionOfIV] + [0] + coloringFromIndex[positionOfIV:]

            # need to sort as calculateIndices doesn't do it
            indices = sorted(calculateIndices(extendedColoring, [positionOfIV]))
            for i in range(0, k):
                for w in range(0, (k - 1) * N):
                    # write the three new matrices according to the rules from the paper
                    if not (terminals.__contains__(introducedVertex)):
                        newData[indices[0], i, w] = data[s, i, w]

                    if (i - 1 >= 0 and i - 1 < k and (w - weights.get(introducedVertex) >= 0) and (
                                    w - weights.get(introducedVertex) < (k - 1) * N)):
                        newData[indices[1], i, w] = data[s, i - 1, w - weights.get(introducedVertex)]
                    else:
                        newData[indices[1], i, w] = 0

                    if (terminals[0] != introducedVertex and i - 1 >= 0 and i - 1 < k and (
                            w - weights.get(introducedVertex) >= 0)):
                        newData[indices[2], i, w] = data[s, i - 1, w - weights.get(introducedVertex)]
                    else:
                        newData[indices[2], i, w] = 0
        writeToFile('test.txt', 'a', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
        return newData
        # newData = np.zeros((3 ** len(vertices),k,(k-1)*N))
        # introducedVertex = node.getLabel()
        # indexInArray = indices.get(introducedVertex)
        # bla = list(indices.values())
        # for j in range(0,len(bla)):
        #     bla[j] = 0
        #
        # rest = list(indices.values())
        # rest.remove(indexInArray)
        # okay from here we iterate over colorings (x), i (y) and the weights (z)
        # we simply assume that v_1 is the first terminal in the terminals array
        # if new vertex is colored 0
        # bla[indexInArray] = 0
        # newIndices = calculateIndices(bla,rest)
        # for x in newIndices:
        #     for y in range(0,k):
        #         for z in range(0,(k-1)*N):
        #             if not(terminals.__contains__(introducedVertex)):
        #                 newData[x,y,z] = data[x,y,z]
        #             else:
        #                 newData[x,y,z] = 0
        #
        # # if new vertex is colored 1
        # bla[indexInArray] = 1
        # newIndices = calculateIndices(bla,rest)
        # for x in newIndices:
        #     for y in range(0,k):
        #         for z in range(0,(k-1)*N):
        #             if(y - 1  >= 0 and y - 1 < k and (z - weights.get(introducedVertex) >= 0) and (z - weights.get(introducedVertex) < (k-1)*N)):
        #                 newData[x, y, z] = data[x, y-1, z-weights.get(introducedVertex)]
        #             else:
        #                 newData[x, y, z] = 0
        #
        # # if new vertex is colored 2
        # bla[indexInArray] = 2
        # newIndices = calculateIndices(bla,rest)
        # for x in newIndices:
        #     for y in range(0,k):
        #         for z in range(0,(k-1)*N):
        #             if(terminals[0] != introducedVertex):
        #                 if (y - 1 >= 0 and y - 1 < k and (z - weights.get(introducedVertex) >= 0) and (z - weights.get(introducedVertex) < (k-1)*N)):
        #                     newData[x,y,z] = data[x,y-1,z-weights.get(introducedVertex)]
        #                 else:
        #                     newData[x,y,z] = 0
        #
        # # writeToFile('data.txt','a',newData,3**3, "after IV " +str(introducedVertex))
        # return newData

    ##### XXXXXXXXXXXXXXXXXXXXXXXXXXX
    if(node.bagType == BagType.F):

        # create new matrix with size of bag (one dimension less than child)
        tmp = 3 ** len(node.getBag())
        newData = np.zeros((tmp, k, (k - 1) * N))

        # which position did forgotten vertex take in child bag
        fgtVertex = node.getLabel()
        childBag = node.getLeft().getBag()
        oldPos = childBag.index(fgtVertex)

        for s in range(0, tmp):
            for i in range(0, k):
                for w in range(0, (k - 1) * N):
                    # get the int value of current coloring as list of ternary values
                    coloring = getIndexAsList(s, len(node.getBag()))
                    # add new position for forgotten bag (init as zero because calculateIndices requests that)
                    coloring = coloring[0:oldPos] + [0] + coloring[oldPos:]
                    # calculate the three indices to access in child data matrix
                    indicesToSum = calculateIndices(coloring, [oldPos])
                    # add the three matrices and write back to new matrix
                    newData[s, i, w] = data[indicesToSum[0], i, w] +\
                                       data[indicesToSum[1], i, w] +\
                                       data[indicesToSum[2], i, w]
        writeToFile('test.txt', 'a', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
        return newData

    ##### XXXXXXXXXXXXXXXXXXXXXXXXXXX



    # if(node.bagType == BagType.F):
    #     newData = np.zeros((3 ** len(vertices), k, (k-1)*N))
    #     forgottenVertex = node.getLabel()
    #
    #     missingNodes = list(indices.values())
    #     val = [0 for i in range(0, len(indices))]
    #     val[indices.get(forgottenVertex)] = 0
    #
    #     missingNodes.remove(indices.get(forgottenVertex))
    #     listForForgottenZero = calculateIndices(val,missingNodes)
    #
    #     val[indices.get(forgottenVertex)] = 1
    #     listForForgottenOne = calculateIndices(val, missingNodes)
    #
    #     val[indices.get(forgottenVertex)] = 2
    #     listForForgottenTwo = calculateIndices(val, missingNodes)
    #
    #     for x in range(0,len(listForForgottenZero)):
    #         for y in range(0,k):
    #             for z in range(0, (k-1)*N):
    #                 value = data[listForForgottenZero[x], y, z] + data[listForForgottenOne[x], y, z] + data[listForForgottenTwo[x], y, z]
    #                 newData[listForForgottenZero[x], y, z] = value
    #                 newData[listForForgottenOne[x], y, z] = value
    #                 newData[listForForgottenTwo[x], y, z] = value
    #
    #     # writeToFile('data.txt','a' ,newData,3**3, "after F " +str(forgottenVertex))
    #     return newData
    #

    if(node.bagType == BagType.J):
        bagSize = len(node.getBag())
        matSize = 3 ** bagSize
        newData = np.zeros((matSize, k, (k-1)*N))
        colorings = calculateIndices([0 for i in range(0,bagSize)], [i for i in range(0,bagSize)])
        for s in colorings:
            for i in range(0, k):
                for w in range(0, (k - 1) * N):
                    value = 0
                    # we use the these bounds to limit the iterations of the loops
                    # searching for the right i1 and i2 resp. w1 and w2
                    # we know i1+i2 = y + #(nodes with coloring 1 or 2)
                    # and w1+w2 = z + sum of the weights of the nodes with coloring 1 or 2
                    # accumulationBound1 refers to the bound in the paper for the 'i' index
                    # resp. accumulationBound2 to the bound in the paper for 'w' index
                    indexAsNodeList = getIndexAsList(s, bagSize)
                    coloredNodes = getNodesByColoring(indexAsNodeList, [1,2], indices)
                    accumulationBound1 = i + len(coloredNodes)
                    accumulationBound2 = w + getSumOfWeights(coloredNodes, weights)
                    for i1 in range(0, accumulationBound1):
                        for w1 in range(0, accumulationBound2):
                            i2 = accumulationBound1 - i1
                            w2 = accumulationBound2 - w1
                            if(w1 >= ((k-1)*N) or w2 >= ((k-1)*N) or i1 >= k or i2 >= k):
                                value += 0
                            else:
                                value += (data[s, i1, w1] * dataright[s, i2, w2])
                    newData[s, i, w] = value
        writeToFile('test.txt', 'a', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
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


#indicesKV = key-value dict where the keys are
# the nodes (e.g. 'a') and the value is the
# index in the index-array according to order
def getNodesByColoring(nodes, coloring, indicesKV):
    tmp = [i for i in range(0,len(nodes)) if nodes[i] in coloring]
    return [key for key,val in indicesKV.items() if val in tmp]

def getSumOfWeights(nodes, weights):
    res = 0
    for i in range(0,len(nodes)):
        res += weights.get(nodes[i])
    return res

def getIndexAsList(x,nrOfVertices):
    if nrOfVertices == 0:
        return [0]
    number = x
    res = []
    for i in range(nrOfVertices-1, -1, -1):
        value = math.floor(number/(3**i))
        number -= (value * 3**i)
        res.append(value)

    return res

# https://www.researchgate.net/figure/221426649_fig1_Fig-1-An-example-of-an-H-coloring-of-G-is-the-mapping-A-a-A-d-A-f-1
# example graph G

#############################################################
######################### BIG EXAMPLE #######################
#############################################################
k = 3
N = 20
vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
edges = [{'a', 'b'}, {'a', 'g'}, {'b', 'g'}, {'b', 'c'},
         {'c', 'e'}, {'g', 'e'}, {'g', 'f'}, {'e', 'f'},
         {'c', 'd'}, {'d', 'e'}]
weights = {vertices[i]: rnd.randint(0,N) for i in range(0,len(vertices))}

ecd = TreeDecomposition(None, None, ['e', 'c', 'd'])
efg = TreeDecomposition(None, None, ['e', 'f', 'g'])
abg = TreeDecomposition(None, None, ['a', 'b', 'g'])
ecg = TreeDecomposition(efg, ecd, ['e', 'c', 'g'])
bcg = TreeDecomposition(abg, ecg, ['b', 'c', 'g'])
bc = TreeDecomposition(bcg, None, ['b', 'c'])

bc = root(bc)
leaf(bc)
join(bc)
addInternalNodes(bc)
edgeBags(bc, edges)

gv = GraphVisualization(bc)
gv.createGraph()

count(vertices, edges, bc, ['c', 'b', 'e'], k, N, weights)

#############################################################
######################### SMALL EXAMPLE #####################
#############################################################
# vertices = ['a','b','c']
# edges = [{'a','c'}, {'b','c'}]
#
# k = 3
# N = 5
# #weights = {vertices[i]: rnd.randint(1,N) for i in range(0,len(vertices))}
# weights = {'a': 1, 'c': 1, 'b': 1}
# bc = TreeDecomposition(None, None, ['b', 'c'])
# ab = TreeDecomposition(bc, None, ['a', 'c'])
#
# ab = root(ab)
# leaf(ab)
# join(ab)
# addInternalNodes(ab)
# edgeBags(ab,edges)
# v = GraphVisualization(ab)
# v.createGraph()
#
# count(vertices, edges, ab, ['a', 'b'], k, N, weights)



