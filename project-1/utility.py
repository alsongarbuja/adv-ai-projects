from enum import Enum

class HeuristicFn(Enum):
    MANHATTAN = "Manhattan"
    EUCLIDEAN = "Euclidean"
    CHEBYSHEV = "Chebyshev"

def open_maze_file(file_name: str) -> list[list[str]]:
    """
    Open the maze file through given file_name and return the 2D matrix form

    Args:
      file_name: The relative path to the file

    Returns:
      A 2D matrix (2D list) containing either the wall('%'), path(' '), start('P') or end('.') in each cell of the maze
    """
    try:
        with open(file_name, "r") as file:
            content = [list(line.strip()) for line in file]
        return content
    except FileNotFoundError:
        print("Error, file not found")
        return []

def update_maze_with_path(maze: list[list[str]], path: list[tuple[int, int]]):
    """
    Add the path to the maze

    Args:
      maze: The 2D list containing the maze data
      path: The list of tuples containing the shortest path given by BFS

    Returns:
      A copy of the 2D list containing the path taken by BFS using '*' in place of the path(' ')
    """

    # Creating a duplicate variable to update
    maze_copy = [list(row) for row in maze]

    # Updating the maze to add the found path with '*'
    for r, c in path:
        if maze_copy[r][c] not in ('P', '.'):
            maze_copy[r][c] = "*"

    return maze_copy

def show_maze_options(algo_used: str, is_multiple: bool = False) -> tuple[str, str]:
    """
    Simple function to show correct maze options according to the type of alogirthm running

    Args:
        is_multiple: A boolean denoting if the algorith is for simple mazes or multiple goal type pages
        algo_used: Abbrebated form of the algorithm used

    Returns:
        A tuple containing the file path and title to be used in visualizing
    """
    maze_relative_path = "./resources/Maze/"
    mazes = ["smallSearch", "tinySearch", "trickySearch"] if is_multiple else ["smallMaze", "mediumMaze", "bigMaze", "openMaze"]

    print("Choose a maze file to run the algorithm againts.")
    for i, filename in enumerate(mazes):
        print(f"{i}) {filename}")
    print("===============================================")

    while True:
        try:
            file_index = int(input("Enter index: "))
            if 0<= file_index < len(mazes):
                break
            print(f"Invalid index. Please choose index between 0 - {len(mazes)-1}")
        except ValueError:
            print(f"Invalid index. Please choose index between 0 - {len(mazes)-1}")

    file_path = maze_relative_path+mazes[file_index]+".lay"
    return (file_path, mazes[file_index]+" Visualized ("+algo_used+")")

def show_heuristic_options():
    """
    Simple function to show heursitic functions options to choose

    Returns:
      The heuristic function choosen by user
    """

    print("Choose a heuristic function to use.")
    for i, hf in enumerate(HeuristicFn):
        print(f"{i}) {hf}")
    print("===============================================")

    while True:
        try:
            file_index = int(input("Enter index: "))
            if 0<= file_index < len(HeuristicFn):
                break
            print(f"Invalid index. Please choose index between 0 - {len(HeuristicFn)-1}")
        except ValueError:
            print(f"Invalid index. Please choose index between 0 - {len(HeuristicFn)-1}")

    return list(HeuristicFn)[file_index]

def ask_allow_diagonal():
    """
    Simple function to ask user if diagonal movement is allowed or not

    Returns:
      Boolean answer by user
    """

    while True:
      answer = input("Allow diagonal movement? (Y/N)")
      if answer == "Y" or answer == "y":
          return True
      elif answer == "N" or answer == "n":
          return False
      else:
        print(f"Invalid index. Please choose index between 0 - {len(HeuristicFn)-1}")

def find_start_goals(maze: list[list[str]]) -> tuple[tuple[int, int], list[tuple[int, int]]]:
    """
    Simple funtion to return the start and goals tuples

    Args:
        maze: A 2D list of characters representing the maze.

    Returns:
        Tuple of start and goals tuples.
    """
    start = (0, 0)
    goals: list[tuple[int, int]] = []

    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == 'P':
                start = (r, c)
            if maze[r][c] == '.':
                goals.append((r, c))

    return (start, goals)
