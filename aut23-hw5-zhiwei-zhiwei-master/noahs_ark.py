import sys
from typing import List, Tuple, Dict
from collections import deque
from collections import defaultdict, Counter

sys.setrecursionlimit(10000)


def get_neighbors(n: int, m: int, i: int, j: int) -> List[Tuple[int, int]]:
    """
    Given a point of the grid, return its neighbors.

    Parameters
    ----------
    n : int
        Number of rows in the grid
    m : int
        Number of columns in the grid
    i : int
        Line number of the point
    j : int
        Column number of the point

    Returns
    -------
        neighbors : List[Tuple[int, int]]
    """
    direction = [(0, 1), (1, 1), (-1, 0), (-1, 1), (0, -1), (-1, -1), (1, 0), (1, -1)]
    adjacent_neighbor = []
    for direction_i, direction_j in direction:
        if 0 <= i + direction_i < n and 0 <= j + direction_j < m:
            adjacent_neighbor.append((i + direction_i, j + direction_j))
    return adjacent_neighbor


def largest_island(heights: List[List[int]]) -> List[List[bool]]:
    """
    It has been raining for 40 days and 40 nights and the whole world is underwater!
    Contemplating where to finally dock your ark, you want to find the largest island.
    You are lucky to have an exceptional topographical map that has the exact heights of all terrain.
    Unfortunately, you can't just find the largest landmass over sea level,
    as water can be trapped in valleys.

    Given an array of heights, return a bit-mask of the largest island.

    Parameters
    ----------
    heights : List[List[int]]
        A topological map of the surrounding land.
        Positive values represent heights above sea level
        and negative values, represent depth below sea level.
        A height of zero is considered underwater

    Returns
    -------
    mask : List[List[bool]]
        Boolean mask of the largest island
    """
    n = len(heights)
    m = len(heights[0])

    visited = [[False for _ in range(m)] for _ in range(n)]

    def flood_fill(i, j):
        for ni, nj in get_neighbors(n, m, i, j):
            if not visited[ni][nj] and heights[ni][nj] > heights[i][j]:
                flood_fill(ni, nj)
        visited[i][j] = True

    for i in range(n):
        for j in range(m):
            if heights[i][j] <= 0 and not visited[i][j]:
                flood_fill(i, j)

    pre_mask = [[0 for _ in range(m)] for _ in range(n)]
    # generate a map which contains all island.

    for i in range(n):
        for j in range(m):
            if visited[i][j]:
                pre_mask[i][j] = 1
            if heights[i][j] <= 0:
                pre_mask[i][j] = 0

    # base on the pre_mask map which contains all island and find the biggest one
    def dfs_iterative(grid, x, y, visited):
        stack = [(x, y)]
        #  prevent RecursionError: maximum recursion depth exceeded
        current_island = []
        area = 0

        while stack:
            x, y = stack.pop()
            if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]) or visited[x][y] or grid[x][y] == 0:
                continue

            visited[x][y] = True
            current_island.append((x, y))
            area += 1

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                stack.append((nx, ny))

        return area, current_island

    def find_largest_island_iterative(map):
        max_area = 0
        largest_island = []
        visited = [[False for _ in range(m)] for _ in range(n)]

        for i in range(n):
            for j in range(m):
                if map[i][j] == 1 and not visited[i][j]:
                    area, current_island = dfs_iterative(map, i, j, visited)
                    if area > max_area:
                        max_area = area
                        largest_island = current_island

        return max_area, largest_island

    max_area, largest_island_coords = find_largest_island_iterative(pre_mask)

    mask = [[0 for _ in range(m)] for _ in range(n)]
    for i, j in largest_island_coords:
        mask[i][j] = 1

    return mask


if __name__ == '__main__':
    # height = [[0, 1, 1, 0], [1, 2, 2, 1], [1, 2, 3, 2], [0, 1, 2, 1]]
    height = [[0, 1, 3, 2, 3], [2, 2, 2, 2, 1], [3, 3, 1, 2, 2], [2, 1, 1, 3, 3], [3, 2, 5, 1, -2]]
    largest_island(height)

# 0 1 1 0
# 1 2 2 1
# 1 2 3 2
# 0 1 2 1
