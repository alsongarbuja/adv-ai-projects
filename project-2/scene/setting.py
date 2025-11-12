import sys
import pygame

from scene.scene import Scene, SceneManager
from utility.button import Button
from utility.dropdown import Dropdown
import scene.global_vars as gv

class SettingScene(Scene):
  """
  Class for setting scene
  """
  def __init__(self, manager: SceneManager, width, height):
    super().__init__(manager)
    self.title = pygame.font.Font(None, 50).render("Breakthrough - Settings", True, (255, 255, 255))
    self.width = width
    self.height = height
    self.DROP_TYPE_1 = Dropdown(
      x=150, y=150, w=100, h=24,
      main_color=(50, 50, 50),
      hover_color=(80, 80, 80),
      font_color=(255, 255, 255),
      options=gv.BOARD_OPTIONS,
      font=pygame.font.Font(None, 18),
      label_text="Board size",
      selected_index=gv.board_index,
      on_change=gv.handle_board_index_change,
    )
    self.DROP = Dropdown(
      x=150, y=250, w=100, h=24,
      main_color=(50, 50, 50),
      hover_color=(80, 80, 80),
      font_color=(255, 255, 255),
      options=gv.RULE_OPTIONS,
      font=pygame.font.Font(None, 18),
      label_text="Win rule",
      selected_index=gv.rule_index,
      on_change=gv.handle_rule_index_change,
    )
    self.BACK_BTN = Button(text_input="Back To Menu", font=pygame.font.Font(None, 18), base_color="#d7fcd4", hovering_color="white", pos=(width / 2, height / 2 + 200))

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
        if self.BACK_BTN.checkForInput(pygame.mouse.get_pos()):
          self.manager.set_scene("menu")
      self.DROP.handle_event(event=e)
      self.DROP_TYPE_1.handle_event(event=e)

  def draw(self, surface):
    surface.fill((0, 0, 0))

    surface.blit(self.title, (self.width // 2 - self.title.get_width() // 2, 80))

    for button in [self.BACK_BTN]:
      button.changeColor(pygame.mouse.get_pos())
      button.update(surface)

    self.DROP.draw(surface)
    self.DROP_TYPE_1.draw(surface)
