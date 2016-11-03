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
import time

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
    with open(filename, mode) as f:
        f.write(stepInfo)
        f.write("\n")
        for i in range(0, fst):
            f.write(str(i))
            f.write("\n")
            f.write(str(array[i]))
            f.write("\n\n")
        f.write("-----------------------------------------------\n")

def count(vertices, edges, niceTreeDecomp, terminals, k, N, weights):
    #startTime = time.time()
    # in-order traversal
    empty = np.zeros((1,1))
    #writeToFile('test.txt', 'w', empty, empty.shape[0], "")
    k = k + 1
    indices = {vertices[i]: i for i in range(0,len(vertices))}
    #print(str(weights))
    result = inorder(niceTreeDecomp, indices, None, k, N, terminals)
    # we search for a solution with k nodes but the arrays indices start at 0
    sol = 0
    #print("is there a solution?")
    for j in range(0,(k-1)*N):
        if((result[0,k-1,j] % 2) == 1):
                #print("yes there is a solution")
                sol += 1
    if(sol == 0):
        sol = 0
        #print("sadly not...")
    #endTime = time.time()
    #print("Executiontime: " + str(endTime-startTime)+"s")

def inorder(node, indices, data, k, N, terminals):
    if(node.getLeft() != None):
        data = inorder(node.getLeft(),indices, data, k, N, terminals)
    if(node.getRight() != None):
        dataright = inorder(node.getRight(),indices, data, k, N, terminals)
    if(node.bagType == BagType.L):
        newData = np.zeros((1, k, (k-1) * N))
        newData[0,0,0] = 1    # leaf initialization
        #writeToFile('test.txt', 'a', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
        return newData
    elif(node.bagType == BagType.R):

        newData = np.zeros((1, k, (k - 1) * N))
        for i in range(0, k):
            for w in range(0, (k -1) * N):
                newData[0, i, w] = data[0, i, w] + data[1, i, w] + data[2,  i, w]
        #writeToFile('test.txt', 'a', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
        return newData

    elif(node.bagType == BagType.IE):

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
        #writeToFile('test.txt', 'a', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
        return newData

    elif(node.bagType == BagType.IV):

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
        #writeToFile('test.txt', 'a', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
        return newData

    elif(node.bagType == BagType.F):

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
        #writeToFile('test.txt', 'a', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
        return newData

    elif(node.bagType == BagType.J):
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
        #writeToFile('test.txt', 'a', newData, newData.shape[0], str(node.bagType) + str(node.getBag()))
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
# k = 3
# vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# N = 2 * len(vertices)
# edges = [{'a', 'b'}, {'a', 'g'}, {'b', 'g'}, {'b', 'c'},
#          {'c', 'e'}, {'g', 'e'}, {'g', 'f'}, {'e', 'f'},
#          {'c', 'd'}, {'d', 'e'}]
# weights = {vertices[i]: rnd.randint(1, N) for i in range(0, len(vertices))}
#
# ecd = TreeDecomposition(None, None, ['e', 'c', 'd'])
# efg = TreeDecomposition(None, None, ['e', 'f', 'g'])
# abg = TreeDecomposition(None, None, ['a', 'b', 'g'])
# ecg = TreeDecomposition(efg, ecd, ['e', 'c', 'g'])
# bcg = TreeDecomposition(abg, ecg, ['b', 'c', 'g'])
# bc = TreeDecomposition(bcg, None, ['b', 'c'])
#
# bc = root(bc)
# leaf(bc)
# join(bc)
# addInternalNodes(bc)
# edgeBags(bc, edges)

# gv = GraphVisualization(bc)
# gv.createGraph()

# count(vertices, edges, bc, ['d','c','e'], k, N, weights)


#############################################################
######################### SMALL EXAMPLE #####################
#############################################################
# vertices = ['a','b','c']
# edges = [{'a','b'}, {'b','c'}]
#
# k = 2
# N = 5
# weights = {vertices[i]: rnd.randint(1,N) for i in range(0,len(vertices))}
# bc = TreeDecomposition(None, None, ['b', 'c'])
# ab = TreeDecomposition(bc, None, ['a', 'b'])
#
# ab = root(ab)
# leaf(ab)
# join(ab)
# addInternalNodes(ab)
# edgeBags(ab,edges)
# v = GraphVisualization(ab)
# v.createGraph()
#
# count(vertices, edges, ab, ['a', 'c'], k, N, weights)
#


#############################################################
######################### LARGE EXAMPLE #####################
#############################################################
# http://treedecompositions.com/#/graph/Js%60RA%3Flh%3Fu%3F

vertices = ['a','b','c','d','e','f','g','h','i','j','k']

edges = [{'a','b'},{'a','c'},{'a','d'},{'a','e'},{'a','j'},{'b','f'},
         {'b','g'},{'b','h'},{'c','i'},{'c','g'},{'c','h'},{'d','f'},
         {'d','k'},{'e','i'},{'e','k'},{'f','i'},{'f','j'},{'g','k'},
         {'h','i'},{'h','k'}]

k = 4
N = 2 * len(vertices)


weights = {vertices[i]: rnd.randint(1, N) for i in range(0, len(vertices))}

a1      = TreeDecomposition(None, None, ['a'])
b2      = TreeDecomposition(None, None, ['b'])

aj1     = TreeDecomposition(a1, None, ['a','j'])
bk2     = TreeDecomposition(b2, None, ['b','k'])
a3      = TreeDecomposition(None, None, ['a'])

afj1    = TreeDecomposition(aj1, None, ['a','f','j'])
bik2    = TreeDecomposition(bk2, None, ['b','i','k'])
ak3     = TreeDecomposition(a3, None, ['a','k'])
a4      = TreeDecomposition(None, None, ['a'])

acfj1   = TreeDecomposition(afj1, None, ['a','c','f','j'])
bhik2   = TreeDecomposition(bik2, None, ['b','h','i','k'])
afk3    = TreeDecomposition(ak3, None, ['a','f','k'])
ak4     = TreeDecomposition(a4, None, ['a','k'])

acf1    = TreeDecomposition(acfj1, None, ['a','c','f'])
bik21   = TreeDecomposition(bhik2, None, ['b','i','k'])
adfk3   = TreeDecomposition(afk3, None, ['a','d','f','k'])
aik4    = TreeDecomposition(ak4, None, ['a','i','k'])

acfk1   = TreeDecomposition(acf1, None, ['a','c','f','k'])
bfik2   = TreeDecomposition(bik21, None, ['b','f','i','k'])
afk31   = TreeDecomposition(adfk3, None, ['a','f','k'])
aeik4   = TreeDecomposition(aik4, None, ['a','e','i','k'])

acfik1  = TreeDecomposition(acfk1, None, ['a','c','f','i','k'])
bcfik2  = TreeDecomposition(bfik2, None, ['b','c','f','i','k'])
afik3   = TreeDecomposition(afk31, None, ['a','f','i','k'])
aik41   = TreeDecomposition(aeik4, None, ['a','i','k'])

abcfik1 = TreeDecomposition(acfik1, None, ['a','b','c','f','i','k'])
abcfik2 = TreeDecomposition(bcfik2, None, ['a','b','c','f','i','k'])
acfik3  = TreeDecomposition(afik3, None, ['a','c','f','i','k'])
afik4   = TreeDecomposition(aik41, None, ['a','f','i','k'])

abcfik11 = TreeDecomposition(abcfik1, abcfik2, ['a','b','c','f','i','k'])
abcfik21 = TreeDecomposition(acfik3, None, ['a','b','c','f','i','k'])
acfik31  = TreeDecomposition(afik4, None, ['a','c','f','i','k'])

abcfik12 = TreeDecomposition(abcfik11, abcfik21, ['a','b','c','f','i','k'])
abcfik22 = TreeDecomposition(acfik31, None, ['a','b','c','f','i','k'])

abcfik13 = TreeDecomposition(abcfik12, abcfik22, ['a','b','c','f','i','k'])

abcfk1   = TreeDecomposition(abcfik13, None, ['a','b','c','f','k'])

abcfgk1  = TreeDecomposition(abcfk1, None, ['a','b','c','f','g','k'])

abcgk1   = TreeDecomposition(abcfgk1, None, ['a','b','c','g','k'])

bcgk1    = TreeDecomposition(abcgk1, None, ['b','c','g','k'])

bcg1     = TreeDecomposition(bcgk1, None, ['b','c','g'])

bc1      = TreeDecomposition(bcg1, None, ['b','c'])

b1       = TreeDecomposition(bc1, None, ['b'])

b1 = root(b1)
leaf(b1)
join(b1)
addInternalNodes(b1)
edgeBags(b1, edges)

gv = GraphVisualization(b1)
gv.createGraph()

runs = 1
t = [0]*runs
for i in range(0,runs):

    s = time.time()
    count(vertices, edges, b1, ['a','d','f','k'], k, N, weights)
    e = time.time()
    t[i] = (e-s)

avg = 0
for i in range(0,runs):
    avg = avg + t[i]

avg = avg/runs

print("Execution Time: "+ str(avg)+"s")










