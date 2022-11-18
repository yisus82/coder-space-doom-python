from math import cos, pi, sin, tan

import pygame

from settings import MAX_DEPTH, TEXTURE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.field_of_vision = pi / 3
        self.num_rays = WINDOW_WIDTH // 2
        self.delta_angle = self.field_of_vision / self.num_rays
        self.screen_distance = self.num_rays / tan(self.field_of_vision / 2)
        self.scale = WINDOW_WIDTH // self.num_rays
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def update_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, projection_height, texture, offset = values
            if projection_height < WINDOW_HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE -
                              self.scale), 0, self.scale, TEXTURE_SIZE
                )
                wall_column = pygame.transform.scale(
                    wall_column, (self.scale, projection_height))
                wall_position = (ray * self.scale, WINDOW_HEIGHT //
                                 2 - projection_height // 2)
            else:
                texture_height = TEXTURE_SIZE * WINDOW_HEIGHT / projection_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - self.scale), TEXTURE_SIZE / 2 -
                    texture_height // 2,
                    self.scale, texture_height
                )
                wall_column = pygame.transform.scale(
                    wall_column, (self.scale, WINDOW_HEIGHT))
                wall_position = (ray * self.scale, 0)
            self.objects_to_render.append((depth, wall_column, wall_position))

    def ray_cast(self):
        self.ray_casting_result = []
        texture_vertical, texture_horizontal = 1, 1
        player_x, player_y = self.game.player.position
        map_x, map_y = self.game.player.map_position
        ray_angle = self.game.player.angle - self.field_of_vision / 2 + 0.0001
        for ray in range(self.num_rays):
            sin_a = sin(ray_angle)
            cos_a = cos(ray_angle)

            # horizontals
            y_horizontal, dy = (
                map_y + 1, 1) if sin_a > 0 else (map_y - 1e-6, -1)
            depth_horizontal = (y_horizontal - player_y) / sin_a
            x_horizontal = player_x + depth_horizontal * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a
            for _ in range(MAX_DEPTH):
                tile_horizontal = int(x_horizontal), int(y_horizontal)
                if tile_horizontal in self.game.map.obstacles:
                    texture_horizontal = self.game.map.obstacles[tile_horizontal]
                    break
                x_horizontal += dx
                y_horizontal += dy
                depth_horizontal += delta_depth

            # verticals
            x_vertical, dx = (
                map_x + 1, 1) if cos_a > 0 else (map_x - 1e-6, -1)
            depth_vertical = (x_vertical - player_x) / cos_a
            y_vertical = player_y + depth_vertical * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a
            for _ in range(MAX_DEPTH):
                tile_vertical = int(x_vertical), int(y_vertical)
                if tile_vertical in self.game.map.obstacles:
                    texture_vertical = self.game.map.obstacles[tile_vertical]
                    break
                x_vertical += dx
                y_vertical += dy
                depth_vertical += delta_depth

            # depth and texture offset
            if depth_vertical < depth_horizontal:
                depth, texture = depth_vertical, texture_vertical
                y_vertical %= 1
                offset = y_vertical if cos_a > 0 else (1 - y_vertical)
            else:
                depth, texture = depth_horizontal, texture_horizontal
                x_horizontal %= 1
                offset = (1 - x_horizontal) if sin_a > 0 else x_horizontal

            # remove fishbowl effect
            depth *= cos(self.game.player.angle - ray_angle)

            # projection
            projection_height = self.screen_distance / (depth + 0.0001)

            # ray casting result
            self.ray_casting_result.append(
                (depth, projection_height, texture, offset))

            ray_angle += self.delta_angle

    def update(self):
        self.ray_cast()
        self.update_objects_to_render()
