import random
import scene.global_vars as gv

MIN_VAL = -float("inf")
MAX_VAL = float("inf")

def alter_turn(turn) -> int:
    """
    Simple function to alter the players turn and return it

    Returns:
      Integer representing next player turn (0 - Green, 1 - White)
    """
    return 1 + (turn * -1)

def move_single_piece(initialPosition, direction, currentTurn):
  """
  Move a single piece in the given direction

  Args:
    initialPosition: Coordinate of the position
    direction: the direction to move to (1 - straight, 2 - left diagonal, 3 - right diagonal)
    currentTurn: current player (0 for green, 1 for white)
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
  def __init__(
      self,
      boardmatrix=None,
      currentTurn=0,
      greenPositions=None,
      whitePositions=None,
      width=8,
      height=8,
      num_green_pieces=0,
      num_white_pieces=0,
      function_type="offensive-1"
    ):
    self.currentTurn = currentTurn
    self.num_green_pieces = num_green_pieces
    self.num_white_pieces = num_white_pieces
    self.width = width
    self.height = height
    self.function_type = function_type
    self.greenPositions = [] if greenPositions is None else greenPositions
    self.whitePositions = [] if whitePositions is None else whitePositions

    if boardmatrix is not None:
      for x in range(self.height):
        for y in range(self.width):
          if boardmatrix[x][y] == 1:
            self.greenPositions.append((x, y))
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

    green_positions = list(self.greenPositions)
    white_positions = list(self.whitePositions)

    # If the turn is green's
    if action.turn == 0:
      if action.coord in self.greenPositions:
        index = green_positions.index(action.coord)
        new_pos = move_single_piece(action.coord, action.direction, action.turn)
        green_positions[index] = new_pos
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
        if new_pos in self.greenPositions:
          green_positions.remove(new_pos)
      else:
        print("Action is not valid")

    new_state = State(function_type=self.function_type, greenPositions=green_positions, whitePositions=white_positions, currentTurn=alter_turn(action.turn), num_green_pieces=self.num_green_pieces, num_white_pieces=self.num_white_pieces, height=self.height, width=self.width)
    return new_state

  def get_actions(self, pos=None):
    """
    Function to get available actions of either a piece or pieces of a player

    Args:
      pos: A tuple of piece coordinate or None if want to get available actions for all pieces
    """
    available_actions = []

    to_use_positions = self.greenPositions if self.currentTurn == 0 else self.whitePositions if pos is None else [pos]
    opponent_positions = self.whitePositions if self.currentTurn == 0 else self.greenPositions

    for pos in sorted(to_use_positions, key=lambda p: (p[0], -p[1]), reverse=True):
      for direc in [1, 2, 3]:
        test_move = move_single_piece(pos, direc, self.currentTurn)
        if (test_move not in to_use_positions) and (-1 < test_move[0] < self.height) and (-1 < test_move[1] < self.width):
          if (direc == 1 and test_move not in opponent_positions) or direc != 1:
            available_actions.append(Action(pos, direc, self.currentTurn))

    return available_actions

  def is_game_state(self):
    """
    A function to check if the state is in game finished state or not
    """

    if gv.rule_index == 0:
      if 0 in [item[0] for item in self.whitePositions] or len(self.greenPositions) == 0:
        return 2
      if self.height-1 in [item[0] for item in self.greenPositions] or len(self.whitePositions) == 0:
        return 1
      return 0
    else:
      piecesInBase = 0
      for coord in self.greenPositions:
        if coord[0] == self.height-1:
          piecesInBase += 1
      for coord in self.whitePositions:
        if coord[0] == 0:
          piecesInBase += 1

      if piecesInBase >= 3:
        return True

      if len(self.greenPositions) <= 2 or len(self.whitePositions) <= 2:
        return True

    return False

  def myscore(self, turn):
    return self.count_pieces(turn) + self.foward_pieces(turn) + self.winningscore(turn)

  def enemyscore(self, turn):
    alternate_turn = alter_turn(turn)
    return self.count_pieces(alternate_turn) + self.foward_pieces(alternate_turn) + self.winningscore(turn)

  def count_pieces(self, turn):
    """
    Simple funciton to count the remaining pieces of the player

    Args:
      turn: A integer signifying which player turn it is (0 - Green, 1 - White)
    """
    if turn == 0:
      return len(self.greenPositions)
    elif turn == 1:
      return len(self.whitePositions)
    return 0

  def foward_pieces(self, turn):
    """
    Simple function to give certian points to each player based on the number of pieces that are moving forward

    Args:
      turn: A integer signifying the current player (0 - Green, 1 - White)
    """
    if turn == 0:
      return sum(pos[0] for pos in self.greenPositions)
    elif turn == 1:
      # Decreasing 7 since white pieces move up the board so the lesser the x coordinate the more point they score
      return sum(7 - pos[0] for pos in self.whitePositions)
    return 0

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
    if self.function_type == "defensive-1":
      return 2 * self.myscore(turn) + random.random()
    if self.function_type == "offensive-1":
      return 2 *(30 - self.enemyscore(turn)) + random.random()
    if self.function_type == "defensive-2":
      return 2 * self.myscore(turn) + 2 * self.space_control(turn) - 2 * self.attack_threats(alter_turn(turn)) + 3 * self.my_safety(turn) + random.random()
    if self.function_type == "offensive-2":
      return 4 * self.myscore(turn) - 3 * self.enemyscore(turn) + 1.5 * self.attack_threats(turn) + random.random()
    return 0

  def attack_threats(self, turn):
    """
    Function to return number of enemy pieces that can be captured by current player in next move:

    Args:
      turn: Current player turn integer
    """
    threats = 0

    pieces_to_use = self.greenPositions if turn == 0 else self.whitePositions
    opponents_to_use = self.whitePositions if turn == 0 else self.greenPositions
    direction = 1 if turn == 0 else -1

    for (r, c) in pieces_to_use:
      for dc in (-1, 1):
        new_r, new_c = r + direction, c + dc
        if 0 <= new_r < self.height and 0 <= new_c < self.width:
          if (new_r, new_c) in opponents_to_use:
            threats += 1

    return threats

  def my_safety(self, turn):
    """
    Function to evaluate if current player pieces are protected or not

    Args:
      turn: A integer representing current player
    """
    safe = 0
    direc = 1 if turn == 0 else -1
    pieces_to_use = self.greenPositions if turn == 0 else self.whitePositions
    pieces_set = set(pieces_to_use)
    for (r, c) in pieces_to_use:
      for dc in (-1, 1):
        if (r - direc, c + dc) in pieces_set:
          safe +=1
          break
    return safe

  def space_control(self, turn):
    """
    Function to give more value to player with more pieces in center rows

    Args:
      turn: A integer denoting the current player
    """
    center_cols = {(self.height-1) // 2}
    if self.height % 2 != 0:
      center_cols.add((self.height-1) //  2 + 1)
    pieces_to_use = self.greenPositions if turn == 0 else self.whitePositions
    return sum(1 for _, c in pieces_to_use if c in center_cols)

  def get_matrix(self):
    """
    Function to get the current board matrix
    """
    matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
    for item in self.greenPositions:
      matrix[item[0]][item[1]] = 1
    for item in self.whitePositions:
      matrix[item[0]][item[1]] = 2
    return matrix
