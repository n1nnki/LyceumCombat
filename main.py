import pygame
import sys

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

    def move(self, keys):
        if self.color == BLUE:
            if keys[pygame.K_a]:
                self.rect.x -= 5
            if keys[pygame.K_d]:
                self.rect.x += 5
            if keys[pygame.K_w] and self.on_ground:
                self.vel_y = -15
                self.on_ground = False
            if keys[pygame.K_f]:
                self.attack(player2)
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
        if self.rect.y >= HEIGHT - 50:
            self.rect.y = HEIGHT - 50
            self.on_ground = True
            self.vel_y = 0

    def attack(self, opponent):

        if self.rect.colliderect(opponent.rect):
            opponent.health -= 10
            print(f"{opponent.color} health: {opponent.health}")

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

        health_bar_length = 50 * (self.health / 100)
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 10, health_bar_length, 5))


player1 = Character(100, HEIGHT - 50, BLUE)
player2 = Character(600, HEIGHT - 50, RED)

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

