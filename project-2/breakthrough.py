
initialBoardMatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [2, 2, 2, 2, 2, 2, 2, 2],
                        [2, 2, 2, 2, 2, 2, 2, 2]]

def move_single_piece(initialPosition, direction, currentTurn):
  """
  Move a single piece in the given direction

  Args:
    initialPosition: Coordinate of the position
    direction: the direction to move to (1 - straight, 2 - left diagonal, 3 - right diagonal)
    currentTurn: current player (0 for black, 1 for white)
  """
  to_move = 1 if currentTurn == 0 else -1

  if direction == 1:
    return initialPosition[0] + to_move, initialPosition[1] + 0
  elif direction == 2:
    return initialPosition[0] + to_move, initialPosition[1] - 1
  elif direction == 3:
    return initialPosition[0] + to_move, initialPosition[1] + 1

  return initialPosition

class Action:
  def __init__(self, coordinate, direction, turn):
    self.coord = coordinate
    self.direction = direction
    self.turn = turn

class State:
  def __init__(self, boardmatrix=None, currentTurn=0, blackPositions=None, whitePositions=None, width=8, height=8):
    self.currentTurn = currentTurn
    self.boardmatrix = initialBoardMatrix if boardmatrix is None else boardmatrix
    self.num_black_pieces = 0
    self.num_white_pieces = 0
    self.width = width
    self.height = height
    self.blackPositions = []
    self.whitePositions = []

    if blackPositions is None or whitePositions is None:
      self.initialPiecesPositions()

  def move_piece(self, action: Action):
    """
    Function to move a piece in each players turn accounting for any capture piece too

    Args:
      action: A object containing the coordinate of the piece to move and the direction to move to

    Returns:
      State after moving the piece
    """

    black_positions = self.blackPositions
    white_positions = self.whitePositions

    # If the turn is black's
    if action.turn == 0:
      if action.coord in black_positions:
        index = black_positions.index(action.coord)
        new_pos = move_single_piece(action.coord, action.direction, self.currentTurn)
        black_positions[index] = new_pos
        if new_pos in white_positions:
          white_positions.remove(new_pos)
      else:
        print("Action is not valid")

    # If the turn is white's
    else:
      if action.coord in white_positions:
        index = white_positions.index(action.coord)
        new_pos = move_single_piece(action.coord, action.direction, self.currentTurn)
        white_positions[index] = new_pos
        if new_pos in black_positions:
          self.blackPositions.remove(new_pos)
      else:
        print("Action is not valid")

    new_state = State(blackPositions=black_positions, whitePositions=white_positions, currentTurn=self.alter_turn())
    return new_state

  def get_actions(self, pos=None):
    """
    Function to get available actions of either a piece or pieces of a player

    Args:
      pos: A tuple of piece coordinate or None if want to get available actions for all pieces
    """
    available_actions = []

    to_use_positions = self.blackPositions if self.currentTurn == 0 else self.whitePositions if pos is None else [pos]
    opponent_positions = self.whitePositions if self.currentTurn == 0 else self.blackPositions

    for pos in sorted(to_use_positions, key=lambda p: (p[0], -p[1]), reverse=True):
      for direc in [1, 2, 3]:
        test_move = move_single_piece(pos, direc, self.currentTurn)
        if (test_move not in to_use_positions) and (-1 < test_move[0] < self.height) and (-1 < test_move[1] < self.width):
          if (direc == 1 and test_move not in opponent_positions) or direc != 1:
            print(test_move, "->", pos)
            available_actions.append(Action(pos, direc, self.currentTurn))

    return available_actions

  def alter_turn(self):
    """
    Simple function to alter the players turn and return it

    Returns:
      Integer representing next player turn (0 - Black, 1 - White)
    """
    return 1 + (self.currentTurn * -1)

  def initialPiecesPositions(self):
    """
    Simple position to append coordinates of black and white pieces positions
    """
    for x in range(self.height):
      for y in range(self.width):
        if self.boardmatrix[x][y] == 1:
          self.blackPositions.append((x, y))
        if self.boardmatrix[x][y] == 2:
          self.whitePositions.append((x, y))

  def reset(self):
    """
    Simple function to reset the state
    """
    self.boardmatrix = initialBoardMatrix
    self.currentTurn = 0
    self.initialPiecesPositions()

  def is_game_state(self, type = 0):
    """
    A function to check if the state is in game finished state or not

    Args:
      type: A optional integer to define the type of game (0 - Normal Breakthrough, 1 - 3 in Base Breakthrough)
    """

    to_complete_pieces_in_base = 1 if type == 0 else 3
    to_complete_remaining_pieces = 0 if type == 0 else 2
    piecesInBase = 0

    for coord in self.blackPositions:
      if coord[0] == len(self.boardmatrix)-1:
        piecesInBase += 1
    for coord in self.whitePositions:
      if coord[0] == 0:
        piecesInBase += 1

    if piecesInBase >= to_complete_pieces_in_base:
      return True

    if len(self.blackPositions) <= to_complete_remaining_pieces or len(self.whitePositions) <= to_complete_remaining_pieces:
      return True

    return False

  def get_value(self, turn):
    # To implement
    return 0

  def get_matrix(self):
    matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
    for item in self.blackPositions:
      matrix[item[0]][item[1]] = 1
    for item in self.whitePositions:
      matrix[item[0]][item[1]] = 2
    return matrix
