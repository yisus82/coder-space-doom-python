from math import atan2, cos, sin
from os.path import join
from random import randint, random

import pygame

from settings import MAX_DEPTH, WINDOW_WIDTH
from sprite_object import AnimatedSprite


class NPC(AnimatedSprite):
    def __init__(self, game, enemy_type, position, scale, shift, animation_time):
        enemies_folder = 'resources/sprites/enemies'
        enemy_path = join(enemies_folder, enemy_type)
        super().__init__(game, enemy_path, position, scale, shift, animation_time)
        self.import_animations(enemy_path)
        self.status = None
        self.update_status('idle')
        sounds_folder = 'resources/sounds/enemies'
        self.import_sounds(sounds_folder)
        self.alive = True
        self.invulnerable = False
        self.invulnerability_time = 0
        self.invulnerability_cooldown = 1500
        self.attacking = False
        self.attack_time = 0
        self.attack_cooldown = 1000
        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 20
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.ray_cast_value = False
        self.chasing_player = False

    def import_animations(self, enemy_path):
        self.animations = {
            'attack': [],
            'death': [],
            'idle': [],
            'pain': [],
            'walk': [],
        }
        for animation_name in self.animations.keys():
            animation_folder = join(enemy_path, animation_name)
            self.animations[animation_name] = self.import_images(
                animation_folder)

    def import_sounds(self, sounds_folder):
        self.sounds = {
            'attack': pygame.mixer.Sound(join(sounds_folder, 'attack.wav')),
            'death': pygame.mixer.Sound(join(sounds_folder, 'death.wav')),
            'pain': pygame.mixer.Sound(join(sounds_folder, 'pain.wav')),
        }

    @property
    def map_position(self):
        return int(self.x), int(self.y)

    def check_hit(self):
        if self.ray_cast_value and self.game.player.weapon.shooting and not self.invulnerable:
            if WINDOW_WIDTH // 2 - self.sprite_half_width < self.screen_x < WINDOW_WIDTH // 2 + self.sprite_half_width:
                self.invulnerable = True
                self.invulnerability_time = pygame.time.get_ticks()
                self.update_status('pain')
                self.sounds['pain'].play()
                self.health -= self.game.player.weapon.damage
                self.check_health()
        elif self.status == 'pain' and not self.invulnerable:
            self.update_status('idle')

    def check_health(self):
        if self.health <= 0:
            self.update_status('death')
            self.sounds['death'].play()

    def update_status(self, new_status):
        if self.status is None or self.status != new_status:
            self.status = new_status
            self.frame_index = 0
            if self.status in self.animations:
                self.images = self.animations[self.status]
                self.image = self.animations[self.status][self.frame_index]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False
        if self.invulnerable and current_time - self.invulnerability_time >= self.invulnerability_cooldown:
            self.invulnerable = False

    def ray_cast_player(self):
        if self.game.player.map_position == self.map_position:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0
        ox, oy = self.game.player.position
        x_map, y_map = self.game.player.map_position
        ray_angle = self.theta
        sin_a = sin(ray_angle)
        cos_a = cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a
        for _ in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_position:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.obstacles:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a
        for _ in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_position:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.obstacles:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)
        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        else:
            return False

    def movement(self):
        next_position = self.game.path_finder.get_path(
            self.map_position, self.game.player.map_position)
        next_x, next_y = next_position
        if next_position not in self.game.object_handler.enemy_positions:
            angle = atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = cos(angle) * self.speed
            dy = sin(angle) * self.speed
            self.move(dx, dy)

    def move(self, dx, dy):
        if self.game.map.is_empty(self.x + dx * self.size, self.y):
            self.x += dx
        if self.game.map.is_empty(self.x, self.y + dy * self.size):
            self.y += dy

    def attack(self):
        if not self.attacking:
            self.attacking = True
            attack_sound = self.sounds['attack']
            attack_sound.set_volume(0.4)
            attack_sound.play()
            if random() < self.accuracy:
                self.game.player.take_damage(self.attack_damage)

    def update(self):
        if self.alive:
            self.render_sprite()
            self.ray_cast_value = self.ray_cast_player()
            self.cooldowns()
            if self.status != 'death':
                self.check_hit()
                if self.status != 'pain':
                    if self.dist <= self.attack_dist:
                        self.update_status('attack')
                        self.attack()
                    elif self.ray_cast_value or self.chasing_player:
                        self.chasing_player = True
                        self.update_status('walk')
                        self.movement()
            elif self.frame_index >= len(self.animations[self.status]) - 1:
                self.alive = False
                return
            self.animate()


class SoldierNPC(NPC):
    def __init__(self, game, position, scale=0.6, shift=0.38, animation_time=0.10):
        super().__init__(game, 'soldier', position, scale, shift, animation_time)


class CacoDemonNPC(NPC):
    def __init__(self, game, position, scale=0.7, shift=0.27, animation_time=0.05):
        super().__init__(game, 'caco_demon', position, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35


class CyberDemonNPC(NPC):
    def __init__(self, game, position, scale=1.0, shift=0.04, animation_time=0.08):
        super().__init__(game, 'cyber_demon', position, scale, shift, animation_time)
        self.attack_dist = 6
        self.health = 350
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25
