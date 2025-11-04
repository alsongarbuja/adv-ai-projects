initialBoardMatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [2, 2, 2, 2, 2, 2, 2, 2],
                        [2, 2, 2, 2, 2, 2, 2, 2]]

def alter_turn(turn) -> int:
    """
    Simple function to alter the players turn and return it

    Returns:
      Integer representing next player turn (0 - Black, 1 - White)
    """
    return 1 + (turn * -1)

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
  def __init__(self, boardmatrix=None, currentTurn=0, blackPositions=None, whitePositions=None, width=8, height=8, num_black_pieces=0, num_white_pieces=0):
    self.currentTurn = currentTurn
    self.num_black_pieces = num_black_pieces
    self.num_white_pieces = num_white_pieces
    self.width = width
    self.height = height
    self.blackPositions = [] if blackPositions is None else blackPositions
    self.whitePositions = [] if whitePositions is None else whitePositions

    if boardmatrix is not None:
      for x in range(self.height):
        for y in range(self.width):
          if boardmatrix[x][y] == 1:
            self.blackPositions.append((x, y))
          if boardmatrix[x][y] == 2:
            self.whitePositions.append((x, y))

  def move_piece(self, action: Action):
    """
    Function to move a piece in each players turn accounting for any capture piece too

    Args:
      action: A object containing the coordinate of the piece to move and the direction to move to

    Returns:
      State after moving the piece
    """

    black_positions = list(self.blackPositions)
    white_positions = list(self.whitePositions)

    # If the turn is black's
    if action.turn == 0:
      if action.coord in self.blackPositions:
        index = black_positions.index(action.coord)
        new_pos = move_single_piece(action.coord, action.direction, action.turn)
        black_positions[index] = new_pos
        if new_pos in self.whitePositions:
          white_positions.remove(new_pos)
      else:
        print("Action is not valid")

    # If the turn is white's
    elif action.turn == 1:
      if action.coord in self.whitePositions:
        index = white_positions.index(action.coord)
        new_pos = move_single_piece(action.coord, action.direction, action.turn)
        white_positions[index] = new_pos
        if new_pos in self.blackPositions:
          black_positions.remove(new_pos)
      else:
        print("Action is not valid")

    new_state = State(blackPositions=black_positions, whitePositions=white_positions, currentTurn=alter_turn(action.turn), num_black_pieces=self.num_black_pieces, num_white_pieces=self.num_white_pieces, height=self.height, width=self.width)
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
            available_actions.append(Action(pos, direc, self.currentTurn))

    return available_actions

  def is_game_state(self, type = 0):
    """
    A function to check if the state is in game finished state or not

    Args:
      type: A optional integer to define the type of game (0 - Normal Breakthrough, 1 - 3 in Base Breakthrough)
    """

    if type == 0:
      if 0 in [item[0] for item in self.whitePositions] or len(self.blackPositions) == 0:
        return 2
      if self.height-1 in [item[0] for item in self.blackPositions] or len(self.whitePositions) == 0:
        return 1
      return 0
    else:
      piecesInBase = 0
      for coord in self.blackPositions:
        if coord[0] == self.height-1:
          piecesInBase += 1
      for coord in self.whitePositions:
        if coord[0] == 0:
          piecesInBase += 1

      if piecesInBase == 3:
        return True

      if len(self.blackPositions) <= 2 or len(self.whitePositions) <= 2:
        return True

    return False

  def myscore(self, turn):
    if turn == 0:
      return len(self.blackPositions) \
        + sum(pos[0] for pos in self.blackPositions) + self.winningscore(turn)
    elif turn == 1:
      return len(self.whitePositions) \
        + sum(7 - pos[0] for pos in self.whitePositions) + self.winningscore(turn)

  def enemyscore(self, turn):
    if turn == 0:
        return len(self.whitePositions) \
                + sum(7 - pos[0] for pos in self.whitePositions) + self.winningscore(turn)
                #+ max(7 - pos[0] for pos in self.white_positions)\

    elif turn == 1:
        return len(self.blackPositions) \
                + sum(pos[0] for pos in self.blackPositions) + self.winningscore(turn)

  def winningscore(self, turn):
    winningvalue = 200
    if turn == 0:
      if self.is_game_state() == 1:
        return winningvalue
      elif self.is_game_state() == 2:
        return -winningvalue
      else:
        return 0
    elif turn == 1:
      if self.is_game_state() == 2:
        return winningvalue
      elif self.is_game_state() == 1:
        return -winningvalue
      else:
        return 0

  def get_value(self, turn):
    # To implement
    return 2 * self.myscore(turn) - 1 * self.enemyscore(turn)

  def get_matrix(self):
    matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
    for item in self.blackPositions:
      matrix[item[0]][item[1]] = 1
    for item in self.whitePositions:
      matrix[item[0]][item[1]] = 2
    return matrix
