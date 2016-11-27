import math as m


# value zB [0,1,2,2,0]
# missing_nodes zB [0,4]
# indices []
# indices of the missing_nodes in value have to be zero!d
def calculate_indices(value, missing_nodes):
    indices = calculate_indices_rec(value, missing_nodes, [])
    return list(set(indices))


def calculate_indices_rec(value, missing_nodes, indices):
    if not missing_nodes:
        return indices
    else:
        # Hornerschema
        start_point = 0
        for i in range(0,len(value)):
            start_point += 3**i * value[i]

        i1 = start_point + 3**missing_nodes[0] * 0
        i2 = start_point + 3**missing_nodes[0] * 1
        i3 = start_point + 3**missing_nodes[0] * 2

        indices = indices + [i1, i2, i3]

        value1 = list(value)
        value1[missing_nodes[0]] = 0
        value2 = list(value)
        value2[missing_nodes[0]] = 1
        value3 = list(value)
        value3[missing_nodes[0]] = 2


        return indices + calculate_indices_rec(value1, missing_nodes[1:], indices) + calculate_indices_rec(value2, missing_nodes[1:], indices) + calculate_indices_rec(value3, missing_nodes[1:], indices)


def get_indices_for_introduce_edge(indices, first_vertex, scnd_vertex):
    val = [0 for i in range(0, len(indices))]
    # what are we doing here? we need all indices except those where one of the edges is colored 1 and the other one 2
    # and vice versa. so we take all indices and remove mentioned from all indices

    val[indices.get(first_vertex)] = 1
    val[indices.get(scnd_vertex)] = 2
    keys = list(indices.keys())
    keys.remove(first_vertex)
    keys.remove(scnd_vertex)
    missing_nodes = []
    for key in keys:
        missing_nodes.append(indices.get(key))
    first = calculate_indices(val, missing_nodes)

    val[indices.get(first_vertex)] = 2
    val[indices.get(scnd_vertex)] = 1
    keys = list(indices.keys())
    keys.remove(first_vertex)
    keys.remove(scnd_vertex)
    missing_nodes = []
    for key in keys:
        missing_nodes.append(indices. get(key))
    scnd = calculate_indices(val, missing_nodes)

    return first+scnd


# indices_kv = key-value dict where the keys are
# the nodes (e.g. 'a') and the value is the
# index in the index-array according to order
def get_nodes_by_coloring(nodes, coloring, indices_kv):
    tmp = [i for i in range(0, len(nodes)) if nodes[i] in coloring]
    return [key for key, val in indices_kv.items() if val in tmp]


def get_sum_of_weights(nodes, weights):
    res = 0
    for i in range(0,len(nodes)):
        res += weights.get(nodes[i])
    return res


def get_index_as_list(x, nr_of_vertices):
    if nr_of_vertices == 0:
        return [0]
    number = x
    res = []
    for i in range(nr_of_vertices-1, -1, -1):
        value = m.floor(number/(3**i))
        number -= (value * 3**i)
        res.append(value)

    return res


def write_to_file(filename, mode, array, fst, step_info):
    with open(filename, mode) as f:
        f.write(step_info)
        f.write("\n")
        for i in range(0, fst):
            f.write(str(i))
            f.write("\n")
            f.write(str(array[i]))
            f.write("\n\n")
        f.write("-----------------------------------------------\n")