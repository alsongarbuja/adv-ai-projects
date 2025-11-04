import pygame

from screen import ScreenManager, MenuScreen, GameScreen

pygame.init()
WIDTH, HEIGHT = 700, 560
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.Font(None, 50)

def main():
  manager = ScreenManager()
  manager.add_screen("menu", MenuScreen(manager=manager, width=WIDTH, Font=FONT))
  manager.add_screen("game", GameScreen(manager=manager, screen=SCREEN, width=WIDTH, height=HEIGHT))
  # game = BreakthroughGame()
  manager.set_screen("menu")

  while 1:
    events = pygame.event.get()
    manager.handle_events(events)
    manager.update()
    manager.draw(SCREEN, FONT)

    pygame.display.flip()
    CLOCK.tick(60)
    # game.run()

if __name__ == '__main__':
    main()
