from utility import show_maze_options, find_start_goals, open_maze_file, update_maze_with_path, HeuristicFn, show_heuristic_options
from visual import visualize_maze
from search_algorithm import a_star_search

# Show the options of mazes
file_path, title = show_maze_options(algo_used="A*")
maze_data = open_maze_file(file_path) # Open the maze file to get the maze data

start, goals = find_start_goals(maze_data) # Find the start and goal points

hf = show_heuristic_options() # Show option for heuristic functions

# Run the a star search algorithm
path, ne, md, mf = a_star_search(maze_data, start, goals[0], hf, allow_diagonal=True if hf != HeuristicFn.MANHATTAN else False)

# Update the maze data with solution path
solved_maze = update_maze_with_path(maze_data, path)
# Visualize the solution maze
visualize_maze(solved_maze, start, goals, path, title, len(path)-1, ne, md, mf)
