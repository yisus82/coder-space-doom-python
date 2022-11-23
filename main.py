import sys

import pygame

from map import Map
from object_handler import ObjectHandler
from object_renderer import ObjectRenderer
from path_finder import PathFinder
from player import Player
from ray_casting import RayCasting
from settings import FPS, TITLE, WINDOW_HEIGHT, WINDOW_WIDTH


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.delta_time = 1
        self.background_music = pygame.mixer.Sound(
            'resources/sounds/background.mp3')
        self.background_music.set_volume(0.4)
        self.new_game()

    def new_game(self):
        self.is_game_over = False
        self.win = False
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.ray_casting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.path_finder = PathFinder(self)
        self.background_music.play(-1)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if self.is_game_over or self.win:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.new_game()
                    return
            self.player.handle_event(event)

    def game_over(self):
        self.is_game_over = True

    def win_game(self):
        self.win = True

    def update(self):
        if self.is_game_over:
            self.object_renderer.draw_game_over_image()
        elif self.win:
            self.object_renderer.draw_win_image()
        else:
            self.player.update()
            self.ray_casting.update()
            self.object_handler.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pygame.display.set_caption(
            f"{TITLE} - {self.clock.get_fps():.2f} FPS")

    def draw(self):
        self.object_renderer.draw()
        self.player.draw()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
