import pygame
import random

try:
    from clases import personaje, variables, meteoritos, enemigos
    from clases.powerups import PowerUpManager
except ModuleNotFoundError:
    import clases.personaje as personaje
    import clases.variables as variables
    import clases.meteoritos as meteoritos
    import clases.enemigos as enemigos
    from clases.powerups import PowerUpManager


class Juego:
    def __init__(self, ventana, clock, recursos, audio, pantallas):
        self.ventana = ventana
        self.clock = clock
        self.recursos = recursos
        self.audio = audio
        self.pantallas = pantallas
        self.WHITE = getattr(variables, "WHITE", (255, 255, 255))

        self.powerups = PowerUpManager(variables.ANCHO, variables.ALTO)
        self.powerup_siguiente_nivel = None

    # ---------------------------------------------------------
    # MISIONES
    # ---------------------------------------------------------
    def crear_misiones_nivel(self, nivel):
     if nivel == 1:
        return [
            {"id": "enemigos", "texto": "Elimina 6 enemigos", "objetivo": 6},
            {"id": "vida_final", "texto": "Termina con al menos 40 de vida", "objetivo": 40},
            {"id": "puntos", "texto": "Consigue 180 puntos", "objetivo": 180},
        ]
     elif nivel == 2:
        return [
            {"id": "enemigos", "texto": "Elimina 8 enemigos", "objetivo": 8},
            {"id": "powerups", "texto": "Recoge 1 power-up", "objetivo": 1},
            {"id": "puntos", "texto": "Consigue 260 puntos", "objetivo": 260},
        ]
     elif nivel == 3:
        return [
            {"id": "enemigos", "texto": "Elimina 10 enemigos", "objetivo": 10},
            {"id": "sin_muchos_golpes", "texto": "Recibe como maximo 3 golpes", "objetivo": 3},
            {"id": "puntos", "texto": "Consigue 300 puntos", "objetivo": 300},
        ]
     elif nivel == 4:
        return [
            {"id": "enemigos", "texto": "Elimina 12 enemigos", "objetivo": 12},
            {"id": "supervivencia", "texto": "Sobrevive 45 segundos", "objetivo": 45},
            {"id": "vida_final", "texto": "Termina con al menos 35 de vida", "objetivo": 35},
        ]
     elif nivel == 5:
        return [
            {"id": "enemigos", "texto": "Elimina 14 enemigos", "objetivo": 14},
            {"id": "sin_muchos_golpes", "texto": "Recibe como maximo 4 golpes", "objetivo": 4},
            {"id": "puntos", "texto": "Consigue 500 puntos", "objetivo": 500},
        ]
     else:
        return []

    def iniciar_progreso_misiones(self):
        return {
            "enemigos": 0,
            "powerups": 0,
            "golpes": 0,
            "segundos": 0,
        }

    def mision_cumplida(self, mision, progreso, vida_jugador, puntuacion):
        mid = mision["id"]
        objetivo = mision["objetivo"]

        if mid == "meteoritos":
            return progreso["meteoritos"] >= objetivo
        elif mid == "enemigos":
            return progreso["enemigos"] >= objetivo
        elif mid == "powerups":
            return progreso["powerups"] >= objetivo
        elif mid == "sin_muchos_golpes":
            return progreso["golpes"] <= objetivo
        elif mid == "puntos":
            return puntuacion >= objetivo
        elif mid == "supervivencia":
            return progreso["segundos"] >= objetivo
        elif mid == "vida_final":
            return vida_jugador >= objetivo

        return False

    def todas_misiones_completadas(self, misiones, progreso, vida_jugador, puntuacion):
        for mision in misiones:
            if not self.mision_cumplida(mision, progreso, vida_jugador, puntuacion):
                return False
        return True

    def dibujar_misiones(self, misiones, progreso, vida_jugador, puntuacion, x=10, y=255):
     font_misiones = pygame.font.SysFont(None, 24)
     y_actual = y

     for mision in misiones:
        cumplida = self.mision_cumplida(mision, progreso, vida_jugador, puntuacion)
        prefijo = "[OK]" if cumplida else "[ ]"

        mid = mision["id"]
        objetivo = mision["objetivo"]

        if mid == "enemigos":
            texto = f"{prefijo} {mision['texto']} ({progreso['enemigos']}/{objetivo})"
        elif mid == "powerups":
            texto = f"{prefijo} {mision['texto']} ({progreso['powerups']}/{objetivo})"
        elif mid == "sin_muchos_golpes":
            texto = f"{prefijo} {mision['texto']} ({progreso['golpes']}/{objetivo})"
        elif mid == "puntos":
            texto = f"{prefijo} {mision['texto']} ({puntuacion}/{objetivo})"
        elif mid == "supervivencia":
            texto = f"{prefijo} {mision['texto']} ({progreso['segundos']}/{objetivo})"
        elif mid == "vida_final":
            texto = f"{prefijo} {mision['texto']} ({vida_jugador}/{objetivo})"
        else:
            texto = f"{prefijo} {mision['texto']}"

        render = font_misiones.render(texto, True, self.WHITE)
        self.ventana.blit(render, (x, y_actual))
        y_actual += 26

    # ---------------------------------------------------------
    # RECOMPENSA ENTRE NIVELES
    # ---------------------------------------------------------
    def pantalla_eleccion_powerup(self):
        opciones = [
            ("speed", "Velocidad +"),
            ("double", "Doble disparo"),
            ("chaos", "Disparo caotico"),
        ]

        seleccion = 0

        while True:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        seleccion = (seleccion - 1) % len(opciones)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        seleccion = (seleccion + 1) % len(opciones)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        return opciones[seleccion][0]
                    elif event.key == pygame.K_1:
                        return opciones[0][0]
                    elif event.key == pygame.K_2:
                        return opciones[1][0]
                    elif event.key == pygame.K_3:
                        return opciones[2][0]

            self.ventana.blit(self.recursos.background_image, (0, 0))

            titulo = variables.font.render("Has completado todas las misiones", True, self.WHITE)
            subtitulo = variables.font.render("Elige 1 power-up para el siguiente nivel", True, self.WHITE)

            self.ventana.blit(titulo, titulo.get_rect(center=(variables.ANCHO // 2, 120)))
            self.ventana.blit(subtitulo, subtitulo.get_rect(center=(variables.ANCHO // 2, 160)))

            ancho_caja = 220
            alto_caja = 90
            espacio = 30
            total_ancho = len(opciones) * ancho_caja + (len(opciones) - 1) * espacio
            inicio_x = (variables.ANCHO - total_ancho) // 2
            y = 250

            for i, (_, texto) in enumerate(opciones):
                x = inicio_x + i * (ancho_caja + espacio)
                rect = pygame.Rect(x, y, ancho_caja, alto_caja)

                color_borde = (255, 255, 0) if i == seleccion else (255, 255, 255)
                pygame.draw.rect(self.ventana, (20, 20, 40), rect)
                pygame.draw.rect(self.ventana, color_borde, rect, 3)

                numero = variables.font.render(f"{i+1}", True, self.WHITE)
                nombre = variables.font.render(texto, True, self.WHITE)

                self.ventana.blit(numero, numero.get_rect(center=(rect.centerx, rect.y + 20)))
                self.ventana.blit(nombre, nombre.get_rect(center=(rect.centerx, rect.y + 55)))

            ayuda = variables.font.render("Flechas o A/D para mover - Enter para elegir", True, self.WHITE)
            self.ventana.blit(ayuda, ayuda.get_rect(center=(variables.ANCHO // 2, 400)))

            pygame.display.flip()

    def aplicar_powerup_inicio_nivel(self, ahora):
        if self.powerup_siguiente_nivel is None:
            return

        if self.powerup_siguiente_nivel in self.powerups.active_until:
            self.powerups.active_until[self.powerup_siguiente_nivel] = ahora + self.powerups.defs[self.powerup_siguiente_nivel]["duracion_ms"]

        self.powerup_siguiente_nivel = None

    # ---------------------------------------------------------
    # JUEGO
    # ---------------------------------------------------------
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

        self.powerups.reset()

        ahora_inicio = pygame.time.get_ticks()
        self.aplicar_powerup_inicio_nivel(ahora_inicio)

        misiones = self.crear_misiones_nivel(nivel_elegido)
        progreso_misiones = self.iniciar_progreso_misiones()
        tiempo_inicio_nivel = pygame.time.get_ticks()

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
            ahora = pygame.time.get_ticks()
            escudo_activo = self.powerups.is_active("shield", ahora)
            progreso_misiones["segundos"] = (ahora - tiempo_inicio_nivel) // 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pausa = not pausa

                    elif event.key == pygame.K_o:
                        self.powerups.spawn_debug("double")

                    elif event.key == pygame.K_1:
                        self.powerups.spawn_debug("speed")
                    elif event.key == pygame.K_2:
                        self.powerups.spawn_debug("double")
                    elif event.key == pygame.K_3:
                        self.powerups.spawn_debug("chaos")
                    elif event.key == pygame.K_4:
                        self.powerups.spawn_debug("shield")

            keys = pygame.key.get_pressed()
            speed = personaje.Personaje.player_speed + self.powerups.get_speed_bonus(ahora)

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

            if not pausa:
                recogidos_antes = len(self.powerups.items)
                self.powerups.update_and_collect(personaje.Personaje.hitbox, ahora)
                recogidos_despues = len(self.powerups.items)

                if recogidos_despues < recogidos_antes:
                    progreso_misiones["powerups"] += 1

            if keys[pygame.K_SPACE] and (ahora - ultimo_disparo) >= cooldown_ms and not pausa:
                player = personaje.Personaje.player
                by = player.top - bala_h

                if self.powerups.is_active("chaos", ahora):
                    for dx in (-4, 0, 4):
                        bx = player.centerx - bala_w // 2
                        balas.append({
                            "rect": pygame.Rect(bx, by, bala_w, bala_h),
                            "vel_x": dx,
                            "vel_y": -bala_speed
                        })

                elif self.powerups.is_active("double", ahora):
                    balas.append({
                        "rect": pygame.Rect(player.centerx - 14, by, bala_w, bala_h),
                        "vel_x": 0,
                        "vel_y": -bala_speed
                    })
                    balas.append({
                        "rect": pygame.Rect(player.centerx + 8, by, bala_w, bala_h),
                        "vel_x": 0,
                        "vel_y": -bala_speed
                    })

                else:
                    bx = player.centerx - bala_w // 2
                    balas.append({
                        "rect": pygame.Rect(bx, by, bala_w, bala_h),
                        "vel_x": 0,
                        "vel_y": -bala_speed
                    })

                ultimo_disparo = ahora
            if pausa:
                self.ventana.blit(self.recursos.background_image, (0, 0))

                mostrar_jugador = True
                if ahora - ultimo_golpe < invulnerabilidad_ms and (ahora // 100) % 2 == 0:
                    mostrar_jugador = False

                if mostrar_jugador:
                    self.ventana.blit(
                        self.recursos.player_image,
                        (personaje.Personaje.player.x, personaje.Personaje.player.y)
                    )

                    if escudo_activo:
                        pygame.draw.circle(
                            self.ventana,
                            (120, 180, 255),
                            personaje.Personaje.player.center,
                            max(personaje.Personaje.player.width, personaje.Personaje.player.height) // 2 + 12,
                            3
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
                    pygame.draw.rect(self.ventana, (255, 220, 80), b["rect"])

                for bb in boss_balas:
                    pygame.draw.rect(self.ventana, (255, 60, 60), bb)

                for fb in final_boss_balas:
                    pygame.draw.rect(self.ventana, (255, 0, 0), fb["rect"])

                self.powerups.draw_items(self.ventana)

                pausa_text = variables.font.render(
                    "Juego pausado",
                    True,
                    (255, 255, 255),
                )
                text_rect = pausa_text.get_rect(center=(variables.ANCHO // 2, variables.ALTO // 2 - 80))
                self.ventana.blit(pausa_text, text_rect)

                info_text = variables.font.render(
                    "   ",
                    True,
                    (255, 255, 255),
                )
                info_rect = info_text.get_rect(center=(variables.ANCHO // 2, variables.ALTO // 2 - 40))
                self.ventana.blit(info_text, info_rect)

                panel_w = 760
                panel_h = 230
                panel_x = (variables.ANCHO - panel_w) // 2
                panel_y = (variables.ALTO - panel_h) // 2 + 70

                panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
                pygame.draw.rect(self.ventana, (15, 15, 35), panel_rect)
                pygame.draw.rect(self.ventana, (255, 255, 255), panel_rect, 3)

                font_misiones = pygame.font.SysFont(None, 24)
                titulo_misiones = variables.font.render("Misiones del nivel", True, self.WHITE)
                self.ventana.blit(titulo_misiones, (panel_x + 20, panel_y + 15))

                self.dibujar_misiones(
                    misiones,
                    progreso_misiones,
                    vida_jugador,
                    variables.puntuacion,
                    x=panel_x + 20,
                    y=panel_y + 75
                )

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
                b["rect"].x += b["vel_x"]
                b["rect"].y += b["vel_y"]

                if (
                    b["rect"].bottom < 0
                    or b["rect"].right < 0
                    or b["rect"].left > variables.ANCHO
                ):
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
                    if not escudo_activo and ahora - ultimo_golpe >= invulnerabilidad_ms:
                        vida_jugador -= 20
                        progreso_misiones["golpes"] += 1
                        ultimo_golpe = ahora
                        meteoritos.meteors.remove(meteor)

                        if vida_jugador <= 0:
                            return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

            for e in enemigos.enemies[:]:
                if personaje.Personaje.hitbox.colliderect(e.rect):
                    if not escudo_activo and ahora - ultimo_golpe >= invulnerabilidad_ms:
                        vida_jugador -= 25
                        progreso_misiones["golpes"] += 1
                        ultimo_golpe = ahora
                        enemigos.enemies.remove(e)

                        if vida_jugador <= 0:
                            return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

            if boss_activo and boss_hp > 0 and personaje.Personaje.hitbox.colliderect(boss_rect):
                if not escudo_activo and ahora - ultimo_golpe >= invulnerabilidad_ms:
                    vida_jugador -= 35
                    progreso_misiones["golpes"] += 1
                    ultimo_golpe = ahora
                    if vida_jugador <= 0:
                        return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

            for bb in boss_balas[:]:
                if personaje.Personaje.hitbox.colliderect(bb):
                    if not escudo_activo and ahora - ultimo_golpe >= invulnerabilidad_ms:
                        vida_jugador -= 15
                        progreso_misiones["golpes"] += 1
                        ultimo_golpe = ahora
                        boss_balas.remove(bb)

                        if vida_jugador <= 0:
                            return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

            if final_boss_activo and final_boss_hp > 0 and personaje.Personaje.hitbox.colliderect(final_boss_rect):
                if not escudo_activo and ahora - ultimo_golpe >= invulnerabilidad_ms:
                    vida_jugador -= 40
                    progreso_misiones["golpes"] += 1
                    ultimo_golpe = ahora
                    if vida_jugador <= 0:
                        return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

            for fb in final_boss_balas[:]:
                if personaje.Personaje.hitbox.colliderect(fb["rect"]):
                    if not escudo_activo and ahora - ultimo_golpe >= invulnerabilidad_ms:
                        vida_jugador -= 20
                        progreso_misiones["golpes"] += 1
                        ultimo_golpe = ahora
                        final_boss_balas.remove(fb)

                        if vida_jugador <= 0:
                            return self.pantallas.pantalla_game_over(nivel_elegido, variables.puntuacion)

            for b in balas[:]:
                hit = False

                for e in enemigos.enemies[:]:
                    if b["rect"].colliderect(e.rect):
                        e.hp -= 1
                        hit = True

                        if e.hp <= 0:
                            print("Enemigo destruido:", e.tipo, e.rect)
                            self.powerups.try_spawn_from_enemy(e.rect, e.tipo)
                            enemigos.enemies.remove(e)
                            progreso_misiones["enemigos"] += 1
                            variables.puntuacion += 60 if e.tipo == "grande" else 20

                        break

                if hit and b in balas:
                    balas.remove(b)

           

            if boss_activo and boss_hp > 0:
                for b in balas[:]:
                    if b["rect"].colliderect(boss_rect):
                        boss_hp -= 1
                        if b in balas:
                            balas.remove(b)

                        if boss_hp <= 0:
                            variables.puntuacion += 150
                            boss_activo = False
                        break

            if final_boss_activo and final_boss_hp > 0:
                for b in balas[:]:
                    if b["rect"].colliderect(final_boss_rect):
                        final_boss_hp -= 1
                        if b in balas:
                            balas.remove(b)

                        if final_boss_hp <= 0:
                            variables.puntuacion += 300
                            final_boss_activo = False
                        break

            nivel_superado = False

            if nivel_elegido == 4:
                if boss_aparecio and not boss_activo:
                    nivel_superado = True
            elif nivel_elegido == 5:
                if final_boss_aparecio and not final_boss_activo:
                    nivel_superado = True
            else:
                if variables.puntuacion >= objetivo_puntos:
                    nivel_superado = True

            if nivel_superado:
               if self.todas_misiones_completadas(misiones, progreso_misiones, vida_jugador, variables.puntuacion):
                self.powerup_siguiente_nivel = random.choice(["speed", "double", "chaos", "shield"])

                return self.pantallas.pantalla_victoria(nivel_elegido, variables.puntuacion)

            self.ventana.blit(self.recursos.background_image, (0, 0))

            mostrar_jugador = True
            if ahora - ultimo_golpe < invulnerabilidad_ms and (ahora // 100) % 2 == 0:
                mostrar_jugador = False

            if mostrar_jugador:
                self.ventana.blit(
                    self.recursos.player_image,
                    (personaje.Personaje.player.x, personaje.Personaje.player.y)
                )

                if escudo_activo:
                    pygame.draw.circle(
                        self.ventana,
                        (120, 180, 255),
                        personaje.Personaje.player.center,
                        max(personaje.Personaje.player.width, personaje.Personaje.player.height) // 2 + 12,
                        3
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
                pygame.draw.rect(self.ventana, (255, 220, 80), b["rect"])

            for bb in boss_balas:
                pygame.draw.rect(self.ventana, (255, 60, 60), bb)

            for fb in final_boss_balas:
                pygame.draw.rect(self.ventana, (255, 0, 0), fb["rect"])

            self.powerups.draw_items(self.ventana)

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


            if self.powerup_siguiente_nivel is not None:
                texto_bonus = variables.font.render(
                    f"Bonus siguiente nivel: {self.powerup_siguiente_nivel}",
                    True,
                    self.WHITE
                )
                self.ventana.blit(texto_bonus, (10, variables.ALTO - 40))

            pygame.display.flip()