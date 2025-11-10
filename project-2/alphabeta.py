from breakthrough import State, MIN_VAL, MAX_VAL

class AlphaBetaAgent:
  def __init__(self, boardmatrix, playerTurn, maxDepth = 4, function_type="offensive-1", game_type=0):
    self.boardmatrix = boardmatrix
    self.playerTurn = playerTurn
    self.maxDepth = maxDepth
    self.function_type = function_type
    self.game_type = game_type
    self.nodes = 0
    self.piece_num = 0

  def maxi(self, state: State, alpha, beta, depth):
    if depth == self.maxDepth or state.is_game_state() != 0:
      return state.get_value(self.playerTurn)
    value = MIN_VAL

    for action in sorted(state.get_actions(), key=lambda action: self.orderaction(action, state), reverse=True):
      self.nodes += 1

      value = max(value, self.mini(state.move_piece(action), alpha, beta, depth+1))
      if value >= beta:
        return value
      alpha = max(alpha, value)
    return value

  def mini(self, state: State, alpha, beta, depth):
    if depth == self.maxDepth or state.is_game_state() != 0:
      return state.get_value(self.playerTurn)
    value = MAX_VAL

    for action in sorted(state.get_actions(), key=lambda action: self.orderaction(action, state), reverse=True):
      self.nodes += 1

      value = min(value, self.maxi(state.move_piece(action), alpha, beta, depth+1))
      if value <= alpha:
        return value
      beta = min(beta, value)
    return value

  def orderaction(self, action, state):
    return 0

  def alpha_beta_decision(self):
    final_action = None
    if self.game_type == 0:
      initialState = State(boardmatrix=self.boardmatrix, currentTurn=self.playerTurn, function_type=self.function_type)
    else:
      initialState = State(boardmatrix=self.boardmatrix, currentTurn=self.playerTurn, function_type=self.function_type, height=5, width=10)
    value = MIN_VAL
    for action in initialState.get_actions():
      self.nodes += 1

      state_ahead = initialState.move_piece(action)
      if state_ahead.is_game_state(self.game_type):
        final_action = action
        break
      min_result = self.mini(state_ahead, MIN_VAL, MAX_VAL, 1)
      if min_result > value:
        final_action = action
        value = min_result

    next_state = initialState.move_piece(final_action)
    if self.playerTurn == 0:
      self.piece_num = next_state.num_white_pieces
    if self.playerTurn == 1:
      self.piece_num = next_state.num_green_pieces

    return next_state, self.nodes, self.piece_num
