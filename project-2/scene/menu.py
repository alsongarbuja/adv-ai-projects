import sys
import pygame

from scene.scene import Scene, SceneManager
from utility.button import Button

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
    self.CMP_VS = Button(text_input="CMP Vs CMP", font=pygame.font.Font(None, 18), base_color="#d7fcd4", hovering_color="white", pos=(width / 2, height / 2 + 100))

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
        # If the play button is pressed change the scene to game scene
        if self.PLAY_BTN.checkForInput(pygame.mouse.get_pos()):
          self.manager.set_scene("choice-vs-cmp")
        # If the cmp vs cmp button is pressed change the scene to choice scene
        if self.CMP_VS.checkForInput(pygame.mouse.get_pos()):
          self.manager.set_scene("choice-auto")

  def draw(self, surface):
    surface.fill((0, 0, 0))

    surface.blit(self.title, (self.width // 2 - self.title.get_width() // 2, 80))

    for button in [self.PLAY_BTN, self.CMP_VS]:
      button.changeColor(pygame.mouse.get_pos())
      button.update(surface)
