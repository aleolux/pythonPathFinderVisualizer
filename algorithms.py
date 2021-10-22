# Code by Adrien TIMBERT @ github.com/aleolux
import pygame
import sys
from grid import Node
from queue import PriorityQueue, SimpleQueue


def heuristic(a: Node, b: Node, is_dijkstra=False):
    """Heuristic function, uses Manhattan distance by default"""
    if is_dijkstra:
        return 0
    return abs(a.i - b.i) + abs(a.j - b.j)


def build_path(node: Node, came_from: dict, draw):
    """build and draw path"""
    path = []
    while node in came_from:
        path.append(node)
        node = came_from[node]
        if not (node.is_end() or node.is_start()):
            node.make_path()
            draw()
    return path


def a_star(start: Node, end: Node, grid: list, is_dijkstra: bool, draw):
    """
    A* algorithm using minHeap
    https://en.wikipedia.org/wiki/A*_search_algorithm
    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """

    f_scores = {node: float("inf") for row in grid for node in row}
    g_scores = f_scores.copy()
    came_from = {}
    counter = 0  # just a tie breaker if two nodes have the same f score

    f_scores[start] = heuristic(start, end)
    g_scores[start] = 0

    open_set_hash = {start}
    open_set = PriorityQueue()
    open_set.put((0, counter, start))

    while len(open_set_hash) > 0:
        for event in pygame.event.get():  # event handler for on quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_f, current_g, current_node = open_set.get()

        if current_node == end:
            current_node.make_end()
            return build_path(current_node, came_from, draw)

        open_set_hash.remove(current_node)

        if current_node != start and current_node != end:
            current_node.make_closed()

        neighbours = current_node.get_neighbours(grid)
        for neighbor in neighbours:
            tentative_g_score = current_g + 1  # it's a 2D grid with step 1

            if neighbor.is_wall() or tentative_g_score >= g_scores[neighbor]:
                continue

            came_from[neighbor] = current_node
            g_scores[neighbor] = tentative_g_score
            f_scores[neighbor] = tentative_g_score + heuristic(neighbor, end, is_dijkstra)

            if neighbor not in open_set_hash:
                counter += 1
                neighbor.make_open()
                open_set_hash.add(neighbor)
                open_set.put((f_scores[neighbor], counter, neighbor))

        draw()
    return []


def bfs(start: Node, end: Node, grid: list, draw):
    """
    BFS algorithm
    https://en.wikipedia.org/wiki/Breadth-first_search
    """
    queue = SimpleQueue()
    queue.put(start)

    open_set_hash = {start}
    came_from = {}

    while not queue.empty():
        for event in pygame.event.get():  # event handler for on quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_node = queue.get()
        open_set_hash.remove(current_node)

        if current_node == end:
            current_node.make_end()
            return build_path(current_node, came_from, draw)

        if not current_node.is_start():
            current_node.make_closed()

        neighbours = current_node.get_neighbours(grid)
        for neighbor in neighbours:
            if neighbor.is_wall() or neighbor.is_closed() or neighbor.is_start():
                continue

            if neighbor == end:
                came_from[neighbor] = current_node
                neighbor.make_end()
                return build_path(current_node, came_from, draw)

            if neighbor not in open_set_hash:
                neighbor.make_open()
                open_set_hash.add(neighbor)
                queue.put(neighbor)
                came_from[neighbor] = current_node

        draw()
    return []


def dfs_iterative(start: Node, end: Node, grid: list, draw):
    """
    DFS iterative algorithm
    https://en.wikipedia.org/wiki/Depth-first_search#:~:text=Depth%2Dfirst%20search%20(DFS),along%20each%20branch%20before%20backtracking
    """
    stack = [start]
    came_from = {}

    while len(stack):
        for event in pygame.event.get():  # event handler for on quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_node = stack.pop()

        if current_node == end:
            current_node.make_end()
            return build_path(current_node, came_from, draw)

        if not current_node.is_start():
            current_node.make_closed()

        neighbours = current_node.get_neighbours(grid)
        for neighbor in neighbours:
            if neighbor.is_wall() or neighbor.is_closed() or neighbor.is_start():
                continue

            stack.append(neighbor)
            neighbor.make_open()
            came_from[neighbor] = current_node

        draw()
    return []
