import matplotlib.pyplot as plt
import numpy as np

def visulize_maze(maze, start, goal, path, filename):
    if maze is None:
        print("Error: No maze with solution found")
        return

    rows = len(maze)
    cols = len(maze[0])

    grid = np.zeros((rows, cols))
    plt.figure(figsize=(6, 6))
    plt.imshow(np.zeros_like(grid), cmap='grey')

    # Fill the wall as skyblue color
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == "%":
                plt.fill_between([j-0.4, j+0.4], i-0.4, i+0.4, color='skyblue')

    # Add a scatter plot (circle) with color orange in place of start node
    plt.scatter(start[1], start[0], color='orange', label='Start (P)', linewidth=2)

    # Add a scatter plot (circle) with color green in place of end node
    plt.scatter(goal[1], goal[0], color='green', label='End (.)', linewidth=2)

    # Plot the entire path as a yellow thin line
    if path:
        path_x, path_y = zip(*path)  # Unzip path into x and y coordinates
        plt.plot(path_y, path_x, color='yellow', linewidth=2)

    # Set the title of the image
    main_title = filename.split("/")
    title = main_title[len(main_title)-1].replace('.lay', ' Visual')
    plt.title(title, fontsize=16)

    plt.show()


def dfs_search(maze):
    """
    Find the shortest path in a maze using Depth-First Search (DFS) algorithm

    Args:
        maze: A 2D list of characters representing the maze.
            '%' = wall, 'p' = start, '.' = end, ' ' = path

    Returns:
        A list of coordinates representing the shortest path, or None if no path is found.
    """

    # Return if invalid maze is passed to the function
    if maze is None:
        return [None, None, None]

    # Calculate the height and width of the maze
    height = len(maze)
    width = len(maze[0])

    start = None
    end = None

    # Looking for the start('P') and end('.') nodes and store them in respective variables
    for r in range(height):
        for c in range(width):
            if maze[r][c] == 'P':
                start = (r, c)
            elif maze[r][c] == '.':
                end = (r, c)

    # Return none in case either start or end or both variables are not found
    if not start or not end:
        return [None, None, None]

    # Stack storing the next nodes to be explored along side the path it took
    stack = [(start, [start])]

    # Set of nodes that are already visited by the algorithm
    visited = {start}

    # The direction right, left, down and up to traverse in each loop
    # Checking choosing different direction to explore first to see changes in the metrics
    # directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    # directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    # directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Variable for holding number of nodes expanded
    nodes_expanded = 0

    # variable for holding maximum depth reached and maximum fringe size
    max_depth = 0
    max_fringe = 0 # fringe size is the maximum number of nodes in the stack at any given time

    # Start of the algorithm
    while stack:
        # Cacluating the new maximum fringe
        max_fringe = max(max_fringe, len(stack))

        # Popping the last element from stack and assiging each values to their respective variables
        (row, col), path = stack.pop()

        # Increasing the expanded node number by 1
        nodes_expanded += 1

        # Stop the loop when end goal is found
        if (row, col) == end:
            print(f"path cost: {len(path)-1}, nodes expanded: {nodes_expanded}, maximum depth: {max_depth}, maximum fringe size: {max_fringe}")
            return [start, end, path]

        # Calculate the new maximum depth
        max_depth = max(max_depth, len(path))

        # Travese on each direction from current node to check for the availble paths
        for dr, dc in directions:
            next_row, next_col = row + dr, col + dc

            # Check if the next node is out of range (i.e invalid)
            if 0 <= next_row < height and 0 <= next_col < width:
                cell_content = maze[next_row][next_col]

                # Check if the next node is a wall('%') or already visited
                if cell_content != "%" and (next_row, next_col) not in visited:
                    # If not visited and not a wall added the next node to the visited set
                    visited.add((next_row, next_col))

                    # Add it to the path list it came from
                    new_path = path + [(next_row, next_col)]

                    # Add it to the stack for exploration in next loop
                    stack.append(((next_row, next_col), new_path))

    # Return none in case no end point is found before stack is empty
    return [None, None, None]

def open_maze(file_name):
    """
    Open the maze file through given file_name and return the 2D matrix form

    Args:
      file_name: The relative path to the file

    Returns:
      A 2D matrix (2D list) containing either the wall('%'), path(' '), start('P') or end('.') in each cell of the maze
    """
    try:
        with open(file_name, "r") as file:
            content = [list(line.strip()) for line in file]
        return content
    except FileNotFoundError:
        print("Error, file not found")
        return None

def draw_path(maze, path):
    """
    Add the path to the maze if any

    Args:
      maze: The 2D list containing the maze data
      path: The list of tuples containing the shortest path given by DFS

    Returns:
      A copy of the 2D list containing the path taken by DFS using '*' in place of the path(' ')
    """
    if path is None:
        print("Error: Path not found")
        return None

    maze_copy = [list(row) for row in maze]

    for r, c in path:
        if maze_copy[r][c] not in ('P', '.'):
            maze_copy[r][c] = "*"

    return maze_copy

maze_file_name = "./resources/Maze/bigMaze.lay"
con = open_maze(maze_file_name)
[start, end, path] = dfs_search(con)
solved_maze = draw_path(con, path)

visulize_maze(solved_maze, start, end, path, maze_file_name)
