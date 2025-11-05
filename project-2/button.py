import pygame

class Button():
  def __init__(self, font: pygame.font.Font, pos, text_input, base_color, hovering_color):
    self.x_pos = pos[0]
    self.y_pos = pos[1]
    self.font = font
    self.text_input = text_input
    self.base_color = base_color
    self.hovering_color = hovering_color
    self.image = pygame.image.load("assets/button_rect.png")
    self.text = self.font.render(self.text_input, True, self.base_color)
    self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
    self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

  def update(self, screen: pygame.Surface):
    screen.blit(self.image, self.rect)
    screen.blit(self.text, self.text_rect)

  def checkForInput(self, position):
    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
      return True
    return False

  def changeColor(self, position):
    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
      self.text = self.font.render(self.text_input, True, self.hovering_color)
    else:
      self.text = self.font.render(self.text_input, True, self.base_color)
