import math as m

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
        value = m.floor(number/(3**i))
        number -= (value * 3**i)
        res.append(value)

    return res

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