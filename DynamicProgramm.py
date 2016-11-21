from BagType import BagType

import utils as ut
import numpy as np

outputFile = './output/test.txt'

def count(vertices, edges, niceTreeDecomp, terminals, k, N, weights):
    #startTime = time.time()
    # in-order traversal
    empty = np.zeros((1,1))
    k += 1
    indices = {vertices[i]: i for i in range(0,len(vertices))}
    result = inorder(niceTreeDecomp, indices, None, k, N, terminals, weights)
    # we search for a solution with k nodes but the arrays indices start at 0
    sol = 0
    #print("solution of size " +str(k-1) + "?")
    for j in range(0,(k-1)*N):
        if(result[0,k-1,j] % 2) == 1:
                print("Yes")
                sol += 1
    if sol == 0:
        print("No")
    #endTime = time.time()
    #print("Executiontime: " + str(endTime-startTime)+"s")


def inorder(node, indices, data, k, N, terminals, weights):
    if node.getLeft() is not None:
        data = inorder(node.getLeft(), indices, data, k, N, terminals, weights)
    if node.getRight() is not None:
        data_right = inorder(node.getRight(), indices, data, k, N, terminals, weights)
    if node.bagType == BagType.L:
        new_data = np.zeros((1, k, (k-1) * N))
        new_data[0,0,0] = 1    # leaf initialization
        #ut.writeToFile(outputFile, 'a', new_data, new_data.shape[0], str(node.bagType) + str(node.getBag()))
        return new_data
    elif node.bagType == BagType.R:

        new_data = np.zeros((1, k, (k - 1) * N))
        for i in range(0, k):
            for w in range(0, (k -1) * N):
                new_data[0, i, w] = data[0, i, w] + data[1, i, w] + data[2,  i, w]
        #ut.writeToFile(outputFile, 'a', new_data, new_data.shape[0], str(node.bagType) + str(node.getBag()))
        return new_data

    elif node.bagType == BagType.IE:

        mat_size = 3 ** len(node.getBag())
        new_data = np.zeros((mat_size, k, (k-1)*N))
        first_vertex = node.getLabel().pop()
        scnd_vertex = node.getLabel().pop()
        pos_first_vertex = node.getBag().index(first_vertex)
        pos_scnd_vertex = node.getBag().index(scnd_vertex)
        for s in range(0, mat_size):
            coloring_from_index = ut.getIndexAsList(s, len(node.getBag()))
            first_col = coloring_from_index[pos_first_vertex]
            scnd_col = coloring_from_index[pos_scnd_vertex]
            if first_col == 0 or scnd_col == 0 or first_col == scnd_col:
                for i in range(0, k):
                    for w in range(0, (k - 1) * N):
                        new_data[s, i, w] = data[s, i, w]
        #ut.writeToFile(outputFile, 'a', new_data, new_data.shape[0], str(node.bagType) + str(node.getBag()))
        return new_data

    elif(node.bagType == BagType.IV):

        #create new data matrix (one dimension bigger than child)
        new_data = np.zeros((3 ** len(node.getBag()), k, (k - 1) * N))
        introduced_vertex = node.getLabel()
        child_bag = node.getLeft().getBag()
        pos_iv = node.getBag().index(introduced_vertex)
        # we have to iterate over all colorings from child bag
        length_child_colors = 3 ** len(child_bag)

        # okay from here we iterate over colorings (x), i (y) and the weights (z)
        # we simply assume that v_1 is the first terminal in the terminals array
        # if new vertex is colored 0
        for s in range(0, length_child_colors):
            coloring_from_index = ut.getIndexAsList(s, len(child_bag))
            # this is the special if the child bag is a leaf
            # and there is no coloring
            if node.getLeft().getBagType() == BagType.L:
                ext_coloring = [pos_iv]
            else:
                ext_coloring = coloring_from_index[0:pos_iv] + [0] + coloring_from_index[pos_iv:]

            # need to sort as calculateIndices doesn't do it
            indices = sorted(ut.calculateIndices(ext_coloring, [pos_iv]))
            for i in range(0, k):
                for w in range(0, (k - 1) * N):
                    # write the three new matrices according to the rules from the paper
                    if not (terminals.__contains__(introduced_vertex)):
                        new_data[indices[0], i, w] = data[s, i, w]

                    if 0 <= i - 1 < k and (w - weights.get(introduced_vertex) >= 0) and (
                                    w - weights.get(introduced_vertex) < (k - 1) * N):
                        new_data[indices[1], i, w] = data[s, i - 1, w - weights.get(introduced_vertex)]
                    else:
                        new_data[indices[1], i, w] = 0

                    if (terminals[0] != introduced_vertex and (0 <= i - 1 < k) and 
                            w - weights.get(introduced_vertex) >= 0):
                        new_data[indices[2], i, w] = data[s, i - 1, w - weights.get(introduced_vertex)]
                    else:
                        new_data[indices[2], i, w] = 0
        #ut.writeToFile(outputFile, 'a', new_data, new_data.shape[0], str(node.bagType) + str(node.getBag()))
        return new_data

    elif node.bagType == BagType.F:

        # create new matrix with size of bag (one dimension less than child)
        tmp = 3 ** len(node.getBag())
        new_data = np.zeros((tmp, k, (k - 1) * N))

        # which position did forgotten vertex take in child bag
        fgt_vertex = node.getLabel()
        child_bag = node.getLeft().getBag()
        old_pos = child_bag.index(fgt_vertex)

        for s in range(0, tmp):
            for i in range(0, k):
                for w in range(0, (k - 1) * N):
                    # get the int value of current coloring as list of ternary values
                    coloring = ut.getIndexAsList(s, len(node.getBag()))
                    # add new position for forgotten bag (init as zero because calculateIndices requests that)
                    coloring = coloring[0:old_pos] + [0] + coloring[old_pos:]
                    # calculate the three indices to access in child data matrix
                    indices_to_sum = ut.calculateIndices(coloring, [old_pos])
                    # add the three matrices and write back to new matrix
                    new_data[s, i, w] = data[indices_to_sum[0], i, w] + data[indices_to_sum[1], i, w] +\
                                       data[indices_to_sum[2], i, w]
        ut.writeToFile(outputFile, 'a', new_data, new_data.shape[0], str(node.bagType) + str(node.getBag()))
        return new_data

    elif node.bagType == BagType.J:
        bag_size = len(node.getBag())
        mat_size = 3 ** bag_size
        new_data = np.zeros((mat_size, k, (k-1)*N))
        colorings = ut.calculateIndices([0 for i in range(0, bag_size)], [i for i in range(0, bag_size)])
        for s in colorings:
            for i in range(0, k):
                for w in range(0, (k - 1) * N):
                    value = 0
                    # we use the these bounds to limit the iterations of the loops
                    # searching for the right i1 and i2 resp. w1 and w2
                    # we know i1+i2 = y + #(nodes with coloring 1 or 2)
                    # and w1+w2 = z + sum of the weights of the nodes with coloring 1 or 2
                    # acc_bound_1 refers to the bound in the paper for the 'i' index
                    # resp. acc_bound_2 to the bound in the paper for 'w' index
                    index_node_as_list = ut.getIndexAsList(s, bag_size)
                    colored_nodes = ut.getNodesByColoring(index_node_as_list, [1,2], indices)
                    acc_bound_1 = i + len(colored_nodes)
                    acc_bound_2 = w + ut.getSumOfWeights(colored_nodes, weights)
                    for i1 in range(0, acc_bound_1):
                        for w1 in range(0, acc_bound_2):
                            i2 = acc_bound_1 - i1
                            w2 = acc_bound_2 - w1
                            if w1 >= ((k-1)*N) or w2 >= ((k-1)*N) or i1 >= k or i2 >= k:
                                value += 0
                            else:
                                value += (data[s, i1, w1] * data_right[s, i2, w2])
                    new_data[s, i, w] = value
        ut.writeToFile(outputFile, 'a', new_data, new_data.shape[0], str(node.bagType) + str(node.getBag()))
        return new_data
    return data
