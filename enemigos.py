# enemigos.py
import pygame
import random

enemy_width = 45
enemy_height = 45

enemies = []

class Enemigo:
    def __init__(self, x, y, speed=3):
        self.rect = pygame.Rect(x, y, enemy_width, enemy_height)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

def spawn_enemy(ancho):
    x = random.randint(0, ancho - enemy_width)
    y = random.randint(-150, -40)
    speed = random.randint(2, 5)
    enemies.append(Enemigo(x, y, speed))