from math import cos, sin, tau

import pygame

from settings import (MOUSE_BORDER_LEFT, MOUSE_BORDER_RIGHT,
                      MOUSE_MAX_RELATIVE_MOVEMENT, MOUSE_SENSITIVITY,
                      PLAYER_ANGLE, PLAYER_MAX_HEALTH, PLAYER_POSITION,
                      PLAYER_SIZE_SCALE, PLAYER_SPEED, WINDOW_HEIGHT,
                      WINDOW_WIDTH)
from weapon import Weapon


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POSITION
        self.angle = PLAYER_ANGLE
        self.speed = PLAYER_SPEED
        self.health = PLAYER_MAX_HEALTH
        self.weapon = Weapon(self, 'shotgun', self.game, 0.4, 0.25, 50)
        self.invulnerable = False
        self.invulnerability_time = 0
        self.invulnerability_cooldown = 1500
        self.pain_sound = pygame.mixer.Sound(
            'resources/sounds/player/pain.wav')

    @property
    def position(self):
        return self.x, self.y

    @property
    def map_position(self):
        return int(self.x), int(self.y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.weapon.fire()

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

    def check_game_over(self):
        if self.health <= 0:
            self.game.game_over()

    def take_damage(self, amount):
        if not self.invulnerable and self.health > 0:
            self.invulnerable = True
            self.invulnerability_time = pygame.time.get_ticks()
            self.health -= amount
            self.pain_sound.play()
            self.check_game_over()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.invulnerable and current_time - self.invulnerability_time >= self.invulnerability_cooldown:
            self.invulnerable = False

    def draw(self):
        self.weapon.draw()

    def update(self):
        self.cooldowns()
        self.mouse_input()
        self.keyboard_input()
        self.weapon.update()
