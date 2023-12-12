
import pytest
import networkx as nx
from utils import generate_complete_weighted_graph, generate_connected_weighted_graph
from dial import dial_shortest_path_length


@pytest.mark.parametrize("size", [10, 20, 50, 100, 500, 1000])
def test_complete(size):
    G = generate_complete_weighted_graph(n=size, max_edge_weight=10)
    expected = nx.single_source_dijkstra_path_length(G, source=0)
    actual = dial_shortest_path_length(G, source=0, max_edge_weight=10)
    assert actual == expected


@pytest.mark.parametrize("size", [10, 20, 50, 100, 500, 1000])
def test_connected(size):
    G = generate_connected_weighted_graph(n=size, max_edge_weight=10)
    expected = nx.single_source_dijkstra_path_length(G, source=0)
    actual = dial_shortest_path_length(G, source=0, max_edge_weight=10)
    assert actual == expected
