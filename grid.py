# Code by Adrien TIMBERT @ github.com/aleolux
import pygame
from random import random
from color_constants import *

WINDOW_HEIGHT = 768
WINDOW_WIDTH = 1024
GRID_OFFSET_X = 60
GRID_OFFSET_Y = 200

COLOR_BLANK = WHITESMOKE
COLOR_OPEN = RGB(178, 255, 102)
COLOR_CLOSED = RGB(255, 120, 120)
COLOR_WALL = RGB(120, 120, 120)
COLOR_PATH = RGB(51, 153, 255)
COLOR_LINES = WHITE
COLOR_END = RGB(0, 0, 153)
COLOR_START = RGB(76, 153, 0)

WALLS_RATE = 0.15

COLUMNS = 57  # must be odd for maze generation
ROWS = 29  # must be odd for maze generation

SPOT_WIDTH = 16
SPOT_HEIGHT = 16

GRID_AREA = ((GRID_OFFSET_X, GRID_OFFSET_Y), (GRID_OFFSET_X + COLUMNS * SPOT_WIDTH, GRID_OFFSET_Y + ROWS * SPOT_HEIGHT))


class Node:
    """Node class"""

    def __init__(self, i, j):
        self.id = "-".join([str(x) for x in [i, j]])
        self.i = i
        self.j = j
        self.x = (self.j * SPOT_WIDTH) + GRID_OFFSET_X
        self.y = (self.i * SPOT_HEIGHT) + GRID_OFFSET_Y
        self.f_score = float("inf")
        self.g_score = float("inf")
        self.color = COLOR_BLANK
        self.previous = None

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __gt__(self, other):
        return self.f_score > other.f_score

    def __str__(self):
        return f"({self.i},{self.j}, f_score: {self.f_score}, g_score: {self.g_score})"

    def get_pos(self):
        return self.i, self.j

    def make_blank(self):
        self.color = COLOR_BLANK

    def make_open(self):
        self.color = COLOR_OPEN

    def make_closed(self):
        self.color = COLOR_CLOSED

    def make_wall(self):
        self.color = COLOR_WALL

    def make_path(self):
        self.color = COLOR_PATH

    def make_start(self):
        self.color = COLOR_START

    def make_end(self):
        self.color = COLOR_END

    def is_open(self):
        return self.color == COLOR_OPEN

    def is_closed(self):
        return self.color == COLOR_CLOSED

    def is_wall(self):
        return self.color == COLOR_WALL

    def is_path(self):
        return self.color == COLOR_PATH

    def is_start(self):
        return self.color == COLOR_START

    def is_end(self):
        return self.color == COLOR_END

    def draw(self, screen):
        """Draw shape for each type of node"""
        if self.is_wall():
            pygame.draw.rect(screen, self.color, (self.x, self.y, SPOT_WIDTH, SPOT_HEIGHT))
        elif self.is_end():
            pygame.draw.circle(screen, self.color, (self.x + (SPOT_WIDTH // 2), self.y + (SPOT_HEIGHT // 2)),
                               SPOT_WIDTH // 2 - 1, 2)
            pygame.draw.circle(screen, self.color, (self.x + (SPOT_WIDTH // 2), self.y + (SPOT_HEIGHT // 2)),
                               SPOT_WIDTH // 2 - 5, 7)
        elif self.is_start():
            pygame.draw.polygon(screen, self.color,
                                points=[(self.x, self.y),
                                        (self.x + SPOT_WIDTH, self.y + (SPOT_HEIGHT // 2)),
                                        (self.x, self.y + SPOT_HEIGHT)], width=0)
        else:
            pygame.draw.circle(screen, self.color, (self.x + (SPOT_WIDTH // 2), self.y + (SPOT_HEIGHT // 2)),
                               SPOT_WIDTH // 2 - 2, 100)

    def get_neighbours(self, grid):
        """Get adjacent node in 4 directions: N, S, E, W"""
        neighbours = []
        if self.i > 0:  # South
            neighbours.append(grid[self.i - 1][self.j])
        if self.j > 0:  # West
            neighbours.append(grid[self.i][self.j - 1])
        if self.i < len(grid) - 1:  # North
            neighbours.append(grid[self.i + 1][self.j])
        if self.j < len(grid[self.i]) - 1:  # East
            neighbours.append(grid[self.i][self.j + 1])
        return neighbours


def generate_grid():
    """Create a ROWS*COLUMNS matrix with Nodes"""
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(COLUMNS):
            grid[i].append(Node(i, j))
    return grid


def build_random_walls(grid):
    """Generate randomly walls on the grid"""
    for row in grid:
        for node in row:
            rand = random()
            if rand < WALLS_RATE and not (node.is_start() or node.is_end()):
                node.make_wall()
    return


def draw_grid_lines(screen):
    """Draw grid lines on the screen"""
    for i in range(1, ROWS):
        pygame.draw.line(screen, COLOR_LINES,
                         (GRID_OFFSET_X, GRID_OFFSET_Y + (i * SPOT_HEIGHT)),
                         (GRID_OFFSET_X + COLUMNS * SPOT_WIDTH, GRID_OFFSET_Y + (i * SPOT_HEIGHT)))
    for i in range(1, COLUMNS):
        pygame.draw.line(screen, COLOR_LINES,
                         (GRID_OFFSET_X + i * SPOT_WIDTH, GRID_OFFSET_Y),
                         (GRID_OFFSET_X + i * SPOT_WIDTH, GRID_OFFSET_Y + SPOT_HEIGHT * ROWS))
    return


def draw(grid, screen):
    """draw the grid on the screen"""
    for row in grid:
        for node in row:
            # print(f"{node.i} {node.j} | {node.x} {node.y}")
            node.draw(screen)
    draw_grid_lines(screen)
    pygame.display.update()
    return


def reset_grid(grid):
    """Make all Node blank"""
    for row in grid:
        for node in row:
            node.make_blank()
    return


def clean_walls(grid):
    """Make all wall Node blank"""
    for row in grid:
        for node in row:
            if node.is_wall():
                node.make_blank()
    return


def clean(grid):
    """Make all Node blank Node except walls"""
    for row in grid:
        for node in row:
            if not (node.is_wall() or node.is_start() or node.is_end()):
                node.make_blank()
    return


def reset_start_end(grid, start=None, end=None):
    """Reset start and End positions"""
    if start is not None:
        start.make_blank()
    if end is not None:
        end.make_blank()
    default_start, default_end = (10, 10), (-10, -10)
    start, end = grid[default_start[0]][default_start[1]], grid[default_end[0]][default_end[1]]
    start.make_start()
    end.make_end()
    return start, end


def is_cursor_in_grid_area(pos):
    """Return True if cursor is within grid area"""
    x, y = pos
    return GRID_AREA[0][0] <= x <= GRID_AREA[1][0] and GRID_AREA[0][1] <= y <= GRID_AREA[1][1]


def spot_coordinates_from_cursor_position(pos):
    """Return position of cursor on the grid"""
    x, y = pos
    return int((y - GRID_OFFSET_Y) // SPOT_HEIGHT), int((x - GRID_OFFSET_X) // SPOT_WIDTH)
