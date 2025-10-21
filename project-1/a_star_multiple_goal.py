from utility import show_maze_options, find_start_goals, open_maze_file, update_maze_with_path, show_heuristic_options, ask_allow_diagonal, greedy_goals_sorting, ask_use_greedy_goals
from visual import visualize_maze
from search_algorithm import a_star_search

# Show the options of mazes
file_path, title = show_maze_options(algo_used="A*", is_multiple=True)
maze_data = open_maze_file(file_path) # Open the maze file to get the maze data

hf = show_heuristic_options() # Show options of heuristic function
allow_diagonal = ask_allow_diagonal()
use_greedy_sort = ask_use_greedy_goals()

start, goals = find_start_goals(maze_data) # Find the start and goal points
new_start = start
final_goals = goals
ne = md = mf = 0
final_path = []

if use_greedy_sort:
  greedy_goals = greedy_goals_sorting(start, goals, hf)
  final_goals = greedy_goals

for goal in final_goals:
  # Run the a star search algorithm
  path, expanded_nodes, depth, fringe = a_star_search(
    maze_data,
    new_start,
    goal,
    heuristic=hf,
    allow_diagonal=allow_diagonal,
    fringe=mf,
    depth=md
  )
  final_path = final_path + path
  ne += expanded_nodes
  md = depth
  mf = fringe
  new_start = goal

# Update the maze data with solution path
solved_maze = update_maze_with_path(maze_data, final_path)
# Visualize the solution maze
visualize_maze(solved_maze, start, goals, final_path, title, len(final_path)-len(goals), ne, md, mf)
