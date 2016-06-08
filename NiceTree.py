# class to implement the nice tree decomposition conversion
# from paper
# 'Solving connectivity problems parameterized by treewidth in
# single exponential time' [Cygan,Nederlof,Pilipczuk,Rooij,Wojtaszczyk]

from BagType import BagType

class NiceTree:
    def __init__(self, left=None, right=None, bag=[], bagType=None):
        self.left = left
        self.right = right
        self.bag = bag
        #convertToNiceTree()
        self.bagType = bagType
        self.labels = []

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
    def addLabel(self, label):
        self.labels.append(label)

def print_NiceTree_indented(self, level=0):
    if self == None:
        print(str(level) + ' none')
        return
    print(str(level) + ' ' + str(self.bag))
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
        tree.left = createLeaf(tree.getBag())

# creates as many new nodes until the bag is empty
# (forgetting one vertex per step)
# so that the last node has an empty bag and
# gets the type leaf bag
def createLeaf(bag):
    if(len(bag) > 1):
        return NiceTree(createLeaf(bag[1:]), None, bag[1:], BagType.IV)
    return NiceTree(None, None, [], BagType.L)

# This function gets the old root of the tree
# and introduces new root nodes as long as
# the bag of the old root is not empty by
# forgetting one vertex in every step.
# The newly introduced nodes are marked as
# forget bags and the last one to be introduced
# as root with an empty bag (definition 2.3)
def root(oldRoot):
    bag = oldRoot.getBag()
    while(len(bag)>1):
        newRoot = NiceTree(oldRoot,None,bag[1:], BagType.F)
        return root(newRoot)
    return NiceTree(oldRoot,None, [],BagType.R)

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
            newLeftNode = NiceTree(leftNode, None, treeBag)
            newRightNode = NiceTree(rightNode, None, treeBag)
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
def hasNoSpecialName(ntree):
    if(hasTwoChildren(ntree)):
        hasNoSpecialName(ntree.getLeft())
        hasNoSpecialName(ntree.getRight)
    else:
        child = getChild(ntree)
        ntreeBag = ntree.getBag()
        childBag = child.getBag()
        intersection = getIntersection(ntreeBag, childBag)
        #TODO in what cases are we sure that we have to introduce new vertices?
        #TODO loop over forgetList -> add new forget bags
        #TODO loop over introduceList -> add new introduce bags
        #TODO glue it together
        forgetList = getBagDifference(ntreeBag, intersection)
        introduceList = getBagDifference(childBag, intersection)




# calculates the intersection of two bags
# example: [a,b,c] and [b,f,g] -> [b]
def getIntersection(firstBag, scndBag):
    return list(set(firstBag).intersection(set(scndBag)))

# calculates the difference of two bags
# example: [a,b,c] and [a] -> [b,c]
def getBagDifference(firstBag, scndBag):
    return list(set(firstBag).difference(set(scndBag)))

# def hasNoSpecialName(ntree):
#     if(not hasTwoChildren(ntree)):
#         child = getChild(ntree)
#         ntreeBag = ntree.getBag()
#         childBag = ntree.getBag()
#         intersection = getIntersection(ntreeBag,childBag)
#         if(len(intersection) > 0):
#             forgetList =


def getChild(ntree):
    left = ntree.getLeft()
    if(left != None):
        return left
    return ntree.getRight()

def hasTwoChildren(ntree):
    if(ntree.getLeft() == None and ntree.getRight() == None):
        return True
    return False


#order: join, internalstuff, leaf, root
