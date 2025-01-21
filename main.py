import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Fighting Game")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


# Класс для персонажа
class Character:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.health = 100  # Начальное здоровье
        self.vel_y = 0
        self.on_ground = False

    def move(self, keys):
        if self.color == BLUE:  # Персонаж 1
            if keys[pygame.K_a]:  # Влево
                self.rect.x -= 5
            if keys[pygame.K_d]:  # Вправо
                self.rect.x += 5
            if keys[pygame.K_w] and self.on_ground:  # Прыжок
                self.vel_y = -15
                self.on_ground = False
            if keys[pygame.K_f]:  # Атака
                self.attack(player2)
        elif self.color == RED:  # Персонаж 2
            if keys[pygame.K_LEFT]:  # Влево
                self.rect.x -= 5
            if keys[pygame.K_RIGHT]:  # Вправо
                self.rect.x += 5
            if keys[pygame.K_UP] and self.on_ground:  # Прыжок
                self.vel_y = -15
                self.on_ground = False
            if keys[pygame.K_RETURN]:  # Атака
                self.attack(player1)

        # Гравитация
        self.vel_y += 1  # Увеличиваем скорость падения
        self.rect.y += self.vel_y

        # Проверка на землю
        if self.rect.y >= HEIGHT - 50:
            self.rect.y = HEIGHT - 50
            self.on_ground = True
            self.vel_y = 0

    def attack(self, opponent):
        # Проверка на столкновение с противником при атаке
        if self.rect.colliderect(opponent.rect):
            opponent.health -= 10  # Снимаем здоровье противнику
            print(f"{opponent.color} health: {opponent.health}")  # Выводим здоровье в консоль

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        # Отображение здоровья персонажа
        health_bar_length = 50 * (self.health / 100)  # Длина полоски здоровья
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 10, health_bar_length, 5))


# Создание персонажей
player1 = Character(100, HEIGHT - 50, BLUE)
player2 = Character(600, HEIGHT - 50, RED)

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Движение персонажей
    player1.move(keys)
    player2.move(keys)

    # Отрисовка сцены
    screen.fill(WHITE)
    player1.draw(screen)
    player2.draw(screen)
    pygame.display.flip()

    pygame.time.Clock().tick(60)  # Ограничение FPS

