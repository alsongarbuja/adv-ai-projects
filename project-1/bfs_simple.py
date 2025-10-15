import time
from collections import deque
from visual import visualize_maze
from utility import open_maze_file, update_maze_with_path, show_maze_options

def bfs_search(maze: list[list[str]]):
    """
    Find the shortest path in a maze using Breadth-First Search (BFS) algorithm

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

    # Queue storing the next nodes to be explored along side the path it took and the depth it is in
    queue = deque([(start, [start], 0)])

    # Set of nodes that are already visited by the algorithm
    visited = {start}

    # The direction right, left, down and up to traverse in each loop
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Variable for holding number of nodes expanded
    nodes_expanded = 0

    # variable for holding maximum depth reached and maximum fringe size
    max_depth = 0
    max_fringe = 0 # fringe size is the maximum number of nodes in the queue at any given time

    # Start of the algorithm
    while queue:
        # Cacluating the new maximum fringe
        max_fringe = max(max_fringe, len(queue))

        # Popping the first element from queue and assiging each values to their respective variables
        (row, col), path, depth = queue.popleft()

        # Increasing the expanded node number by 1
        nodes_expanded += 1

        # Stop the loop when end goal is found
        if (row, col) == end:
            print(f"path cost: {len(path)-1}, nodes expanded: {nodes_expanded}, maximum depth: {max_depth}, maximum fringe size: {max_fringe}")
            return (start, end, path)

        # Calculate the new maximum depth
        max_depth = max(max_depth, depth)

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

                    # Add it to the queue for exploration in next loop
                    queue.append(((next_row, next_col), new_path, depth+1))

    # Return none in case no end point is found before queue is empty
    return (None, None, None)

file_path, title = show_maze_options()
con = open_maze_file(file_path)

start_time = time.perf_counter()
start, end, path = bfs_search(con)
end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"Time elapsed: {elapsed_time * 1000} ms")

if not start or not end or not path:
    print("Error: Start or End or Path not found")
else:
  solved_maze = update_maze_with_path(con, path)
  visualize_maze(solved_maze, start, [end], path, title)
