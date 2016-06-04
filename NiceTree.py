import Tree
from enum import Enum

def leaf(tree):
    if(tree.getLeft() != None):
        return leaf(tree.getLeft())

    if(tree.getRight() != None):
        return leaf(tree.getRight())

    if(not tree.getBag()):
        tree.left = createLeaf(tree.getBag())
        return

def createLeaf(bag):
    if(not bag):
        return NiceTree(createLeaf(bag[-1]), None, bag, BagType.IV)
    return NiceTree(None, None, [], BagType.L)

#def convertToNiceTree():

class NiceTree(Tree):
    def __init__(self, left=None, right=None, bag=[], bagType=None):
        Tree.__init__(left,right,bag)
        #convertToNiceTree()
        self.bagType = bagType

    def setType(self,type):
        self.type = type
    def getBagType(self):
        return self.bagType

class BagType(Enum):
    IV = 'introduce vertex'
    IE = 'introduce edge'
    J  = 'join'
    F  = 'forget'
    L  = 'leaf'
    R  = 'root'