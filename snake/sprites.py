import pygame as pg

from settings import BLUE, RED

class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.block_size = game.block_size
        self.image = pg.Surface((self.block_size, self.block_size))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = (1, 0)
        self.cords = []
        self.move_cooldown = 0

    def update(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.direction = (0, -1)
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.direction = (0, 1)
        elif keys[pg.K_LEFT] or keys[pg.K_a]:
            self.direction = (-1, 0)
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.direction = (1, 0)

        if self.move_cooldown == 8:
            self.cords.insert(0, (self.rect.x, self.rect.y))
            self.rect.x += (self.block_size * self.direction[0])
            self.rect.y += (self.block_size * self.direction[1])
            self.move_cooldown = 0

        self.move_cooldown += 1

class PlayerBody(pg.sprite.Sprite):
    
    _id_num = -1

    def __new__(cls, game, head, reset):
        if not reset:
            cls._id_num += 1
            return super().__new__(cls)
        else:
            cls._id_num = -1

    def __init__(self, game, head, reset):
        pg.sprite.Sprite.__init__(self)
        self.cords = head.cords
        self.image = pg.Surface((game.block_size, game.block_size))
        self.image.fill((BLUE))
        self.rect = self.image.get_rect()
        self.id_num = self._id_num
        self.rect.x = self.cords[self.id_num][0]
        self.rect.y = self.cords[self.id_num][1]
        self.head = head

    def update(self):
        self.rect.x = self.head.cords[self.id_num][0]
        self.rect.y = self.head.cords[self.id_num][1]

class Point(pg.sprite.Sprite):

    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((game.block_size, game.block_size))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Button(pg.sprite.Sprite):

    def __init__(self, width, height, x, y, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
