import pygame
import clases.variables as variables

class Personaje:
    player_width = 80
    player_height = 80
    player_speed = 5

    # Rect para dibujar (tamaño del sprite)
    player = pygame.Rect(
        variables.ANCHO // 2 - player_width // 2,
        variables.ALTO - player_height - 10,
        player_width,
        player_height,
    )

    # Hitbox más pequeña (colisiones)
    HITBOX_SCALE = 0.62

    hitbox = pygame.Rect(0, 0,
                         int(player_width * HITBOX_SCALE),
                         int(player_height * HITBOX_SCALE))

    @classmethod
    def update_hitbox(cls):
        # Mantener la hitbox siempre centrada en el jugador
        cls.hitbox.center = cls.player.center

# Inicializar hitbox al crear la clase
Personaje.update_hitbox()