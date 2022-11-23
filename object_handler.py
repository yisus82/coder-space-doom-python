from os.path import join
from random import choices, randrange

from enemy import CacoDemonNPC, CyberDemonNPC, SoldierNPC
from sprite_object import AnimatedSprite, SpriteObject


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.enemy_list = []
        self.enemy_positions = []
        self.static_sprite_folder = 'resources/sprites/static_sprites/'
        self.animated_sprite_folder = 'resources/sprites/animated_sprites/'

        # sprites
        self.add_sprite('candelabra', 'static', (10.5, 3.5))
        self.add_sprite('green_light', 'animated', (11.5, 3.5))
        self.add_sprite('green_light', 'animated', (1.5, 1.5))
        self.add_sprite('green_light', 'animated', (1.5, 7.5))
        self.add_sprite('green_light', 'animated', (5.5, 3.25))
        self.add_sprite('green_light', 'animated', (5.5, 4.75))
        self.add_sprite('green_light', 'animated', (7.5, 2.5))
        self.add_sprite('green_light', 'animated', (7.5, 5.5))
        self.add_sprite('green_light', 'animated', (14.5, 1.5))
        self.add_sprite('green_light', 'animated', (14.5, 4.5))
        self.add_sprite('green_light', 'animated', (14.5, 24.5))
        self.add_sprite('green_light', 'animated', (14.5, 30.5))
        self.add_sprite('green_light', 'animated', (1.5, 30.5))
        self.add_sprite('green_light', 'animated', (1.5, 24.5))
        self.add_sprite('red_light', 'animated', (14.5, 5.5))
        self.add_sprite('red_light', 'animated', (14.5, 7.5))
        self.add_sprite('red_light', 'animated', (12.5, 7.5))
        self.add_sprite('red_light', 'animated', (9.5, 7.5))
        self.add_sprite('red_light', 'animated', (14.5, 12.5))
        self.add_sprite('red_light', 'animated', (9.5, 20.5))
        self.add_sprite('red_light', 'animated', (10.5, 20.5))
        self.add_sprite('red_light', 'animated', (3.5, 14.5))
        self.add_sprite('red_light', 'animated', (3.5, 18.5))

        # enemies
        self.enemy_count = 20
        self.enemy_types = ['soldier', 'caco_demon', 'cyber_demon']
        self.weights = [70, 20, 10]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.spawn_enemies()

    def add_sprite(self, sprite_name, sprite_type, position):
        if sprite_type == 'static':
            sprite_path = join(self.static_sprite_folder, sprite_name)
            sprite = SpriteObject(self.game, sprite_path, position)
        elif sprite_type == 'animated':
            sprite_path = join(self.animated_sprite_folder, sprite_name)
            sprite = AnimatedSprite(self.game, sprite_path, position)
        else:
            return
        self.sprite_list.append(sprite)

    def add_enemy(self, enemy_type, position):
        if enemy_type == 'soldier':
            enemy = SoldierNPC(self.game, position)
        elif enemy_type == 'caco_demon':
            enemy = CacoDemonNPC(self.game, position)
        elif enemy_type == 'cyber_demon':
            enemy = CyberDemonNPC(self.game, position)
        else:
            return
        self.enemy_list.append(enemy)

    def spawn_enemies(self):
        for _ in range(self.enemy_count):
            enemy_type = choices(self.enemy_types, self.weights)[0]
            position = x, y = randrange(
                self.game.map.cols), randrange(self.game.map.rows)
            while (position in self.game.map.obstacles) or (position in self.restricted_area) or (position in self.enemy_positions):
                position = x, y = randrange(
                    self.game.map.cols), randrange(self.game.map.rows)
            self.add_enemy(enemy_type, (x + 0.5, y + 0.5))
            self.enemy_positions.append(position)

    def check_win(self):
        if not len(self.enemy_positions):
            self.game.win_game()

    def update(self):
        for sprite in self.sprite_list:
            sprite.update()
        for enemy in self.enemy_list:
            enemy.update()
        self.enemy_positions = [
            enemy.map_position for enemy in self.enemy_list if enemy.alive]
        self.check_win()
