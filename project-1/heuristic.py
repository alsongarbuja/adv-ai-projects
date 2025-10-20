import math

def heuristic_calculation(current: tuple[int, int], goal: tuple[int, int], function_to_use: str = "Manhattan"):
  if function_to_use == "Euclidean":
    return math.sqrt((current[0]-goal[0])**2 + (current[1]-goal[1])**2)

  if function_to_use == "Chebyshev":
    return max(abs(current[0] - goal[0]), abs(current[1] - goal[1]))

  return abs(current[0]-goal[0]) + abs(current[1]-goal[1])
