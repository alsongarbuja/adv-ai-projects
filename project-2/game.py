import pygame

from scene.scene import SceneManager
from scene.menu import MenuScene
from scene.game_scene import GameScene
from scene.cmp_choice import PlayerVsCMPChoiceScene
from scene.cmp_vs_cmp_choice import CMPVSCPMChoiceScene

pygame.init()
WIDTH, HEIGHT = 700, 560
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

def main():
  manager = SceneManager()
  manager.add_scene("menu", MenuScene(manager=manager, width=WIDTH, height=HEIGHT))
  manager.add_scene("game", GameScene(manager=manager, scene=SCREEN, width=WIDTH, height=HEIGHT))
  manager.add_scene("choice-auto", CMPVSCPMChoiceScene(manager=manager, width=WIDTH, height=HEIGHT))
  manager.add_scene("choice-vs-cmp", PlayerVsCMPChoiceScene(manager=manager, width=WIDTH, height=HEIGHT))
  manager.set_scene("menu")

  while 1:
    events = pygame.event.get()
    manager.handle_events(events)
    manager.update()
    manager.draw(SCREEN)

    pygame.display.flip()
    CLOCK.tick(60)

if __name__ == '__main__':
    main()
