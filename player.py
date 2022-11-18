from math import cos, sin, tau

import pygame

from settings import (MOUSE_BORDER_LEFT, MOUSE_BORDER_RIGHT,
                      MOUSE_MAX_RELATIVE_MOVEMENT, MOUSE_SENSITIVITY,
                      PLAYER_ANGLE, PLAYER_POSITION, PLAYER_SIZE_SCALE,
                      PLAYER_SPEED, WINDOW_HEIGHT, WINDOW_WIDTH)


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POSITION
        self.angle = PLAYER_ANGLE
        self.speed = PLAYER_SPEED

    @property
    def position(self):
        return self.x, self.y

    @property
    def map_position(self):
        return int(self.x), int(self.y)

    def mouse_input(self):
        mouse_x = pygame.mouse.get_pos()[0]
        if mouse_x < MOUSE_BORDER_LEFT or mouse_x > MOUSE_BORDER_RIGHT:
            pygame.mouse.set_pos([WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2])
        self.relative_movement = pygame.mouse.get_rel()[0]
        self.relative_movement = max(-MOUSE_MAX_RELATIVE_MOVEMENT,
                                     min(MOUSE_MAX_RELATIVE_MOVEMENT, self.relative_movement))
        self.angle += self.relative_movement * MOUSE_SENSITIVITY * self.game.delta_time
        self.angle %= tau

    def keyboard_input(self):
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

    def move(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.game.map.is_empty(self.x + dx * scale, self.y):
            self.x += dx
        if self.game.map.is_empty(self.x, self.y + dy * scale):
            self.y += dy

    def draw(self):
        pygame.draw.circle(self.game.screen, 'green',
                           (self.x * 100, self.y * 100), 15)

    def update(self):
        self.mouse_input()
        self.keyboard_input()
