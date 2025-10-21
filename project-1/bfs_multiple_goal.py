from utility import show_maze_options, find_start_goals, open_maze_file, update_maze_with_path, ask_use_greedy_goals, greedy_goals_sorting
from visual import visualize_maze
from heuristic import HeuristicFn
from search_algorithm import bfs_search

# Show the options of mazes
file_path, title = show_maze_options(algo_used="BFS", is_multiple=True)
maze_data = open_maze_file(file_path) # Open the maze file to get the maze data

start, goals = find_start_goals(maze_data) # Find the start and goal points
final_goals = goals
new_start = start
ne = md = mf = 0
final_path = []

use_greedy_sort = ask_use_greedy_goals()

if use_greedy_sort:
  greedy_goals = greedy_goals_sorting(start, goals, HeuristicFn.MANHATTAN)
  final_goals = greedy_goals

for goal in final_goals:
  # Run the BFS search algorithm
  path, expanded_nodes, depth, fringe = bfs_search(maze_data, new_start, goal, md, mf)
  final_path = final_path + path
  ne += expanded_nodes
  md = depth
  mf = fringe
  new_start = goal

# Update the maze data with solution path
solved_maze = update_maze_with_path(maze_data, final_path)
# Visualize the solution maze
visualize_maze(solved_maze, start, goals, final_path, title, len(final_path)-len(goals), ne, md, mf)
