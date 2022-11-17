from math import cos, pi, sin, tan

import pygame

from settings import MAX_DEPTH, WINDOW_HEIGHT, WINDOW_WIDTH


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.field_of_vision = pi / 3
        self.num_rays = WINDOW_WIDTH // 2
        self.delta_angle = self.field_of_vision / self.num_rays
        self.screen_distance = self.num_rays / tan(self.field_of_vision / 2)
        self.scale = WINDOW_WIDTH // self.num_rays

    def ray_cast(self):
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
                if tile_horizontal in self.game.map.obstacle_positions:
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
                if tile_vertical in self.game.map.obstacle_positions:
                    break
                x_vertical += dx
                y_vertical += dy
                depth_vertical += delta_depth

            # depth
            if depth_vertical < depth_horizontal:
                depth = depth_vertical
            else:
                depth = depth_horizontal

            # remove fishbowl effect
            depth *= cos(self.game.player.angle - ray_angle)

            # projection
            projection_height = self.screen_distance / (depth + 0.0001)

            # draw walls
            color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            pygame.draw.rect(self.game.screen, color, (ray * self.scale, WINDOW_HEIGHT //
                             2 - projection_height // 2, self.scale, projection_height))

            ray_angle += self.delta_angle

    def update(self):
        self.ray_cast()
