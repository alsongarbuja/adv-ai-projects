import matplotlib.pyplot as plt
import numpy as np

def visulize_maze(maze: list[list[str]], start: tuple[int, int], goal: tuple[int, int], path: list[tuple[int, int]], title: str):
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
    plt.title(title, fontsize=16)

    plt.show()

def heuristic(current, goal):
    """Calculate the Manhattan distance heuristic."""
    return abs(current[0] - goal[0]) + abs(current[1] + goal[1]);

def a_start_search(maze: list[list[str]]):
    """
    Find the shortest path in a maze using A Start Search (A*) algorithm

    Args:
        maze: A 2D list of characters representing the maze.
            '%' = wall, 'p' = start, '.' = end, ' ' = path

    Returns:
        A list of coordinates representing the shortest path, or None if no path is found.
    """

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
        return (None, None, None)

    open_list = [(0, 0, start, [start])]
    g_costs = {start: 0}

    # The direction right, left, down and up to traverse in each loop
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Variable for holding number of nodes expanded
    nodes_expanded = 0

    # variable for holding maximum depth reached and maximum fringe size
    max_depth = 0
    max_fringe = 0 # fringe size is the maximum number of nodes in the queue at any given time

    # Start of the algorithm
    while open_list:
        # Calcluating the new maximum fringe
        max_fringe = max(max_fringe, len(open_list))

        # Find and remove the node with the lowest f_cost
        current_node_index = open_list.index(min(open_list))
        _, g_cost, (row, col), path = open_list.pop(current_node_index)

        # Increasing the expanded node number by 1
        nodes_expanded += 1

        # Calculating the new maximum depth
        max_depth = max(max_depth, len(path) - 1)

        # Stop the loop when end goal is found
        if (row, col) == end:
            print(f"path cost: {len(path)-1}, nodes expanded: {nodes_expanded}, maximum depth: {max_depth}, maximum fringe size: {max_fringe}")
            return (start, end, path)

        for dr, dc in directions:
            next_row, next_col = row + dr, col + dc
            neighbor = (next_row, next_col)

            if 0 <= next_row < height and 0 <= next_col < width and maze[next_row][next_col] != "%":
                new_g_cost = g_cost + 1
                if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_g_cost
                    h_cost = heuristic(neighbor, end)
                    new_f_cost = new_g_cost + h_cost
                    new_path = path + [neighbor]
                    open_list.append((new_f_cost, new_g_cost, neighbor, new_path))

    # Return none in case no end point is found before queue is empty
    return (None, None, None)

def open_maze(file_name: str):
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
        return []

def update_maze_with_path(maze: list[list[str]], path: list[tuple[int, int]]):
    """
    Add the path to the maze if any

    Args:
      maze: The 2D list containing the maze data
      path: The list of tuples containing the shortest path given by BFS

    Returns:
      A copy of the 2D list containing the path taken by BFS using '*' in place of the path(' ')
    """

    # Creating a duplicate variable to update
    maze_copy = [list(row) for row in maze]

    # Updating the maze to add the found path with '*'
    for r, c in path:
        if maze_copy[r][c] not in ('P', '.'):
            maze_copy[r][c] = "*"

    return maze_copy

maze_relative_path = "./resources/Maze/"
mazes = ["smallMaze", "mediumMaze", "bigMaze", "openMaze"]

print("Choose a maze file to run the algorithm againts.")
for i, filename in enumerate(mazes):
    print(f"{i}) {filename}")
print("===============================================")

while True:
  try:
    file_index = int(input("Enter index: "))
    if 0<= file_index < len(mazes):
      break
    print(f"Invalid index. Please choose index between 0 - {len(mazes)-1}")
  except ValueError:
    print(f"Invalid index. Please choose index between 0 - {len(mazes)-1}")

con = open_maze(maze_relative_path+mazes[file_index]+".lay")
start, end, path = a_start_search(con)

if not start or not end or not path:
    print("Error: Start or End or Path not found")
else:
  solved_maze = update_maze_with_path(con, path)
  visulize_maze(solved_maze, start, end, path, mazes[file_index]+" Visual")
