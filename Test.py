from NiceTree import NiceTree
from NiceTree import print_NiceTree_indented
from NiceTree import leaf
from NiceTree import root
from NiceTree import join
from NiceTree import addInternalNodes

# example graph G
vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
edges = [{'a', 'b'}, {'a', 'g'}, {'b', 'g'}, {'b', 'c'},
         {'c', 'e'}, {'g', 'e'}, {'g', 'f'}, {'e', 'f'},
         {'c', 'd'}, {'d', 'e'}]

ecd = NiceTree(None,None,['e', 'c', 'd'])
efg = NiceTree(None,None,['e', 'f', 'g'])
abg = NiceTree(None,None,['a', 'b', 'g'])
ecg = NiceTree(efg,ecd,['e', 'c', 'g'])
bcg = NiceTree(abg,ecg,['b', 'c', 'g'])
bc = NiceTree(bcg, None,['b', 'c'])

#treeDecomp = [rootNode1, rootNode2]

join(bc)
addInternalNodes(bc)
leaf(bc)
bc = root(bc)
print_NiceTree_indented(bc)
print('------')



