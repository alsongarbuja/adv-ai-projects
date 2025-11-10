import numpy as np

from breakthrough import State

class MiniMaxAgent:
  def __init__(self, boardmatrix, playerTurn, maxDepth = 3, function_type="offensive-1"):
    self.boardmatrix = boardmatrix
    self.playerTurn = playerTurn
    self.maxDepth = maxDepth
    self.function_type = function_type
    self.nodes = 0
    self.piece_num = 0

  def maxi(self, state: State, depth):
    if depth == self.maxDepth or state.is_game_state() != 0:
      return state.get_value(self.playerTurn)
    value = -np.inf
    for action in state.get_actions():
      value = max(value, self.mini(state.move_piece(action), depth + 1))
      self.nodes += 1
    return value

  def mini(self, state: State, depth):
    if depth == self.maxDepth or state.is_game_state() != 0:
      return state.get_value(self.playerTurn)
    value = np.inf
    for action in state.get_actions():
      value = min(value, self.maxi(state.move_piece(action), depth + 1))
      self.nodes += 1
    return value

  def minimax_search(self):
    action_to_do = None

    currentState = State(boardmatrix=self.boardmatrix, currentTurn=self.playerTurn, function_type=self.function_type)

    value = -np.inf
    for action in currentState.get_actions():
      self.nodes += 1
      state_ahead = currentState.move_piece(action)
      if state_ahead.is_game_state():
        action_to_do = action
        break
      min_result = self.mini(state_ahead, 1)
      if min_result > value:
        action_to_do = action
        value = min_result
    next_state = currentState.move_piece(action_to_do)

    if self.playerTurn == 0:
      self.piece_num = next_state.num_green_pieces
    elif self.playerTurn == 1:
      self.piece_num = next_state.num_white_pieces

    return next_state, self.nodes, self.piece_num
