# class to implement the nice tree decomposition conversion
# from paper
# 'Solving connectivity problems parameterized by treewidth in
# single exponential time' [Cygan,Nederlof,Pilipczuk,Rooij,Wojtaszczyk]

# TODO assert isIstance etc, class name, class functions, bag as set
# TODO getTreewidth

from BagType import BagType
import copy
import string

class TreeDecomposition:
    def __init__(self, left=None, right=None, bag=None, bagType=None):
        self.left = left
        self.right = right
        self.bag = bag
        #convertToNiceTree()
        self.bagType = bagType
        self.label = {}

    def setBagType(self,bagType):
        self.bagType = bagType
    def getBagType(self):
        return self.bagType
    def __str__(self):
        return str(self.bag)
    def getRight(self):
        return self.right
    def getLeft(self):
        return self.left
    def getBag(self):
        return self.bag
    def setRight(self, right):
        self.right = right
    def setLeft(self, left):
        self.left = left
    def setLabel(self, label):
        self.label = label
    def getLabel(self):
        return self.label
def print_NiceTree_indented(self, level=0):
    if self == None:
        print(str(level) + ' none')
        return
    print(str(level) + ' ' + str(self.bag) + ' ' + str(self.getBagType()) + ' ' + str(self.getLabel()))
    print_NiceTree_indented(self.left, level+1)
    print_NiceTree_indented(self.right, level+1)

# This function traverses the tree in-order
# and searches for the leaves of the tree
# (both children non-existent)
# when it finds one, it sets its left child
# as the result of createLeaf with its bag
def leaf(tree):

    if(tree.getLeft() != None):
        leaf(tree.getLeft())

    if(tree.getRight() != None):
        leaf(tree.getRight())

    if((len(tree.getBag()) > 0) and (tree.getLeft() == None) and (tree.getRight() == None)):
        tree.setBagType(BagType.IV)
        tree.setLabel(str(tree.getBag()[0]))
        tree.left = createLeaf(tree.getBag())

# creates as many new nodes until the bag is empty
# (forgetting one vertex per step)
# so that the last node has an empty bag and
# gets the type leaf bag
def createLeaf(bag):
    if(len(bag) > 1):
        newBag = TreeDecomposition(createLeaf(bag[1:]), None, bag[1:], BagType.IV)
        newBag.setLabel(str(bag[1]))
        return newBag
    return TreeDecomposition(None, None, [], BagType.L)

def childIsSmaller(oldRoot):
    return getBagDifference(oldRoot.getBag(),getChild(oldRoot).getBag()) == 1

# used to define the BagType of the old root
def root(oldRoot):
    bagDiff = getBagDifference(oldRoot.getBag(),getChild(oldRoot).getBag())
    if(bagDiff == 1):
        oldRoot.setBagType(BagType.IV)
        oldRoot.setLabel(str(bagDiff[0]))
    else:
        oldRoot.setBagType(BagType.F)
        oldRoot.setLabel(str(getBagDifference(getChild(oldRoot).getBag(), oldRoot.getBag())[0]))
    return initRoot(oldRoot)

# This function gets the old root of the tree
# and introduces new root nodes as long as
# the bag of the old root is not empty by
# forgetting one vertex in every step.
# The newly introduced nodes are marked as
# forget bags and the last one to be introduced
# as root with an empty bag (definition 2.3)
def initRoot(oldRoot):
    bag = oldRoot.getBag()
    while(len(bag)>1):
        newRoot = TreeDecomposition(oldRoot, None, bag[1:], BagType.F)
        newRoot.setLabel(str(bag[0]))
        return initRoot(newRoot)
    return TreeDecomposition(oldRoot, None, [], BagType.R)

# The join function traverses the given tree in-order
# and checks for every node if there are two children
# if yes (and their bags are not equal -> already joined)
# then we introduce a join bag and two equal children
# (according to definition 2.3)
# otherwise we continue traversing
def join(tree):
    leftNode = tree.getLeft()
    rightNode = tree.getRight()
    if(hasTwoChildren(tree)):
        rightBag = tree.getRight().getBag()
        leftBag = tree.getLeft().getBag()
        if(not areEqualBags(rightBag,leftBag)):
            tree.setBagType(BagType.J)
            treeBag = tree.getBag()
            newLeftNode = TreeDecomposition(leftNode, None, treeBag)
            newRightNode = TreeDecomposition(rightNode, None, treeBag)
            tree.setLeft(newLeftNode)
            tree.setRight(newRightNode)
    if(leftNode != None):
        join(leftNode)
    if(rightNode != None):
        join(rightNode)

def areEqualBags(firstBag, scndBag):
    return len([x for x in firstBag if x not in scndBag]) == 0


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
def addInternalNodes(ntree):
    if(hasTwoChildren(ntree)):
        addInternalNodes(ntree.getLeft())
        addInternalNodes(ntree.getRight())
    else:
        child = getChild(ntree)
        ntreeBag = copy.copy(ntree.getBag())
        if(child != None and ntreeBag != None):
            childBag = child.getBag()
            intersection = getIntersection(ntreeBag, childBag)
            forgetList = getBagDifference(ntreeBag, intersection)
            introduceList = getBagDifference(childBag, intersection)
            # forgetList = list of vertices which have to be removed from the bag
            # while traversing downwards the tree (we remove one each step)
            # introduceList = list of vertices which have to be added to the bag
            # while traversing downwards the tree (we add one each step)
            # if we know that the sum of those two lists equals 1 or less than
            # we  know we don't have to introduce/forget vertices
            # otherwise we have two cases:
            #   1:  we still have to forget bags
            #   2:  we have to introduce bags
            if((len(forgetList) + len(introduceList)) > 1):
                if(len(forgetList) > 0):
                    #case 1
                    ntreeBag.remove(forgetList[0])
                    newChild = TreeDecomposition(child, None, ntreeBag, BagType.F)
                    newChild.setLabel(str(introduceList[0]))
                    ntree.setBagType(BagType.IV)
                    ntree.setLabel(str(forgetList[0]))
                    ntree.setLeft(newChild)
                    addInternalNodes(newChild)
                elif(len(introduceList) > 0):
                    #case 2
                    ntreeBag.add(introduceList[0])
                    newChild = TreeDecomposition(child, None, ntreeBag, BagType.IV)
                    newChild.setLabel(str(introduceList[0]))
                    ntree.setBagType(BagType.F)
                    ntree.setLabel(str(forgetList[0]))
                    ntree.setLeft(newChild)
                    addInternalNodes(newChild)
            if(child.getBag() != None):
                addInternalNodes(child)

# calculates the intersection of two bags
# example: [a,b,c] and [b,f,g] -> [b]
def getIntersection(firstBag, scndBag):
    return list(set(firstBag).intersection(set(scndBag)))

# calculates the difference of two bags
# ! result depends on order of parameters !
# example: [a,b,c] and [a] -> [b,c]
def getBagDifference(firstBag, scndBag):
    return list(set(firstBag).difference(set(scndBag)))

def getChild(ntree):
    left = ntree.getLeft()
    if(left != None):
        return left
    return ntree.getRight()

def hasTwoChildren(ntree):
    if(ntree.getLeft() != None and ntree.getRight() != None):
        return True
    return False

# execute inOrderEdgeBag for each edge
def edgeBags(ntree, edges):
    for edge in edges:
        inOrderEdgeBag(ntree, edge, False)

# this function traverse the tree in-order
# for each edge of the initial graph and
# should place an extra 'introduce edge bag'
# above the first node which contains the edge
def inOrderEdgeBag(ntree, edge, found):
    if(not found):
        leftChild = ntree.getLeft()
        rightChild = ntree.getRight()
        if(leftChild != None):
            if(containsEdge(edge,leftChild.getBag())):
                newNode = TreeDecomposition(leftChild, None, leftChild.getBag(), BagType.IE)
                newNode.setLabel(edge)
                ntree.setLeft(newNode)
                return inOrderEdgeBag(ntree, edge, True)
            else:
                inOrderEdgeBag(leftChild, edge, False)
        if(rightChild != None):
            if(containsEdge(edge,rightChild.getBag())):
                newNode = TreeDecomposition(rightChild, None, rightChild.getBag(), BagType.IE)
                newNode.setLabel(edge)
                ntree.setLeft(newNode)
                return inOrderEdgeBag(ntree, edge, True)
            else:
                inOrderEdgeBag(rightChild, edge, False)


def hasAtLeastOneChild(ntree):
    if(ntree.getLeft() == None):
        if(ntree.getRight() == None):
            return False
    return True

def containsEdge(edge, bag):
    return len(set(edge).intersection(set(bag))) == 2


index = 0
def incrementIndex():
    global index
    index += 1
def saveHeader(file):
    file.write("graph NiceTreeDecomposition {\n")
    file.write("size=\"1,1\";\n")
    file.write("node [shape=box];\n")

def saveNodes(file,ntree):
    #write the node
    global index
    nodeSymbol = getNextSymbol()
    incrementIndex()
    file.write(getEdgeLine(nodeSymbol, ntree))
    leftChild = ntree.getLeft()
    rightChild = ntree.getRight()
    left = False
    right = False
    if(leftChild != None):
        leftSymbol = getNextSymbol()
        incrementIndex()
        file.write(getEdgeLine(leftSymbol, leftChild))
        file.write(nodeSymbol + " -- " + leftSymbol  + " [type=s];\n")
        left = True
    if(rightChild != None):
        rightSymbol = getNextSymbol()
        incrementIndex()
        file.write(getEdgeLine(rightSymbol, rightChild))
        file.write(nodeSymbol + " -- " + rightSymbol + " [type=s];\n")
        right = True
    if left: saveNodes(file, leftChild)
    if right: saveNodes(file, rightChild)

def getEdgeLine(symbol, ntree):
    return symbol + " [label=\"{{" + str(ntree.getBagType().value) + "|" + str(ntree.getBag()) + "}}\"];\n"


def saveFinish(file):
    file.write("}")

def saveTreeDecomposition(ntree, edges):
    file = open("treeDecomposition.txt", "w")
    saveHeader(file)
    saveNodes(file, ntree)
    #saveEdges(file, edges)
    saveFinish(file)
    file.close()

def getNextSymbol():
    alph = list(string.ascii_uppercase)
    return alph[index%24] + str(index // 24)



