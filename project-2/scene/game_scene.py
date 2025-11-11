import time
import math
import os
import copy
import pygame

from breakthrough import initialBoardMatrix
from minimax import MiniMaxAgent
from alphabeta import AlphaBetaAgent
from scene.scene import Scene
import scene.global_vars as gv

class GameScene(Scene):
  def __init__(self, manager, scene: pygame.Surface, width: int, height: int):
    self.manager = manager
    self.width, self.height = width, height
    self.sizeofcell = int(560/8)
    self.scene = scene
    self.scene.fill([255, 255, 255])

    self.board = 0
    self.greenpiece = 0
    self.whitepiece = 0
    self.greenoutline = 0
    self.whiteoutline = 0
    self.metric_bg = 0
    self.reset = 0
    self.winner = 0
    self.computer = None
    self.minimax_profile = None
    self.alphabeta_profile = None
    self.player_profile = None
    self.off_one = None
    self.off_two = None
    self.def_one = None
    self.def_two = None

    self.status = 0
    self.turn = 0

    self.ori_x = 0
    self.ori_y = 0
    self.new_x = 0
    self.new_y = 0

    self.boardmatrix = copy.deepcopy(initialBoardMatrix)

    self.total_nodes_1 = 0
    self.total_nodes_2 = 0
    self.total_time_1 = 0
    self.total_time_2 = 0
    self.total_step_1 = 0
    self.total_step_2 = 0
    self.eat_piece = 0

    self.ai_delay_start = None
    self.ai_delay_duration = 200

    pygame.display.set_caption("Breakthrough Game")

    self.initgraphics()

  def update(self):
    self.scene.fill([255, 255, 255])

    if gv.gameplay_option == 1 and self.turn == 0:
      if self.ai_delay_start:
        if pygame.time.get_ticks() - self.ai_delay_start < self.ai_delay_duration:
          return
        else:
          self.ai_delay_start = None

    if self.status == 5 or (gv.gameplay_option == 1 and self.turn == 0):
      if self.turn == 0:
        start = time.process_time()
        self.ai_move(gv.ai_function_one_type_index, gv.AI_FUNCTION_OPTIONS[gv.ai_function_one_index])
        self.total_time_1 += (time.process_time() - start)
        self.total_step_1 += 1

      elif self.turn == 1:
        start = time.process_time()
        self.ai_move(gv.ai_function_two_type_index, gv.AI_FUNCTION_OPTIONS[gv.ai_function_two_index])
        self.total_time_2 += (time.process_time() - start)
        self.total_step_2 += 1

  def handle_events(self, events):
    for event in events:
      if event.type == pygame.QUIT:
        exit()
      elif event.type == pygame.MOUSEBUTTONDOWN and self.isreset(event.pos):
        self.boardmatrix = copy.deepcopy(initialBoardMatrix)
        self.status = 5 if gv.gameplay_option == 2 else 0
        self.total_nodes_1, self.total_nodes_2, self.total_step_1, self.total_step_2 = 0, 0, 0, 0
        self.total_time_1, self.total_time_2 = 0, 0
        self.turn = 0
      elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 0:
        x, y = event.pos
        coor_y = math.floor(x / self.sizeofcell)
        coor_x = math.floor(y / self.sizeofcell)
        if 0 <= coor_x < len(self.boardmatrix) and 0 <= coor_y < len(self.boardmatrix[0]):
          if self.boardmatrix[coor_x][coor_y] == self.turn+1:
            self.status = 1
            self.ori_y = math.floor(x / self.sizeofcell)
            self.ori_x = math.floor(y / self.sizeofcell)
      elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 1:
        x, y = event.pos
        self.new_y = math.floor(x / self.sizeofcell)
        self.new_x = math.floor(y / self.sizeofcell)
        if self.isabletomove():
          self.movepiece()
          if (self.new_x == 7 and self.boardmatrix[self.new_x][self.new_y] == 1) \
            or (self.new_x == 0 and self.boardmatrix[self.new_x][self.new_y] == 2):
            self.status = 3
        elif 0 <= self.new_x < len(self.boardmatrix) and 0 <= self.new_y < len(self.boardmatrix[0]):
          if self.boardmatrix[self.new_x][self.new_y] == self.boardmatrix[self.ori_x][self.ori_y]:
            self.ori_x = self.new_x
            self.ori_y = self.new_y

  def initgraphics(self):
    # Load board
    self.board = pygame.image.load_extended(os.path.join('assets', 'board.png'))
    self.board = pygame.transform.scale(self.board, (560, 560))

    # Load pieces
    self.greenpiece = pygame.image.load_extended(os.path.join('assets', 'green-piece.png'))
    self.greenpiece = pygame.transform.scale(self.greenpiece, (self.sizeofcell- 20, self.sizeofcell - 20))
    self.whitepiece = pygame.image.load_extended(os.path.join('assets', 'white-piece.png'))
    self.whitepiece = pygame.transform.scale(self.whitepiece, (self.sizeofcell - 20, self.sizeofcell - 20))

    # Load the outlines
    self.greenoutline = pygame.image.load_extended(os.path.join('assets', 'green-outline.png'))
    self.greenoutline = pygame.transform.scale(self.greenoutline, (self.sizeofcell - 10, self.sizeofcell - 10))
    self.whiteoutline = pygame.image.load_extended(os.path.join('assets', 'white-outline.png'))
    self.whiteoutline = pygame.transform.scale(self.whiteoutline, (self.sizeofcell - 10, self.sizeofcell - 10))

    # Load reset
    self.reset = pygame.image.load_extended(os.path.join('assets', 'return.png'))
    self.reset = pygame.transform.scale(self.reset, (80, 80))

    # Load extra UI assets
    self.winner = pygame.image.load_extended(os.path.join('assets', 'winner.png'))
    self.winner = pygame.transform.scale(self.winner, (100, 100))
    self.metric_bg = pygame.image.load_extended(os.path.join('assets', 'metrics-bg.png'))
    self.metric_bg = pygame.transform.scale(self.metric_bg, (500, 200))

    # Load the algorithm profiles
    self.minimax_profile = pygame.image.load_extended(os.path.join('assets', 'min-max-profile.png'))
    self.minimax_profile = pygame.transform.scale(self.minimax_profile, (80, 80))
    self.alphabeta_profile = pygame.image.load_extended(os.path.join('assets', 'alpha-beta-profile.png'))
    self.alphabeta_profile = pygame.transform.scale(self.alphabeta_profile, (80, 80))

    # Load the player profile
    self.player_profile = pygame.image.load_extended(os.path.join('assets', 'character.png'))
    self.player_profile = pygame.transform.scale(self.player_profile, (80, 80))

    # Load evaluation function icons
    self.off_one = pygame.image.load_extended(os.path.join('assets', 'sword.png'))
    self.off_one = pygame.transform.scale(self.off_one, (30, 30))
    self.off_two = pygame.image.load_extended(os.path.join('assets', 'dice_sword.png'))
    self.off_two = pygame.transform.scale(self.off_two, (30, 30))
    self.def_one = pygame.image.load_extended(os.path.join('assets', 'shield.png'))
    self.def_one = pygame.transform.scale(self.def_one, (30, 30))
    self.def_two = pygame.image.load_extended(os.path.join('assets', 'dice_shield.png'))
    self.def_two = pygame.transform.scale(self.def_two, (30, 30))

  def draw(self, scene):
    if gv.gameplay_option == 2 and not self.isgoalstate():
      self.status = 5
    self.scene.blit(self.board, (0, 0))
    self.scene.blit(self.reset, (590, self.height // 2 - 50))

    self.draw_metrics()

    players_pos = [(620, 50), (620, self.height - 190)]
    if gv.gameplay_option != 0:
      if gv.ai_function_one_type_index == 0:
        self.scene.blit(self.minimax_profile, players_pos[0])
      elif gv.ai_function_one_type_index == 1:
        self.scene.blit(self.alphabeta_profile, players_pos[0])
      if gv.ai_function_one_index == 0:
        self.scene.blit(self.off_one, (players_pos[0][0], players_pos[0][1]+90))
      elif gv.ai_function_one_index == 1:
        self.scene.blit(self.def_one, (players_pos[0][0], players_pos[0][1]+90))
      elif gv.ai_function_one_index == 2:
        self.scene.blit(self.off_two, (players_pos[0][0], players_pos[0][1]+90))
      elif gv.ai_function_one_index == 3:
        self.scene.blit(self.def_two, (players_pos[0][0], players_pos[0][1]+90))

    if gv.gameplay_option == 1:
      self.scene.blit(self.player_profile, players_pos[1])

    if gv.gameplay_option == 2:
      if gv.ai_function_two_type_index == 0:
        self.scene.blit(self.minimax_profile, players_pos[1])
      elif gv.ai_function_two_type_index == 1:
        self.scene.blit(self.alphabeta_profile, players_pos[1])
      if gv.ai_function_two_index == 0:
        self.scene.blit(self.off_one, (players_pos[1][0], players_pos[1][1]+90))
      elif gv.ai_function_two_index == 1:
        self.scene.blit(self.def_one, (players_pos[1][0], players_pos[1][1]+90))
      elif gv.ai_function_two_index == 2:
        self.scene.blit(self.off_two, (players_pos[1][0], players_pos[1][1]+90))
      elif gv.ai_function_two_index == 3:
        self.scene.blit(self.def_two, (players_pos[1][0], players_pos[1][1]+90))

    for i in range(8):
      for j in range(8):
        if self.boardmatrix[i][j] == 1:
          self.scene.blit(self.greenpiece, (self.sizeofcell * j + 15, self.sizeofcell * i + 15))
        elif self.boardmatrix[i][j] == 2:
          self.scene.blit(self.whitepiece, (self.sizeofcell * j + 15, self.sizeofcell * i + 15))
    if self.status == 1:
        # only downward is acceptable
        if self.boardmatrix[self.ori_x][self.ori_y] == 1:
            x1 = self.ori_x + 1
            y1 = self.ori_y - 1
            x2 = self.ori_x + 1
            y2 = self.ori_y + 1
            x3 = self.ori_x + 1
            y3 = self.ori_y
            # left down
            if y1 >= 0 and self.boardmatrix[x1][y1] != 1:
                self.scene.blit(self.greenoutline,
                                  (self.sizeofcell * y1 + 4, self.sizeofcell * x1 + 4))
            # right down
            if y2 <= 7 and self.boardmatrix[x2][y2] != 1:
                self.scene.blit(self.greenoutline,
                                  (self.sizeofcell * y2 + 4, self.sizeofcell * x2 + 4))
            # down
            if x3 <= 7 and self.boardmatrix[x3][y3] == 0:
                self.scene.blit(self.greenoutline,
                                  (self.sizeofcell * y3 + 4, self.sizeofcell * x3 + 4))

        if self.boardmatrix[self.ori_x][self.ori_y] == 2:
            x1 = self.ori_x - 1
            y1 = self.ori_y - 1
            x2 = self.ori_x - 1
            y2 = self.ori_y + 1
            x3 = self.ori_x - 1
            y3 = self.ori_y
            # left up
            if y1 >= 0 and self.boardmatrix[x1][y1] != 2:
                self.scene.blit(self.whiteoutline,
                                  (self.sizeofcell * y1 + 4, self.sizeofcell * x1 + 4))
            # right up
            if y2 <= 7 and self.boardmatrix[x2][y2] != 2:
                self.scene.blit(self.whiteoutline,
                                  (self.sizeofcell * y2 + 4, self.sizeofcell * x2 + 4))
            # up
            if x3 >= 0 and self.boardmatrix[x3][y3] == 0:
                self.scene.blit(self.whiteoutline,
                                  (self.sizeofcell * y3 + 4, self.sizeofcell * x3 + 4))
    if self.status == 3:
        self.scene.blit(self.winner, (self.width // 2 + 100, self.height // 2 - 50))

  def draw_metrics(self):
    self.scene.blit(self.metric_bg, (590, 20))
    self.scene.blit(self.metric_bg, (590, self.height - 220))

    player_text = f"Current player: {'Green' if self.turn==0 else 'White'}" if self.status != 3 else f"Winner: {'Green' if self.turn==1 else 'White'}"

    turn_text = pygame.font.Font(None, 24).render(player_text, True, (0,0,0))
    turn_text_rect = turn_text.get_rect()
    turn_text_rect.center = (self.width // 2 + 300, self.height // 2)

    self.scene.blit(turn_text, turn_text_rect)

    # if self.status == 5 or (gv.gameplay_option == 1 and self.turn == 0):
    # Draw metrics for Green
    steps_text = pygame.font.Font(None, 24).render(f"Number of Moves: {self.total_step_1}", True, (0,0,0))
    steps_text_rect = steps_text.get_rect()
    steps_text_rect.midright = (self.width - 150, 60)

    self.scene.blit(steps_text, steps_text_rect)

    nodes_text = pygame.font.Font(None, 24).render(f"Nodes expanded till now: {self.total_nodes_1}", True, (0,0,0))
    nodes_text_rect = nodes_text.get_rect()
    nodes_text_rect.midright = (self.width - 150, 90)

    self.scene.blit(nodes_text, nodes_text_rect)

    nodes_avg_text = pygame.font.Font(None, 24).render(f"Avg Nodes expanded per move: {self.total_nodes_1/(self.total_step_1 if self.total_step_1 > 0 else 1):.3f}", True, (0,0,0))
    nodes_avg_text_rect = nodes_avg_text.get_rect()
    nodes_avg_text_rect.midright = (self.width - 150, 120)

    self.scene.blit(nodes_avg_text, nodes_avg_text_rect)

    time_avg_text = pygame.font.Font(None, 24).render(f"Avg Time per move: {self.total_time_1/(self.total_step_1 if self.total_step_1 > 0 else 1):.3f}", True, (0,0,0))
    time_avg_text_rect = time_avg_text.get_rect()
    time_avg_text_rect.midright = (self.width - 150, 150)

    self.scene.blit(time_avg_text, time_avg_text_rect)

    piece_eaten_text = pygame.font.Font(None, 24).render(f"Pieces eaten: {16-self.get_pieces_eaten(1)}", True, (0,0,0))
    piece_eaten_text_rect = piece_eaten_text.get_rect()
    piece_eaten_text_rect.midright = (self.width - 150, 180)

    self.scene.blit(piece_eaten_text, piece_eaten_text_rect)

    # Draw metrics for White
    steps_text_2 = pygame.font.Font(None, 24).render(f"Number of Moves: {self.total_step_2}", True, (0,0,0))
    steps_text_rect_2 = steps_text_2.get_rect()
    steps_text_rect_2.midright = (self.width - 150, self.height - 180)

    self.scene.blit(steps_text_2, steps_text_rect_2)

    nodes_text_2 = pygame.font.Font(None, 24).render(f"Nodes expanded till now: {self.total_nodes_2}", True, (0,0,0))
    nodes_text_rect_2 = nodes_text_2.get_rect()
    nodes_text_rect_2.midright = (self.width - 150, self.height - 150)

    self.scene.blit(nodes_text_2, nodes_text_rect_2)

    nodes_avg_text_2 = pygame.font.Font(None, 24).render(f"Avg Nodes expanded per move: {self.total_nodes_2/(self.total_step_2 if self.total_step_2 > 0 else 1):.3f}", True, (0,0,0))
    nodes_avg_text_2_rect = nodes_avg_text_2.get_rect()
    nodes_avg_text_2_rect.midright = (self.width - 150, self.height - 110)

    self.scene.blit(nodes_avg_text_2, nodes_avg_text_2_rect)

    time_avg_text_2 = pygame.font.Font(None, 24).render(f"Avg Time per move: {self.total_time_2/(self.total_step_2 if self.total_step_2 > 0 else 1):.3f}", True, (0,0,0))
    time_avg_text_2_rect = time_avg_text_2.get_rect()
    time_avg_text_2_rect.midright = (self.width - 150, self.height - 80)

    self.scene.blit(time_avg_text_2, time_avg_text_2_rect)

    piece_eaten_text_2 = pygame.font.Font(None, 24).render(f"Pieces eaten: {16-self.get_pieces_eaten(0)}", True, (0,0,0))
    piece_eaten_text_2_rect = piece_eaten_text_2.get_rect()
    piece_eaten_text_2_rect.midright = (self.width - 150, self.height - 50)

    self.scene.blit(piece_eaten_text_2, piece_eaten_text_2_rect)

      # piece_eaten_text = pygame.font.Font(None, 24).render(f"Piece eaten till now: {self.eat_piece}", True, (0,0,0))
      # piece_eaten_text_rect = piece_eaten_text.get_rect()
      # piece_eaten_text_rect.midright = (self.width - 200, 140)

      # self.scene.blit(piece_eaten_text, piece_eaten_text_rect)

  def movepiece(self):
    self.boardmatrix[self.new_x][self.new_y] = self.boardmatrix[self.ori_x][self.ori_y]
    self.boardmatrix[self.ori_x][self.ori_y] = 0
    self.turn = 1 + (self.turn * -1)
    self.status = 0

    if gv.gameplay_option == 1 and self.turn == 0:
      self.ai_delay_start = pygame.time.get_ticks()

  def isreset(self, pos):
    x, y = pos
    if 670 >= x >= 590 and (self.height // 2 - 50) <= y <= (self.height // 2 - 50) + 80:
        return True
    return False

  def isabletomove(self):
    if self.new_y > len(self.boardmatrix[0])-1 or self.new_x > len(self.boardmatrix)-1:
      return 0
    if (self.boardmatrix[self.ori_x][self.ori_y] == 1
        and self.boardmatrix[self.new_x][self.new_y] != 1
        and self.new_x - self.ori_x == 1
        and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
        and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 2)) \
        or (self.boardmatrix[self.ori_x][self.ori_y] == 2
            and self.boardmatrix[self.new_x][self.new_y] != 2
            and self.ori_x - self.new_x == 1
            and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
            and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 1)):
        return 1
    return 0

  def ai_move(self, searchtype, evaluation):
    if searchtype == 0:
      return self.ai_move_minimax(evaluation)
    elif searchtype == 1:
      return self.ai_move_alphabeta(evaluation)

  def ai_move_minimax(self, function_type):
    board, nodes, piece = MiniMaxAgent(boardmatrix=self.boardmatrix, playerTurn=self.turn, function_type=function_type).minimax_search()
    self.boardmatrix = board.get_matrix()
    if self.turn == 0:
        self.total_nodes_1 += nodes
    elif self.turn == 1:
        self.total_nodes_2 += nodes
    self.turn = 1 + (self.turn * -1)
    self.eat_piece = 16 - piece
    if self.isgoalstate():
      self.status = 3
      print(self.boardmatrix)

  def ai_move_alphabeta(self, function_type):
    board, nodes, piece = AlphaBetaAgent(self.boardmatrix, self.turn, 4, function_type).alpha_beta_decision()
    self.boardmatrix = board.get_matrix()
    if self.turn == 0:
        self.total_nodes_1 += nodes
    elif self.turn == 1:
        self.total_nodes_2 += nodes
    self.eat_piece = 16 - piece
    self.turn = 1 + (self.turn * -1)
    if self.isgoalstate():
        self.status = 3

  def isgoalstate(self, base=0):
    if base == 0:
        if 2 in self.boardmatrix[0] or 1 in self.boardmatrix[7]:
            return True
        else:
            for line in self.boardmatrix:
                if 1 in line or 2 in line:
                    return False
        # return True
    else:
        count = 0
        for i in self.boardmatrix[0]:
            if i == 2:
                count += 1
        if count == 3:
            return True
        count = 0
        for i in self.boardmatrix[7]:
            if i == 1:
                count += 1
        if count == 3:
            return True
        count1 = 0
        count2 = 0
        for line in self.boardmatrix:
            for i in line:
                if i == 1:
                    count1 += 1
                elif i == 2:
                    count2 += 1
        if count1 <= 2 or count2 <= 2:
            return True
    return False

  def get_pieces_eaten(self, turn):
    return sum(1 for r in self.boardmatrix for c in r if c == turn+1)
