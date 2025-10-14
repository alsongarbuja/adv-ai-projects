import heapq
import time
from visual import visualize_maze
from utility import open_maze_file, update_maze_with_path, show_maze_options

def heuristic(current: tuple[int, int], goal: tuple[int, int]) -> int:
    """Calculate the Manhattan distance heuristic."""
    return abs(current[0] - goal[0]) + abs(current[1] + goal[1]);

def a_start_search(maze: list[list[str]]) -> tuple[tuple[int, int] | None, tuple[int, int] | None, list[tuple[int, int]] | None]:
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

    open_list = []
    heapq.heappush(open_list, (0, 0, start, [start]))
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
        _, g_cost, (row, col), path = heapq.heappop(open_list)

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
                    heapq.heappush(open_list, (new_f_cost, new_g_cost, neighbor, new_path))

    # Return none in case no end point is found before queue is empty
    return (None, None, None)

file_path, title = show_maze_options()
con = open_maze_file(file_path)

start_time = time.perf_counter()
start, end, path = a_start_search(con)
end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"Time elapsed: {elapsed_time * 1000} ms")

if not start or not end or not path:
    print("Error: Start or End or Path not found")
else:
    solved_maze = update_maze_with_path(con, path)
    visualize_maze(solved_maze, start, [end], path, title)
