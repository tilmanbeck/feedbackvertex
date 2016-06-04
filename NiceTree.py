import Tree

def leaf(tree):
    if(tree.getLeft() != None):
        return leaf(tree.getLeft())

    if(tree.getRight() != None):
        return leaf(tree.getRight())

    if(not bag):
        tree.left = createLeaf(bag)
    pass

def createLeaf(bag):
    if(not bag):
        return NiceTree(createLeaf(bag[-1]),None,bag,'I')
    return NiceTree(None,None,[],'Leaf')

def convertToNiceTree():
    pass


class NiceTree(Tree):
    def __init__(self, left=None, right=None, bag=[], type=''):
        Tree.__init__(left,right,bag)
        convertToNiceTree()
        self.type = type
        
    def setType(self,type):
        self.type = type
    def getType(self):
        return self.type