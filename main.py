import sys

import pygame

from map import Map
from player import Player
from ray_casting import RayCasting
from settings import BACKGROUND_COLOR, FPS, TITLE, WINDOW_HEIGHT, WINDOW_WIDTH


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.ray_casting = RayCasting(self)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def update(self):
        self.player.update()
        self.ray_casting.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(f"{TITLE} - {self.clock.get_fps():.2f} FPS")

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.map.draw()
        self.player.draw()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
