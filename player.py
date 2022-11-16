from math import cos, sin, tau

import pygame

from settings import (PLAYER_ANGLE, PLAYER_POSITION, PLAYER_ROTATION_SPEED,
                      PLAYER_SPEED, WINDOW_WIDTH)


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POSITION
        self.angle = PLAYER_ANGLE
        self.speed = PLAYER_SPEED
        self.rotation_speed = PLAYER_ROTATION_SPEED

    @property
    def position(self):
        return self.x, self.y

    @property
    def map_position(self):
        return int(self.x), int(self.y)

    def movement_input(self):
        sin_a = sin(self.angle)
        cos_a = cos(self.angle)
        dx, dy = 0, 0
        speed = self.speed * self.game.delta_time
        speed_sin = sin_a * speed
        speed_cos = cos_a * speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx += speed_cos
            dy += speed_sin
        elif keys[pygame.K_s]:
            dx -= speed_cos
            dy -= speed_sin
        elif keys[pygame.K_a]:
            dx += speed_sin
            dy -= speed_cos
        elif keys[pygame.K_d]:
            dx -= speed_sin
            dy += speed_cos
        self.move(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed * self.game.delta_time
        elif keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed * self.game.delta_time
        self.angle %= tau

    def move(self, dx, dy):
        if self.game.map.is_empty(self.x + dx, self.y):
            self.x += dx
        if self.game.map.is_empty(self.x, self.y + dy):
            self.y += dy

    def draw(self):
        pygame.draw.line(self.game.screen,
                         'yellow',
                         (self.x * 100, self.y * 100),
                         (self.x * 100 + WINDOW_WIDTH * cos(self.angle),
                             self.y * 100 + WINDOW_WIDTH * sin(self.angle)),
                         2)
        pygame.draw.circle(self.game.screen, 'green',
                           (self.x * 100, self.y * 100), 15)

    def update(self):
        self.movement_input()
