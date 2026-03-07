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

# ✅ Fondo a pantalla completa
background_image = pygame.transform.smoothscale(background_image, (variables.ANCHO, variables.ALTO))

# --- Escalar imágenes ---
player_image = escalar_cuadrado(player_image, personaje.Personaje.player_width)
meteor_image = escalar_cuadrado(meteor_image, meteoritos.meteor_width)
enemy_image = escalar_cuadrado(enemy_image, enemigos.enemy_width)

# =========================
#   Estados
# =========================
MENU = "menu"
JUGANDO = "jugando"
GAMEOVER = "gameover"
estado = MENU

# Fuentes
font_title = pygame.font.SysFont(None, 84)
font_btn = pygame.font.SysFont(None, 44)
font_hint = pygame.font.SysFont(None, 26)

def dibujar_boton(surface, rect, texto, mouse_pos):
    hover = rect.collidepoint(mouse_pos)
    color = (80, 180, 120) if hover else (60, 140, 95)
    pygame.draw.rect(surface, color, rect, border_radius=14)
    pygame.draw.rect(surface, (20, 20, 20), rect, 3, border_radius=14)
    txt = font_btn.render(texto, True, (245, 245, 245))
    surface.blit(txt, txt.get_rect(center=rect.center))
    return hover

def pantalla_inicio():
    """Devuelve True si el usuario quiere empezar."""
    ventana.fill((10, 10, 18))
    ventana.blit(background_image, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    titulo = font_title.render("STAR WARS", True, (240, 240, 240))
    ventana.blit(titulo, titulo.get_rect(center=(variables.ANCHO // 2, variables.ALTO // 2 - 170)))

    subt = font_hint.render("Daniel y Rubén", True, (210, 210, 210))
    ventana.blit(subt, subt.get_rect(center=(variables.ANCHO // 2, variables.ALTO // 2 - 125)))

    boton = pygame.Rect(0, 0, 320, 80)
    boton.center = (variables.ANCHO // 2, variables.ALTO // 2 - 10)
    hover = dibujar_boton(ventana, boton, "INICIAR JUEGO", mouse_pos)

    hint = font_hint.render("Click o ENTER", True, (200, 200, 200))
    ventana.blit(hint, hint.get_rect(center=(variables.ANCHO // 2, variables.ALTO // 2 + 70)))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hover:
            return True

    return False

def pantalla_gameover():
    """
    Devuelve:
      - "retry" si reintentar
      - "menu" si volver al menú
      - None si no se elige nada
    """
    ventana.fill((10, 0, 0))
    ventana.blit(background_image, (0, 0))

    # Capa oscura encima para que se lea bien
    overlay = pygame.Surface((variables.ANCHO, variables.ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    ventana.blit(overlay, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    titulo = font_title.render("GAME OVER", True, (255, 220, 220))
    ventana.blit(titulo, titulo.get_rect(center=(variables.ANCHO // 2, variables.ALTO // 2 - 180)))

    score_txt = pygame.font.SysFont(None, 42).render(f"Puntuación: {variables.puntuacion}", True, (245, 245, 245))
    ventana.blit(score_txt, score_txt.get_rect(center=(variables.ANCHO // 2, variables.ALTO // 2 - 120)))

    btn_retry = pygame.Rect(0, 0, 280, 72)
    btn_retry.center = (variables.ANCHO // 2, variables.ALTO // 2 - 20)
    hover_retry = dibujar_boton(ventana, btn_retry, "REINTENTAR", mouse_pos)

    btn_menu = pygame.Rect(0, 0, 280, 72)
    btn_menu.center = (variables.ANCHO // 2, variables.ALTO // 2 + 70)
    hover_menu = dibujar_boton(ventana, btn_menu, "MENÚ", mouse_pos)

    hint = font_hint.render("ENTER = reintentar | M = menú", True, (220, 220, 220))
    ventana.blit(hint, hint.get_rect(center=(variables.ANCHO // 2, variables.ALTO // 2 + 150)))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "retry"
            if event.key == pygame.K_m:
                return "menu"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hover_retry:
                return "retry"
            if hover_menu:
                return "menu"

    return None

# =========================
#   Variables de partida
# =========================
balas = []
bala_w, bala_h = 6, 16
bala_speed = 10
cooldown_ms = 220
ultimo_disparo = 0

MAX_ENEMIGOS = 4
SPAWN_ENEMIGO_PROB = 0.03

def iniciar_partida():
    """Resetea TODO lo necesario para empezar limpio."""
    global balas, ultimo_disparo

    variables.puntuacion = 0
    meteoritos.meteors.clear()
    enemigos.enemies.clear()

    balas = []
    ultimo_disparo = 0

    personaje.Personaje.player.centerx = variables.ANCHO // 2
    personaje.Personaje.player.bottom = variables.ALTO - 10
    personaje.Personaje.update_hitbox()

def loop_juego():
    """1 frame de juego. Devuelve 'gameover' si pierdes, 'menu' si ESC, o None."""
    global ultimo_disparo

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "menu"

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

    personaje.Personaje.update_hitbox()

    # --- Disparar ---
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

    # --- Colisiones jugador ---
    for meteor in meteoritos.meteors:
        if personaje.Personaje.hitbox.colliderect(meteor):
            return "gameover"

    for e in enemigos.enemies:
        if personaje.Personaje.hitbox.colliderect(e.rect):
            return "gameover"

    # --- Colisiones balas vs enemigos ---
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

    ventana.blit(player_image, (personaje.Personaje.player.x, personaje.Personaje.player.y))

    for meteor in meteoritos.meteors:
        ventana.blit(meteor_image, (meteor.x, meteor.y))

    for e in enemigos.enemies:
        ventana.blit(enemy_image, (e.rect.x, e.rect.y))

    for b in balas:
        pygame.draw.rect(ventana, (255, 220, 80), b)

    puntuacion_text = variables.font.render(f"Puntuacion: {variables.puntuacion}", True, variables.WHITE)
    ventana.blit(puntuacion_text, (10, 10))

    pygame.display.flip()
    return None

# =========================
#   Bucle principal
# =========================
while True:
    if estado == MENU:
        clock.tick(60)
        if pantalla_inicio():
            iniciar_partida()
            estado = JUGANDO

    elif estado == JUGANDO:
        resultado = loop_juego()
        if resultado == "menu":
            estado = MENU
        elif resultado == "gameover":
            estado = GAMEOVER

    elif estado == GAMEOVER:
        clock.tick(60)
        accion = pantalla_gameover()
        if accion == "retry":
            iniciar_partida()
            estado = JUGANDO
        elif accion == "menu":
            estado = MENU