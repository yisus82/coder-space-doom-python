from os.path import normpath

import pygame

from settings import (DIGIT_SIZE, FLOOR_COLOR, TEXTURE_SIZE, WINDOW_HEIGHT,
                      WINDOW_WIDTH)


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.wall_textures = {i: self.get_texture(
            f'resources/textures/walls/{i}.png') for i in range(1, 6)}
        self.sky_image = self.get_texture(
            'resources/textures/sky.png', (WINDOW_WIDTH, WINDOW_HEIGHT // 2))
        self.sky_offset = 0
        self.blood_screen = self.get_texture(
            'resources/textures/blood_screen.png', (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.digits = {str(i): self.get_texture(f'resources/textures/digits/{i}.png', [DIGIT_SIZE] * 2)
                       for i in range(10)}
        self.game_over_image = self.get_texture(
            'resources/textures/game_over.png', (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.win_image = self.get_texture(
            'resources/textures/win.png', (WINDOW_WIDTH, WINDOW_HEIGHT))

    def get_texture(self, path, resolution=(TEXTURE_SIZE, TEXTURE_SIZE)):
        normalized_path = normpath(path)
        image = pygame.image.load(normalized_path).convert_alpha()
        return pygame.transform.scale(image, resolution)

    def draw_game_objects(self):
        objects_to_render = sorted(
            self.game.ray_casting.objects_to_render, key=lambda o: o[0], reverse=True)
        for _, image, pos in objects_to_render:
            self.game.screen.blit(image, pos)

    def draw_win_image(self):
        self.game.screen.blit(self.win_image, (0, 0))

    def draw_game_over_image(self):
        self.game.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.game.screen.blit(
                self.digits[char], (WINDOW_WIDTH // 2 - DIGIT_SIZE * len(health) // 2 + i * DIGIT_SIZE, 20))

    def draw_player_damage(self):
        self.game.screen.blit(self.blood_screen, (0, 0))

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
        self.draw_game_objects()
        self.draw_player_health()
