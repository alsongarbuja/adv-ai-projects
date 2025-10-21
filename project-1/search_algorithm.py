import heapq
from collections import deque

from heuristic import heuristic_calculation
from utility import HeuristicFn

def bfs_search(
    maze: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
    depth: int = 0,
    fringe: int = 0,
    nodes: int = 0,
  ):
  """
  Finds the shortest path of the maze using Breadth first search algorithm

  Args:
    maze: A list of lists of string containing maze data
          where '%' is wall, 'P' is start and '.' is end
    start: Tuple containing start coordinate
    goal: Tuple containing end coordinate
    depth: Maximum depth from previous loop, default 0
    fringe: Maximum fringe from previous loop, default 0
    nodes: Number of nodes expanded from previous loop, default 0

  Returns:
    Tuple containing the path list, total nodes expanded, maximum depth, maximum fringe
  """

  height = len(maze)
  width = len(maze[0])

  # List of tuple containing current node, path it took and depth of the node
  # Using a queue for its FIFO (First in First out) property
  frontier = deque([(start, [start], 0)])
  visited = {start} # Set of nodes already visited

  # Variables for metrics
  max_depth = depth
  max_fringe = fringe
  nodes_expanded = nodes

  # Directions to traverse (up, down, left and right)
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

  while frontier:
    max_fringe = max(max_fringe, len(frontier)) # Calculate the max fringe
    (row, col), path, depth = frontier.popleft() # Pop the node that was inserted first
    nodes_expanded += 1 # Increase the nodes expanded variable

    # Break the while loop if goal is found and return the path, nodes expanded, maximum depth and maximum fringe
    if (row, col) == goal:
      return (path, nodes_expanded, max_depth, max_fringe)

    max_depth = max(max_depth, depth) # Calculate the max depth

    # For each direction
    for dr, dc in directions:
      nr, nc = row+dr, col+dc
      neighbor = (nr, nc)

      # Proceed only if the neighbor coordinate is within the maze bound and not a wall
      if 0 <= nr < height and 0 <= nc < width and maze[nr][nc] != "%":
        # Proceed only if the neighbor is not visited
        if neighbor not in visited:
          visited.add(neighbor)
          new_path = path + [neighbor]
          frontier.append((neighbor, new_path, depth+1))

  # If frontier is empty before end goal is found
  return (None, None, None, None)

def dfs_search(
    maze: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
    depth: int = 0,
    fringe: int = 0,
    nodes: int = 0,
  ):
  """
  Finds the shortest path of the maze using Depth first search algorithm

  Args:
    maze: A list of lists of string containing maze data
          where '%' is wall, 'P' is start and '.' is end
    start: Tuple containing start coordinate
    goal: Tuple containing end coordinate
    depth: Maximum depth from previous loop, default 0
    fringe: Maximum fringe from previous loop, default 0
    nodes: Number of nodes expanded from previous loop, default 0

  Returns:
    Tuple containing the path list, total nodes expanded, maximum depth, maximum fringe
  """

  height = len(maze)
  width = len(maze[0])

  # List of tuple containing current node and the list of path it took
  # Using a stack for its LIFO (Last in First out) property
  frontier = [(start, [start])]
  visited = {start} # Set of nodes already visited

  # Variables for metrics
  max_depth = depth
  max_fringe = fringe
  nodes_expanded = nodes

  # Directions to traverse (up, down, left and right)
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

  #directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
  #directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
  #directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  #directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

  while frontier:
    max_fringe = max(max_fringe, len(frontier)) # Calculate the max fringe
    (row, col), path = frontier.pop() # Pop the node that was inserted first
    nodes_expanded += 1 # Increase the nodes expanded variable

    # Break the while loop if goal is found and return the path, nodes expanded, maximum depth and maximum fringe
    if (row, col) == goal:
      return (path, nodes_expanded, max_depth, max_fringe)

    max_depth = max(max_depth, len(path)) # Calculate the max depth

    # For each direction
    for dr, dc in directions:
      nr, nc = row+dr, col+dc
      neighbor = (nr, nc)

      # Proceed only if the neighbor coordinate is within the maze bound and not a wall
      if 0 <= nr < height and 0 <= nc < width and maze[nr][nc] != "%":
        # Proceed only if the neighbor is not visited
        if neighbor not in visited:
          visited.add(neighbor)
          new_path = path + [neighbor]
          frontier.append((neighbor, new_path))

  # If frontier is empty before end goal is found
  return (None, None, None, None)

def a_star_search(
    maze: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
    heuristic: HeuristicFn = HeuristicFn.MANHATTAN,
    allow_diagonal: bool = False,
    depth: int = 0,
    fringe: int = 0,
    nodes: int = 0,
  ):
  """
  Finds the shortest path of the maze using A star search algorithm

  Args:
    maze: A list of lists of string containing maze data
          where '%' is wall, 'P' is start and '.' is end
    start: Tuple containing start coordinate
    goal: Tuple containing end coordinate
    heuristic: Enum of heuristic function that can be used, default to manhattan
    allow_diagonal: Boolean to determine if diagonal movement is allowed or not, default False
    depth: Maximum depth from previous loop, default 0
    fringe: Maximum fringe from previous loop, default 0
    nodes: Number of nodes expanded from previous loop, default 0

  Returns:
    Tuple containing the path list, total nodes expanded, maximum depth, maximum fringe
  """

  height = len(maze)
  width = len(maze[0])

  # List of tuple containing f_cost(actual cost), g_cost(estimate cost), current node and list of path it took
  # Using a priority queue for its priority based pop and FIFO (First in First out) properties
  frontier = [(0, 0, start, [start])]
  g_costs = {start: 0} # Set containing the estimated cost from each path

  # Variables for metrics
  max_depth = depth
  max_fringe = fringe
  nodes_expanded = nodes

  # Directions to traverse (up, down, left and right) and (down-left, down-right, up-left and up-right) for diagonal movement
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] if not allow_diagonal else [(-1, 0), (1, 0), (0, -1), (0, 1), (1, -1), (1, 1), (-1, -1), (-1, 1)]

  while frontier:
    max_fringe = max(max_fringe, len(frontier)) # Calculate the max fringe
    _, g_cost, (row, col), path = heapq.heappop(frontier) # Pop the node with least amount of f_cost
    nodes_expanded += 1 # Increase the nodes expanded variable
    max_depth = max(max_depth, len(path)-1) # Calculate the max depth

    # Break the while loop if goal is found and return the path, nodes expanded, maximum depth and maximum fringe
    if (row, col) == goal:
      return (path, nodes_expanded, max_depth, max_fringe)

    # For each direction
    for dr, dc in directions:
      nr, nc = row+dr, col+dc
      neighbor = (nr, nc)

      # Proceed only if the neighbor coordinate is within the maze bound and not a wall
      if 0 <= nr < height and 0 <= nc < width and maze[nr][nc] != "%":
        new_g_cost = g_cost + 1 # Calculate new estimation cost for the neighbor node

        # Proceed only either the neighbor is visited first time or the estimation cost has decreased than previously recorded cost for the neighbor node
        if neighbor not in g_costs or new_g_cost < g_costs[neighbor]:
          g_costs[neighbor] = new_g_cost
          h_cost = heuristic_calculation(neighbor, goal, heuristic)
          new_f_cost = new_g_cost + h_cost
          new_path = path + [neighbor]
          heapq.heappush(frontier, (new_f_cost, new_g_cost, neighbor, new_path))
          # Use the -new_g_cost when using Chebyshev heuristic function and want less node expanded in open maze
          # heapq.heappush(frontier, (new_f_cost, -new_g_cost, neighbor, new_path))

  # If frontier is empty before end goal is found
  return (None, None, None, None)
