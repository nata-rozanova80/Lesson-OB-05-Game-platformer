import os
import pygame
import sys

# Инициализация Pygame
pygame.init()


# Основные параметры окна
screen_width, screen_height = 1500, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Платформер")



run = True

class Character():
    def __int__(self, name):
        self.name = name

    def move_char(self):
        pass


class Vinni(Character):
    name = "Vinni"


class Enemy(Character):
    name = "urchin"


class Objects():
    def __int__(self, obj_name):
        self.obj_name = obj_name

    def object_move(self):
        pass


class Coin(Objects):
    obj_name = "coin"


class Platform(Objects):
    obj_name = "platform"

puh = pygame.image.load(Vinni.png)
urchin = pygame.image.load(C:\Users\Иван\Documents\GitHub\Lesson-OB-05-Game-platformer\q.png)
coin = pygame.image.load(coin40.png)
platform = pygame.image.load(platform150.png)