from os.path import normpath

import pygame

from settings import FLOOR_COLOR, TEXTURE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture(
            'resources/textures/sky.png', (WINDOW_WIDTH, WINDOW_HEIGHT // 2))
        self.sky_offset = 0

    @staticmethod
    def get_texture(path, resolution=(TEXTURE_SIZE, TEXTURE_SIZE)):
        normalized_path = normpath(path)
        image = pygame.image.load(normalized_path).convert_alpha()
        return pygame.transform.scale(image, resolution)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/wall_1.png'),
            2: self.get_texture('resources/textures/wall_2.png'),
            3: self.get_texture('resources/textures/wall_3.png'),
            4: self.get_texture('resources/textures/wall_4.png'),
            5: self.get_texture('resources/textures/wall_5.png'),
        }

    def render_game_objects(self):
        objects_to_render = sorted(
            self.game.ray_casting.objects_to_render, key=lambda o: o[0], reverse=True)
        for _, image, pos in objects_to_render:
            self.game.screen.blit(image, pos)

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 *
                           self.game.player.relative_movement) % WINDOW_WIDTH
        self.game.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.game.screen.blit(
            self.sky_image, (-self.sky_offset + WINDOW_WIDTH, 0))
        pygame.draw.rect(self.game.screen, FLOOR_COLOR,
                         (0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT))

    def draw(self):
        self.draw_background()
        self.render_game_objects()
