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
    self.reset = 0
    self.winner = 0
    self.computer = None
    self.minimax_profile = None
    self.alphabeta_profile = None

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

        print('total_step_1 = ', self.total_step_1,
              'total_nodes_1 = ', self.total_nodes_1,
              'node_per_move_1 = ', self.total_nodes_1 / self.total_step_1,
              'time_per_move_1 = ', self.total_time_1 / self.total_step_1,
              'have_eaten = ', self.eat_piece)

      elif self.turn == 1:
        start = time.process_time()
        self.ai_move(gv.ai_function_two_type_index, gv.AI_FUNCTION_OPTIONS[gv.ai_function_two_index])
        self.total_time_2 += (time.process_time() - start)
        self.total_step_2 += 1

        print('total_step_2 = ', self.total_step_2,
              'total_nodes_2 = ', self.total_nodes_2,
              'node_per_move_2 = ', self.total_nodes_2 / self.total_step_2,
              'time_per_move_2 = ', self.total_time_2 / self.total_step_2,
              'have_eaten: ', self.eat_piece)

  def handle_events(self, events):
    for event in events:
      if event.type == pygame.QUIT:
        exit()
      elif event.type == pygame.MOUSEBUTTONDOWN and self.isreset(event.pos):
        self.boardmatrix = copy.deepcopy(initialBoardMatrix)
        self.status = 0
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
    self.board = pygame.image.load_extended(os.path.join('assets', 'board.png'))
    self.board = pygame.transform.scale(self.board, (560, 560))
    self.greenpiece = pygame.image.load_extended(os.path.join('assets', 'green-piece.png'))
    self.greenpiece = pygame.transform.scale(self.greenpiece, (self.sizeofcell- 20, self.sizeofcell - 20))
    self.whitepiece = pygame.image.load_extended(os.path.join('assets', 'white-piece.png'))
    self.whitepiece = pygame.transform.scale(self.whitepiece, (self.sizeofcell - 20, self.sizeofcell - 20))
    self.greenoutline = pygame.image.load_extended(os.path.join('assets', 'green-outline.png'))
    self.greenoutline = pygame.transform.scale(self.greenoutline, (self.sizeofcell - 10, self.sizeofcell - 10))
    self.whiteoutline = pygame.image.load_extended(os.path.join('assets', 'white-outline.png'))
    self.whiteoutline = pygame.transform.scale(self.whiteoutline, (self.sizeofcell - 10, self.sizeofcell - 10))
    self.reset = pygame.image.load_extended(os.path.join('assets', 'reset.jpg'))
    self.reset = pygame.transform.scale(self.reset, (80, 80))
    self.winner = pygame.image.load_extended(os.path.join('assets', 'winner.png'))
    self.winner = pygame.transform.scale(self.winner, (250, 250))
    self.minimax_profile = pygame.image.load_extended(os.path.join('assets', 'min-max-profile.png'))
    self.minimax_profile = pygame.transform.scale(self.minimax_profile, (80, 80))
    self.alphabeta_profile = pygame.image.load_extended(os.path.join('assets', 'alpha-beta-profile.png'))
    self.alphabeta_profile = pygame.transform.scale(self.alphabeta_profile, (80, 80))

  def draw(self, scene):
    if gv.gameplay_option == 2 and not self.isgoalstate():
      self.status = 5
    self.scene.blit(self.board, (0, 0))
    self.scene.blit(self.reset, (590, 150))

    self.draw_metrics()

    players_pos = [(590, 10), (590, 420)]
    if gv.ai_function_one_type_index == 0 and gv.gameplay_option != 0:
      self.scene.blit(self.minimax_profile, players_pos[0])
    if gv.ai_function_one_type_index == 1 and gv.gameplay_option != 0:
      self.scene.blit(self.alphabeta_profile, players_pos[0])
    if gv.ai_function_two_type_index == 0 and gv.gameplay_option == 2:
      self.scene.blit(self.minimax_profile, players_pos[1])
    if gv.ai_function_two_type_index == 1 and gv.gameplay_option == 2:
      self.scene.blit(self.alphabeta_profile, players_pos[1])

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
        self.scene.blit(self.winner, (100, 100))

  def draw_metrics(self):
    turn_text = pygame.font.Font(None, 24).render(f"Current player: {'Green' if self.turn==0 else 'White'}", True, (0,0,0))
    turn_text_rect = turn_text.get_rect()
    turn_text_rect.midright = (self.width - 20, 100)

    self.scene.blit(turn_text, turn_text_rect)

    if self.status == 5 or (gv.gameplay_option == 1 and self.turn == 0):
      steps_render_text = f"Steps till now: {self.total_step_1 if self.turn==0 else self.total_step_2}"
      nodes_render_text = f"Nodes expanded till now: {self.total_nodes_1 if self.turn==0 else self.total_nodes_2}"
      piece_eaten_render_text = f"Piece eaten till now: {self.eat_piece}"

      steps_text = pygame.font.Font(None, 24).render(steps_render_text, True, (0,0,0))
      steps_text_rect = steps_text.get_rect()
      steps_text_rect.midright = (self.width - 20, 150)

      self.scene.blit(steps_text, steps_text_rect)

      nodes_text = pygame.font.Font(None, 24).render(nodes_render_text, True, (0,0,0))
      nodes_text_rect = nodes_text.get_rect()
      nodes_text_rect.midright = (self.width - 20, 200)

      self.scene.blit(nodes_text, nodes_text_rect)

      piece_eaten_text = pygame.font.Font(None, 24).render(piece_eaten_render_text, True, (0,0,0))
      piece_eaten_text_rect = piece_eaten_text.get_rect()
      piece_eaten_text_rect.midright = (self.width - 20, 250)

      self.scene.blit(piece_eaten_text, piece_eaten_text_rect)

  def movepiece(self):
    self.boardmatrix[self.new_x][self.new_y] = self.boardmatrix[self.ori_x][self.ori_y]
    self.boardmatrix[self.ori_x][self.ori_y] = 0
    self.turn = 1 + (self.turn * -1)
    self.status = 0

    if gv.gameplay_option == 1 and self.turn == 0:
      self.ai_delay_start = pygame.time.get_ticks()

  def isreset(self, pos):
    x, y = pos
    if 670 >= x >= 590 and 150 <= y <= 230:
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
    elif self.turn == 2:
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
