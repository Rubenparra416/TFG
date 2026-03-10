import pygame
import random

try:
    from clases import personaje, variables, meteoritos, enemigos
except ModuleNotFoundError:
    import clases.personaje as personaje
    import clases.variables as variables
    import clases.meteoritos as meteoritos
    import clases.enemigos as enemigos


class Juego:
    def __init__(self, ventana, clock, recursos, audio, pantallas):
        self.ventana = ventana
        self.clock = clock
        self.recursos = recursos
        self.audio = audio
        self.pantallas = pantallas
        self.WHITE = getattr(variables, "WHITE", (255, 255, 255))

def jugar(self, nivel_elegido):
    if nivel_elegido == 1:
        self.audio.reproducir_musica(self.audio.LEVEL1_MUSIC_FILES, "nivel 1")
    elif nivel_elegido == 2:
        self.audio.reproducir_musica(self.audio.LEVEL2_MUSIC_FILES, "nivel 2")
    elif nivel_elegido == 3:
        self.audio.reproducir_musica(self.audio.LEVEL3_MUSIC_FILES, "nivel 3")
    elif nivel_elegido == 4:
        self.audio.reproducir_musica(self.audio.LEVEL4_MUSIC_FILES, "nivel 4")
    elif nivel_elegido == 5:
        self.audio.reproducir_musica(self.audio.LEVEL5_MUSIC_FILES, "nivel 5")
    else:
        self.audio.reproducir_musica(self.audio.INTRO_MUSIC_FILES, f"nivel {nivel_elegido}")

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

    vida_max = 100
    vida_jugador = vida_max
    ultimo_golpe = 0
    invulnerabilidad_ms = 800

    boss_aparecio = False
    boss_activo = False
    boss_hp = 8
    boss_rect = pygame.Rect(variables.ANCHO // 2 - 65, 40, 130, 130)
    boss_dir = 4
    boss_balas = []
    boss_bala_w, boss_bala_h = 8, 18
    boss_bala_speed = 7
    boss_cooldown = 900
    ultimo_disparo_boss = 0

    final_boss_aparecio = False
    final_boss_activo = False
    final_boss_hp = 15
    final_boss_rect = pygame.Rect(variables.ANCHO // 2 - 90, 30, 180, 180)
    final_boss_dir = 5
    final_boss_balas = []
    final_boss_bala_w, final_boss_bala_h = 10, 22
    final_boss_bala_speed = 8
    final_boss_cooldown = 500
    ultimo_disparo_final_boss = 0

    while True:
        self.clock.tick(60)

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
            self.ventana.blit(self.recursos.background_image, (0, 0))

            mostrar_jugador = True
            if ahora - ultimo_golpe < invulnerabilidad_ms:
                if (ahora // 100) % 2 == 0:
                    mostrar_jugador = False

            if mostrar_jugador:
                self.ventana.blit(
                    self.recursos.player_image,
                    (personaje.Personaje.player.x, personaje.Personaje.player.y)
                )

            for meteor in meteoritos.meteors:
                self.ventana.blit(self.recursos.meteor_image, (meteor.x, meteor.y))

            for e in enemigos.enemies:
                if e.tipo == "grande":
                    self.ventana.blit(self.recursos.enemy_big_image, (e.rect.x, e.rect.y))
                else:
                    self.ventana.blit(self.recursos.enemy_image, (e.rect.x, e.rect.y))

            if boss_activo and boss_hp > 0:
                self.ventana.blit(self.recursos.enemy_shooter_image, (boss_rect.x, boss_rect.y))

            if final_boss_activo and final_boss_hp > 0:
                self.ventana.blit(self.recursos.enemy_shooter_image, (final_boss_rect.x, final_boss_rect.y))

            for b in balas:
                pygame.draw.rect(self.ventana, (255, 220, 80), b)

            for bb in boss_balas:
                pygame.draw.rect(self.ventana, (255, 60, 60), bb)

            for fb in final_boss_balas:
                pygame.draw.rect(self.ventana, (255, 0, 0), fb["rect"])

            pausa_text = variables.font.render(
                "Juego pausado - Presiona P para continuar",
                True,
                (255, 255, 255),
            )
            text_rect = pausa_text.get_rect(center=(variables.ANCHO // 2, variables.ALTO // 2))
            self.ventana.blit(pausa_text, text_rect)
            pygame.display.flip()
            continue

        if nivel_elegido == 4 and variables.puntuacion >= 400 and not boss_aparecio:
            boss_aparecio = True
            boss_activo = True
            meteoritos.meteors.clear()
            enemigos.enemies.clear()

        if nivel_elegido == 5 and variables.puntuacion >= 600 and not final_boss_aparecio:
            final_boss_aparecio = True
            final_boss_activo = True
            meteoritos.meteors.clear()
            enemigos.enemies.clear()

        if not final_boss_activo and not boss_activo:
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

        for b in balas[:]:
            b.y -= bala_speed
            if b.bottom < 0:
                balas.remove(b)

        for meteor in meteoritos.meteors[:]:
            meteor.y += velocidad_meteoritos
            if meteor.top > variables.ALTO:
                meteoritos.meteors.remove(meteor)
                variables.puntuacion += 10

        for e in enemigos.enemies[:]:
            e.update()
            if e.rect.top > variables.ALTO:
                enemigos.enemies.remove(e)

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

        for meteor in meteoritos.meteors[:]:
            if personaje.Personaje.hitbox.colliderect(meteor):
                if ahora - ultimo_golpe >= invulnerabilidad_ms:
                    vida_jugador -= 20
                    ultimo_golpe = ahora
                    if meteor in meteoritos.meteors:
                        meteoritos.meteors.remove(meteor)

                    if vida_jugador <= 0:
                        return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

        for e in enemigos.enemies[:]:
            if personaje.Personaje.hitbox.colliderect(e.rect):
                if ahora - ultimo_golpe >= invulnerabilidad_ms:
                    vida_jugador -= 25
                    ultimo_golpe = ahora
                    if e in enemigos.enemies:
                        enemigos.enemies.remove(e)

                    if vida_jugador <= 0:
                        return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

        if boss_activo and boss_hp > 0 and personaje.Personaje.hitbox.colliderect(boss_rect):
            if ahora - ultimo_golpe >= invulnerabilidad_ms:
                vida_jugador -= 35
                ultimo_golpe = ahora
                if vida_jugador <= 0:
                    return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

        for bb in boss_balas[:]:
            if personaje.Personaje.hitbox.colliderect(bb):
                if ahora - ultimo_golpe >= invulnerabilidad_ms:
                    vida_jugador -= 15
                    ultimo_golpe = ahora
                    if bb in boss_balas:
                        boss_balas.remove(bb)

                    if vida_jugador <= 0:
                        return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

        if final_boss_activo and final_boss_hp > 0 and personaje.Personaje.hitbox.colliderect(final_boss_rect):
            if ahora - ultimo_golpe >= invulnerabilidad_ms:
                vida_jugador -= 40
                ultimo_golpe = ahora
                if vida_jugador <= 0:
                    return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

        for fb in final_boss_balas[:]:
            if personaje.Personaje.hitbox.colliderect(fb["rect"]):
                if ahora - ultimo_golpe >= invulnerabilidad_ms:
                    vida_jugador -= 20
                    ultimo_golpe = ahora
                    if fb in final_boss_balas:
                        final_boss_balas.remove(fb)

                    if vida_jugador <= 0:
                        return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

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

        if nivel_elegido == 4:
            if boss_aparecio and not boss_activo:
                return self.pantallas.pantalla_victoria(nivel_elegido, variables.puntuacion)
        elif nivel_elegido == 5:
            if final_boss_aparecio and not final_boss_activo:
                return self.pantallas.pantalla_victoria(nivel_elegido, variables.puntuacion)
        else:
            if variables.puntuacion >= objetivo_puntos:
                return self.pantallas.pantalla_victoria(nivel_elegido, variables.puntuacion)

        self.ventana.blit(self.recursos.background_image, (0, 0))

        mostrar_jugador = True
        if ahora - ultimo_golpe < invulnerabilidad_ms:
            if (ahora // 100) % 2 == 0:
                mostrar_jugador = False

        if mostrar_jugador:
            self.ventana.blit(
                self.recursos.player_image,
                (personaje.Personaje.player.x, personaje.Personaje.player.y)
            )

        for meteor in meteoritos.meteors:
            self.ventana.blit(self.recursos.meteor_image, (meteor.x, meteor.y))

        for e in enemigos.enemies:
            if e.tipo == "grande":
                self.ventana.blit(self.recursos.enemy_big_image, (e.rect.x, e.rect.y))
            else:
                self.ventana.blit(self.recursos.enemy_image, (e.rect.x, e.rect.y))

        if boss_activo and boss_hp > 0:
            self.ventana.blit(self.recursos.enemy_shooter_image, (boss_rect.x, boss_rect.y))

        if final_boss_activo and final_boss_hp > 0:
            self.ventana.blit(self.recursos.enemy_shooter_image, (final_boss_rect.x, final_boss_rect.y))

        for b in balas:
            pygame.draw.rect(self.ventana, (255, 220, 80), b)

        for bb in boss_balas:
            pygame.draw.rect(self.ventana, (255, 60, 60), bb)

        for fb in final_boss_balas:
            pygame.draw.rect(self.ventana, (255, 0, 0), fb["rect"])

        if nivel_elegido == 4:
            if not boss_aparecio:
                progreso_texto = f"Puntuacion: {variables.puntuacion}/400"
            else:
                progreso_texto = f"Puntuacion: {variables.puntuacion} - Boss"
        elif nivel_elegido == 5:
            if not final_boss_aparecio:
                progreso_texto = f"Puntuacion: {variables.puntuacion}/600"
            else:
                progreso_texto = f"Puntuacion: {variables.puntuacion} - Final Boss"
        else:
            progreso_texto = f"Puntuacion: {variables.puntuacion}/{objetivo_puntos}"

        progreso_render = variables.font.render(progreso_texto, True, self.WHITE)
        self.ventana.blit(progreso_render, (10, 10))

        nivel_text = variables.font.render(f"Nivel: {nivel_elegido}", True, self.WHITE)
        self.ventana.blit(nivel_text, (10, 45))

        vida_text = variables.font.render(
            f"Vida: {vida_jugador}/{vida_max}", True, self.WHITE
        )
        self.ventana.blit(vida_text, (10, 80))

        self.pantallas.dibujar_barra_vida(self.ventana, 10, 115, vida_jugador, vida_max)

        pausa_info = variables.font.render("P para pausar", True, self.WHITE)
        self.ventana.blit(pausa_info, (10, 150))

        if boss_activo and boss_hp > 0:
            boss_text = variables.font.render(f"Boss HP: {boss_hp}", True, self.WHITE)
            self.ventana.blit(boss_text, (10, 185))

        if final_boss_activo and final_boss_hp > 0:
            final_boss_text = variables.font.render(
                f"Final Boss HP: {final_boss_hp}", True, self.WHITE
            )
            self.ventana.blit(final_boss_text, (10, 220))

        pygame.display.flip()