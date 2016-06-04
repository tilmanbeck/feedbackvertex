class Tree:
    def __init__(self, parent=None, left=None, right=None, bag=[]):
        self.parent = parent
        self.left = left
        self.right = right
        self.bag = bag

    def __str__(self):
        return str(self.bag)
    def getRight(self):
        return self.right
    def getLeft(self):
        return self.left
    def getBag(self):
        return self.bag

def print_tree_indented(self, level=0):
    if self == None:
        print '  '
        return
    print '  ' * level + str(self.bag)
    print_tree_indented(self.left, level+1)
    print_tree_indented(self.right, level+1)

#leaf node creation
#

bc = Tree(bcg, None,['b','c'])
bcg = Tree(bc,abg,ecg,['b','c','g'])
ecg = Tree(efg,ecd,['e','c','g'])
ecd = Tree(None,None,['e','d','c'])
efg = Tree(None,None,['g', 'f', 'e'])
abg = Tree(None,None,['b', 'g', 'a'])

print_tree_indented(bc)

