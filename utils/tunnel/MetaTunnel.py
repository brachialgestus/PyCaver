import networkx as nx
import TunnelPoint
import Tunnel
import matplotlib.pyplot as plt

class MetaTunnel:
    def __init__(self):
        self.graph = nx.Graph()
        self.root = None

    def add_first(self, tunnel : Tunnel):
        self.root = tunnel.root
        self.graph = tunnel.graph 

    def set_graph(self, graph):
        self.graph = graph

    def __str__(self):
        return "Meta Tunnel"
    
    def print_graph(self):
        print("nodes:", self.graph.nodes())
        print("edges:", self.graph.edges())

    def draw(self):
        nx.draw(self.graph, with_labels=True, font_weight='bold')
        plt.savefig("meta_tunnel.png")

        