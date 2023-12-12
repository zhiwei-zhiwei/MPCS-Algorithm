
from __future__ import annotations
import random
import networkx as nx


def generate_complete_weighted_graph(n=50, max_edge_weight: int | None = None):
    if max_edge_weight is None:
        max_edge_weight = n
    
    if not isinstance(max_edge_weight, int) or max_edge_weight < 1:
        raise ValueError("Max weight must be a positive integer")
    
    G = nx.complete_graph(n)
    
    for u, v in G.edges:
        G[u][v]["weight"] = random.randint(1, max_edge_weight)
    
    return G


def generate_connected_weighted_graph(n=50, max_edge_weight: int | None = None, edge_probability: float = 0.2):
    if max_edge_weight is None:
        max_edge_weight = n
   
    if not isinstance(max_edge_weight, int) or max_edge_weight < 1:
        raise ValueError("Max weight must be a positive integer")
    
    G = nx.random_labeled_tree(n)

    for u, v in G.edges:
        G[u][v]["weight"] = random.randint(1, max_edge_weight)

    for u, v in nx.non_edges(G):
        if random.random() < edge_probability:
            G.add_edge(u, v, weight=random.randint(1, max_edge_weight))

    return G
