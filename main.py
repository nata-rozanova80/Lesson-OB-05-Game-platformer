import pygame
import random
import time

# Константы
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60
MONET_COUNT_TO_WIN = 5
HERO_LIVES = 3
GRAVITY = 0.5  # Гравитация
JUMP_STRENGTH = 15  # Сила прыжка

max_platforms = 5 # Максимальное количество платформ
current_platforms = 0  # Текущее количество платформ
o = 0 # Считаем количество обновлений
c = 0 # Количество монет
enemy_count = 0 # Количество установленных врагов

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Платформер")
clock = pygame.time.Clock()

try:
    hero_image = pygame.image.load('Vinni.png')
    enemy_image = pygame.image.load('q35.png')
    coin_image = pygame.image.load('coin.png')
    platform_image = pygame.image.load('platform.png')
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
        self.jump_pressed = False  # Флаг для отслеживания нажатия кнопки прыжка

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        # Проверка нажатия кнопки "вверх"
        if keys[pygame.K_UP]:
            if self.on_ground_flag or not self.jump_pressed:  # Если на земле или не было последнего прыжка
                self.vel_y = -JUMP_STRENGTH  # Прыжок
                self.rect.x += 10  # Перемещение вправо при прыжке
                print(f"Прыжок {player.rect.x, player.rect.y}")  # Вывод координат героя
                self.jump_pressed = True  # Устанавливаем флаг, что прыжок был выполнен

            else:
                self.jump_pressed = False  # Сбрасываем флаг, если кнопка не нажата


        # Применение гравитации
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y


        # Проверка на столкновение с платформами

        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.rect.y > 500:
            self.rect.y = 500

        # hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            for hit in hits:
                if self.rect.bottom >= hit.rect.top and self.rect.bottom <= hit.rect.top + 5:
                    self.rect.y = hit.rect.top - self.rect.height  # Фиксация на платформе
                    self.vel_y = 0
                    self.on_ground_flag = True
                else:
                    self.on_ground_flag = False  # Если нет столкновений, значит не на платформе

        # Ограничение по Y
            if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
                self.rect.y = SCREEN_HEIGHT - self.rect.height
                self.vel_y = 0
                self.on_ground_flag = True


    def collect_coin(self):
        self.coins_collected += 1


    def fall(self):
        # Падение до координаты y = 500 или до следующей платформы
        while not self.on_ground_flag and self.rect.y < 500:
            self.rect.y += 5  # Падение вниз

        # Устанавливаем координаты y в 500, если они ниже
        if self.rect.y > 500:
            Hero.rect.y = 500

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

# Функция для проверки расстояния между платформами
def is_too_close(new_platform, platforms):
    for platform in platforms:
        if abs(new_platform.rect.x - platform.rect.x) < 100 and abs(new_platform.rect.y - platform.rect.y) < 50:
            return True
    return False

max_platforms = 7 # Максимальное количество платформ
current_platforms = 0  # Инициализация счётчика платформ

while current_platforms < max_platforms:  # Создание платформ
    platform_y = random.randint(200, 400)  # Интервал по Y
    platform_x = random.randint(10, SCREEN_WIDTH - 100)  ###
    new_platform = Platform(platform_x, platform_y)

    # Проверка на близость к другим платформам
    if not is_too_close(new_platform, platforms):
        platforms.add(new_platform)
        all_sprites.add(new_platform)
        current_platforms += 1  # Увеличиваем счётчик платформ
        print(f"№ платформы: {current_platforms}")
        print(f'Координаты платформы: X: {new_platform.rect.x}, Y: {new_platform.rect.y}')


    # Создание монет на платформе
    coin = Coin(new_platform.rect.x + random.randint(5, new_platform.rect.width - 10), new_platform.rect.y - 20)
    coins.add(coin)
    all_sprites.add(coin)


    # Проверка наличия монет рядом с платформой перед установкой врага
    for enemy_count in range (1,5):
        enemy_x = new_platform.rect.x + random.randint(5, new_platform.rect.width - 10)
        if not any(abs(coin.rect.x - enemy_x) <= 50 and coin.rect.y == new_platform.rect.y - 20 for coin in coins):
            enemy = Enemy(enemy_x, new_platform.rect.y - 50)
            enemies.add(enemy)
            all_sprites.add(enemy)
            enemy_count +=1

# Функция для отображения текста
def display_message(screen, message, font, color, position):
    text_surface = font.render(message, True, color)
    screen.blit(text_surface, position)

# Основной цикл игры
running = True

# Инициализация шрифта
font = pygame.font.Font(None, 74)  # Размер шрифта 74
game_over = False
result = None

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()
    o += 1
    print(f"Обновления: {o}")

    # Проверка столкновений
    if pygame.sprite.spritecollide(player, coins, True):
        c += 1
        print(f"Coins: {c}")
        player.collect_coin()

    if pygame.sprite.spritecollide(player, enemies, False):
        player.lives -= 1
        print(f"Еж= жизнь-1: {player.lives}")
        player.rect.y = 500  # Установить героя на землю после столкновения
        player.vel_y = 0  # Обнуляем вертикальную скорость
        player.on_ground_flag = True  # Устанавливаем флаг, что на земле
        player.rect.x = 50  # Сбрасываем позицию героя, если это нужно
        continue  # Продолжаем цикл, чтобы не завершать игру

    # Проверка на поражение
    if player.lives == 0:
        game_over = True
        print("упс")
        display_message(screen, "Жаль. Ты проиграл.", font, (255, 0, 0), (200, SCREEN_HEIGHT // 2))
        pygame.display.flip()  # Обновление экрана
        time.sleep(1)
        running = False

    # # Проверка победы
    if player.coins_collected >= MONET_COUNT_TO_WIN:
        game_over = True
        print("Победа!")
        display_message(screen, "Ура! Ты победил!", font, (75, 0, 130), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()  # Обновление экрана
        time.sleep(1)
        running = False


    # Рендеринг
    screen.fill((154, 205, 50))
    all_sprites.draw(screen)

    platforms.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
