from os.path import join

import pygame

from settings import WINDOW_HEIGHT, WINDOW_WIDTH
from sprite_object import AnimatedSprite


class Weapon(AnimatedSprite):
    def __init__(self, player, weapon_name, game, scale, animation_time, damage):
        weapons_folder = 'resources/sprites/weapons'
        weapon_path = join(weapons_folder, weapon_name)
        sound_folder = 'resources/sounds/weapons'
        sound_path = join(sound_folder, weapon_name + '.wav')
        self.sound = pygame.mixer.Sound(sound_path)
        self.player = player
        super().__init__(game, weapon_path, self.player.position, scale, animation_time)
        self.images = [pygame.transform.smoothscale(image, (self.image.get_width() * scale, self.image.get_height() * scale))
                       for image in self.images]
        self.image = self.images[0]
        self.weapon_pos = (
            WINDOW_WIDTH // 2 - self.images[0].get_width() // 2, WINDOW_HEIGHT - self.images[0].get_height())
        self.damage = damage
        self.shooting = False

    def fire(self):
        if not self.shooting:
            self.shooting = True
            self.sound.play()

    def animate(self):
        self.animate_shot()

    def animate_shot(self):
        if self.shooting:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.images):
                self.frame_index = 0
                self.shooting = False
            self.image = self.images[int(self.frame_index)]

    def draw(self):
        self.game.screen.blit(self.image, self.weapon_pos)
