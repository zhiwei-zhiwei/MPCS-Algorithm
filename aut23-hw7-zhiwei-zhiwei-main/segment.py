from typing import List, Hashable

import networkx as nx
import numpy as np


def segment_image(k: int, image: np.ndarray) -> np.ndarray:
    """
    Segment a grayscale image into n segments with MST-based segmentation.
    Create an undirected graph representation of the image and
    run the described modified Kruskal's algorithm to form segments

    Parameters
    ----------
    k : int
        Parameter determining whether segments are contiguous
    image : np.ndarray
        Two dimensions NumPy array representing a grayscale image

    Returns
    -------
    segments : np.ndarray
        Two dimensional NumPy array of the same dimensions as `image`.
        Each entry contains the label of the segment the corresponding
        pixel belongs.
    """
    assert len(image.shape) == 2
    # TODO
    # First step
    # https://stackoverflow.com/questions/14847457/how-do-i-find-the-length-or-dimensions-size-of-a-numpy-matrix-in-python
    row, col = image.shape
    vertices = [(r, c) for r in range(row) for c in range(col)]
    values = image.flatten()
    uf = UnionFind(vertices, values)

    # generate the graph
    graph = nx.Graph()  # relay on networkx
    for i in range(row):
        for j in range(col):
            neighbors = [
                (i - 1, j),
                (i + 1, j),
                (i, j - 1),
                (i, j + 1),
                (i - 1, j - 1),
                (i - 1, j + 1),
                (i + 1, j - 1),
                (i + 1, j + 1)]
            for u, v in neighbors:
                if 0 <= u < row and 0 <= v < col:
                    w = abs(image[i, j] - image[u, v])
                    graph.add_edge((i, j), (u, v), weight=w)

    # Second step
    # https://stackoverflow.com/questions/42856659/how-to-sort-edges-in-networkx-based-on-their-weight
    print(graph.edges.data())
    sorted_edges = sorted(graph.edges(data=True), key=lambda e: e[2].get('weight', 1))
    for (u, v, w) in sorted_edges:
        weights = w['weight']
        if uf.find(u) != uf.find(v):
            threshold = min(uf.max_diff(u) + k / uf._size[uf.find(u)], uf.max_diff(v) + k / uf._size[uf.find(v)])
            if weights <= threshold:
                uf.union(u, v)

    # Third
    segments = {}
    segments_label = 0
    # https://numpy.org/doc/stable/reference/generated/numpy.zeros.html
    res_segment = np.zeros(image.shape, dtype=int)  # make sure it has the same size and ready to add label
    for (r, c) in vertices:
        v = uf.find((r, c))
        if v not in segments:
            # assign the label
            segments[v] = segments_label
        segments_label += 1
        res_segment[r, c] = segments[v]

    return res_segment

    # uf = UnionFind(vertices, values)
    # formula for calculating the threshold in step 3(iii) and 3(iv) of the algorithm
    # threshold = min(uf.max_diff(u) + k / uf.size(u), uf.max_diff(v) + k / uf.size(v))


class UnionFind:
    """
    Union-Find data structure

    Attributes
    ----------
    parent : Dict[Hashable, Hashable]
        Dictionary pointing to a vertex to its representative
    min_values : Dict[Hashable, any]
        Minimum value in each segment
    max_values : Dict[Hashable, any]
        Maximum value in each segment

    Methods
    -------
    find(x: Hashable) -> Hashable
        Given a vertex `x`, return the representative of the segment it belongs
    union(x: Hashable, y: Hashable) -> None
        Combines the two segments connected by the edge (x,y) into one segment
    max_diff(x: Hashable) -> int
        Given a vertex, returns the largest difference in values between
        any vertices in the segment `x` belongs to
    """

    def __init__(self, vertices: List[Hashable], values: List):
        """
        Parameters
        ----------
        vertices : List[Hashable]
            List of vertices
        values : List
            Grayscale values for each vertex
        """
        # the parent of x, used by find() to retrieve x's segment
        self.parent = {x: x for x in vertices}
        # the smallest value in x's segment
        self.min_values = {x: values[idx] for idx, x in enumerate(vertices)}
        # the largest value in x's segment
        self.max_values = {x: values[idx] for idx, x in enumerate(vertices)}
        # # https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
        # size(U) is the number of vertices in the segment U
        # since each segment at least has one vertex
        self._size = {x: 1 for x in vertices}
        # represents the approximate depth of the tree representing a set, and uses union by rank
        # initialized the rank to zero
        self.rank = {x: 0 for x in vertices}

    def size(self, x: Hashable) -> int:
        # since the testcase doesn't accept the dict structure
        root = self.find(x)
        return self._size[root]

    def find(self, x: Hashable) -> Hashable:
        """
        Given a vertex `x`, return the representative of the segment it belongs

        Parameters
        ----------
        x : Hashable
            A vertex of the graph

        Returns
        -------
        representative : Hashable
            The representative of the segment that `x` belongs to
        """
        # TODO: Make sure you use path compression
        # https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: Hashable, y: Hashable) -> None:
        """
        Combines the two segments connected by the edge (x,y) into one segment

        Parameters
        ----------
        x : Hashable
            A vertex
        y : Hashable
            Another vertex
        """
        # TODO: Combine the two segments into one if they are different
        #       Make sure to update al relevant auxiliary variables
        u = self.find(x)
        v = self.find(y)
        if self.rank[u] < self.rank[v]:
            self.parent[u] = v
        elif self.rank[u] > self.rank[v]:
            self.parent[v] = u
        else:
            # self.rank[u] == self.rank[v]:
            self.parent[v] = u
            self.rank[u] += 1

        # update relevant variables
        self._size[u] += self._size[v]
        self.min_values[u] = min(self.min_values[u], self.min_values[v])
        self.max_values[u] = max(self.max_values[u], self.max_values[v])

    def max_diff(self, x: Hashable) -> int:
        """
        Given a vertex, returns the largest difference in values between
        any vertices in the segment `x` belongs to

        Parameters
        ----------
        x : Hashable
            A vertex

        Returns
        -------
        diff : int
            Largest difference in values between any vertices in the segment `x` belongs to
        """
        return self.max_values[self.find(x)] - self.min_values[self.find(x)]


if __name__ == "__main__":
    # You can manually test your code here
    # sample_image = np.array([
    #     [10, 20, 30, 33],
    #     [5, 6, 7, 8],
    #     [12, 13, 23, 43],
    #     [22, 64, 90, 100]
    # ])
    #
    # sample_k = 10
    #
    # segmented_image = segment_image(sample_k, sample_image)
    # print(segmented_image)

    import utils

    utils.load_segment_save_image(9, "wave.png", "new_wave_segmented.png")
    utils.load_segment_save_image(3, "smiling.png", "new_smiling_segmented.png")
    pass
