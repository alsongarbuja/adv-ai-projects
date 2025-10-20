import time
from visual import visualize_maze
from utility import open_maze_file, show_maze_options, update_maze_with_path, find_start_goals

def dfs_multiple(maze: list[list[str]], start: tuple[int, int], end: tuple[int, int], depth: int, fringe_size: int) -> tuple[list[tuple[int, int]], int, int, int]:
    """
    Finds the shortest path in a maze using Depth-First Search (DFS) algorithm

    Args:
        maze: A 2D list of characters representing the maze.
            '%' = wall, 'p' = start, '.' = end, ' ' = path
        start: A tuple containg the coordinates of the start location
        goal: A tuple containg the coordinates of the goal location
        depth: Maximum depth
        fringe_size: Maximum fringe size
    
    Returns:
         A tuple containing list of coordinates representing the shortest path, max depth traversed, max fringe size and total nodes expanded 
    """

    # Calculate the height and width of the maze
    height = len(maze)
    width = len(maze[0])

    # Stack storing the next nodes to be explored along side the path it took
    frontier = [(start, [start])]

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
    max_depth = depth
    max_fringe = fringe_size # fringe size is the maximum number of nodes in the stack at any given time

    # Start of the algorithm
    while frontier:
        # Cacluating the new maximum fringe
        max_fringe = max(max_fringe, len(frontier))

        # Popping the last element from stack and assiging each values to their respective variables
        (row, col), path = frontier.pop()

        # Increasing the expanded node number by 1
        nodes_expanded += 1

        # Stop the loop when end goal is found
        if (row, col) == end:
            #print(f"path cost: {len(path)-1}, nodes expanded: {nodes_expanded}, maximum depth: {max_depth}, maximum fringe size: {max_fringe}")
            return (path, max_depth, max_fringe, nodes_expanded)

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
                    frontier.append(((next_row, next_col), new_path))

    # Return none in case no end point is found before stack is empty
    return ([], max_depth, max_fringe, nodes_expanded)

file_path, title = show_maze_options("DFS", True)
con = open_maze_file(file_path)

start, goals = find_start_goals(con)
final_path: list[tuple[int, int]] = []
new_start = start
max_depth = 0
max_fringe = 0
total_nodes = 0

start_time = time.perf_counter()

for goal in goals:
    new_path, dp, fs, ne = dfs_multiple(con, new_start, goal, max_depth, max_fringe)
    final_path = final_path + new_path
    new_start = goal
    max_depth = dp
    max_fringe = fs
    total_nodes += ne

end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"path cost: {len(final_path)-len(goals)}, nodes expanded: {total_nodes}, maximum depth: {max_depth}, maximum fringe size: {max_fringe}")
print(f"Elapsed time: {elapsed_time*1000}ms")

if not start or len(goals) == 0 or len(final_path) == 0:
    print("Error: Start or End or Path not found")
else:
  solved_maze = update_maze_with_path(con, final_path)
  visualize_maze(solved_maze, start, goals, final_path, title, len(final_path)-len(goals), total_nodes, max_depth, max_fringe)
