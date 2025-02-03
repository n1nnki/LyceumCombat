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
bgfight = pygame.transform.scale(bgfight, (WIDTH, HEIGHT))
bgmenu = pygame.transform.scale(bgmenu, (WIDTH, HEIGHT))
screen.blit(bgfight, (0, 0))

#музыка и звуки
menumusic = pygame.mixer.Sound("data/Music/menuTheme.mp3")
menumusic.play()
fightmusic = pygame.mixer.Sound("data/Music/fightTheme.mp3")



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
                if mp[0] > i[0] and mp[0] < i[0] + 500 and mp[1] > i[1] and mp[1] < i[1] + 200:
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


a = [(750, 500, u'PLAY', (0, 0, 0), (255, 0, 0), 0),
     (750, 700, u'EXIT', (0, 0, 0), (255, 0, 0), 1)]
game = Menu(a)
game.menu()


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, color, file, coliderx, colidery):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(file).convert_alpha()
        self.rect = pygame.Rect(x, y, coliderx, colidery)
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

        self.shieldblue = False
        self.shieldred = False

        self.deadblue = False
        self.deadred = False

        self.attackblue2 = False
        self.attackred2 = False

    # увеличивание персонажей
    def transforming(self, image):
        self.image = pygame.transform.scale(image, (500, 500))

    def move(self, keys):
        if self.color == BLUE:
            if self.blueright:
                file = 'Right'
            if self.blueleft:
                file = 'Left'
            if not all(keys):
                self.runblue = False
                self.attackblue = False
                self.attackblue2 = False
                self.shieldblue = False
            if keys[pygame.K_a] and self.rect.x >= 0:
                self.attackblue = False
                self.attackblue2 = False
                self.runblue = True
                self.rect.x -= 10
                self.blueleft = True
                self.blueright = False
            if keys[pygame.K_d] and self.rect.x <= WIDTH - 500:
                self.attackblue = False
                self.attackblue2 = False
                self.runblue = True

                self.rect.x += 10
                self.blueleft = False
                self.blueright = True
            if keys[pygame.K_w] and self.on_ground:
                self.jumpblue = True
                self.vel_y = -22
                self.on_ground = False
            if keys[pygame.K_f]:
                self.runblue = False
                self.attackblue = True
                self.attack(player2, player1)
            if keys[pygame.K_e]:
                self.attackblue2 = True
                self.runblue = False
                self.attack(player2, player1)
            if keys[pygame.K_c]:
                self.attackblue2 = False
                self.attackblue = False
                self.runblue = False
                self.shieldblue = True
            elif self.runblue and not self.jumpblue and not self.attackblue and not self.attackblue2:
                self.frame += 0.2
                if self.frame > 7:
                    self.frame -= 7
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png']
                self.image = pygame.image.load(
                    'data/Sprites/Fighter/' + file + '/Run/' + anim[int(self.frame)]).convert_alpha()
                self.transforming(self.image)
            elif not self.runblue and not self.jumpblue and not self.attackblue and not self.attackblue2:
                self.frame += 0.2
                if self.frame > 5:
                    self.frame -= 5
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
                self.image = pygame.image.load(
                    'data/Sprites/Fighter/' + file + '/Idle/' + anim[int(self.frame)]).convert_alpha()
                self.transforming(self.image)
            elif self.jumpblue:
                self.frame += 0.2
                if self.frame > 9:
                    self.frame -= 9
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png']
                self.image = pygame.image.load(
                    'data/Sprites/Fighter/' + file + '/Jump/' + anim[int(self.frame)]).convert_alpha()
                self.transforming(self.image)

            if self.shieldblue:
                self.image = pygame.image.load('data/Sprites/Fighter/' + file + '/Shield/2.png')
                self.transforming(self.image)
            if self.attackblue:
                self.runblue = False
                self.frame += 0.15
                if self.frame > 3:
                    self.frame -= 3
                anim = ['1.png', '2.png', '3.png', '4.png']
                try:
                    self.image = pygame.image.load(
                        'data/Sprites/Fighter/' + file + '/Attack_1/' + anim[int(self.frame)]).convert_alpha()
                    self.transforming(self.image)
                except IndexError:
                    self.frame = 0
            if self.attackblue2:
                self.frame += 0.15
                if self.frame > 3:
                    self.frame -= 3
                anim = ['1.png', '2.png', '3.png', '4.png']
                try:
                    self.image = pygame.image.load(
                        'data/Sprites/Fighter/' + file + '/Attack_2/' + anim[int(self.frame)]).convert_alpha()
                    self.transforming(self.image)
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
                self.attackred2 = False
                self.shieldred = False
            if keys[pygame.K_LEFT] and self.rect.x >= 0:
                self.attackred = False
                self.attackred2 = False
                self.runred = True
                self.rect.x -= 10
                self.redleft = True
                self.redright = False
            if keys[pygame.K_RIGHT] and self.rect.x <= WIDTH - 500:
                self.attackred = False
                self.attackred2 = False
                self.runred = True

                self.rect.x += 10
                self.redleft = False
                self.redright = True
            if keys[pygame.K_UP] and self.on_ground:
                self.jumpred = True
                self.vel_y = -22
                self.on_ground = False
            if keys[pygame.K_l]:
                self.runred = False
                self.attackred = True
                self.shieldred = False
                self.attack(player1, player2)
            if keys[pygame.K_k]:
                self.runred = False
                self.attackred2 = True
                self.attack(player1, player2)
            if keys[pygame.K_SPACE]:
                self.shieldred = True
                self.attackred2 = False
                self.attackred = False
            if self.runred and not self.jumpred and not self.attackred:
                self.frame += 0.2
                if self.frame > 7:
                    self.frame -= 7
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png']
                self.image = pygame.image.load(
                    'data/Sprites/Samurai/' + filer + '/Run/' + anim[int(self.frame)]).convert_alpha()
                self.transforming(self.image)
            elif not self.runred and not self.jumpred and not self.attackred and self.on_ground:
                self.frame += 0.2
                if self.frame > 5:
                    self.frame -= 5
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
                self.image = pygame.image.load(
                    'data/Sprites/Samurai/' + filer + '/Idle/' + anim[int(self.frame)]).convert_alpha()
                self.transforming(self.image)
            elif self.jumpred and not self.on_ground:
                self.frame += 0.2
                if self.frame > 9:
                    self.frame -= 9
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png',
                        '11.png', '12.png']
                self.image = pygame.image.load(
                    'data/Sprites/Samurai/' + filer + '/Jump/' + anim[int(self.frame)]).convert_alpha()
                self.transforming(self.image)
            if self.shieldred:
                self.image = pygame.image.load('data/Sprites/Samurai/' + filer + '/Shield/2.png')
                self.transforming(self.image)
            if self.attackred:
                self.runred = False
                self.frame += 0.2

                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
                try:
                    self.image = pygame.image.load(
                        'data/Sprites/Samurai/' + filer + '/Attack_1/' + anim[int(self.frame)]).convert_alpha()
                    self.transforming(self.image)
                except IndexError:
                    self.frame = 0

            if self.attackred2:
                self.runred = False
                self.frame += 0.004
                if self.frame > 3:
                    self.frame -= 3

                anim = ['1.png', '2.png', '3.png']
                try:
                    self.image = pygame.image.load(
                        'data/Sprites/Samurai/' + filer + '/Attack_2/' + anim[int(self.frame)]).convert_alpha()
                    self.transforming(self.image)

                except IndexError:
                    self.frame = 0
            if self.on_ground:
                self.jumpred = False
        self.vel_y += 1
        self.rect.y += self.vel_y

        # Проверка на землю
        if self.rect.y >= HEIGHT - 700:
            self.rect.y = HEIGHT - 700
            self.on_ground = True
            self.vel_y = 0
            self.jumpblue = False
            self.runred = False

    def attack(self, opponent, character):
        if character.color == BLUE and opponent.shieldred and self.rect.colliderect(opponent.rect):
            opponent.health -= 0.1
        elif character.color == RED and opponent.shieldblue and self.rect.colliderect(opponent.rect):
            opponent.health -= 0.1
        elif self.rect.colliderect(opponent.rect):
            opponent.health -= 0.45
            print(f"{opponent.color} health: {opponent.health}")

    def draw(self, surface):
        screen.blit(self.image, self.rect)


player1 = Character(150, HEIGHT - 50, BLUE, 'data/Sprites/Fighter/Right/Idle/1.png', 200, 300)
player2 = Character(1300, HEIGHT - 50, RED, 'data/Sprites/Samurai/Left/Idle/1.png', 150, 300)


def healthbars(surface):
    health_bar_length = 500 * (player1.health / 100)
    health_bar_lengthred = 500 * (player2.health / 100)
    pygame.draw.rect(surface, (0, 0, 0), (65, 77.5, 500 + 10, 22))
    pygame.draw.rect(surface, (255, 0, 0), (70, 80, health_bar_length, 15))
    pygame.draw.rect(surface, (0, 0, 0), (WIDTH - 555, 77.5, 510, 22))
    pygame.draw.rect(surface, (255, 0, 0), (WIDTH - 550, 80, health_bar_lengthred, 15))
    f1 = pygame.font.Font('data/Fonts/japanbrush.ttf', 36)
    text1 = f1.render('Fighter', 1, (255, 255, 255))
    text2 = f1.render('Samurai', 1, (255, 255, 255))

    screen.blit(text1, (50, 40))
    screen.blit(text2, (1770, 40))

anim_played = False

#музыка
menumusic.stop()
fightmusic.play()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                sound = pygame.mixer.Sound('data/sounds/chetkiy-rezkiy-udar-kulakom.mp3')
                sound.play()
            if event.key == pygame.K_e:
                sound = pygame.mixer.Sound('data/sounds/udar-so-zvukom2.mp3')
                sound.play()
            if event.key == pygame.K_k:
                sound = pygame.mixer.Sound('data/sounds/trenirovochnyiy-udar-mechom.mp3')
                sound.play()
            if event.key == pygame.K_l:
                sound = pygame.mixer.Sound('data/sounds/virtuoznyiy-udar-mechom-vo-vremya-trenirovki.mp3')
                sound.play()
            if event.key == pygame.K_ESCAPE:
                game = Menu(a)
                game.menu()

    keys = pygame.key.get_pressed()
    if player1.health >= 0 and player2.health >= 0:
        player1.move(keys)
        player2.move(keys)
        screen.blit(bgfight, (0, 0))
        player1.draw(screen)
        player2.draw(screen)
        healthbars(screen)
        if player2.health <= 0:
            f3 = pygame.font.Font('data/Fonts/japanbrush.ttf', 70)
            text1 = f3.render(f'''Fighter wins Press ESC to enter the menu''', 1, (255, 255, 255))
            screen.blit(text1, (300, 120))
        if player1.health <= 0:
            f3 = pygame.font.Font('data/Fonts/japanbrush.ttf', 70)
            text1 = f3.render(f'''Samurai wins Press ESC to enter the menu''', 1, (255, 255, 255))
            screen.blit(text1, (300, 120))

    pygame.display.flip()

    pygame.time.Clock().tick(60)
