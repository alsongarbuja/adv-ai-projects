import matplotlib.pyplot as plt
import numpy as np
from collections import deque

def visulize_maze(maze, start, goal, path, filename):
    if maze is None:
        print("Error: No maze with solution found")
        return

    rows = len(maze)
    cols = len(maze[0])

    grid = np.zeros((rows, cols))
    plt.figure(figsize=(6, 6))
    plt.imshow(np.zeros_like(grid), cmap='gray')

    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == "%":
                plt.fill_between([j-0.5, j+0.5], i-0.5, i+0.5, color='skyblue')
    plt.scatter(start[1], start[0], color='green', s=50, label='Start (P)', linewidth=2)
    plt.scatter(goal[1], goal[0], color='red', s=50, label='End (.)', linewidth=2)

    # Plot the entire path as a white thin line
    if path:
        path_x, path_y = zip(*path)  # Unzip path into x and y coordinates
        plt.plot(path_y, path_x, color='yellow', linewidth=2)  # White thin line

    # Set axis labels
    plt.xlabel('Column', fontsize=14)
    plt.ylabel('Row', fontsize=14)

    # Remove internal grid lines and ticks but keep the axis lines and labels
    plt.gca().set_xticks(np.arange(0, cols, 1))
    plt.gca().set_yticks(np.arange(0, rows, 1))
    plt.gca().set_xticklabels(np.arange(0, cols, 1), fontsize=10)
    plt.gca().set_yticklabels(np.arange(0, rows, 1), fontsize=10)

    plt.grid(False)  # Disable the internal grid

    # Add axis lines but remove the inner frame
    plt.gca().spines['top'].set_color('none')
    plt.gca().spines['right'].set_color('none')

    # Adjust axis limits to fit the search space
    plt.xlim(-0.5, cols - 0.5)
    plt.ylim(rows - 0.5, -0.5)
    title = filename.replace('.lay', ' Visual')
    plt.title(title, fontsize=16)

    plt.show()


def bfs_search(maze):
    """
    Find the shortest path in a maze using Breadth-First Search (BFS) algorithm

    Args:
        maze: A 2D list of characters representing the maze.
            '%' = wall, 'p' = start, '.' = end, ' ' = path

    Returns:
        A list of coordinates representing the shortest path, or None if no path is found.
    """

    height = len(maze)
    width = len(maze[0])

    start = None
    end = None

    for r in range(height):
        for c in range(width):
            if maze[r][c] == 'P':
                start = (r, c)
            elif maze[r][c] == '.':
                end = (r, c)

    if not start or not end:
        return [None, None, None]

    queue = deque([(start, [start])])
    visited = {start}

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        (row, col), path = queue.popleft()

        if (row, col) == end:
            return [start, end, path]

        for dr, dc in directions:
            next_row, next_col = row + dr, col + dc

            if 0 <= next_row < height and 0 <= next_col < width:
                cell_content = maze[next_row][next_col]
                if cell_content != "%" and (next_row, next_col) not in visited:
                    visited.add((next_row, next_col))
                    new_path = path + [(next_row, next_col)]
                    queue.append(((next_row, next_col), new_path))

    return [None, None, None]

def open_maze(file_name):
    try:
        with open(file_name, "r") as file:
            content = [list(line.strip()) for line in file]
        return content
    except FileNotFoundError:
        print("Error, file not found")
        return None


def draw_path(maze, path):
    """Add the path to the maze if any"""
    if path is None:
        print("Error: Path not found")
        return None

    maze_copy = [list(row) for row in maze]

    for r, c in path:
        if maze_copy[r][c] not in ('p', '.'):
            maze_copy[r][c] = "*"

    return maze_copy

maze_file_name = "sample maze file.lay"
con = open_maze(maze_file_name)
[start, end, path] = bfs_search(con)
solved_maze = draw_path(con, path)

visulize_maze(solved_maze, start, end, path, maze_file_name)
