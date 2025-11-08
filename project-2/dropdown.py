import pygame

class Dropdown:
  def __init__(self, x, y, w, h, main_color, hover_color, font, font_color, options, label_text, selected_index=0):
    self.rect = pygame.Rect(x, y, w, h)
    self.main_color = main_color
    self.hover_color = hover_color
    self.font_color = font_color
    self.font = font
    self.options = options
    self.selected_index = selected_index
    self.expanded = False
    self.label_text = label_text
    self.label_surface = self.font.render(label_text, True, font_color) if label_text else None

  def draw(self, surface):
    if self.label_surface:
      label_x = self.rect.x
      label_y = self.rect.y - self.label_surface.get_height() - 5
      surface.blit(self.label_surface, (label_x, label_y))

      # Draw main box
    pygame.draw.rect(surface, self.main_color, self.rect)
    pygame.draw.rect(surface, (100, 100, 100), self.rect, 2)

    # Draw selected text
    selected_text = self.font.render(self.options[self.selected_index], True, self.font_color)
    surface.blit(selected_text, (self.rect.x + 10, self.rect.y + 5))

    # Draw dropdown list if expanded
    if self.expanded:
      for i, option in enumerate(self.options):
        opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
        color = self.hover_color if opt_rect.collidepoint(pygame.mouse.get_pos()) else self.main_color
        pygame.draw.rect(surface, color, opt_rect)
        pygame.draw.rect(surface, (100, 100, 100), opt_rect, 1)
        text = self.font.render(option, True, self.font_color)
        surface.blit(text, (opt_rect.x + 10, opt_rect.y + 5))

  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = event.pos
      # Click on main box toggles dropdown
      if self.rect.collidepoint(mouse_pos):
        self.expanded = not self.expanded
      elif self.expanded:
        # Check options
        for i, option in enumerate(self.options):
          opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
          if opt_rect.collidepoint(mouse_pos):
            self.selected_index = i
            self.expanded = False
            return i
          else:
            # Clicked outside
            self.expanded = False
