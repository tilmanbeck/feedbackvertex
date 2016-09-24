import graphviz as gv
import string

index = 0
class GraphVisualization:

    def incrementIndex(self):
        global index
        index += 1

    def getNextSymbol(self):
        alph = list(string.ascii_uppercase)
        value = alph[index%24] + str(index // 24)
        self.incrementIndex()
        return value

    def getPath(self):
        return self.path

    def __init__(self, treeDecomposition):
        self.tree = treeDecomposition

    def getLabel(self, ntree):
        return str(ntree.getBagType().value) + " | " + str(ntree.getBag()) + " | label: " + str(ntree.getLabel())

    def addNodesAndEdges(self, ntree, g):
        assert isinstance(g, gv.Graph)
        nodeSymbol = self.getNextSymbol()
        g.node(nodeSymbol,self.getLabel(ntree))
        leftChild = ntree.getLeft()
        leftSymbol = self.getNextSymbol()
        g.node(leftSymbol, self.getLabel(leftChild))
        g.edge(nodeSymbol,leftSymbol)
        self.addChildren(leftChild, g, leftSymbol)

    def addChildren(self, ntree, g, oldSymbol):
        assert isinstance(g, gv.Graph)
        leftChild = ntree.getLeft()
        rightChild = ntree.getRight()
        left = False
        right = False
        if(leftChild != None):
            leftSymbol = self.getNextSymbol()
            g.node(leftSymbol, self.getLabel(leftChild))
            g.edge(oldSymbol,leftSymbol)
            left = True
        if(rightChild != None):
            rightSymbol = self.getNextSymbol()
            g.node(rightSymbol,self.getLabel(rightChild))
            g.edge(oldSymbol, rightSymbol)
            right = True
        if left: self.addChildren(leftChild, g,leftSymbol)
        if right: self.addChildren(rightChild, g,rightSymbol)

    def apply_styles(self, graph, styles):
        graph.graph_attr.update(
            ('graph' in styles and styles['graph']) or {}
        )
        graph.node_attr.update(
            ('nodes' in styles and styles['nodes']) or {}
        )
        graph.edge_attr.update(
            ('edges' in styles and styles['edges']) or {}
        )
        return graph

    def createGraph(self):
        styles = {
            'graph': {
                'label': 'Nice Tree Decomposition',
                'labelloc': 'top',
                'fontsize': '16',
                'fontcolor': 'white',
                'bgcolor': '#333333',
                'rankdir': 'TB',
            },
            'nodes': {
                'fontname': 'Helvetica',
                'shape': 'box',
                'fontcolor': 'white',
                'color': 'white',
                'style': 'filled',
                'fillcolor': '#006699',
            },
            'edges': {
                'style': 'dashed',
                'color': 'white',
                'arrowhead': 'open',
                'fontname': 'Courier',
                'fontsize': '12',
                'fontcolor': 'white',
            }
        }
        g = gv.Graph(format='svg')
        self.addNodesAndEdges(self.tree, g)
        g = self.apply_styles(g, styles)
        # filename = g.save('graph', '.')
        # render doesnt work so i save it
        g.render(filename='./graph', view=True)



