from visual import visualize_maze
from utility import open_maze_file, update_maze_with_path, show_maze_options, find_start_goals

from search_algorithm import bfs_search

# Show the options of mazes
file_path, title = show_maze_options("BFS")
maze_data = open_maze_file(file_path) # Open the maze file to get the maze data
start, goals = find_start_goals(maze_data) # Find the start and goal points

# Run the BFS search algorithm
path, ne, md, mf = bfs_search(maze_data, start, goals[0])

# Update the maze data with solution path
solved_maze = update_maze_with_path(maze_data, path)
# Visualize the solution maze
visualize_maze(solved_maze, start, goals, path, title, len(path)-1, ne, md, mf)
