import pygame
import random

enemies = []

enemy_width = 60
enemy_height = 60

class Enemy:
    def __init__(self, x, y, width=60, height=60, speed=4, hp=1, tipo="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.hp = hp
        self.tipo = tipo

    def update(self):
        self.rect.y += self.speed

def spawn_enemy(ancho_pantalla, nivel=1):
    # En nivel 3 pueden salir enemigos grandes
    if nivel == 3 and random.random() < 0.35:
        width = 95
        height = 95
        x = random.randint(0, ancho_pantalla - width)
        y = random.randint(-150, -80)
        enemigo = Enemy(x, y, width, height, speed=3, hp=3, tipo="grande")
    else:
        width = 60
        height = 60
        x = random.randint(0, ancho_pantalla - width)
        y = random.randint(-120, -60)
        enemigo = Enemy(x, y, width, height, speed=4, hp=1, tipo="normal")

    enemies.append(enemigo)