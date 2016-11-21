# class to implement the nice tree decomposition conversion
# from paper
# 'Solving connectivity problems parameterized by treewidth in
# single exponential time' [Cygan,Nederlof,Pilipczuk,Rooij,Wojtaszczyk]

# TODO assert isIstance etc, class name, class functions, bag as set
# TODO getTreewidth

from BagType import BagType
import copy
import string


index = 0


class TreeDecomposition:
    def __init__(self, left=None, right=None, bag=None, bag_type=None):
        self.left = left
        self.right = right
        self.bag = bag
        #convertToNiceTree()
        self.bag_type = bag_type
        self.label = {}

    def set_bag_type(self, bag_type):
        self.bag_type = bag_type
        
    def get_bag_type(self):
        return self.bag_type
    
    def __str__(self):
        return str(self.bag)
    
    def get_right(self):
        return self.right
    
    def get_left(self):
        return self.left
    
    def get_bag(self):
        return self.bag
    
    def set_right(self, right):
        self.right = right
        
    def set_left(self, left):
        self.left = left
        
    def set_label(self, label):
        self.label = label
        
    def get_label(self):
        return self.label


def print_nice_tree_indented(self, level=0):
    if self is None:
        print(str(level) + ' none')
        return
    print(str(level) + ' ' + str(self.bag) + ' ' + str(self.get_bag_type()) + ' ' + str(self.get_label()))
    print_nice_tree_indented(self.left, level+1)
    print_nice_tree_indented(self.right, level+1)


# This function traverses the tree in-order
# and searches for the leaves of the tree
# (both children non-existent)
# when it finds one, it sets its left child
# as the result of create_leaf with its bag
def leaf(tree):

    if tree.get_left() is not None:
        leaf(tree.get_left())

    if tree.get_right() is not None:
        leaf(tree.get_right())

    if (len(tree.get_bag()) > 0) and (tree.get_left() is None) and (tree.get_right() is None):
        tree.set_bag_type(BagType.IV)
        tree.set_label(str(tree.get_bag()[0]))
        tree.left = create_leaf(tree.get_bag())


# creates as many new nodes until the bag is empty
# (forgetting one vertex per step)
# so that the last node has an empty bag and
# gets the type leaf bag
def create_leaf(bag):
    if len(bag) > 1:
        new_bag = TreeDecomposition(create_leaf(bag[1:]), None, bag[1:], BagType.IV)
        new_bag.set_label(str(bag[1]))
        return new_bag
    return TreeDecomposition(None, None, [], BagType.L)


def is_child_smaller(old_root):
    return get_bag_difference(old_root.get_bag(), get_child(old_root).get_bag()) == 1


# used to define the BagType of the old root
def root(old_root):
    bag_diff = get_bag_difference(old_root.get_bag(), get_child(old_root).get_bag())
    if bag_diff == 1:
        old_root.set_bag_type(BagType.IV)
        old_root.set_label(str(bag_diff[0]))
    else:
        old_root.set_bag_type(BagType.F)
        old_root.set_label(str(get_bag_difference(get_child(old_root).get_bag(), old_root.get_bag())[0]))
    return init_root(old_root)


# This function gets the old root of the tree
# and introduces new root nodes as long as
# the bag of the old root is not empty by
# forgetting one vertex in every step.
# The newly introduced nodes are marked as
# forget bags and the last one to be introduced
# as root with an empty bag (definition 2.3)
def init_root(old_root):
    bag = old_root.get_bag()
    while len(bag) > 1:
        new_root = TreeDecomposition(old_root, None, bag[1:], BagType.F)
        new_root.set_label(str(bag[0]))
        return init_root(new_root)
    return TreeDecomposition(old_root, None, [], BagType.R)


# The join function traverses the given tree in-order
# and checks for every node if there are two children
# if yes (and their bags are not equal -> already joined)
# then we introduce a join bag and two equal children
# (according to definition 2.3)
# otherwise we continue traversing
def join(tree):
    left_node = tree.get_left()
    right_node = tree.get_right()
    if has_two_children(tree):
        right_bag = tree.get_right().get_bag()
        left_bag = tree.get_left().get_bag()
        if not are_equals_bags(right_bag, left_bag):
            tree.set_bag_type(BagType.J)
            tree_bag = tree.get_bag()
            new_left_node = TreeDecomposition(left_node, None, tree_bag)
            new_right_node = TreeDecomposition(right_node, None, tree_bag)
            tree.set_left(new_left_node)
            tree.set_right(new_right_node)
    if left_node is not None:
        join(left_node)
    if right_node is not None:
        join(right_node)


def are_equals_bags(first_bag, scnd_bag):
    return len([x for x in first_bag if x not in scnd_bag]) == 0


# A nice tree decomposition (definition 2.3) uses
# structures of the standard nice tree decomposition.
# This function takes care that the third property
# of definition 2.2 of a nice standard nice tree
# decomposition is guaranteed. We achieve this by
# introducing forget bags and introduce vertex bags
# between two connected nodes whose intersection is
# bigger than one and/or if they contain different
# vertices.
# We first 'forget' all vertices of the parent node
# and from there on we introduce all the vertices
# which existed in the previous child node
# Additionally, we use the assumption that if a node
# has two children, we don't have to examine it
# as we executed join beforehand
def add_internal_nodes(ntree):
    if has_two_children(ntree):
        add_internal_nodes(ntree.get_left())
        add_internal_nodes(ntree.get_right())
    else:
        child = get_child(ntree)
        ntree_bag = copy.copy(ntree.get_bag())
        if child is not None and ntree_bag is not None:
            child_bag = child.get_bag()
            intersection = get_intersection(ntree_bag, child_bag)
            forget_list = get_bag_difference(ntree_bag, intersection)
            introduce_list = get_bag_difference(child_bag, intersection)
            # forget_list = list of vertices which have to be removed from the bag
            # while traversing downwards the tree (we remove one each step)
            # introduce_list = list of vertices which have to be added to the bag
            # while traversing downwards the tree (we add one each step)
            # if we know that the sum of those two lists equals 1 or less than
            # we  know we don't have to introduce/forget vertices
            # otherwise we have two cases:
            #   1:  we still have to forget bags
            #   2:  we have to introduce bags
            if (len(forget_list) + len(introduce_list)) > 1:
                if len(forget_list) > 0:
                    #case 1
                    ntree_bag.remove(forget_list[0])
                    new_child = TreeDecomposition(child, None, ntree_bag, BagType.F)
                    new_child.set_label(str(introduce_list[0]))
                    ntree.set_bag_type(BagType.IV)
                    ntree.set_label(str(forget_list[0]))
                    ntree.set_left(new_child)
                    add_internal_nodes(new_child)
                elif len(introduce_list) > 0:
                    #case 2
                    ntree_bag.add(introduce_list[0])
                    new_child = TreeDecomposition(child, None, ntree_bag, BagType.IV)
                    new_child.set_label(str(introduce_list[0]))
                    ntree.set_bag_type(BagType.F)
                    ntree.set_label(str(forget_list[0]))
                    ntree.set_left(new_child)
                    add_internal_nodes(new_child)
            if child.get_bag() is not None:
                add_internal_nodes(child)


# calculates the intersection of two bags
# example: [a,b,c] and [b,f,g] -> [b]
def get_intersection(first_bag, scnd_bag):
    return list(set(first_bag).intersection(set(scnd_bag)))


# calculates the difference of two bags
# ! result depends on order of parameters !
# example: [a,b,c] and [a] -> [b,c]
def get_bag_difference(first_bag, scnd_bag):
    return list(set(first_bag).difference(set(scnd_bag)))


def get_child(ntree):
    left = ntree.get_left()
    if left is not None:
        return left
    return ntree.get_right()


def has_two_children(ntree):
    if ntree.get_left() is not None and ntree.get_right() is not None:
        return True
    return False


# execute inorder_edge_bag for each edge
def edge_bags(ntree, edges):
    for edge in edges:
        inorder_edge_bag(ntree, edge, False)


# this function traverse the tree in-order
# for each edge of the initial graph and
# should place an extra 'introduce edge bag'
# above the first node which contains the edge
def inorder_edge_bag(ntree, edge, found):
    if not found:
        left_child = ntree.get_left()
        right_child = ntree.get_right()
        if left_child is not None:
            if contains_edge(edge, left_child.get_bag()):
                new_node = TreeDecomposition(left_child, None, left_child.get_bag(), BagType.IE)
                new_node.set_label(edge)
                ntree.set_left(new_node)
                return inorder_edge_bag(ntree, edge, True)
            else:
                inorder_edge_bag(left_child, edge, False)
        if right_child is not None:
            if contains_edge(edge, right_child.get_bag()):
                new_node = TreeDecomposition(right_child, None, right_child.get_bag(), BagType.IE)
                new_node.set_label(edge)
                ntree.set_left(new_node)
                return inorder_edge_bag(ntree, edge, True)
            else:
                inorder_edge_bag(right_child, edge, False)


def has_at_least_one_child(ntree):
    if ntree.get_left() is None:
        if ntree.get_right() is None:
            return False
    return True


def contains_edge(edge, bag):
    return len(set(edge).intersection(set(bag))) == 2


def increment_index():
    global index
    index += 1
    
    
def save_header(file):
    file.write("graph NiceTreeDecomposition {\n")
    file.write("size=\"1,1\";\n")
    file.write("node [shape=box];\n")


def save_nodes(file, ntree):
    #write the node
    global index
    node_symbol = get_next_symbol()
    increment_index()
    file.write(get_edge_line(node_symbol, ntree))
    left_child = ntree.get_left()
    right_child = ntree.get_right()
    left = False
    right = False
    if left_child is not None:
        left_symbol = get_next_symbol()
        increment_index()
        file.write(get_edge_line(left_symbol, left_child))
        file.write(node_symbol + " -- " + left_symbol + " [type=s];\n")
        left = True
    if right_child is not None:
        right_symbol = get_next_symbol()
        increment_index()
        file.write(get_edge_line(right_symbol, right_child))
        file.write(node_symbol + " -- " + right_symbol + " [type=s];\n")
        right = True
    if left: 
        save_nodes(file, left_child)
    if right: 
        save_nodes(file, right_child)


def get_edge_line(symbol, ntree):
    return symbol + " [label=\"{{" + str(ntree.get_bag_type().value) + "|" + str(ntree.get_bag()) + "}}\"];\n"


def save_finish(file):
    file.write("}")


def save_tree_decomposition(ntree, edges):
    file = open("treeDecomposition.txt", "w")
    save_header(file)
    save_nodes(file, ntree)
    #saveEdges(file, edges)
    save_finish(file)
    file.close()


def get_next_symbol():
    alph = list(string.ascii_uppercase)
    return alph[index % 24] + str(index // 24)



