import networkx as nx
from TunnelPoint import TunnelPoint
from Tunnel import Tunnel

import json
from CustomDecoder import CustomDecoder
from CustomEncoder import CustomEncoder

import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
        return f"Meta Tunnel, root: {self.root}"
    
    def write_to_json(self, filename : str = "meta_tunnel.json"):
        data = nx.node_link_data(self.graph, edges="links")
        meta_data = {
            #"root" : (self.root.x, self.root.y, self.root.z),
            "root" : self.root,
            "graph" : data
        }
        with open(filename, 'w') as f:
            json.dump(meta_data, f, indent=4, cls=CustomEncoder)

    def read_from_json(self, filename : str):
        with open(filename, "r") as f:
            data = json.load(f, object_hook=CustomDecoder.tunnelpoint_decoder)
        self.graph = nx.node_link_graph(data["graph"], edges="links")
        self.root = data["root"]

    def plot(self, filename : str = "meta_tunnel.png"):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # draw nodes
        for node in self.graph.nodes():
            ax.scatter(node.x, node.y, node.z, c='b', marker='o')

        # draw edges
        for edge in self.graph.edges():
            node1 = edge[0]
            node2 = edge[1]
            ax.plot([node1.x, node2.x], [node1.y, node2.y], [node1.z, node2.z], c='b')

        plt.savefig(filename)

    def iplot(self, filename : str = "network_graph.html"):
        Xn = [node.x for node in self.graph.nodes()]
        Yn = [node.y for node in self.graph.nodes()]
        Zn = [node.z for node in self.graph.nodes()]

        node_values = [(node.radius)*10 for node in self.graph.nodes]

        special_node = list(self.graph.nodes)[0]

        node_trace = go.Scatter3d(
            x=Xn, y=Yn, z=Zn,
            mode='markers',
            marker=dict(size=node_values, 
                        opacity=0.8,
                        color=['red' if node == special_node else 'blue' for node in self.graph.nodes]),
            hoverinfo='text'
        )

        fig = go.Figure(data=[node_trace])
        fig.write_html(filename)
        