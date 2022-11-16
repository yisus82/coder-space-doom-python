from math import cos, sin

import pygame

from settings import DELTA_ANGLE, HALF_FIELD_OF_VISION, MAX_DEPTH, NUM_RAYS


class RayCasting:
    def __init__(self, game):
        self.game = game

    def ray_cast(self):
        player_x, player_y = self.game.player.position
        map_x, map_y = self.game.player.map_position
        ray_angle = self.game.player.angle - HALF_FIELD_OF_VISION + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = sin(ray_angle)
            cos_a = cos(ray_angle)

            # horizontals
            y_hor, dy = (map_y + 1, 1) if sin_a > 0 else (map_y - 1e-6, -1)
            depth_hor = (y_hor - player_y) / sin_a
            x_hor = player_x + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a
            for _ in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.obstacle_positions:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (map_x + 1, 1) if cos_a > 0 else (map_x - 1e-6, -1)
            depth_vert = (x_vert - player_x) / cos_a
            y_vert = player_y + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a
            for _ in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.obstacle_positions:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth
            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor

            # draw for debugging purposes
            pygame.draw.line(self.game.screen, 'yellow',
                             (player_x * 100, player_y * 100),
                             (100 * player_x + 100 * depth * cos_a,
                              100 * player_y + 100 * depth * sin_a),
                             2)

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
