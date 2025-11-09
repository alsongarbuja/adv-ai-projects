import sys
import pygame

from scene.scene import Scene, SceneManager
from utility.button import Button
from utility.dropdown import Dropdown
import scene.global_vars as gv

class CMPVSCPMChoiceScene(Scene):
  """
  Class for Computer Vs Computer Choice scene
  """
  def __init__(self, manager: SceneManager, width, height):
    super().__init__(manager)
    self.title = pygame.font.Font(None, 50).render("Breakthrough - Choose Options", True, (255, 255, 255))
    self.width = width
    self.height = height
    self.DROP_TYPE_1 = Dropdown(
      x=150, y=150, w=100, h=24,
      main_color=(50, 50, 50),
      hover_color=(80, 80, 80),
      font_color=(255, 255, 255),
      options=gv.AI_FUNCTION_TYPES_OPTIONS,
      font=pygame.font.Font(None, 18),
      label_text="Algorithm for black",
      selected_index=gv.ai_function_one_type_index,
      on_change=gv.handle_ai_one_function_type_index_change,
    )
    self.DROP_TYPE_2 = Dropdown(
      x=350, y=150, w=100, h=24,
      main_color=(50, 50, 50),
      hover_color=(80, 80, 80),
      font_color=(255, 255, 255),
      options=gv.AI_FUNCTION_TYPES_OPTIONS,
      font=pygame.font.Font(None, 18),
      label_text="Algorithm for white",
      selected_index=gv.ai_function_two_type_index,
      on_change=gv.handle_ai_two_function_type_index_change,
    )
    self.DROP = Dropdown(
      x=150, y=250, w=100, h=24,
      main_color=(50, 50, 50),
      hover_color=(80, 80, 80),
      font_color=(255, 255, 255),
      options=gv.AI_FUNCTION_OPTIONS,
      font=pygame.font.Font(None, 18),
      label_text="Function type for black",
      selected_index=gv.ai_function_one_index,
      on_change=gv.handle_ai_one_function_index_change,
    )
    self.DROP_2 = Dropdown(
      x=350, y=250, w=100, h=24,
      main_color=(50, 50, 50),
      hover_color=(80, 80, 80),
      font_color=(255, 255, 255),
      options=gv.AI_FUNCTION_OPTIONS,
      font=pygame.font.Font(None, 18),
      label_text="Function type for white",
      selected_index=gv.ai_function_two_index,
      on_change=gv.handle_ai_two_function_index_change,
    )
    self.PLAY_BTN = Button(text_input="Play", font=pygame.font.Font(None, 18), base_color="#d7fcd4", hovering_color="white", pos=(width / 2, height / 2 + 120))
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
        if self.PLAY_BTN.checkForInput(pygame.mouse.get_pos()):
          self.manager.set_scene("game")
        if self.BACK_BTN.checkForInput(pygame.mouse.get_pos()):
          self.manager.set_scene("menu")
      self.DROP.handle_event(event=e)
      self.DROP_2.handle_event(event=e)
      self.DROP_TYPE_2.handle_event(event=e)
      self.DROP_TYPE_1.handle_event(event=e)

  def draw(self, surface):
    surface.fill((0, 0, 0))

    surface.blit(self.title, (self.width // 2 - self.title.get_width() // 2, 80))

    for button in [self.PLAY_BTN, self.BACK_BTN]:
      button.changeColor(pygame.mouse.get_pos())
      button.update(surface)

    self.DROP.draw(surface)
    self.DROP_2.draw(surface)
    self.DROP_TYPE_1.draw(surface)
    self.DROP_TYPE_2.draw(surface)
