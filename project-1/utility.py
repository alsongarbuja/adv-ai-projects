
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

def show_maze_options(is_multiple: bool = False) -> tuple[str, str]:
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
    return (file_path, mazes[file_index]+" Visualized")

