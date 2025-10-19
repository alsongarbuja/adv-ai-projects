import heapq
import time
from visual import visualize_maze
from utility import open_maze_file, show_maze_options, update_maze_with_path, find_start_goals

def heuristic(current: tuple[int, int], goal: tuple[int, int]) -> int:
    """Calculates the Manhattan distance heuristic."""
    return abs(current[0] - goal[0]) + abs(current[1] + goal[1]);

def a_start_search(maze: list[list[str]], start: tuple[int, int], end: tuple[int, int], depth: int, fringe_size: int) -> tuple[list[tuple[int, int]], int, int, int]:
    """
    Finds the shortest path in a maze using A Start Search (A*) algorithm

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

    frontier = []
    heapq.heappush(frontier, (0, 0, start, [start]))
    g_costs = {start: 0}

    # The direction right, left, down and up to traverse in each loop
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Variable for holding number of nodes expanded
    nodes_expanded = 0

    # variable for holding maximum depth reached and maximum fringe size
    max_depth = depth
    max_fringe = fringe_size # fringe size is the maximum number of nodes in the queue at any given time

    # Start of the algorithm
    while frontier:
        # Calcluating the new maximum fringe
        max_fringe = max(max_fringe, len(frontier))

        # Find and remove the node with the lowest f_cost
        _, g_cost, (row, col), path = heapq.heappop(frontier)

        # Increasing the expanded node number by 1
        nodes_expanded += 1

        # Calculating the new maximum depth
        max_depth = max(max_depth, len(path) - 1)

        # Stop the loop when end goal is found
        if (row, col) == end:
            #print(f"path cost: {len(path)-1}, nodes expanded: {nodes_expanded}, maximum depth: {max_depth}, maximum fringe size: {max_fringe}")
            return (path, max_depth, max_fringe, nodes_expanded)

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
                    heapq.heappush(frontier, (new_f_cost, new_g_cost, neighbor, new_path))

    # Return none in case no end point is found before queue is empty
    return ([], max_depth, max_fringe, nodes_expanded)

file_path, title = show_maze_options(True)
con = open_maze_file(file_path)

start, goals = find_start_goals(con)
final_path: list[tuple[int, int]] = []
new_start = start
max_depth = 0
max_fringe = 0
total_nodes = 0

start_time = time.perf_counter()

for goal in goals:
    new_path, md, mf, ne = a_start_search(con, new_start, goal, max_depth, max_fringe)
    final_path = final_path + new_path
    new_start = goal
    max_depth = md
    max_fringe = mf
    total_nodes += ne
    
end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"path cost: {len(final_path)-len(goals)}, nodes expanded: {total_nodes}, maximum depth: {max_depth}, maximum fringe size: {max_fringe}")
print(f"Time elapsed: {elapsed_time * 1000} ms")

if not start or len(goals) == 0 or len(final_path) == 0:
    print("Error: Start or End or Path not found")
else:
    solved_maze = update_maze_with_path(con, final_path)
    visualize_maze(solved_maze, start, goals, final_path, title)
