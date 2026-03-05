import pygame
import variables


class Personaje():
    player_width = 40
    player_height = 60
    player = pygame.Rect(
        variables.ANCHO // 2 - player_width // 2,
        variables.ALTO - player_height - 10,
        player_width,
        player_height,
    )
    player_speed = 5 