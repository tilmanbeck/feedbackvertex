import graphviz as gv
import string

index = 0


class GraphVisualization:

    def increment_index(self):
        global index
        index += 1

    def get_next_symbol(self):
        alph = list(string.ascii_uppercase)
        value = alph[index % 24] + str(index // 24)
        self.increment_index()
        return value

    def get_path(self):
        return self.path

    def __init__(self, tree_decomposition):
        self.tree = tree_decomposition

    def get_label(self, ntree):
        return str(ntree.get_bag_type().value) + " | " + str(ntree.get_bag()) + " | label: " + str(ntree.get_label())

    def add_nodes_and_edges(self, ntree, g):
        assert isinstance(g, gv.Graph)
        node_symbol = self.get_next_symbol()
        g.node(node_symbol, self.get_label(ntree))
        left_child = ntree.get_left()
        left_symbol = self.get_next_symbol()
        g.node(left_symbol, self.get_label(left_child))
        g.edge(node_symbol, left_symbol)
        self.add_children(left_child, g, left_symbol)

    def add_children(self, ntree, g, old_symbol):
        assert isinstance(g, gv.Graph)
        left_child = ntree.get_left()
        right_child = ntree.get_right()
        left = False
        right = False
        if left_child is not None:
            left_symbol = self.get_next_symbol()
            g.node(left_symbol, self.get_label(left_child))
            g.edge(old_symbol,left_symbol)
            left = True
        if right_child is not None:
            right_symbol = self.get_next_symbol()
            g.node(right_symbol,self.get_label(right_child))
            g.edge(old_symbol, right_symbol)
            right = True
        if left:
            self.add_children(left_child, g, left_symbol)
        if right:
            self.add_children(right_child, g, right_symbol)

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

    def create_graph(self):
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
        self.add_nodes_and_edges(self.tree, g)
        g = self.apply_styles(g, styles)
        # filename = g.save('graph', '.')
        # render doesnt work so i save it
        g.render(filename='./graph', view=True)



