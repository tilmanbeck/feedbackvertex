from BagType import BagType

class NiceTree:
    def __init__(self, left=None, right=None, bag=[], bagType=None):
        self.left = left
        self.right = right
        self.bag = bag
        #convertToNiceTree()
        self.bagType = bagType

    def setType(self,type):
        self.type = type
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

def print_NiceTree_indented(self, level=0):
    if self == None:
        print(str(level) + ' none')
        return
    print(str(level) + ' ' + str(self.bag))
    print_NiceTree_indented(self.left, level+1)
    print_NiceTree_indented(self.right, level+1)

def leaf(tree):

    if(tree.getLeft() != None):
        leaf(tree.getLeft())

    if(tree.getRight() != None):
        leaf(tree.getRight())

    if((len(tree.getBag()) > 0) and (tree.getLeft() == None) and (tree.getRight() == None)):
        tree.left = createLeaf(tree.getBag())

#def convertToNiceTree():

def createLeaf(bag):
    if(len(bag) > 1):
        return NiceTree(createLeaf(bag[1:]), None, bag[1:], BagType.IV)
    return NiceTree(None, None, [], BagType.L)
