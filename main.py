import pygame
import sys
from timer import RepeatTimer
import time

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Fighting Game")


bgfight = pygame.image.load('data/Backgrounds/fightbackground.png').convert()
bgmenu = pygame.image.load('data/Backgrounds/menubackground.jpg').convert()
bgfight = pygame.transform.scale(bgfight, (1920, 1080))
bgmenu = pygame.transform.scale(bgmenu, (1920, 1080))
def DrawBack():
    screen.blit(bgfight, (0, 0))

DrawBack()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

info = pygame.Surface((800, 30))


class Menu:
    def __init__(self, punkts=[800, 300, u'Punkt', (250, 250, 30), (250, 30, 250)]):
        self.punkts = punkts

    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1] - 30))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1] - 30))

    def menu(self):
        done = True
        font_menu = pygame.font.Font('data/Fonts/japanbrush.ttf', 200)
        pygame.key.set_repeat(0, 0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while done:
            screen.blit(bgmenu, (0, 0))
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 300 and mp[1] > i[1] and mp[1] < i[1] + 100:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        exit()
            pygame.display.flip()


a = [(775, 300, u'PLAY', (0, 0, 0), (255, 0, 0), 0),
     (775, 600, u'EXIT', (0, 0, 0), (255, 0, 0), 1)]
game = Menu(a)
game.menu()


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, color, file):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(file).convert_alpha()
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.health = 100
        self.vel_y = 0

        self.on_ground = False

        self.runblue = True
        self.runred = True

        self.jumpblue = False
        self.jumpred = False

        self.frame = 0

        self.blueleft = False
        self.redleft = True

        self.blueright = True
        self.redright = False

        self.attackblue = False
        self.attackred = False

    def move(self, keys):
        if self.color == BLUE:
            if self.blueright:
                file = 'Right'
            if self.blueleft:
                file = 'Left'
            if not all(keys):
                self.runblue = False
                self.attackblue = False
            if keys[pygame.K_a]:
                self.attackblue = False
                self.runblue = True
                self.rect.x -= 5
                self.blueleft = True
                self.blueright = False
            if keys[pygame.K_d]:
                self.attackblue = False
                self.runblue = True

                self.rect.x += 5
                self.blueleft = False
                self.blueright = True
            if keys[pygame.K_w] and self.on_ground:
                self.jumpblue = True
                self.vel_y = -15
                self.on_ground = False
            if keys[pygame.K_f]:
                self.attackblue = True
                self.attack(player2)
            elif self.runblue and not self.jumpblue and not self.attackblue:
                self.frame += 0.2
                if self.frame > 7:
                    self.frame -= 7
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png']
                self.image = pygame.image.load(
                    'data/Sprites/Fighter/' + file + '/Run/' + anim[int(self.frame)]).convert_alpha()
            elif not self.runblue and not self.jumpblue and not self.attackblue:
                self.frame += 0.2
                if self.frame > 5:
                    self.frame -= 5
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
                self.image = pygame.image.load(
                    'data/Sprites/Fighter/' + file + '/Idle/' + anim[int(self.frame)]).convert_alpha()
            elif self.jumpblue:
                self.frame += 0.2
                if self.frame > 9:
                    self.frame -= 9
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png']
                self.image = pygame.image.load(
                    'data/Sprites/Fighter/' + file + '/Jump/' + anim[int(self.frame)]).convert_alpha()

            if self.attackblue:
                self.runblue = False
                self.frame += 0.2
                if self.frame > 3:
                    self.frame -= 3
                anim = ['1.png', '2.png', '3.png', '4.png']
                try:
                    self.image = pygame.image.load(
                        'data/Sprites/Fighter/' + file + '/Attack_1/' + anim[int(self.frame)]).convert_alpha()
                except IndexError:
                    self.frame = 0


        elif self.color == RED:
            if self.redright:
                filer = 'Right'
            if self.redleft:
                filer = 'Left'
            if not all(keys):
                self.runred = False
                self.attackred = False
            if keys[pygame.K_LEFT]:
                self.attackred = False
                self.runred = True
                self.rect.x -= 5
                self.redleft = True
                self.redright = False
            if keys[pygame.K_RIGHT]:
                self.attackred = False
                self.runred = True

                self.rect.x += 5
                self.redleft = False
                self.redright = True
            if keys[pygame.K_UP] and self.on_ground:
                self.jumpred = True
                self.vel_y = -15
                self.on_ground = False
            if keys[pygame.K_RETURN]:
                self.attackred = True
                self.attack(player1)
            if self.runred and not self.jumpred and not self.attackred:
                self.frame += 0.2
                if self.frame > 7:
                    self.frame -= 7
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png']
                self.image = pygame.image.load(
                    'data/Sprites/Samurai/' + filer + '/Run/' + anim[int(self.frame)]).convert_alpha()
            elif not self.runred and not self.jumpred and not self.attackred and self.on_ground:
                self.frame += 0.2
                if self.frame > 5:
                    self.frame -= 5
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
                self.image = pygame.image.load(
                    'data/Sprites/Samurai/' + filer + '/Idle/' + anim[int(self.frame)]).convert_alpha()
            elif self.jumpred and not self.on_ground:
                self.frame += 0.2
                if self.frame > 9:
                    self.frame -= 9
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png', '11.png', '12.png']
                self.image = pygame.image.load(
                    'data/Sprites/Samurai/' + filer + '/Jump/' + anim[int(self.frame)]).convert_alpha()

            if self.attackred:
                self.runred = False
                self.frame += 0.2

                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
                try:
                    self.image = pygame.image.load(
                        'data/Sprites/Samurai/' + filer + '/Attack_1/' + anim[int(self.frame)]).convert_alpha()
                except IndexError:
                    self.frame = 0
            if self.on_ground:
                self.jumpred = False
        self.vel_y += 1
        self.rect.y += self.vel_y

        # Проверка на землю
        if self.rect.y >= HEIGHT - 320:
            self.rect.y = HEIGHT - 320
            self.on_ground = True
            self.vel_y = 0
            self.jumpblue = False
            self.runred = False

    def attack(self, opponent):

        if self.rect.colliderect(opponent.rect):
            opponent.health -= 0.5
            print(f"{opponent.color} health: {opponent.health}")

    def draw(self, surface):
        screen.blit(self.image, self.rect)
        health_bar_length = 50 * (self.health / 100)
        pygame.draw.rect(surface, (255, 0, 0), (0, 0, health_bar_length, 5))


player1 = Character(300, HEIGHT - 50, BLUE, 'data/Sprites/Fighter/Right/Idle/1.png')
player2 = Character(1550, HEIGHT - 50, RED, 'data/Sprites/Samurai/Left/Idle/1.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    player1.move(keys)
    player2.move(keys)
    screen.blit(bgfight, (0, 0))
    player1.draw(screen)
    player2.draw(screen)
    pygame.display.flip()

    pygame.time.Clock().tick(60)
