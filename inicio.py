import pygame
import random

# Importamos nuestros módulos del juego
# personaje -> contiene la nave del jugador
# variables -> contiene colores, tamaño de pantalla, puntuación, etc.
# meteoritos -> contiene la lista de meteoritos y sus tamaños
# enemigos -> contiene la lista de enemigos y cómo se generan
import clases.personaje as personaje
import clases.variables as variables
import clases.meteoritos as meteoritos
import clases.enemigos as enemigos
import sys

# Inicia todos los módulos de pygame
pygame.init()

# Creamos una fuente de texto general y la guardamos en variables
# Esto nos permite usarla en otras partes del juego para mostrar textos
variables.font = pygame.font.SysFont(None, 36)


# ------------------------------------------------------------
# FUNCIÓN: escalar_cuadrado
# ------------------------------------------------------------
# Esta función sirve para:
# 1. Recortar una imagen al centro en forma de cuadrado
# 2. Escalarla al tamaño que queramos
#
# ¿Por qué hacemos esto?
# Porque algunas imágenes no son cuadradas y se deforman al redimensionarlas.
# Así primero cogemos la parte central cuadrada y luego la ajustamos bien.
def escalar_cuadrado(image, side):
    width, height = image.get_size()   # tamaño original de la imagen
    base = min(width, height)          # usamos el lado más pequeño para hacer el cuadrado
    x = (width - base) // 2            # coordenada X para recortar desde el centro
    y = (height - base) // 2           # coordenada Y para recortar desde el centro

    # Recortamos la imagen a un cuadrado central
    square = image.subsurface((x, y, base, base)).copy()

    # Escalamos la imagen cuadrada al tamaño deseado
    return pygame.transform.smoothscale(square, (side, side))


# ------------------------------------------------------------
# VENTANA PRINCIPAL DEL JUEGO
# ------------------------------------------------------------
# Creamos la ventana usando el ancho y alto guardados en variables
ventana = pygame.display.set_mode((variables.ANCHO, variables.ALTO))

# Título de la ventana
pygame.display.set_caption("Juego Star Wars de Daniel y Ruben")

# Clock sirve para controlar los FPS (frames por segundo)
clock = pygame.time.Clock()


# ------------------------------------------------------------
# CARGA DE IMÁGENES
# ------------------------------------------------------------
# convert_alpha() se usa para imágenes con transparencia (PNG)
player_image = pygame.image.load("assets/milenario.png").convert_alpha()
meteor_image = pygame.image.load("assets/meteorito.png").convert_alpha()
background_image = pygame.image.load("assets/fondo.jpg").convert()

# Imagen del enemigo normal
enemy_base_image = pygame.image.load("assets/enemigo.png").convert_alpha()

# Imagen del enemigo grande
enemy_big_base_image = pygame.image.load("assets/enemigo2.png").convert_alpha()

# Ajustamos el fondo al tamaño completo de la pantalla
background_image = pygame.transform.smoothscale(background_image, (variables.ANCHO, variables.ALTO))


# ------------------------------------------------------------
# ESCALAR IMÁGENES
# ------------------------------------------------------------
# Adaptamos las imágenes a los tamaños del juego
player_image = escalar_cuadrado(player_image, personaje.Personaje.player_width)
meteor_image = escalar_cuadrado(meteor_image, meteoritos.meteor_width)

# Enemigo normal a 60x60
enemy_image = escalar_cuadrado(enemy_base_image, 60)

# Enemigo grande a 95x95
enemy_big_image = escalar_cuadrado(enemy_big_base_image, 95)


# ------------------------------------------------------------
# FUENTES DEL MENÚ
# ------------------------------------------------------------
# Estas fuentes se usan para los textos de las pantallas del juego
font_titulo = pygame.font.SysFont(None, 70)
font_subtitulo = pygame.font.SysFont(None, 42)
font_nivel = pygame.font.SysFont(None, 36)
font_boton = pygame.font.SysFont(None, 40)


# ------------------------------------------------------------
# FUNCIÓN: pantalla_inicio
# ------------------------------------------------------------
# Muestra el menú inicial:
# - elegir nivel del 1 al 5
# - moverse con flechas o hacer clic con el ratón
# - pulsar JUGAR
#
# Devuelve el número del nivel elegido
def pantalla_inicio():
    niveles = [1, 2, 3, 4, 5]   # lista de niveles
    nivel_seleccionado = 0       # empezamos seleccionando el primer nivel

    # Botón de jugar
    boton_jugar = pygame.Rect(variables.ANCHO // 2 - 100, 500, 200, 60)

    # Lista donde guardaremos los rectángulos visuales de los niveles
    rects_niveles = []

    while True:
        # Posición actual del ratón
        mouse_pos = pygame.mouse.get_pos()

        # Dibujamos fondo
        ventana.blit(background_image, (0, 0))

        # Capa oscura semitransparente encima del fondo para que el texto se vea mejor
        overlay = pygame.Surface((variables.ANCHO, variables.ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        ventana.blit(overlay, (0, 0))

        # Título principal
        titulo = font_titulo.render("Juego Star Wars", True, (255, 255, 255))
        ventana.blit(titulo, (variables.ANCHO // 2 - titulo.get_width() // 2, 60))

        # Subtítulo
        subtitulo = font_subtitulo.render("Selecciona un nivel", True, (255, 220, 80))
        ventana.blit(subtitulo, (variables.ANCHO // 2 - subtitulo.get_width() // 2, 150))

        # Limpiamos la lista de rectángulos para volver a crearla en cada frame
        rects_niveles.clear()

        # Dibujamos los 5 niveles
        for i, nivel in enumerate(niveles):
            # Creamos el rectángulo de cada nivel
            rect = pygame.Rect(variables.ANCHO // 2 - 120, 220 + i * 50, 240, 40)
            rects_niveles.append(rect)

            # Comprobamos si el ratón está encima
            hover = rect.collidepoint(mouse_pos)

            # Comprobamos si este nivel es el seleccionado
            seleccionado = i == nivel_seleccionado

            # Elegimos colores según el estado
            if seleccionado:
                color_fondo = (50, 120, 255)
                color_texto = (255, 255, 255)
            elif hover:
                color_fondo = (80, 80, 80)
                color_texto = (255, 255, 255)
            else:
                color_fondo = (30, 30, 30)
                color_texto = (200, 200, 200)

            # Dibujamos el rectángulo
            pygame.draw.rect(ventana, color_fondo, rect, border_radius=8)
            pygame.draw.rect(ventana, (255, 255, 255), rect, 2, border_radius=8)

            # Dibujamos el texto del nivel
            texto_nivel = font_nivel.render(f"Nivel {nivel}", True, color_texto)
            ventana.blit(
                texto_nivel,
                (
                    rect.centerx - texto_nivel.get_width() // 2,
                    rect.centery - texto_nivel.get_height() // 2
                )
            )

        # Dibujamos el botón jugar
        hover_boton = boton_jugar.collidepoint(mouse_pos)
        color_boton = (0, 180, 90) if hover_boton else (0, 140, 70)
        pygame.draw.rect(ventana, color_boton, boton_jugar, border_radius=10)
        pygame.draw.rect(ventana, (255, 255, 255), boton_jugar, 2, border_radius=10)

        texto_jugar = font_boton.render("JUGAR", True, (255, 255, 255))
        ventana.blit(
            texto_jugar,
            (
                boton_jugar.centerx - texto_jugar.get_width() // 2,
                boton_jugar.centery - texto_jugar.get_height() // 2
            )
        )

        # Instrucciones
        instrucciones = font_nivel.render("Usa flechas ↑ ↓ o haz clic", True, (230, 230, 230))
        ventana.blit(instrucciones, (variables.ANCHO // 2 - instrucciones.get_width() // 2, 575))

        # Actualizamos la pantalla
        pygame.display.flip()

        # Gestionamos eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Controles de teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    nivel_seleccionado = (nivel_seleccionado - 1) % 5
                elif event.key == pygame.K_DOWN:
                    nivel_seleccionado = (nivel_seleccionado + 1) % 5
                elif event.key == pygame.K_RETURN:
                    return niveles[nivel_seleccionado]

            # Controles de ratón
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Si pulsamos en un nivel, lo seleccionamos
                for i, rect in enumerate(rects_niveles):
                    if rect.collidepoint(event.pos):
                        nivel_seleccionado = i

                # Si pulsamos el botón JUGAR, empezamos
                if boton_jugar.collidepoint(event.pos):
                    return niveles[nivel_seleccionado]


# ------------------------------------------------------------
# FUNCIÓN: pantalla_game_over
# ------------------------------------------------------------
# Muestra la pantalla cuando pierdes
# Opciones:
# - R para repetir
# - ESC para salir
#
# Devuelve:
# "repetir" o "salir"
def pantalla_game_over(nivel, puntuacion):
    font_game_over = pygame.font.SysFont(None, 90)
    font_info = pygame.font.SysFont(None, 42)
    font_small = pygame.font.SysFont(None, 32)

    while True:
        ventana.blit(background_image, (0, 0))

        overlay = pygame.Surface((variables.ANCHO, variables.ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        ventana.blit(overlay, (0, 0))

        texto_go = font_game_over.render("GAME OVER", True, (255, 60, 60))
        ventana.blit(texto_go, (variables.ANCHO // 2 - texto_go.get_width() // 2, 140))

        texto_puntos = font_info.render(f"Puntuacion final: {puntuacion}", True, (255, 255, 255))
        ventana.blit(texto_puntos, (variables.ANCHO // 2 - texto_puntos.get_width() // 2, 260))

        texto_nivel = font_info.render(f"Nivel jugado: {nivel}", True, (255, 255, 255))
        ventana.blit(texto_nivel, (variables.ANCHO // 2 - texto_nivel.get_width() // 2, 315))

        texto_reiniciar = font_small.render("Pulsa R para repetir el nivel", True, (255, 220, 80))
        ventana.blit(texto_reiniciar, (variables.ANCHO // 2 - texto_reiniciar.get_width() // 2, 410))

        texto_salir = font_small.render("Pulsa ESC para salir", True, (220, 220, 220))
        ventana.blit(texto_salir, (variables.ANCHO // 2 - texto_salir.get_width() // 2, 450))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "repetir"
                elif event.key == pygame.K_ESCAPE:
                    return "salir"


# ------------------------------------------------------------
# FUNCIÓN: pantalla_victoria
# ------------------------------------------------------------
# Muestra la pantalla cuando llegas al objetivo de puntos
# Opciones:
# - N para pasar al siguiente nivel
# - R para repetir
# - ESC para salir
#
# Devuelve:
# "siguiente", "repetir" o "salir"
def pantalla_victoria(nivel, puntuacion):
    font_win = pygame.font.SysFont(None, 80)
    font_info = pygame.font.SysFont(None, 42)
    font_small = pygame.font.SysFont(None, 32)

    while True:
        ventana.blit(background_image, (0, 0))

        overlay = pygame.Surface((variables.ANCHO, variables.ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        ventana.blit(overlay, (0, 0))

        # Texto principal distinto según si es el último nivel o no
        if nivel < 5:
            texto_win = font_win.render("NIVEL COMPLETADO", True, (80, 255, 120))
        else:
            texto_win = font_win.render("HAS COMPLETADO EL JUEGO", True, (80, 255, 120))

        ventana.blit(texto_win, (variables.ANCHO // 2 - texto_win.get_width() // 2, 120))

        texto_puntos = font_info.render(f"Puntuacion final: {puntuacion}", True, (255, 255, 255))
        ventana.blit(texto_puntos, (variables.ANCHO // 2 - texto_puntos.get_width() // 2, 240))

        texto_nivel = font_info.render(f"Nivel actual: {nivel}", True, (255, 255, 255))
        ventana.blit(texto_nivel, (variables.ANCHO // 2 - texto_nivel.get_width() // 2, 290))

        # Si no es el último nivel, mostramos la opción de pasar al siguiente
        if nivel < 5:
            texto_siguiente = font_small.render("Pulsa N para pasar al siguiente nivel", True, (255, 220, 80))
            ventana.blit(texto_siguiente, (variables.ANCHO // 2 - texto_siguiente.get_width() // 2, 390))
        else:
            texto_fin = font_small.render("Ya no quedan mas niveles galacticos", True, (255, 220, 80))
            ventana.blit(texto_fin, (variables.ANCHO // 2 - texto_fin.get_width() // 2, 390))

        texto_reiniciar = font_small.render("Pulsa R para repetir este nivel", True, (220, 220, 220))
        ventana.blit(texto_reiniciar, (variables.ANCHO // 2 - texto_reiniciar.get_width() // 2, 430))

        texto_salir = font_small.render("Pulsa ESC para salir", True, (220, 220, 220))
        ventana.blit(texto_salir, (variables.ANCHO // 2 - texto_salir.get_width() // 2, 470))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n and nivel < 5:
                    return "siguiente"
                elif event.key == pygame.K_r:
                    return "repetir"
                elif event.key == pygame.K_ESCAPE:
                    return "salir"


# ------------------------------------------------------------
# FUNCIÓN: jugar
# ------------------------------------------------------------
# Ejecuta una partida completa de un nivel
# Recibe como parámetro el nivel elegido
#
# Devuelve:
# - resultado de pantalla_game_over
# - resultado de pantalla_victoria
# - "salir" si se cierra el juego
def jugar(nivel_elegido):
    # Reiniciamos puntuación y listas
    variables.puntuacion = 0
    meteoritos.meteors.clear()
    enemigos.enemies.clear()

    # Colocamos al jugador en su posición inicial
    personaje.Personaje.player.x = variables.ANCHO // 2 - personaje.Personaje.player_width // 2
    personaje.Personaje.player.y = variables.ALTO - personaje.Personaje.player_height - 10
    personaje.Personaje.update_hitbox()

    # Configuración según el nivel
    if nivel_elegido == 1:
        velocidad_meteoritos = 4
        max_enemigos = 2
        spawn_enemigo_prob = 0.01
    elif nivel_elegido == 2:
        velocidad_meteoritos = 5
        max_enemigos = 3
        spawn_enemigo_prob = 0.02
    elif nivel_elegido == 3:
        velocidad_meteoritos = 6
        max_enemigos = 4
        spawn_enemigo_prob = 0.03
    elif nivel_elegido == 4:
        velocidad_meteoritos = 7
        max_enemigos = 5
        spawn_enemigo_prob = 0.04
    else:
        velocidad_meteoritos = 8
        max_enemigos = 6
        spawn_enemigo_prob = 0.05

    # Puntos necesarios para completar el nivel
    objetivo_puntos = 1000

    # Lista de balas del jugador
    balas = []

    # Tamaño de las balas
    bala_w, bala_h = 6, 16

    # Velocidad de las balas
    bala_speed = 10

    # Tiempo mínimo entre disparos (en milisegundos)
    cooldown_ms = 220

    # Momento del último disparo
    ultimo_disparo = 0

    run = True
    while run:
        # Limitamos a 60 FPS
        clock.tick(60)

        # ------------------------------------
        # EVENTOS
        # ------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"

        # ------------------------------------
        # MOVIMIENTO DEL JUGADOR
        # ------------------------------------
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

        # Actualizamos la hitbox después de mover el jugador
        personaje.Personaje.update_hitbox()

        # ------------------------------------
        # DISPARO DEL JUGADOR
        # ------------------------------------
        ahora = pygame.time.get_ticks()

        # Solo dispara si se pulsa espacio y ha pasado el cooldown
        if keys[pygame.K_SPACE] and (ahora - ultimo_disparo) >= cooldown_ms:
            bx = personaje.Personaje.player.centerx - bala_w // 2
            by = personaje.Personaje.player.top - bala_h

            # Creamos una bala como rectángulo y la añadimos a la lista
            balas.append(pygame.Rect(bx, by, bala_w, bala_h))
            ultimo_disparo = ahora

        # ------------------------------------
        # GENERAR METEORITOS
        # ------------------------------------
        if len(meteoritos.meteors) < 5:
            meteor_x = random.randint(0, variables.ANCHO - meteoritos.meteor_width)
            meteor_y = random.randint(-100, -40)
            meteor_rect = pygame.Rect(
                meteor_x,
                meteor_y,
                meteoritos.meteor_width,
                meteoritos.meteor_height
            )
            meteoritos.meteors.append(meteor_rect)

        # ------------------------------------
        # GENERAR ENEMIGOS
        # ------------------------------------
        if len(enemigos.enemies) < max_enemigos and random.random() < spawn_enemigo_prob:
            enemigos.spawn_enemy(variables.ANCHO, nivel_elegido)

        # ------------------------------------
        # ACTUALIZAR BALAS
        # ------------------------------------
        for b in balas[:]:
            b.y -= bala_speed
            if b.bottom < 0:
                balas.remove(b)

        # ------------------------------------
        # ACTUALIZAR METEORITOS
        # ------------------------------------
        for meteor in meteoritos.meteors[:]:
            meteor.y += velocidad_meteoritos

            # Si el meteorito sale por abajo, se elimina y sumamos puntos
            if meteor.top > variables.ALTO:
                meteoritos.meteors.remove(meteor)
                variables.puntuacion += 5

        # ------------------------------------
        # ACTUALIZAR ENEMIGOS
        # ------------------------------------
        for e in enemigos.enemies[:]:
            e.update()
            if e.rect.top > variables.ALTO:
                enemigos.enemies.remove(e)

        # ------------------------------------
        # COLISIONES JUGADOR VS METEORITOS
        # ------------------------------------
        for meteor in meteoritos.meteors:
            if personaje.Personaje.hitbox.colliderect(meteor):
                return pantalla_game_over(nivel_elegido, variables.puntuacion)

        # ------------------------------------
        # COLISIONES JUGADOR VS ENEMIGOS
        # ------------------------------------
        for e in enemigos.enemies:
            if personaje.Personaje.hitbox.colliderect(e.rect):
                return pantalla_game_over(nivel_elegido, variables.puntuacion)

        # ------------------------------------
        # COLISIONES BALAS VS ENEMIGOS
        # ------------------------------------
        for b in balas[:]:
            hit = False

            for e in enemigos.enemies[:]:
                if b.colliderect(e.rect):
                    # Si una bala toca a un enemigo, le quitamos 1 de vida
                    e.hp -= 1
                    hit = True

                    # Si la vida llega a 0, el enemigo muere
                    if e.hp <= 0:
                        enemigos.enemies.remove(e)

                        # El enemigo grande da más puntos
                        if e.tipo == "grande":
                            variables.puntuacion += 60
                        else:
                            variables.puntuacion += 20
                    break

            # Eliminamos la bala si ha golpeado algo
            if hit:
                balas.remove(b)

        # ------------------------------------
        # COMPROBAR VICTORIA
        # ------------------------------------
        if variables.puntuacion >= objetivo_puntos:
            return pantalla_victoria(nivel_elegido, variables.puntuacion)

        # ------------------------------------
        # DIBUJAR TODO EN PANTALLA
        # ------------------------------------
        ventana.fill(variables.BLACK)
        ventana.blit(background_image, (0, 0))

        # Dibujamos la nave del jugador
        ventana.blit(player_image, (personaje.Personaje.player.x, personaje.Personaje.player.y))

        # Dibujamos meteoritos
        for meteor in meteoritos.meteors:
            ventana.blit(meteor_image, (meteor.x, meteor.y))

        # Dibujamos enemigos
        for e in enemigos.enemies:
            if e.tipo == "grande":
                ventana.blit(enemy_big_image, (e.rect.x, e.rect.y))
            else:
                ventana.blit(enemy_image, (e.rect.x, e.rect.y))

        # Dibujamos balas
        for b in balas:
            pygame.draw.rect(ventana, (255, 220, 80), b)

        # Mostramos puntuación
        puntuacion_text = variables.font.render(f"Puntuacion: {variables.puntuacion}", True, variables.WHITE)
        ventana.blit(puntuacion_text, (10, 10))

        # Mostramos nivel actual
        nivel_text = variables.font.render(f"Nivel: {nivel_elegido}", True, variables.WHITE)
        ventana.blit(nivel_text, (10, 45))

        # Mostramos objetivo de puntos
        objetivo_text = variables.font.render(f"Objetivo: {objetivo_puntos}", True, variables.WHITE)
        ventana.blit(objetivo_text, (10, 80))

        # Actualizamos pantalla
        pygame.display.flip()

    return "salir"


# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------
# Primero elegimos un nivel en el menú
nivel_actual = pantalla_inicio()

# Bucle principal del juego completo
while True:
    resultado = jugar(nivel_actual)

    # Si el jugador quiere salir, terminamos
    if resultado == "salir":
        break

    # Si quiere repetir, volvemos a jugar el mismo nivel
    elif resultado == "repetir":
        continue

    # Si quiere pasar al siguiente nivel
    elif resultado == "siguiente":
        if nivel_actual < 5:
            nivel_actual += 1
        else:
            break

# Cerramos pygame y salimos del programa
pygame.quit()
sys.exit()