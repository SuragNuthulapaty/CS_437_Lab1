import math
import heapq
import enum

class DIR(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP_RIGHT= 4
    DOWN_RIGHT = 5
    DOWN_LEFT = 6
    UP_LEFT = 7

"""
https://www.geeksforgeeks.org/a-search-algorithm-in-python/

This code was nearly entirely pulled from the above link which was a resource we used 
in order to learn how A* works, and how to implement it specifically

The big changes we made was the back tracking approach. We created the DIR class
and developed the trace_path function to return distances instead of just printing
what the path the algirithm foudn was. Doing it this way allowed us to command the 
car to moce in specific directions
"""

class Cell:
    def __init__(self):
        self.parent_i = 0
        self.parent_j = 0
        self.f = float('inf')
        self.g = float('inf')
        self.h = 0

ROW = 300
COL = 100

def is_valid(src):
    row, col = src
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

def is_unblocked(grid, src):
    row, col = src
    return grid[row][col] == 0

def is_destination(src, dest):
    row, col = src
    return row == dest[0] and col == dest[1]

def calculate_h_value(src, dest):
    row, col = src
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

def trace_path(cell_details, dest):
    path = []
    row = dest[0]
    col = dest[1]

    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    path.append((row, col))
    path.reverse()

    print(path)
    
    dirs = []

    for i in range(1, len(path)):
        delta_x = path[i][0] - path[i - 1][0]
        delta_y = path[i][1] - path[i - 1][1]

        if delta_x == 1 and delta_y == 0:
            dirs.append(DIR.RIGHT)
        elif delta_x == 1 and delta_y == -1:
            dirs.append(DIR.DOWN_RIGHT)
        elif delta_x == 0 and delta_y == -1:
            dirs.append(DIR.DOWN)
        elif delta_x == -1 and delta_y == -1:
            dirs.append(DIR.DOWN_LEFT)
        elif delta_x == -1 and delta_y == 0:
            dirs.append(DIR.LEFT)
        elif delta_x == -1 and delta_y == 1:
            dirs.append(DIR.UP_LEFT)
        elif delta_x == 0 and delta_y == 1:
            dirs.append(DIR.UP)
        elif delta_x == 1 and delta_y == 1:
            dirs.append(DIR.UP_RIGHT)
    
    return dirs

def a_star_search(grid, src, dest):
    if not is_valid(src) or not is_valid(dest):
        return []

    if not is_unblocked(grid, src) or not is_unblocked(grid, dest):
        return []

    if is_destination(src, dest):
        return []

    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    found_dest = False

    while len(open_list) > 0:
        p = heapq.heappop(open_list)

        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            if is_valid((new_i, new_j)) and is_unblocked(grid, (new_i, new_j)) and not closed_list[new_i][new_j]:
                if is_destination((new_i, new_j), dest):
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    dirs = trace_path(cell_details, dest)
                    found_dest = True
                    return dirs, False
                else:
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value((new_i, new_j), dest)
                    f_new = g_new + h_new

                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    if not found_dest:
        print("Failed to find the destination cell")
    
    return [DIR.DOWN], True
