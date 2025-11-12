AI_FUNCTION_OPTIONS = ["offensive-1", "defensive-1", "offensive-2", "defensive-2"]
ai_function_one_index = AI_FUNCTION_OPTIONS.index("offensive-1")
ai_function_two_index = AI_FUNCTION_OPTIONS.index("defensive-1")

AI_FUNCTION_TYPES_OPTIONS = ["minimax", "alpha-beta"]
ai_function_one_type_index = AI_FUNCTION_TYPES_OPTIONS.index("minimax")
ai_function_two_type_index = AI_FUNCTION_TYPES_OPTIONS.index("alpha-beta")

BOARD_OPTIONS = ["8x8", "5x10"]
board_index = BOARD_OPTIONS.index("8x8")

RULE_OPTIONS = ["Standard", "3-worker-base"]
rule_index = RULE_OPTIONS.index("Standard")

initialBoardMatrices = [
  # 8x8 board matrix
  [[1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [2, 2, 2, 2, 2, 2, 2, 2],
  [2, 2, 2, 2, 2, 2, 2, 2]],

  # 5x10 board matrix
  [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
]

# Determines which mode of gameplay is being played
# 0 - Normal Player vs Player
# 1 - Player Vs Computer
# 2 - Computer Vs Computer / Auto
gameplay_option = 0

def handle_ai_one_function_index_change(index: int):
  global ai_function_one_index
  ai_function_one_index = index

def handle_ai_two_function_index_change(index: int):
  global ai_function_two_index
  ai_function_two_index = index

def handle_ai_one_function_type_index_change(index: int):
  global ai_function_one_type_index
  ai_function_one_type_index = index

def handle_ai_two_function_type_index_change(index: int):
  global ai_function_two_type_index
  ai_function_two_type_index = index

def handle_board_index_change(index: int):
  global board_index
  board_index = index

def handle_rule_index_change(index: int):
  global rule_index
  rule_index = index
