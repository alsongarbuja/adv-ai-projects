# Project 1 (Search Algorithm)

In this project we had to search a 2D maze for the shortest path from starting point `'P'` to end point `'.'`.

We created 3 algorithms [BFS](https://en.wikipedia.org/wiki/Breadth-first_search), [DFS](https://en.wikipedia.org/wiki/Depth-first_search), and [A\*](https://en.wikipedia.org/wiki/A*_search_algorithm) to find the paths.

There are two parts to the project.

### Part 1: Basic path finding

Here we have 4 mazes [Small Maze](https://github.com/alsongarbuja/adv-ai-projects/blob/main/project-1/resources/Maze/smallMaze.lay), [Medium Maze](https://github.com/alsongarbuja/adv-ai-projects/blob/main/project-1/resources/Maze/mediumMaze.lay), [Big Maze](https://github.com/alsongarbuja/adv-ai-projects/blob/main/project-1/resources/Maze/bigMaze.lay) and [Open Maze](https://github.com/alsongarbuja/adv-ai-projects/blob/main/project-1/resources/Maze/openMaze.lay) which contains a starting point `'P'` and a single goal point `'.'`

> To Run the algorithms run the following commands.

First change the directory into `project-1`

```bash
cd project-1
```

#### For BFS

```bash
python bfs_single_goal.py
```

#### For DFS

```bash
python dfs_single_goal.py
```

#### For A\*

```bash
python a_star_single_goal.py
```

Choose the maze from given option for all algorithms. `Note: for a* also select the heuristic function`

### Part 2: Multiple goal

Here we have 3 mazes [Tiny search](https://github.com/alsongarbuja/adv-ai-projects/blob/main/project-1/resources/Maze/tinySearch.lay), [Tricky Search](https://github.com/alsongarbuja/adv-ai-projects/blob/main/project-1/resources/Maze/trickySearch.lay) and [Small Search](https://github.com/alsongarbuja/adv-ai-projects/blob/main/project-1/resources/Maze/smallSearch.lay) which contains a starting point `'P'` and a single goal point `'.'`

> To Run the algorithms run the following commands.

First change the directory into `project-1`

```bash
cd project-1
```

#### For BFS

```bash
python bfs_multiple_goal.py
```

#### For DFS

```bash
python dfs_multiple_goal.py
```

#### For A\*

```bash
python a_star_multiple_goal.py
```

Choose the maze from given option for all algorithms. `Note: for a* also select the heuristic function`
