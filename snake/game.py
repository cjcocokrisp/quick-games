import pygame as pg
from settings import *
from sprites import Button, Player, PlayerBody, Point
from random import randint
import json

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.block_size = 25
        self.score = 0
        self.state = 'menu'

    def new(self):
        self.all_sprites = pg.sprite.Group()
        if self.state == 'menu':
            self.data = self.load_data()
            self.play_button = Button(300, 100, WIDTH / 2 - 150, HEIGHT / 2, WHITE)
            self.quit_button = Button(300, 100, WIDTH / 2 - 150, HEIGHT / 2 + 125, WHITE)
            self.all_sprites.add(self.play_button, self.quit_button)
        elif self.state == 'playing':
            self.points = pg.sprite.Group()
            self.player_body = pg.sprite.Group()
            self.player = Player(self, 100, 250)
            point_cords = self.calc_point_cords()
            self.point = Point(self, point_cords[0], point_cords[1])
            self.points.add(self.point)
            self.all_sprites.add(self.player, self.point)
        elif self.state == 'game_over':
            self.return_button = Button(300, 100, WIDTH / 2 - 150, HEIGHT / 2 + 70, WHITE)
            self.all_sprites.add(self.return_button)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            if self.state == 'menu':
                self.menu()
            elif self.state == 'playing':
                self.update()
            elif self.state == 'game_over':
                self.game_over()
            self.draw()

    def menu(self):
        mouse_pos = pg.mouse.get_pos()

        if pg.mouse.get_pressed()[0] and self.play_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.state = 'playing'
                self.playing = False
                self.new()

        if pg.mouse.get_pressed()[0] and self.quit_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.running = False 
                self.playing = False

    def update(self):
        self.all_sprites.update()

        point_hits = pg.sprite.spritecollide(self.player, self.points, False)
        for hit in point_hits:
            hit.kill()
            point_cords = self.calc_point_cords()
            point = Point(self, point_cords[0], point_cords[1])
            self.points.add(point)
            increase_length = PlayerBody(self, self.player, False)
            self.player_body.add(increase_length)
            self.all_sprites.add(point, increase_length)
            self.score += 1

        body_hits = pg.sprite.spritecollide(self.player, self.player_body, False)
        for hit in body_hits:
            self.playing = False
            self.state = 'game_over'
            self.new()

        if self.player.rect.x > WIDTH - self.block_size or self.player.rect.x < self.block_size:
            self.playing = False
            self.state = 'game_over'
            self.new()

        if self.player.rect.y > HEIGHT - self.block_size or self.player.rect.y < self.block_size:
            self.playing = False
            self.state = 'game_over'
            self.new()

    def game_over(self):
        body_reset = PlayerBody(self, self.player, True)
        try: 
            if self.new_hs:
                pass
        except:
            if self.score > self.data['high_score']:
                self.new_hs = True
                self.data['high_score'] = self.score
            else:
                self.new_hs = False

        mouse_pos = pg.mouse.get_pos()

        if pg.mouse.get_pressed()[0] and self.return_button.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.data['total_score'] += self.score
                self.data['games_played'] += 1
                self.save_data()
                self.state = 'menu'
                self.playing = False
                self.new()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                self.running = False

    def draw(self):
        self.screen.fill((0, 40, 0))
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        if self.state == 'menu':
            self.draw_text("SNAKE", 64, WHITE, WIDTH / 2, 100)
            self.draw_text("PLAY", 48, BLACK, WIDTH / 2, HEIGHT / 2 + 25)
            self.draw_text("QUIT", 48, BLACK, WIDTH / 2, HEIGHT / 2 + 150)
            self.draw_text(f"High Score: {self.data['high_score']}", 48, WHITE, WIDTH / 2, 200)
        elif self.state == 'playing':
            self.draw_text(f"Score: {self.score}", 20, WHITE, WIDTH / 2, 0)
        elif self.state == 'game_over':
            self.draw_text("GAME OVER!", 64, WHITE, WIDTH / 2, HEIGHT / 2 - 125)
            self.draw_text(f"Score: {self.score}", 48, WHITE, WIDTH / 2, HEIGHT / 2 - 55)
            self.draw_text("CONTINUE", 48, BLACK, WIDTH / 2, HEIGHT / 2 + 90)
            if self.new_hs:
                self.draw_text("NEW HIGH SCORE!", 48, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font('assets/comicsans.ttf', size)
        text_surface = font.render(text, True, color) 
        text_rect = text_surface.get_rect() 
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_grid(self):
            green = 'light'
            for x in range(self.block_size, self.block_size * 22, self.block_size):
                for y in range(self.block_size, self.block_size * 22, self.block_size):
                    if green == 'light':
                        color = GREEN
                        rect = pg.Rect(x, y, self.block_size, self.block_size)
                        pg.draw.rect(self.screen, color, rect)
                        green = 'dark'
                    elif green == 'dark':
                        color = DARK_GREEN
                        rect = pg.Rect(x, y, self.block_size, self.block_size)
                        pg.draw.rect(self.screen, color, rect)
                        green = 'light'
        
    def calc_point_cords(self):
        x = randint(25, WIDTH - 50)
        while x % 25 != 0:
            x -= 1
        y = randint(25, HEIGHT - 50)
        while y % 25 != 0:
            y -= 1

        return (x, y)

    def load_data(self):
        with open('data.json', 'r') as f:
            data = json.load(f)

        f.close()
        return data

    def save_data(self):
        with open('data.json', 'w') as f:
            json.dump(self.data, f, indent=4)

        f.close()