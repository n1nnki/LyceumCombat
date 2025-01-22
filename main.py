import pygame
import sys
from timer import RepeatTimer
import time

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Fighting Game")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


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
        self.redleft = False

        self.blueright = True
        self.redright = True

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
                    'Sprites/Fighter/' + file + '/Run/' + anim[int(self.frame)]).convert_alpha()
            elif not self.runblue and not self.jumpblue and not self.attackblue:
                self.frame += 0.2
                if self.frame > 5:
                    self.frame -= 5
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
                self.image = pygame.image.load(
                    'Sprites/Fighter/' + file + '/Idle/' + anim[int(self.frame)]).convert_alpha()
            elif self.jumpblue:
                self.frame += 0.2
                if self.frame > 9:
                    self.frame -= 9
                anim = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png']
                self.image = pygame.image.load(
                    'Sprites/Fighter/' + file + '/Jump/' + anim[int(self.frame)]).convert_alpha()

            if self.attackblue:
                self.runblue = False
                self.frame += 0.2
                if self.frame > 3:
                    self.frame -= 3
                anim = ['1.png', '2.png', '3.png', '4.png']
                try:
                    self.image = pygame.image.load(
                        'Sprites/Fighter/' + file + '/Attack_1/' + anim[int(self.frame)]).convert_alpha()
                except IndexError:
                    self.frame = 0


        elif self.color == RED:
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.rect.x += 5
            if keys[pygame.K_UP] and self.on_ground:
                self.vel_y = -15
                self.on_ground = False
            if keys[pygame.K_RETURN]:
                self.attack(player1)

        self.vel_y += 1
        self.rect.y += self.vel_y

        # Проверка на землю
        if self.rect.y >= HEIGHT - 200:
            self.rect.y = HEIGHT - 200
            self.on_ground = True
            self.vel_y = 0
            self.jumpblue = False

    def attack(self, opponent):

        if self.rect.colliderect(opponent.rect):
            opponent.health -= 10
            print(f"{opponent.color} health: {opponent.health}")

    def draw(self, surface):
        screen.blit(self.image, self.rect)

        health_bar_length = 50 * (self.health / 100)
        pygame.draw.rect(surface, (255, 0, 0), (0, 0, health_bar_length, 5))


player1 = Character(100, HEIGHT - 50, BLUE, 'Sprites/Fighter/Right/Idle/1.png')
player2 = Character(600, HEIGHT - 50, RED, 'Sprites/Samurai/Idle/1.png')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    player1.move(keys)
    player2.move(keys)
    screen.fill(WHITE)
    player1.draw(screen)
    player2.draw(screen)
    pygame.display.flip()

    pygame.time.Clock().tick(60)
