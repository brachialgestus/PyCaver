import networkx as nx
import TunnelPoint
import Tunnel

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
        return "Meta Tunnel"
    
    def plot(self):
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

        plt.savefig("meta_tunnel.png")

    def iplot(self):
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


        # Create figure
        fig = go.Figure(data=[node_trace])
        fig.write_html("network_graph.html")
        