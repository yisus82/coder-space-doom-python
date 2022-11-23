from math import atan2, cos, hypot, pi, tan, tau
from os import walk
from os.path import join, normpath

import pygame

from settings import WINDOW_HEIGHT, WINDOW_WIDTH


class SpriteObject:
    def __init__(self, game, path, position, sprite_scale=0.7, height_shift=0.27):
        self.game = game
        self.images = self.import_images(path)
        self.image = self.images[0]
        self.x, self.y = position
        self.sprite_scale = sprite_scale
        self.height_shift = height_shift
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.field_of_vision = pi / 3
        self.num_rays = WINDOW_WIDTH // 2
        self.delta_angle = self.field_of_vision / self.num_rays
        self.screen_distance = self.num_rays / tan(self.field_of_vision / 2)
        self.scale = WINDOW_WIDTH // self.num_rays

    def import_images(self, path):
        normalized_path = normpath(path)
        image_surfaces = []
        for _, _, filenames in walk(normalized_path):
            for filename in sorted(filenames):
                full_path = join(normalized_path, filename)
                try:
                    image_surface = pygame.image.load(
                        full_path).convert_alpha()
                    image_surfaces.append(image_surface)
                except pygame.error:
                    pass
            break
        return image_surfaces

    def get_sprite_projection(self):
        projection = self.screen_distance / self.norm_dist * self.sprite_scale
        image_ratio = self.image.get_width() / self.image.get_height()
        projection_width, projection_height = projection * image_ratio, projection
        image = pygame.transform.scale(
            self.image, (projection_width, projection_height))
        self.sprite_half_width = projection_width // 2
        height_shift = projection_height * self.height_shift
        position = self.screen_x - self.sprite_half_width, WINDOW_HEIGHT // 2 - \
            projection_height // 2 + height_shift
        return (image, position)

    def render_sprite(self):
        self.dx = self.x - self.game.player.x
        self.dy = self.y - self.game.player.y
        self.theta = atan2(self.dy, self.dx)
        delta = self.theta - self.game.player.angle
        if (self.dx > 0 and self.game.player.angle > pi) or (self.dx < 0 and self.dy < 0):
            delta += tau
        delta_rays = delta / self.delta_angle
        self.screen_x = (self.num_rays // 2 + delta_rays) * self.scale
        self.dist = hypot(self.dx, self.dy)
        self.norm_dist = self.dist * cos(delta)
        if -self.image.get_width() // 2 < self.screen_x < (WINDOW_WIDTH + self.image.get_width() // 2) and self.norm_dist > 0.5:
            image, position = self.get_sprite_projection()
            self.game.ray_casting.objects_to_render.append(
                (self.norm_dist, image, position))

    def update(self):
        self.render_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path, position, sprite_scale=0.8, height_shift=0.16, animation_speed=0.14):
        super().__init__(game, path, position, sprite_scale, height_shift)
        self.animation_speed = animation_speed
        self.frame_index = 0

    def update(self):
        super().update()
        self.animate()

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.images):
            self.frame_index = 0
        self.image = self.images[int(self.frame_index)]
