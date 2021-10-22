# Code by Adrien TIMBERT @ github.com/aleolux
# Credits:
# http://weblog.jamisbuck.org/2011/1/12/maze-generation-recursive-division-algorithm
# https://stackoverflow.com/questions/23530756/maze-recursive-division-algorithm-design
import random
import math


def create_outside_walls(grid: list):
    """Create border walls"""
    for idx, row in enumerate(grid):  # for each row
        if idx == 0 or idx == len(grid) - 1:  # fill the first and the last row
            for node in row:
                if not (node.is_start() or node.is_end()):
                    node.make_wall()
        else:  # fill the first and the last columns
            node = row[0]
            if not (node.is_start() or node.is_end()):
                node.make_wall()
            node = row[-1]
            if not (node.is_start() or node.is_end()):
                node.make_wall()
    return


def make_maze(grid, draw):
    """
    Starting point of the maze generator: uses recursive division
    - walls on even cells, doors in odd cells: require odd grid dimensions!
    """
    create_outside_walls(grid)
    add_inner_walls(random.choice([True, False]), 1, len(grid[0]) - 2, 1, len(grid) - 2, grid, draw)
    return


def add_inner_walls(is_horizontal, min_x, max_x, min_y, max_y, grid, draw):
    """Inner walls generation"""
    if is_horizontal:
        if max_x - min_x < 2:
            return

        y = random.choice([_ for _ in range(min_y, max_y + 1) if _ % 2 == 0])
        add_horizontal_wall(min_x, max_x, y, grid, draw)

        add_inner_walls(not is_horizontal, min_x, max_x, min_y, y - 1, grid, draw)
        add_inner_walls(not is_horizontal, min_x, max_x, y + 1, max_y, grid, draw)

    else:
        if max_y - min_y < 2:
            return

        x = random.choice([_ for _ in range(min_x, max_x + 1) if _ % 2 == 0])
        add_vertical_wall(min_y, max_y, x, grid, draw)

        add_inner_walls(not is_horizontal, min_x, x - 1, min_y, max_y, grid, draw)
        add_inner_walls(not is_horizontal, x + 1, max_x, min_y, max_y, grid, draw)
    return


def add_horizontal_wall(min_x, max_x, y, grid, draw):
    """Draw am horizontal wall"""
    hole = math.floor(random_number(min_x, max_x) / 2) * 2 + 1

    for i in range(min_x, max_x + 1):
        if i != hole:
            if not (grid[y][i].is_start() or grid[y][i].is_end()):
                grid[y][i].make_wall()
        draw()
    return


def add_vertical_wall(min_y, max_y, x, grid, draw):
    """Draw a vertical wall"""
    hole = math.floor(random_number(min_y, max_y) / 2) * 2 + 1

    for i in range(min_y, max_y + 1):
        if i != hole:
            if not (grid[i][x].is_start() or grid[i][x].is_end()):
                grid[i][x].make_wall()
        draw()
    return


def random_number(min_num, max_num):
    """Random number drawer"""
    return math.floor(random.random() * (max_num - min_num + 1) + min_num)
