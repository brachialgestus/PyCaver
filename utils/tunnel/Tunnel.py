import networkx as nx
from TunnelPoint import TunnelPoint

class Tunnel:
    def __init__(self, name):
        self.name = name
        self.graph = nx.Graph()
        self.root = None
        self.last = None

    def add_root(self, TunnelPoint):
        self.root = TunnelPoint
        self.graph.add_node(TunnelPoint)
        self.last = TunnelPoint

    def add_TunnelPoint(self, TunnelPoint : TunnelPoint):
        self.graph.add_node(TunnelPoint)
        self.graph.add_edge(self.last, TunnelPoint)
        self.last = TunnelPoint

    def __str__(self):
        return self.name + " Tunnel"
    
    def print_graph(self):
        print("nodes:", self.graph.nodes())
        print("edges:", self.graph.edges())

    def get_coordinates(self):
        return [node.get_coordinates() for node in self.graph.nodes()]