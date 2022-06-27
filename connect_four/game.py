import pygame as pg
from settings import *
from sprites import Button
from random import randint

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Connect 4")
        self.clock = pg.time.Clock()
        self.running = True
        self.red_wins = 0
        self.yellow_wins = 0

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        self.button1 = Button(132, 3, BLACK)
        self.button2 = Button(132 + 93, 3, BLACK)
        self.button3 = Button(132 + 93 * 2, 3, BLACK)
        self.button4 = Button(132 + 93 * 3, 3, BLACK)
        self.button5 = Button(132 + 93 * 4, 3, BLACK)
        self.button6 = Button(132 + 93 * 5, 3, BLACK)
        self.button7 = Button(132 + 93 * 6, 3, BLACK)
        self.buttons.add(self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7)
        self.all_sprites.add(self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7)
        if randint(0, 1) == 0:
            self.turn = 'red'
        else:
            self.turn = 'yellow'
        self.pieces_placed = 0
        self.bored = [[None for i in range(7)] for i in range(6)]
        self.pressed = False
        self.run()

    def run(self):
        self.playing = True
        self.screen.fill((255, 255, 255))
        self.draw_board()
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        
        for button in self.buttons:
            button.image.fill(self.determine_color())

        mouse_pos = pg.mouse.get_pos()

        if self.pressed and self.button1.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.place_process(0)

        if self.pressed and self.button2.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.place_process(1)

        if self.pressed and self.button3.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.place_process(2)

        if self.pressed and self.button4.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.place_process(3)

        if self.pressed and self.button5.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.place_process(4)

        if self.pressed and self.button6.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.place_process(5)

        if self.pressed and self.button7.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            self.place_process(6)

        self.pressed = False

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                self.pressed = True

    def draw(self):
        self.all_sprites.draw(self.screen)
        self.draw_text(f'Red Wins: {self.red_wins}', 48, RED, 0 + 150, HEIGHT - 64)
        self.draw_text(f'Yellow Wins: {self.yellow_wins}', 48, YELLOW, WIDTH - 180, HEIGHT - 64)
        pg.display.flip()
        
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font('assets/comicsans.ttf', size)
        text_surface = font.render(text, True, color) 
        text_rect = text_surface.get_rect() 
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_board(self):
        board = pg.Rect(75, 25, 700, 580)
        pg.draw.rect(self.screen, BLUE, board)
        for y in range(6):
            for x in range(7):
                pg.draw.circle(self.screen, WHITE, (146.4285714286 + ((CIRCLE_RADIUS * 2) * x), 545 - ((CIRCLE_RADIUS * 2) * y)), CIRCLE_RADIUS)

    def determine_color(self):
        if self.turn == 'red':
            return RED
        elif self.turn == 'yellow':
            return YELLOW

    def place_process(self, col):
        row = self.place_piece(col, self.turn)
        pg.draw.circle(self.screen, self.determine_color(), (146.4285714286 + ((CIRCLE_RADIUS * 2) * col), 545 - ((CIRCLE_RADIUS * 2) * self.determine_row(row))), CIRCLE_RADIUS)
        self.pieces_placed += 1
        if self.check_for_win(row, col):
            self.show_winner()
        self.change_turn()

    def change_turn(self):
        if self.turn == 'red':
            self.turn = 'yellow'
        elif self.turn == 'yellow':
            self.turn = 'red'  

    def place_piece(self, col, color):
        for y in range(len(self.bored)):
            try:
                if self.bored[y + 1][col] != None:
                    self.bored[y][col] = color
                    return y
            except:
                self.bored[y][col] = color
                return y

    def determine_row(self, row):
        row -= 5
        if row < 0:
            row *= -1
        return row

    def check_for_win(self, row, col):
        try:
            chain = 1
            for x in range(1, 4):
                if self.bored[row][col] == self.bored[row][col + x]:
                    chain += 1
            if chain == 4:
                return True
        except:
            pass

        try:
            chain = 1
            for x in range(1, 4):
                if self.bored[row][col] == self.bored[row][col - x]:
                    chain += 1
            if chain == 4:
                return True
        except:
            pass

        try:
            chain = 1
            for x in range(1, 4):
                if self.bored[row][col] == self.bored[row + x][col]:
                    chain += 1
            if chain == 4:
                return True
        except:
            pass
        
        try:
            chain = 1
            for x in range(1, 4):
                if self.bored[row][col] == self.bored[row][col - x]:
                    chain += 1
            if chain == 4:
                return True
        except:
            pass

        try:
            chain = 1
            for x in range(1, 4):
                if self.bored[row][col] == self.bored[row + x][col + x]:
                    chain += 1
            if chain == 4:
                return True
        except:
            pass

        try:
            chain = 1
            for x in range(1, 4):
                if self.bored[row][col] == self.bored[row - x][col - x]:
                    chain += 1
            if chain == 4:
                return True
        except:
            pass

        try:
            chain = 1
            for x in range(1, 4):
                if self.bored[row][col] == self.bored[row + x][col - x]:
                    chain += 1
            if chain == 4:
                return True
        except:
            pass

        try:
            chain = 1
            for x in range(1, 4):
                if self.bored[row][col] == self.bored[row - x][col + x]:
                    chain += 1
            if chain == 4:
                return True
        except:
            pass
        
        return False

    def show_winner(self):
        self.draw_text(f'{self.turn.capitalize()} WINS!', 128, self.determine_color(), WIDTH / 2, HEIGHT / 2 - 64)
        pg.display.flip()
        pg.time.wait(2000)
        if self.turn == 'red':
            self.red_wins += 1
        elif self.turn == 'yellow':
            self.yellow_wins += 1
        self.playing = False
        self.new()