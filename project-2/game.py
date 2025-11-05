import pygame

from scene import SceneManager, MenuScene, GameScene

pygame.init()
WIDTH, HEIGHT = 700, 560
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.Font(None, 50)

def main():
  manager = SceneManager()
  manager.add_scene("menu", MenuScene(manager=manager, width=WIDTH, height=HEIGHT, Font=FONT))
  manager.add_scene("game", GameScene(manager=manager, scene=SCREEN, width=WIDTH, height=HEIGHT))
  manager.set_scene("menu")

  while 1:
    events = pygame.event.get()
    manager.handle_events(events)
    manager.update()
    manager.draw(SCREEN, FONT)

    pygame.display.flip()
    CLOCK.tick(60)

if __name__ == '__main__':
    main()
