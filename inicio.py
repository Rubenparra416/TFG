import pygame
import random
import sys
from pathlib import Path

try:
    from clases import personaje, variables, meteoritos, enemigos
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parent))

import clases.personaje as personaje
import clases.variables as variables
import clases.meteoritos as meteoritos
import clases.enemigos as enemigos


pygame.init()
variables.font = pygame.font.SysFont(None, 36)

WHITE = getattr(variables, "WHITE", (255, 255, 255))


# ------------------------------------------------------------
# RUTAS DE MUSICA
# ------------------------------------------------------------
INTRO_MUSIC_FILES = [
    "assets/intro.ogg",
    "assets/musica/intro.mp3",
    "assets/musica/intro.ogg",
    "assets/musica/intro.mp3",
    "assets/star_wars_theme.ogg",
    "assets/star_wars_theme.mp3",
]

LEVEL1_MUSIC_FILES = [
    "assets/nivel1.ogg",
    "assets/musica/nivel1.mp3",
    "assets/level1.ogg",
    "assets/level1.mp3",
    "assets/musica/nivel1.ogg",
    "assets/musica/nivel1.mp3",
]

GAME_OVER_MUSIC_FILES = [
    "assets/musica/imperio.ogg",
    "assets/musica/imperio.mp3",
    "assets/musica/imperial_march.ogg",
    "assets/musica/imperial_march.mp3",
]

VICTORY_MUSIC_FILES = [
    "assets/musica/premio.ogg",
    "assets/musica/premio.mp3",
]


# ------------------------------------------------------------
# FUNCION: reproducir_musica
# ------------------------------------------------------------
def reproducir_musica(files, nombre, volume=0.35):
    for relative_path in files:
        track_path = Path(relative_path)
        if not track_path.exists():
            continue

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(str(track_path))
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
            return True
        except pygame.error as exc:
            print(f"No se pudo reproducir musica de {nombre} ({track_path}): {exc}")

    print(f"No se encontro musica de {nombre}. Coloca un archivo en assets/.")
    return False


# ------------------------------------------------------------
# FUNCION: escalar_cuadrado
# ------------------------------------------------------------
def escalar_cuadrado(image, side):
    width, height = image.get_size()
    base = min(width, height)
    x = (width - base) // 2
    y = (height - base) // 2
    square = image.subsurface((x, y, base, base)).copy()
    return pygame.transform.smoothscale(square, (side, side))


# ------------------------------------------------------------
# FUNCION: dibujar_barra_vida
# ------------------------------------------------------------
def dibujar_barra_vida(surface, x, y, vida, vida_max, ancho=220, alto=22):
    porcentaje = max(0, vida) / vida_max
    ancho_relleno = int(ancho * porcentaje)

    pygame.draw.rect(surface, (60, 60, 60), (x, y, ancho, alto), border_radius=6)

    if porcentaje > 0.6:
        color = (50, 220, 90)
    elif porcentaje > 0.3:
        color = (255, 200, 50)
    else:
        color = (220, 60, 60)

    pygame.draw.rect(surface, color, (x, y, ancho_relleno, alto), border_radius=6)
    pygame.draw.rect(surface, (255, 255, 255), (x, y, ancho, alto), 2, border_radius=6)


# ------------------------------------------------------------
# FUNCION: desbloquear_siguiente_nivel
# ------------------------------------------------------------
def desbloquear_siguiente_nivel(nivel_completado):
    if (
        nivel_completado == variables.nivel_desbloqueado
        and nivel_completado < variables.MAX_NIVELES
    ):
        variables.nivel_desbloqueado += 1


# ------------------------------------------------------------
# VENTANA PRINCIPAL DEL JUEGO
# ------------------------------------------------------------
ventana = pygame.display.set_mode((variables.ANCHO, variables.ALTO))
pygame.display.set_caption("Juego Star Wars de Daniel y Ruben")
clock = pygame.time.Clock()

reproducir_musica(INTRO_MUSIC_FILES, "intro")


# ------------------------------------------------------------
# CARGA DE IMAGENES
# ------------------------------------------------------------
player_image = pygame.image.load("assets/milenario.png").convert_alpha()
meteor_image = pygame.image.load("assets/meteorito.png").convert_alpha()
background_image = pygame.image.load("assets/fondo.jpg").convert()
enemy_base_image = pygame.image.load("assets/enemigo.png").convert_alpha()
enemy_big_base_image = pygame.image.load("assets/enemigo2.png").convert_alpha()
title_image = pygame.image.load("assets/titulo.png").convert_alpha()
enemy_shooter_image = pygame.image.load("assets/boss.png").convert_alpha()

game_over_image = None
try:
    game_over_image = pygame.image.load("assets/game_over.png").convert_alpha()
    game_over_image = pygame.transform.smoothscale(game_over_image, (400, 200))
except Exception as e:
    print("No se pudo cargar assets/game_over.png:", e)

background_image = pygame.transform.smoothscale(
    background_image, (variables.ANCHO, variables.ALTO)
)

player_image = escalar_cuadrado(player_image, personaje.Personaje.player_width)
meteor_image = escalar_cuadrado(meteor_image, meteoritos.meteor_width)
enemy_image = escalar_cuadrado(enemy_base_image, 60)
enemy_big_image = escalar_cuadrado(enemy_big_base_image, 95)
enemy_shooter_image = escalar_cuadrado(enemy_shooter_image, 130)

title_image = pygame.transform.smoothscale(title_image, (1000, 350))

# ------------------------------------------------------------
# FUENTES
# ------------------------------------------------------------
font_subtitulo = pygame.font.SysFont(None, 42)
font_nivel = pygame.font.SysFont(None, 36)
font_boton = pygame.font.SysFont(None, 40)


# ------------------------------------------------------------
# PANTALLA DE INICIO
# ------------------------------------------------------------
def pantalla_inicio():
    reproducir_musica(INTRO_MUSIC_FILES, "intro")

    niveles = [1, 2, 3, 4, 5]
    nivel_seleccionado = 0

    boton_jugar = pygame.Rect(variables.ANCHO // 2 - 100, 560, 200, 60)
    rects_niveles = []

    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        ventana.blit(background_image, (0, 0))

        overlay = pygame.Surface((variables.ANCHO, variables.ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        ventana.blit(overlay, (0, 0))

        ventana.blit(
            title_image,
            (variables.ANCHO // 2 - title_image.get_width() // 2, -50)
        )

        subtitulo = font_subtitulo.render(
            "Selecciona un nivel", True, (255, 220, 80)
        )
        ventana.blit(
            subtitulo,
            (variables.ANCHO // 2 - subtitulo.get_width() // 2, 220)
        )

        info_bloqueo = font_nivel.render(
            f"Nivel maximo desbloqueado: {variables.nivel_desbloqueado}",
            True,
            (230, 230, 230)
        )
        ventana.blit(
            info_bloqueo,
            (variables.ANCHO // 2 - info_bloqueo.get_width() // 2, 255)
        )

        rects_niveles.clear()

        for i, nivel in enumerate(niveles):
            rect = pygame.Rect(variables.ANCHO // 2 - 120, 290 + i * 50, 240, 40)
            rects_niveles.append(rect)

            bloqueado = nivel > variables.nivel_desbloqueado
            hover = rect.collidepoint(mouse_pos)
            seleccionado = i == nivel_seleccionado

            if bloqueado:
                color_fondo = (50, 50, 50)
                color_texto = (140, 140, 140)
            elif seleccionado:
                color_fondo = (50, 120, 255)
                color_texto = (255, 255, 255)
            elif hover:
                color_fondo = (80, 80, 80)
                color_texto = (255, 255, 255)
            else:
                color_fondo = (30, 30, 30)
                color_texto = (200, 200, 200)

            pygame.draw.rect(ventana, color_fondo, rect, border_radius=8)
            pygame.draw.rect(ventana, (255, 255, 255), rect, 2, border_radius=8)

            texto_nivel = font_nivel.render(f"Nivel {nivel}", True, color_texto)
            ventana.blit(
                texto_nivel,
                (
                    rect.centerx - texto_nivel.get_width() // 2,
                    rect.centery - texto_nivel.get_height() // 2,
                ),
            )

        nivel_elegido = niveles[nivel_seleccionado]
        nivel_bloqueado = nivel_elegido > variables.nivel_desbloqueado

        hover_boton = boton_jugar.collidepoint(mouse_pos)
        if nivel_bloqueado:
            color_boton = (90, 90, 90)
        else:
            color_boton = (0, 180, 90) if hover_boton else (0, 140, 70)

        pygame.draw.rect(ventana, color_boton, boton_jugar, border_radius=10)
        pygame.draw.rect(ventana, (255, 255, 255), boton_jugar, 2, border_radius=10)

        texto_jugar = font_boton.render("JUGAR", True, (255, 255, 255))
        ventana.blit(
            texto_jugar,
            (
                boton_jugar.centerx - texto_jugar.get_width() // 2,
                boton_jugar.centery - texto_jugar.get_height() // 2,
            ),
        )

        instrucciones = font_nivel.render(
            "Usa flechas ↑ ↓ o haz clic", True, (230, 230, 230)
        )
        ventana.blit(
            instrucciones,
            (variables.ANCHO // 2 - instrucciones.get_width() // 2, 650),
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    nivel_seleccionado = max(0, nivel_seleccionado - 1)
                elif event.key == pygame.K_DOWN:
                    nivel_seleccionado = min(
                        variables.nivel_desbloqueado - 1,
                        nivel_seleccionado + 1
                    )
                elif event.key == pygame.K_RETURN:
                    nivel_elegido = niveles[nivel_seleccionado]
                    if nivel_elegido <= variables.nivel_desbloqueado:
                        return nivel_elegido

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(rects_niveles):
                    if rect.collidepoint(event.pos) and niveles[i] <= variables.nivel_desbloqueado:
                        nivel_seleccionado = i

                if boton_jugar.collidepoint(event.pos):
                    nivel_elegido = niveles[nivel_seleccionado]
                    if nivel_elegido <= variables.nivel_desbloqueado:
                        return nivel_elegido


# ------------------------------------------------------------
# PANTALLA GAME OVER
# ------------------------------------------------------------
def pantalla_game_over(nivel, puntuacion):
    font_info = pygame.font.SysFont(None, 42)
    font_small = pygame.font.SysFont(None, 32)

    reproducir_musica(GAME_OVER_MUSIC_FILES, "game over")

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "repetir"
                elif event.key == pygame.K_ESCAPE:
                    return "salir"
                else:
                    return "menu"

        ventana.blit(background_image, (0, 0))

        overlay = pygame.Surface((variables.ANCHO, variables.ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        ventana.blit(overlay, (0, 0))

        if game_over_image is not None:
            ventana.blit(
                game_over_image,
                (
                    variables.ANCHO // 2 - game_over_image.get_width() // 2,
                    90,
                ),
            )
        else:
            font_game_over = pygame.font.SysFont(None, 90)
            texto_go = font_game_over.render("GAME OVER", True, (255, 60, 60))
            ventana.blit(
                texto_go,
                (variables.ANCHO // 2 - texto_go.get_width() // 2, 140),
            )

        texto_imperio = font_info.render(
            "Ha ganado el Imperio", True, (255, 220, 80)
        )
        ventana.blit(
            texto_imperio,
            (variables.ANCHO // 2 - texto_imperio.get_width() // 2, 250),
        )

        texto_puntos = font_info.render(
            f"Puntuacion final: {puntuacion}", True, (255, 255, 255)
        )
        ventana.blit(
            texto_puntos,
            (variables.ANCHO // 2 - texto_puntos.get_width() // 2, 330),
        )

        texto_nivel = font_info.render(
            f"Nivel jugado: {nivel}", True, (255, 255, 255)
        )
        ventana.blit(
            texto_nivel,
            (variables.ANCHO // 2 - texto_nivel.get_width() // 2, 380),
        )

        texto_reiniciar = font_small.render(
            "Pulsa R para repetir el nivel", True, (255, 220, 80)
        )
        ventana.blit(
            texto_reiniciar,
            (variables.ANCHO // 2 - texto_reiniciar.get_width() // 2, 470),
        )

        texto_menu = font_small.render(
            "Pulsa cualquier otra tecla para volver al menu",
            True,
            (255, 220, 80),
        )
        ventana.blit(
            texto_menu,
            (variables.ANCHO // 2 - texto_menu.get_width() // 2, 510),
        )

        texto_salir = font_small.render(
            "Pulsa ESC para salir", True, (220, 220, 220)
        )
        ventana.blit(
            texto_salir,
            (variables.ANCHO // 2 - texto_salir.get_width() // 2, 550),
        )

        pygame.display.flip()


# ------------------------------------------------------------
# PANTALLA VICTORIA
# ------------------------------------------------------------
def pantalla_victoria(nivel, puntuacion):
    desbloquear_siguiente_nivel(nivel)

    font_win = pygame.font.SysFont(None, 80)
    font_info = pygame.font.SysFont(None, 42)
    font_small = pygame.font.SysFont(None, 32)

    reproducir_musica(VICTORY_MUSIC_FILES, "victoria")

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n and nivel < variables.MAX_NIVELES:
                    return "siguiente"
                elif event.key == pygame.K_r:
                    return "repetir"
                elif event.key == pygame.K_ESCAPE:
                    return "salir"

        ventana.blit(background_image, (0, 0))

        overlay = pygame.Surface((variables.ANCHO, variables.ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        ventana.blit(overlay, (0, 0))

        if nivel < variables.MAX_NIVELES:
            texto_win = font_win.render("NIVEL COMPLETADO", True, (80, 255, 120))
        else:
            texto_win = font_win.render(
                "HAS COMPLETADO EL JUEGO", True, (80, 255, 120)
            )

        ventana.blit(
            texto_win,
            (variables.ANCHO // 2 - texto_win.get_width() // 2, 120),
        )

        texto_puntos = font_info.render(
            f"Puntuacion final: {puntuacion}", True, (255, 255, 255)
        )
        ventana.blit(
            texto_puntos,
            (variables.ANCHO // 2 - texto_puntos.get_width() // 2, 240),
        )

        texto_nivel = font_info.render(
            f"Nivel actual: {nivel}", True, (255, 255, 255)
        )
        ventana.blit(
            texto_nivel,
            (variables.ANCHO // 2 - texto_nivel.get_width() // 2, 290),
        )

        if nivel < variables.MAX_NIVELES:
            texto_desbloqueado = font_info.render(
                f"Has desbloqueado el nivel {min(nivel + 1, variables.MAX_NIVELES)}",
                True,
                (255, 220, 80)
            )
            ventana.blit(
                texto_desbloqueado,
                (variables.ANCHO // 2 - texto_desbloqueado.get_width() // 2, 340)
            )

            texto_siguiente = font_small.render(
                "Pulsa N para pasar al siguiente nivel",
                True,
                (255, 220, 80)
            )
            ventana.blit(
                texto_siguiente,
                (variables.ANCHO // 2 - texto_siguiente.get_width() // 2, 390)
            )
        else:
            texto_fin = font_small.render(
                "Ya no quedan mas niveles galacticos",
                True,
                (255, 220, 80)
            )
            ventana.blit(
                texto_fin,
                (variables.ANCHO // 2 - texto_fin.get_width() // 2, 390)
            )

        texto_reiniciar = font_small.render(
            "Pulsa R para repetir este nivel", True, (220, 220, 220)
        )
        ventana.blit(
            texto_reiniciar,
            (variables.ANCHO // 2 - texto_reiniciar.get_width() // 2, 430),
        )

        texto_salir = font_small.render(
            "Pulsa ESC para salir", True, (220, 220, 220)
        )
        ventana.blit(
            texto_salir,
            (variables.ANCHO // 2 - texto_salir.get_width() // 2, 470),
        )

        pygame.display.flip()


# ------------------------------------------------------------
# JUGAR UN NIVEL
# ------------------------------------------------------------
def jugar(nivel_elegido):
    if nivel_elegido == 1:
        reproducir_musica(LEVEL1_MUSIC_FILES, "nivel 1")
    else:
        reproducir_musica(INTRO_MUSIC_FILES, f"nivel {nivel_elegido}")

    variables.puntuacion = 0
    meteoritos.meteors.clear()
    enemigos.enemies.clear()

    personaje.Personaje.player.x = (
        variables.ANCHO // 2 - personaje.Personaje.player_width // 2
    )
    personaje.Personaje.player.y = (
        variables.ALTO - personaje.Personaje.player_height - 10
    )
    personaje.Personaje.update_hitbox()

    if nivel_elegido == 1:
        velocidad_meteoritos = 4
        max_enemigos = 2
        spawn_enemigo_prob = 0.01
    elif nivel_elegido == 2:
        velocidad_meteoritos = 6
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

    objetivo_puntos = 500 + (nivel_elegido - 1) * 100

    balas = []
    bala_w, bala_h = 6, 16
    bala_speed = 10
    cooldown_ms = 220
    ultimo_disparo = 0
    pausa = False

    # Vida del jugador
    vida_max = 100
    vida_jugador = vida_max
    ultimo_golpe = 0
    invulnerabilidad_ms = 800

    # Boss nivel 4
    boss_activo = nivel_elegido == 4
    boss_hp = 8
    boss_rect = pygame.Rect(variables.ANCHO // 2 - 65, 40, 130, 130)
    boss_dir = 4
    boss_balas = []
    boss_bala_w, boss_bala_h = 8, 18
    boss_bala_speed = 7
    boss_cooldown = 900
    ultimo_disparo_boss = 0

    # Final boss nivel 5
    final_boss_aparecio = False
    final_boss_activo = False
    final_boss_hp = 5
    final_boss_rect = pygame.Rect(variables.ANCHO // 2 - 90, 30, 180, 180)
    final_boss_dir = 5
    final_boss_balas = []
    final_boss_bala_w, final_boss_bala_h = 10, 22
    final_boss_bala_speed = 8
    final_boss_cooldown = 500
    ultimo_disparo_final_boss = 0

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pausa = not pausa

        keys = pygame.key.get_pressed()
        speed = personaje.Personaje.player_speed
        ahora = pygame.time.get_ticks()

        if not pausa:
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and personaje.Personaje.player.left > 0:
                personaje.Personaje.player.x -= speed
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and personaje.Personaje.player.right < variables.ANCHO:
                personaje.Personaje.player.x += speed
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and personaje.Personaje.player.top > 0:
                personaje.Personaje.player.y -= speed
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and personaje.Personaje.player.bottom < variables.ALTO:
                personaje.Personaje.player.y += speed

        personaje.Personaje.update_hitbox()

        if keys[pygame.K_SPACE] and (ahora - ultimo_disparo) >= cooldown_ms and not pausa:
            bx = personaje.Personaje.player.centerx - bala_w // 2
            by = personaje.Personaje.player.top - bala_h
            balas.append(pygame.Rect(bx, by, bala_w, bala_h))
            ultimo_disparo = ahora

        if pausa:
            ventana.blit(background_image, (0, 0))

            mostrar_jugador = True
            if ahora - ultimo_golpe < invulnerabilidad_ms:
                if (ahora // 100) % 2 == 0:
                    mostrar_jugador = False

            if mostrar_jugador:
                ventana.blit(player_image, (personaje.Personaje.player.x, personaje.Personaje.player.y))

            for meteor in meteoritos.meteors:
                ventana.blit(meteor_image, (meteor.x, meteor.y))

            for e in enemigos.enemies:
                if e.tipo == "grande":
                    ventana.blit(enemy_big_image, (e.rect.x, e.rect.y))
                else:
                    ventana.blit(enemy_image, (e.rect.x, e.rect.y))

            if boss_activo and boss_hp > 0:
                ventana.blit(enemy_shooter_image, (boss_rect.x, boss_rect.y))

            if final_boss_activo and final_boss_hp > 0:
                ventana.blit(enemy_shooter_image, (final_boss_rect.x, final_boss_rect.y))

            for b in balas:
                pygame.draw.rect(ventana, (255, 220, 80), b)

            for bb in boss_balas:
                pygame.draw.rect(ventana, (255, 60, 60), bb)

            for fb in final_boss_balas:
                pygame.draw.rect(ventana, (255, 0, 0), fb["rect"])

            pausa_text = variables.font.render(
                "Juego pausado - Presiona P para continuar",
                True,
                (255, 255, 255),
            )
            text_rect = pausa_text.get_rect(center=(variables.ANCHO // 2, variables.ALTO // 2))
            ventana.blit(pausa_text, text_rect)
            pygame.display.flip()
            continue

        # Aparicion del final boss
        if nivel_elegido == 5 and variables.puntuacion >= 600 and not final_boss_aparecio:
            final_boss_aparecio = True
            final_boss_activo = True
            meteoritos.meteors.clear()
            enemigos.enemies.clear()

        # Meteoritos y enemigos normales solo si no esta activo el final boss
        if not final_boss_activo:
            if len(meteoritos.meteors) < 5:
                meteor_x = random.randint(0, variables.ANCHO - meteoritos.meteor_width)
                meteor_y = random.randint(-100, -40)
                meteor_rect = pygame.Rect(
                    meteor_x,
                    meteor_y,
                    meteoritos.meteor_width,
                    meteoritos.meteor_height,
                )
                meteoritos.meteors.append(meteor_rect)

            if len(enemigos.enemies) < max_enemigos and random.random() < spawn_enemigo_prob:
                enemigos.spawn_enemy(variables.ANCHO, nivel_elegido)

        # Balas jugador
        for b in balas[:]:
            b.y -= bala_speed
            if b.bottom < 0:
                balas.remove(b)

        # Movimiento meteoritos
        for meteor in meteoritos.meteors[:]:
            meteor.y += velocidad_meteoritos
            if meteor.top > variables.ALTO:
                meteoritos.meteors.remove(meteor)
                variables.puntuacion += 10

        # Movimiento enemigos normales
        for e in enemigos.enemies[:]:
            e.update()
            if e.rect.top > variables.ALTO:
                enemigos.enemies.remove(e)

        # Boss nivel 4
        if boss_activo and boss_hp > 0:
            boss_rect.x += boss_dir
            if boss_rect.left <= 0 or boss_rect.right >= variables.ANCHO:
                boss_dir *= -1

            if ahora - ultimo_disparo_boss >= boss_cooldown:
                bbx = boss_rect.centerx - boss_bala_w // 2
                bby = boss_rect.bottom
                boss_balas.append(pygame.Rect(bbx, bby, boss_bala_w, boss_bala_h))
                ultimo_disparo_boss = ahora

        for bb in boss_balas[:]:
            bb.y += boss_bala_speed
            if bb.top > variables.ALTO:
                boss_balas.remove(bb)

        # Final boss nivel 5
        if final_boss_activo and final_boss_hp > 0:
            final_boss_rect.x += final_boss_dir
            if final_boss_rect.left <= 0 or final_boss_rect.right >= variables.ANCHO:
                final_boss_dir *= -1

            if ahora - ultimo_disparo_final_boss >= final_boss_cooldown:
                centro_x = final_boss_rect.centerx
                y = final_boss_rect.bottom
                velocidades_x = [-4, 0, 4]

                for i, vx in enumerate(velocidades_x):
                    x = centro_x - 20 + i * 20
                    final_boss_balas.append({
                        "rect": pygame.Rect(x, y, final_boss_bala_w, final_boss_bala_h),
                        "vel_x": vx,
                        "vel_y": final_boss_bala_speed
                    })

                ultimo_disparo_final_boss = ahora

        for fb in final_boss_balas[:]:
            fb["rect"].x += fb["vel_x"]
            fb["rect"].y += fb["vel_y"]

            if (
                fb["rect"].top > variables.ALTO
                or fb["rect"].right < 0
                or fb["rect"].left > variables.ANCHO
            ):
                final_boss_balas.remove(fb)

        # Colisiones jugador con meteoritos
        for meteor in meteoritos.meteors[:]:
            if personaje.Personaje.hitbox.colliderect(meteor):
                if ahora - ultimo_golpe >= invulnerabilidad_ms:
                    vida_jugador -= 20
                    ultimo_golpe = ahora
                    if meteor in meteoritos.meteors:
                        meteoritos.meteors.remove(meteor)

                    if vida_jugador <= 0:
                        return pantalla_game_over(nivel_elegido, variables.puntuacion)

        # Colisiones jugador con enemigos normales
        for e in enemigos.enemies[:]:
            if personaje.Personaje.hitbox.colliderect(e.rect):
                if ahora - ultimo_golpe >= invulnerabilidad_ms:
                    vida_jugador -= 25
                    ultimo_golpe = ahora
                    if e in enemigos.enemies:
                        enemigos.enemies.remove(e)

                    if vida_jugador <= 0:
                        return pantalla_game_over(nivel_elegido, variables.puntuacion)

        # Colision jugador con boss nivel 4
        if boss_activo and boss_hp > 0 and personaje.Personaje.hitbox.colliderect(boss_rect):
            if ahora - ultimo_golpe >= invulnerabilidad_ms:
                vida_jugador -= 35
                ultimo_golpe = ahora
                if vida_jugador <= 0:
                    return pantalla_game_over(nivel_elegido, variables.puntuacion)

        # Colision balas boss nivel 4 con jugador
        for bb in boss_balas[:]:
            if personaje.Personaje.hitbox.colliderect(bb):
                if ahora - ultimo_golpe >= invulnerabilidad_ms:
                    vida_jugador -= 15
                    ultimo_golpe = ahora
                    if bb in boss_balas:
                        boss_balas.remove(bb)

                    if vida_jugador <= 0:
                        return pantalla_game_over(nivel_elegido, variables.puntuacion)

        # Colision jugador con final boss
        if final_boss_activo and final_boss_hp > 0 and personaje.Personaje.hitbox.colliderect(final_boss_rect):
            if ahora - ultimo_golpe >= invulnerabilidad_ms:
                vida_jugador -= 40
                ultimo_golpe = ahora
                if vida_jugador <= 0:
                    return pantalla_game_over(nivel_elegido, variables.puntuacion)

        # Colision balas final boss con jugador
        for fb in final_boss_balas[:]:
            if personaje.Personaje.hitbox.colliderect(fb["rect"]):
                if ahora - ultimo_golpe >= invulnerabilidad_ms:
                    vida_jugador -= 20
                    ultimo_golpe = ahora
                    if fb in final_boss_balas:
                        final_boss_balas.remove(fb)

                    if vida_jugador <= 0:
                        return pantalla_game_over(nivel_elegido, variables.puntuacion)

        # Balas jugador contra enemigos normales
        for b in balas[:]:
            hit = False
            for e in enemigos.enemies[:]:
                if b.colliderect(e.rect):
                    e.hp -= 1
                    hit = True
                    if e.hp <= 0:
                        enemigos.enemies.remove(e)
                        variables.puntuacion += 60 if e.tipo == "grande" else 20
                    break

            if hit and b in balas:
                balas.remove(b)

        # Balas jugador contra boss nivel 4
        if boss_activo and boss_hp > 0:
            for b in balas[:]:
                if b.colliderect(boss_rect):
                    boss_hp -= 1
                    if b in balas:
                        balas.remove(b)

                    if boss_hp <= 0:
                        variables.puntuacion += 150
                        boss_activo = False
                    break

        # Balas jugador contra final boss
        if final_boss_activo and final_boss_hp > 0:
            for b in balas[:]:
                if b.colliderect(final_boss_rect):
                    final_boss_hp -= 1
                    if b in balas:
                        balas.remove(b)

                    if final_boss_hp <= 0:
                        variables.puntuacion += 300
                        final_boss_activo = False
                    break

        # Victoria
        if nivel_elegido == 5:
            if final_boss_aparecio and not final_boss_activo:
                return pantalla_victoria(nivel_elegido, variables.puntuacion)
        else:
            if variables.puntuacion >= objetivo_puntos:
                return pantalla_victoria(nivel_elegido, variables.puntuacion)

        # Dibujado
        ventana.blit(background_image, (0, 0))

        mostrar_jugador = True
        if ahora - ultimo_golpe < invulnerabilidad_ms:
            if (ahora // 100) % 2 == 0:
                mostrar_jugador = False

        if mostrar_jugador:
            ventana.blit(player_image, (personaje.Personaje.player.x, personaje.Personaje.player.y))

        for meteor in meteoritos.meteors:
            ventana.blit(meteor_image, (meteor.x, meteor.y))

        for e in enemigos.enemies:
            if e.tipo == "grande":
                ventana.blit(enemy_big_image, (e.rect.x, e.rect.y))
            else:
                ventana.blit(enemy_image, (e.rect.x, e.rect.y))

        if boss_activo and boss_hp > 0:
            ventana.blit(enemy_shooter_image, (boss_rect.x, boss_rect.y))

        if final_boss_activo and final_boss_hp > 0:
            ventana.blit(enemy_shooter_image, (final_boss_rect.x, final_boss_rect.y))

        for b in balas:
            pygame.draw.rect(ventana, (255, 220, 80), b)

        for bb in boss_balas:
            pygame.draw.rect(ventana, (255, 60, 60), bb)

        for fb in final_boss_balas:
            pygame.draw.rect(ventana, (255, 0, 0), fb["rect"])

               # Texto combinado de puntuacion
        if nivel_elegido == 5:
            if not final_boss_aparecio:
                progreso_texto = f"Puntuacion: {variables.puntuacion}/600"
            else:
                progreso_texto = f"Puntuacion: {variables.puntuacion} - Final Boss"
        else:
            progreso_texto = f"Puntuacion: {variables.puntuacion}/{objetivo_puntos}"

        progreso_render = variables.font.render(progreso_texto, True, WHITE)
        ventana.blit(progreso_render, (10, 10))

        nivel_text = variables.font.render(f"Nivel: {nivel_elegido}", True, WHITE)
        ventana.blit(nivel_text, (10, 45))

        vida_text = variables.font.render(
            f"Vida: {vida_jugador}/{vida_max}", True, WHITE
        )
        ventana.blit(vida_text, (10, 80))

        dibujar_barra_vida(ventana, 10, 115, vida_jugador, vida_max)


        if boss_activo and boss_hp > 0:
            boss_text = variables.font.render(f"Boss HP: {boss_hp}", True, WHITE)
            ventana.blit(boss_text, (10, 185))

        if final_boss_activo and final_boss_hp > 0:
            final_boss_text = variables.font.render(
                f"Final Boss HP: {final_boss_hp}", True, WHITE
            )
            ventana.blit(final_boss_text, (10, 220))

        pygame.display.flip()


# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------
nivel_actual = pantalla_inicio()

if nivel_actual == "salir":
    pygame.quit()
    sys.exit()

while True:
    resultado = jugar(nivel_actual)

    if resultado == "salir":
        break
    elif resultado == "bloqueado":
        nivel_actual = pantalla_inicio()
        if nivel_actual == "salir":
            break
    elif resultado == "repetir":
        continue
    elif resultado == "siguiente":
        if nivel_actual < variables.MAX_NIVELES:
            nivel_actual += 1
        else:
            break
    else:
        nivel_actual = pantalla_inicio()
        if nivel_actual == "salir":
            break

pygame.quit()
sys.exit()