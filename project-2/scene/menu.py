import os
import sys
import pygame

from scene.scene import Scene, SceneManager
from utility.button import Button
import scene.global_vars as gv

class MenuScene(Scene):
  """
  Class for Menu Scene
  """
  def __init__(self, manager: SceneManager, width, height):
    super().__init__(manager)
    self.title = pygame.font.Font(None, 50).render("Breakthrough", False, (255, 255, 255))
    self.width = width
    self.height = height
    self.PLAY_BTN = Button(text_input="Play", font=pygame.font.Font(None, 18), base_color="#d7fcd4", hovering_color="white", pos=(width / 2, height / 2))
    self.PLAY_VS_BTN = Button(text_input="Play With Computer", font=pygame.font.Font(None, 18), base_color="#d7fcd4", hovering_color="white", pos=(width / 2, height / 2 + 100))
    self.CMP_VS = Button(text_input="CMP Vs CMP", font=pygame.font.Font(None, 18), base_color="#d7fcd4", hovering_color="white", pos=(width / 2, height / 2 + 200))

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
      elif e.type == pygame.MOUSEBUTTONDOWN:
        MOUSE_POS = pygame.mouse.get_pos()
        # If the play button is pressed change the scene to game scene
        if self.PLAY_BTN.checkForInput(MOUSE_POS):
          gv.gameplay_option = 0
          if gv.board_index == 0:
            self.manager.set_scene("game")
          else:
            self.manager.set_scene("game-extended")
        # If the play with computer button is pressed change scene to choice scene for computer
        if self.PLAY_VS_BTN.checkForInput(MOUSE_POS):
          gv.gameplay_option = 1
          self.manager.set_scene("choice-vs-cmp")
        # If the cmp vs cmp button is pressed change the scene to choice scene for computers
        if self.CMP_VS.checkForInput(MOUSE_POS):
          gv.gameplay_option = 2
          self.manager.set_scene("choice-auto")
        if self.width - 150 <= MOUSE_POS[0] < self.width - 50 and 100 <= MOUSE_POS[1] < 200:
          self.manager.set_scene("setting")

  def draw(self, surface):
    surface.fill((0, 0, 0))

    settings_img = pygame.image.load_extended(os.path.join('assets', 'settings.png'))
    settings_img = pygame.transform.scale(settings_img, (100, 100))
    settings_img = pygame.transform.rotate(settings_img, 5)

    surface.blit(settings_img, (self.width - 150, 50))
    surface.blit(self.title, (self.width // 2 - self.title.get_width() // 2, 80))

    for button in [self.PLAY_BTN, self.CMP_VS, self.PLAY_VS_BTN]:
      button.changeColor(pygame.mouse.get_pos())
      button.update(surface)
