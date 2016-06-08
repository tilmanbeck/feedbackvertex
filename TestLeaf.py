from NiceTree import NiceTree
from NiceTree import print_NiceTree_indented
from NiceTree import leaf
from NiceTree import root

ecd = NiceTree(None,None,['e','c','d'])
efg = NiceTree(None,None,['e', 'f', 'g'])
abg = NiceTree(None,None,['a', 'b', 'g'])
ecg = NiceTree(efg,ecd,['e','c','g'])
bcg = NiceTree(abg,ecg,['b','c','g'])
bc = NiceTree(bcg, None,['b','c'])

print_NiceTree_indented(bc)
print('- - - - - - - - -')
leaf(bc)
bc = root(bc)
print_NiceTree_indented(bc)