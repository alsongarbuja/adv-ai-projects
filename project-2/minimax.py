import numpy as np

class MiniMaxAgent:
  def __init__(self, state, playerTurn, maxDepth = 3, function_type="defensive"):
    self.boardState = state
    self.playerTurn = playerTurn
    self.maxDepth = maxDepth
    self.function_type = function_type

  def minimax_search(self):
    def maximize_value():
      v = -np.inf
      for a in game.actions(self.boardState):
        v = max(v, minimizing_value(game.result(self.boardState, a)))
      return v

    def minimizing_value(state):
      v = np.inf
      for a in game.actions(state):
        v = min(v, maximize_value(game.result(state, a)))
      return v

    if self.playerTurn == 1:
      return maximize_value()

    return minimizing_value()
