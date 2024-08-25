import pygame
import random

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 60
MONET_COUNT_TO_WIN = 20
HERO_LIVES = 3
GRAVITY = 0.5  # Гравитация
JUMP_STRENGTH = 10  # Сила прыжка

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Платформер")
clock = pygame.time.Clock()

try:
    hero_image = pygame.image.load('Vinni.png')
    enemy_image = pygame.image.load('q.png')
    coin_image = pygame.image.load('coin40.png')
    platform_image = pygame.image.load('platform150.png')
except pygame.error as e:
    print(f"Ошибка загрузки изображения: {e}")
    pygame.quit()


# Классы игры
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = hero_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 100
        self.lives = HERO_LIVES
        self.coins_collected = 0
        self.vel_y = 0  # Вертикальная скорость
        self.on_ground_flag = True  # Флаг, указывающий, находитесь ли вы на земле

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP] and self.on_ground_flag:
            self.vel_y = -JUMP_STRENGTH  # Прыжок
            self.on_ground_flag = False  # Устанавливаем флаг, что не на земле


        # Применение гравитации
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y


        # Проверка на столкновение с платформами
        if self.rect.y >= 500:  # Если герой достиг координаты 500
            self.rect.y = 500
            self.vel_y = 0  # Сбрасываем вертикальную скорость
            self.on_ground_flag = True  # Устанавливаем флаг, что на земле
        else:
            self.on_ground_flag = self.on_ground()  # Проверка, находимся ли на платформе



    def collect_coin(self):
        self.coins_collected += 1


    def on_ground(self):
        # Проверка на столкновение с платформами
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            for hit in hits:
                if self.rect.bottom >= hit.rect.top and self.rect.bottom <= hit.rect.top + 5:
                    return True
        return False

    def fall(self):
        # Падение до координаты y = 500 или до следующей платформы
        while not self.on_ground() and self.rect.y < 500:
            self.rect.y += 5  # Падение вниз

        # Устанавливаем координаты y в 500, если они ниже
        if self.rect.y >= 500:
            self.rect.y = 500

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = platform_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Инициализация объектов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
platforms = pygame.sprite.Group()

player = Hero()
all_sprites.add(player)

# Создание врагов, монет и платформ
for _ in range(5):
    enemy = Enemy(random.randint(100, SCREEN_WIDTH - 100), random.randint(300, SCREEN_HEIGHT - 200))
    enemies.add(enemy)
    all_sprites.add(enemy)

for _ in range(10):
    coin = Coin(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 400))
    coins.add(coin)
    all_sprites.add(coin)

for _ in range(5):
    platform = Platform(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 50))
    platforms.add(platform)
    all_sprites.add(platform)

# Основной цикл игры
running = True

print(player.rect.x, player.rect.y)
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()

    # Проверка столкновений
    if pygame.sprite.spritecollide(player, coins, True):
        player.collect_coin()

    if pygame.sprite.spritecollide(player, enemies, False):
        player.lives -= 1
        if player.lives <= 0:
            print("Game Over")
            running = False

    # Проверка победы
    if player.coins_collected >= MONET_COUNT_TO_WIN:
        print("Победа!")
        running = False

    # Рендеринг
    screen.fill((154, 205, 50))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
