import pygame
import sys

from clases import variables
from clases.recursos import Recursos
from clases.gestor_audio import GestorAudio
from clases.pantallas import Pantallas
from clases.juego import Juego


pygame.init()
variables.font = pygame.font.SysFont("arial", 36, bold=True)

ventana = pygame.display.set_mode((variables.ANCHO, variables.ALTO))
pygame.display.set_caption("Juego Star Wars de Daniel y Ruben")
clock = pygame.time.Clock()

recursos = Recursos()
audio = GestorAudio()
pantallas = Pantallas(ventana, clock, recursos, audio)
juego = Juego(ventana, clock, recursos, audio, pantallas)

nivel_actual = pantallas.pantalla_inicio()

if nivel_actual == "salir":
    pygame.quit()
    sys.exit()

while True:
    resultado = juego.jugar(nivel_actual)

    if resultado == "salir":
        break
    elif resultado == "repetir":
        continue
    elif resultado == "siguiente":
        if nivel_actual < variables.MAX_NIVELES:
            nivel_actual += 1
        else:
            break
    else:
        nivel_actual = pantallas.pantalla_inicio()
        if nivel_actual == "salir":
            break

pygame.quit()
sys.exit()