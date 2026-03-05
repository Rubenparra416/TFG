import pygame
import random
import personaje
import variables
import meteoritos
import enemigos

pygame.init()
variables.font = pygame.font.SysFont(None, 36)

def escalar_cuadrado(image, side):
    width, height = image.get_size()
    base = min(width, height)
    x = (width - base) // 2
    y = (height - base) // 2
    square = image.subsurface((x, y, base, base)).copy()
    return pygame.transform.smoothscale(square, (side, side))

# --- Ventana ---
ventana = pygame.display.set_mode((variables.ANCHO, variables.ALTO))
pygame.display.set_caption("Juego Star Wars de Daniel y Ruben")
clock = pygame.time.Clock()

# --- Cargar imágenes ---
player_image = pygame.image.load("assets/milenario.png").convert_alpha()
meteor_image = pygame.image.load("assets/meteorito.png").convert_alpha()
background_image = pygame.image.load("assets/fondo.jpg").convert()
enemy_image = pygame.image.load("assets/enemigo.png").convert_alpha()

# --- Escalar imágenes ---
player_image = escalar_cuadrado(player_image, personaje.Personaje.player_width)
meteor_image = escalar_cuadrado(meteor_image, meteoritos.meteor_width)
enemy_image = escalar_cuadrado(enemy_image, enemigos.enemy_width)

# --- Disparos (balas) ---
balas = []
bala_w, bala_h = 6, 16
bala_speed = 10
cooldown_ms = 220
ultimo_disparo = 0

# --- Config enemigos ---
MAX_ENEMIGOS = 4
SPAWN_ENEMIGO_PROB = 0.03

run = True
while run:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # --- Movimiento jugador ---
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

    # >>> IMPORTANTÍSIMO: sincronizar hitbox tras mover
    personaje.Personaje.update_hitbox()

    # --- Disparar (espacio) ---
    ahora = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and (ahora - ultimo_disparo) >= cooldown_ms:
        bx = personaje.Personaje.player.centerx - bala_w // 2
        by = personaje.Personaje.player.top - bala_h
        balas.append(pygame.Rect(bx, by, bala_w, bala_h))
        ultimo_disparo = ahora

    # --- Generar meteoritos ---
    if len(meteoritos.meteors) < 5:
        meteor_x = random.randint(0, variables.ANCHO - meteoritos.meteor_width)
        meteor_y = random.randint(-100, -40)
        meteor_rect = pygame.Rect(meteor_x, meteor_y, meteoritos.meteor_width, meteoritos.meteor_height)
        meteoritos.meteors.append(meteor_rect)

    # --- Generar enemigos ---
    if len(enemigos.enemies) < MAX_ENEMIGOS and random.random() < SPAWN_ENEMIGO_PROB:
        enemigos.spawn_enemy(variables.ANCHO)

    # --- Update balas ---
    for b in balas[:]:
        b.y -= bala_speed
        if b.bottom < 0:
            balas.remove(b)

    # --- Update meteoritos ---
    for meteor in meteoritos.meteors[:]:
        meteor.y += 5
        if meteor.top > variables.ALTO:
            meteoritos.meteors.remove(meteor)
            variables.puntuacion += 1

    # --- Update enemigos ---
    for e in enemigos.enemies[:]:
        e.update()
        if e.rect.top > variables.ALTO:
            enemigos.enemies.remove(e)

    # --- Colisiones: jugador vs meteoritos (USANDO HITBOX) ---
    for meteor in meteoritos.meteors:
        if personaje.Personaje.hitbox.colliderect(meteor):
            run = False

    # --- Colisiones: jugador vs enemigos (USANDO HITBOX) ---
    for e in enemigos.enemies:
        if personaje.Personaje.hitbox.colliderect(e.rect):
            run = False

    # --- Colisiones: balas vs enemigos ---
    for b in balas[:]:
        hit = False
        for e in enemigos.enemies[:]:
            if b.colliderect(e.rect):
                enemigos.enemies.remove(e)
                hit = True
                variables.puntuacion += 20
                break
        if hit:
            balas.remove(b)

    # --- Dibujar ---
    ventana.fill(variables.BLACK)
    ventana.blit(background_image, (0, 0))

    # jugador (se dibuja con player, pero choca con hitbox)
    ventana.blit(player_image, (personaje.Personaje.player.x, personaje.Personaje.player.y))

    # meteoritos
    for meteor in meteoritos.meteors:
        ventana.blit(meteor_image, (meteor.x, meteor.y))

    # enemigos
    for e in enemigos.enemies:
        ventana.blit(enemy_image, (e.rect.x, e.rect.y))

    # balas
    for b in balas:
        pygame.draw.rect(ventana, (255, 220, 80), b)

    # (OPCIONAL) dibujar hitbox para verla y ajustar
    # pygame.draw.rect(ventana, (255, 0, 0), personaje.Personaje.hitbox, 2)

    # puntuación
    puntuacion_text = variables.font.render(f"Puntuacion: {variables.puntuacion}", True, variables.WHITE)
    ventana.blit(puntuacion_text, (10, 10))

    pygame.display.flip()

pygame.quit()