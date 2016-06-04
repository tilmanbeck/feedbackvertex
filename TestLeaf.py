from NiceTree import NiceTree
from NiceTree import print_NiceTree_indented
from NiceTree import leaf

ecd = NiceTree(None,None,['e','d','c'])
efg = NiceTree(None,None,['g', 'f', 'e'])
abg = NiceTree(None,None,['b', 'g', 'a'])
ecg = NiceTree(efg,ecd,['e','c','g'])
bcg = NiceTree(abg,ecg,['b','c','g'])
bc = NiceTree(bcg, None,['b','c'])

print_NiceTree_indented(bc)
print('- - - - - - - - -')
leaf(bc)
#print_NiceTree_indented(bc)