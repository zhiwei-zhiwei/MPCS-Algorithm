from __future__ import annotations

from typing import Hashable

import networkx as nx

from utils import generate_complete_weighted_graph


def dial_shortest_path_length(
    G: nx.Graph, source: Hashable, max_edge_weight: int | None = None
) -> dict[Hashable, float]:
    """Compute single-source shortest path distances via Dial's algorithm.

    Parameters
    ----------
    G : nx.Graph
        An undirected graph with bounded positive integer edge weights.
    source : Hashable
        The source vertex.
    max_edge_weight : Optional[int], optional
        Maximum edge weight in G, by default None.
        Will be calculated in Theta(E) time if not provided.

    Returns
    -------
    distance : dict[Hashable, float]
        Shortest path distances from source in G.

    Examples
    --------
    >>> G = generate_complete_weighted_graph(n=20, max_edge_weight=5)
    >>> expected = nx.single_source_dijkstra_path_length(G, source=0)
    >>> actual = dial_shortest_path_length(G, source=0, max_edge_weight=5)
    >>> actual == expected
    True
    """
    if max_edge_weight is None:
        # Compute max edge weight if not provided
        max_edge_weight = max(d["weight"] for u, v, d in G.edges(data=True))

    # TODO: Implement Dial's algorithm
    # reference: https://www.codingninjas.com/studio/library/dials-algorithm
    # initialize values
    d = {node: float('inf') for node in G.nodes}
    buckets = [[] for _ in range(max_edge_weight * (len(G) - 1))]
    visited = set()

    # Initialize the basis case
    d[source] = 0
    buckets[0].append(source)

    while True:
        # Find the non-empty bucket with the smallest distance
        bucket_val = None
        for i, bucket in enumerate(buckets):
            if bucket:
                bucket_val = i
                break

        if bucket_val is None:
            break  # finish while loop condition

        while buckets[bucket_val]:
            v = buckets[bucket_val].pop(0)
            if v in visited:
                # run faster, to prevent multiple checks, but doesn't affect the algo very much
                continue
            visited.add(v)

            for neighbor, data in G[v].items():
                # Reference: https://networkx.org/documentation/stable/tutorial.html
                w = data['weight']
                distance = bucket_val + w
                if distance < d[neighbor]:
                    d[neighbor] = distance
                    buckets[distance].append(neighbor)

    return d


if __name__ == "__main__":
    import doctest

    doctest.testmod()