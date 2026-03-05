import pygame
import random
import personaje
import variables
import meteoritos
pygame.init()
variables.font = pygame.font.SysFont(None, 36)


# Creacion de la ventana
ventana= pygame.display.set_mode((variables.ANCHO, variables.ALTO)) 

#nombre de la ventana
pygame.display.set_caption("Juego Star Wars de Daniel y Ruben")
#Reloj para controlar los FPS
clock = pygame.time.Clock()
#para abrir la ventana permanete y cerrar al hacer un evento de cierre
run = True
while run== True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    speed = personaje.Personaje.player_speed
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and personaje.Personaje.player.left > 0:
        personaje.Personaje.player.x -= speed

    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and personaje.Personaje.player.right < variables.ANCHO:
        personaje.Personaje.player.x += speed
    
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and personaje.Personaje.player.top > 0:
        personaje.Personaje.player.y -= speed
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and personaje.Personaje.player.bottom < variables.ALTO:
        personaje.Personaje.player.y += speed

    #Generar meteoritos
    if len(meteoritos.meteors) < 5:
        meteor_x = random.randint(0, variables.ANCHO - meteoritos.meteor_width)
        meteor_y = random.randint(-100, -40)
        meteor_rect = pygame.Rect(meteor_x, meteor_y, meteoritos.meteor_width, meteoritos.meteor_height)
        meteoritos.meteors.append(meteor_rect)
    ventana.fill(variables.BLACK)
    pygame.draw.rect(ventana, variables.WHITE, personaje.Personaje.player)
    #Mover meteoritos
    for meteor in meteoritos.meteors:
        pygame.draw.rect(ventana, variables.RED, meteor)
        meteor.y += 5
        if meteor.top > variables.ALTO:
            meteoritos.meteors.remove(meteor)
            variables.puntuacion += 1

    #Detectar coliniones
    for meteor in meteoritos.meteors:
        if personaje.Personaje.player.colliderect(meteor):
            run = False
    #Mostrar puntuacion
    puntuacion_text = variables.font.render(f"Puntuacion: {variables.puntuacion}", True, variables.WHITE)
    ventana.blit(puntuacion_text, (10, 10))

    #Actualizar la ventana
    pygame.display.flip()
    clock.tick(60)


pygame.quit()