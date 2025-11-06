import sys
import time
import math
import os
import copy
import pygame

from breakthrough import initialBoardMatrix
from minimax import MiniMaxAgent
from alphabeta import AlphaBetaAgent
from button import Button

class SceneManager:
  """
  Class to act as the manager of all the screens in the game
  """
  def __init__(self):
    # Object of scene name and Scene (key-value pairs)
    self.scenes = {}
    # Object holding the current scene or None
    self.current_scene = None

  def add_scene(self, name, scene_obj):
    """
    Function to add scene into the scenes object

    Args:
      name: Name of the scene
      scene_obj: A Scene Object
    """
    self.scenes[name] = scene_obj

  def set_scene(self, name):
    """
    Function to set the scene to current scene

    Args:
      name: Name of the scene
    """
    self.current_scene = self.scenes.get(name)

  def handle_events(self, events: list[pygame.Event]):
    """
    Function to handle events if the current scene have events

    Args:
      events: List of pygame Events
    """
    if self.current_scene:
      self.current_scene.handle_events(events)

  def update(self):
    """
    Function to handle update in the current scene
    """
    if self.current_scene:
      self.current_scene.update()

  def draw(self, surface: pygame.Surface, font: pygame.font.Font):
    """
    Function to handle drawing elements in scene in current scene

    Args:
      surface: A pygame Surface
      font: A pygame Font
    """
    if self.current_scene:
      self.current_scene.draw(surface, font)

class Scene:
  """
  Base class for scene
  """
  def __init__(self, manager):
    self.manager = manager

  def handle_events(self, events):
    pass

  def update(self):
    pass

  def draw(self, surface: pygame.Surface, font: pygame.font.Font):
    pass

class MenuScene(Scene):
  """
  Class for Menu Scene
  """
  def __init__(self, manager: SceneManager, width, height, Font: pygame.font.Font):
    super().__init__(manager)
    self.title = Font.render("Breakthrough", True, (255, 255, 255))
    self.width = width
    self.height = height
    self.PLAY_BTN = Button(text_input="Play", font=Font, base_color="#d7fcd4", hovering_color="white", pos=(width / 2, height / 2))
    # self.CMP_VS = Button(text_input="CMP Vs CMP", font=Font, base_color="#d7fcd4", hovering_color="white", pos=(width / 2, height / 2 + 100))
    # self.CMP_VS_PLAYER = Button(text_input="CMP Vs Player", font=Font, base_color="#d7fcd4", hovering_color="white", pos=(width / 2, height / 2 + 200))

  def handle_events(self, events: list[pygame.Event]):
    """
    Function to handle events in the game

    Args:
      events: list of pygame events
    """
    for e in events:
      # If close button is pressed close the pygame window
      if e.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      # If the play button is pressed change the scene to game scene
      elif e.type == pygame.MOUSEBUTTONDOWN:
        if self.PLAY_BTN.checkForInput(pygame.mouse.get_pos()):
          self.manager.set_scene("game")
        # if self.CMP_VS.checkForInput(pygame.mouse.get_pos()):
        #   self.manager.set_scene("choose_cmps")
        # if self.CMP_VS_PLAYER.checkForInput(pygame.mouse.get_pos()):
        #   self.manager.set_scene("choose_cmp")

  def draw(self, surface, Font):
    surface.fill((0, 0, 0))

    surface.blit(self.title, (self.width // 2 - self.title.get_width() // 2, 80))

    for button in [self.PLAY_BTN]:
      button.changeColor(pygame.mouse.get_pos())
      button.update(surface)

class GameScene(Scene):
  def __init__(self, manager, scene: pygame.Surface, width: int, height: int):
    self.width, self.height = width, height
    self.sizeofcell = int(560/8)
    self.scene = scene
    self.scene.fill([255, 255, 255])

    self.board = 0
    self.blackpiece = 0
    self.whitepiece = 0
    self.outline = 0
    self.reset = 0
    self.winner = 0
    self.computer = None

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

    pygame.display.set_caption("Breakthrough Game")

    # self.clock = pygame.time.Clock()
    self.initgraphics()

  def update(self):
    # self.clock.tick(60)

    self.scene.fill([255, 255, 255])

    if self.status == 5:
      if self.turn == 0:
        start = time.process_time()
        self.ai_move(2, "offensive-1")
        self.total_time_1 += (time.process_time() - start)
        self.total_step_1 += 1

        print('total_step_1 = ', self.total_step_1,
              'total_nodes_1 = ', self.total_nodes_1,
              'node_per_move_1 = ', self.total_nodes_1 / self.total_step_1,
              'time_per_move_1 = ', self.total_time_1 / self.total_step_1,
              'have_eaten = ', self.eat_piece)

      elif self.turn == 1:
        start = time.process_time()
        self.ai_move(2, "defensive-1")
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
      elif event.type == pygame.MOUSEBUTTONDOWN and self.iscomputer(event.pos):
        self.ai_move_minimax(1)
      elif event.type == pygame.MOUSEBUTTONDOWN and self.isauto(event.pos):
        self.status = 5
      elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 0:
        x, y = event.pos
        coor_y = math.floor(x / self.sizeofcell)
        coor_x = math.floor(y / self.sizeofcell)
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
        elif self.boardmatrix[self.new_x][self.new_y] == self.boardmatrix[self.ori_x][self.ori_y]:
          self.ori_x = self.new_x
          self.ori_y = self.new_y

    # self.display()

    # pygame.display.flip()

  def initgraphics(self):
    self.board = pygame.image.load_extended(os.path.join('assets', 'board.png'))
    self.board = pygame.transform.scale(self.board, (560, 560))
    self.blackpiece = pygame.image.load_extended(os.path.join('assets', 'black-piece.png'))
    self.blackpiece = pygame.transform.scale(self.blackpiece, (self.sizeofcell- 20, self.sizeofcell - 20))
    self.whitepiece = pygame.image.load_extended(os.path.join('assets', 'white-piece.png'))
    self.whitepiece = pygame.transform.scale(self.whitepiece, (self.sizeofcell - 20, self.sizeofcell - 20))
    self.outline = pygame.image.load_extended(os.path.join('assets', 'outline.png'))
    self.outline = pygame.transform.scale(self.outline, (self.sizeofcell - 10, self.sizeofcell - 10))
    self.reset = pygame.image.load_extended(os.path.join('assets', 'reset.jpg'))
    self.reset = pygame.transform.scale(self.reset, (80, 80))
    self.winner = pygame.image.load_extended(os.path.join('assets', 'winner.png'))
    self.winner = pygame.transform.scale(self.winner, (250, 250))
    self.computer = pygame.image.load_extended(os.path.join('assets', 'computer.png'))
    self.computer = pygame.transform.scale(self.computer, (80, 80))
    self.auto = pygame.image.load_extended(os.path.join('assets', 'auto.png'))
    self.auto = pygame.transform.scale(self.auto, (80, 80))

  def draw(self, scene, font):
    self.scene.blit(self.board, (0, 0))
    self.scene.blit(self.reset, (590, 50))
    self.scene.blit(self.computer, (590, 200))
    self.scene.blit(self.auto, (590, 340))
    for i in range(8):
      for j in range(8):
        if self.boardmatrix[i][j] == 1:
          self.scene.blit(self.blackpiece, (self.sizeofcell * j + 15, self.sizeofcell * i + 15))
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
                self.scene.blit(self.outline,
                                  (self.sizeofcell * y1 + 4, self.sizeofcell * x1 + 4))
            # right down
            if y2 <= 7 and self.boardmatrix[x2][y2] != 1:
                self.scene.blit(self.outline,
                                  (self.sizeofcell * y2 + 4, self.sizeofcell * x2 + 4))
            # down
            if x3 <= 7 and self.boardmatrix[x3][y3] == 0:
                self.scene.blit(self.outline,
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
                self.scene.blit(self.outline,
                                  (self.sizeofcell * y1 + 4, self.sizeofcell * x1 + 4))
            # right up
            if y2 <= 7 and self.boardmatrix[x2][y2] != 2:
                self.scene.blit(self.outline,
                                  (self.sizeofcell * y2 + 4, self.sizeofcell * x2 + 4))
            # up
            if x3 >= 0 and self.boardmatrix[x3][y3] == 0:
                self.scene.blit(self.outline,
                                  (self.sizeofcell * y3 + 4, self.sizeofcell * x3 + 4))
    if self.status == 3:
        self.scene.blit(self.winner, (100, 100))

  def movepiece(self):
    self.boardmatrix[self.new_x][self.new_y] = self.boardmatrix[self.ori_x][self.ori_y]
    self.boardmatrix[self.ori_x][self.ori_y] = 0
    self.turn = 1 + (self.turn * -1)
    self.status = 0

  def isreset(self, pos):
    x, y = pos
    if 670 >= x >= 590 and 50 <= y <= 130:
        return True
    return False

  def iscomputer(self, pos):
    x, y = pos
    if 590 <= x <= 670 and 200 <= y <= 280:
        return True
    return False

  def isauto(self, pos):
    x, y = pos
    if 590 <= x <= 670 and 340 <= y <= 420:
        return True
    return False

  def isabletomove(self):
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
    if searchtype == 1:
        return self.ai_move_minimax(evaluation)
    elif searchtype == 2:
        return self.ai_move_alphabeta(evaluation)

  def ai_move_minimax(self, function_type):
    board, nodes, piece = MiniMaxAgent(self.boardmatrix, self.turn, 3, function_type).minimax_search()
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
    board, nodes, piece = AlphaBetaAgent(self.boardmatrix, self.turn, 5, function_type).alpha_beta_decision()
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
            print("2 or 1")
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
