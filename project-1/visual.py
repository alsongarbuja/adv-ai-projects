import matplotlib.pyplot as plt
import numpy as np

def visualize_maze(maze: list[list[str]], start: tuple[int, int], goals: list[tuple[int, int]], path: list[tuple[int, int]], title: str) -> None:
    """
    Simple function to visualize the maze after finding the shortest path

    Args:
        maze: A 2D matrix containing the maze data with path denoted by '*'
        start: A tuple for start position
        goals: List of tuples of all the goal positions
        path: List of tuples which are the path taken by the algorithm
        title: A string containing the title to show above the visual
    """
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
    
    for goal in goals:
        # Add a scatter plot (circle) with color green in place of end node
        plt.scatter(goal[1], goal[0], color='green', label='End (.)', linewidth=2)

    # Plot the entire path as a yellow thin line
    if path:
        path_x, path_y = zip(*path)  # Unzip path into x and y coordinates
        plt.plot(path_y, path_x, color='yellow', linewidth=2)

    # Set the title of the image
    plt.title(title, fontsize=16)
    plt.xticks([])
    plt.yticks([])
    plt.show()
