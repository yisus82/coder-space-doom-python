from sprite_object import AnimatedSprite, SpriteObject


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.animated_sprite_path = 'resources/sprites/animated_sprites/'

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

    def update(self):
        for sprite in self.sprite_list:
            sprite.update()

    def add_sprite(self, sprite_name, sprite_type, position):
        if sprite_type == 'static':
            sprite_path = self.static_sprite_path + sprite_name
            sprite = SpriteObject(self.game, sprite_path, position)
        elif sprite_type == 'animated':
            sprite_path = self.animated_sprite_path + sprite_name
            sprite = AnimatedSprite(self.game, sprite_path, position)
        else:
            return
        self.sprite_list.append(sprite)
