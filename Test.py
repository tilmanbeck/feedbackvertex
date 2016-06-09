from TreeDecomposition import TreeDecomposition
from TreeDecomposition import print_NiceTree_indented
from TreeDecomposition import leaf
from TreeDecomposition import root
from TreeDecomposition import join
from TreeDecomposition import addInternalNodes
from TreeDecomposition import saveTreeDecomposition
from TreeDecomposition import edgeBags
from TreeDecomposition import getNextSymbol
from BagType import BagType
from Graphviz import GraphVisualization

# example graph G
vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
edges = [{'a', 'b'}, {'a', 'g'}, {'b', 'g'}, {'b', 'c'},
         {'c', 'e'}, {'g', 'e'}, {'g', 'f'}, {'e', 'f'},
         {'c', 'd'}, {'d', 'e'}]

ecd = TreeDecomposition(None, None, ['e', 'c', 'd'])
efg = TreeDecomposition(None, None, ['e', 'f', 'g'])
abg = TreeDecomposition(None, None, ['a', 'b', 'g'])
ecg = TreeDecomposition(efg, ecd, ['e', 'c', 'g'])
bcg = TreeDecomposition(abg, ecg, ['b', 'c', 'g'])
bc = TreeDecomposition(bcg, None, ['b', 'c'])



#order: join, internalstuff, leaf, root, edge bags
print('------')
bc = root(bc)
leaf(bc)
join(bc)
addInternalNodes(bc)
edgeBags(bc,edges)
print_NiceTree_indented(bc)
print('------')

#saveTreeDecomposition(bc,edges)
gv = GraphVisualization(bc)
gv.createGraph()


