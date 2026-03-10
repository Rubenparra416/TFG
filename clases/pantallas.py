import pygame

try:
    from clases import variables
except ModuleNotFoundError:
    import clases.variables as variables


class Pantallas:
    def __init__(self, ventana, clock, recursos, audio):
        self.ventana = ventana
        self.clock = clock
        self.recursos = recursos
        self.audio = audio
        self.WHITE = getattr(variables, "WHITE", (255, 255, 255))

    def dibujar_barra_vida(self, surface, x, y, vida, vida_max, ancho=220, alto=22):
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

    def desbloquear_siguiente_nivel(self, nivel_completado):
        if (
            nivel_completado == variables.nivel_desbloqueado
            and nivel_completado < variables.MAX_NIVELES
        ):
            variables.nivel_desbloqueado += 1

    def pantalla_inicio(self):
        self.audio.reproducir_musica(self.audio.INTRO_MUSIC_FILES, "intro")

        niveles = [1, 2, 3, 4, 5]
        nivel_seleccionado = 0

        boton_jugar = pygame.Rect(variables.ANCHO // 2 - 100, 560, 200, 60)
        rects_niveles = []

        while True:
            self.clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            self.ventana.blit(self.recursos.background_image, (0, 0))

            overlay = pygame.Surface((variables.ANCHO, variables.ALTO), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            self.ventana.blit(overlay, (0, 0))

            self.ventana.blit(
                self.recursos.title_image,
                (variables.ANCHO // 2 - self.recursos.title_image.get_width() // 2, -50)
            )

            subtitulo = self.recursos.font_subtitulo.render(
                "Selecciona un nivel", True, (255, 220, 80)
            )
            self.ventana.blit(
                subtitulo,
                (variables.ANCHO // 2 - subtitulo.get_width() // 2, 220)
            )

            info_bloqueo = self.recursos.font_nivel.render(
                f"Nivel maximo desbloqueado: {variables.nivel_desbloqueado}",
                True,
                (230, 230, 230)
            )
            self.ventana.blit(
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

                pygame.draw.rect(self.ventana, color_fondo, rect, border_radius=8)
                pygame.draw.rect(self.ventana, (255, 255, 255), rect, 2, border_radius=8)

                texto_nivel = self.recursos.font_nivel.render(f"Nivel {nivel}", True, color_texto)
                self.ventana.blit(
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

            pygame.draw.rect(self.ventana, color_boton, boton_jugar, border_radius=10)
            pygame.draw.rect(self.ventana, (255, 255, 255), boton_jugar, 2, border_radius=10)

            texto_jugar = self.recursos.font_boton.render("JUGAR", True, (255, 255, 255))
            self.ventana.blit(
                texto_jugar,
                (
                    boton_jugar.centerx - texto_jugar.get_width() // 2,
                    boton_jugar.centery - texto_jugar.get_height() // 2,
                ),
            )

            instrucciones = self.recursos.font_nivel.render(
                "Usa flechas ↑ ↓ o haz clic", True, (230, 230, 230)
            )
            self.ventana.blit(
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

    def pantalla_game_over(self, nivel, puntuacion):
        font_info = pygame.font.SysFont("arial", 30, bold=True)
        font_small = pygame.font.SysFont("arial", 24, bold=True)

        self.audio.reproducir_musica(self.audio.GAME_OVER_MUSIC_FILES, "game over")

        while True:
            self.clock.tick(60)

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

            self.ventana.blit(self.recursos.background_image, (0, 0))

            overlay = pygame.Surface((variables.ANCHO, variables.ALTO), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.ventana.blit(overlay, (0, 0))

            if self.recursos.game_over_image is not None:
                self.ventana.blit(
                    self.recursos.game_over_image,
                    (
                        variables.ANCHO // 2 - self.recursos.game_over_image.get_width() // 2,
                        70,
                    ),
                )
            else:
                font_game_over = pygame.font.SysFont("arial", 70, bold=True)
                texto_go = font_game_over.render("GAME OVER", True, (255, 60, 60))
                self.ventana.blit(
                    texto_go,
                    (variables.ANCHO // 2 - texto_go.get_width() // 2, 100),
                )

            panel_width = 700
            panel_height = 340
            panel_x = variables.ANCHO // 2 - panel_width // 2
            panel_y = 240

            panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            panel.fill((20, 10, 10, 185))
            self.ventana.blit(panel, (panel_x, panel_y))

            pygame.draw.rect(
                self.ventana,
                (255, 80, 80),
                (panel_x, panel_y, panel_width, panel_height),
                3,
                border_radius=18
            )

            pygame.draw.rect(
                self.ventana,
                (255, 255, 255),
                (panel_x + 8, panel_y + 8, panel_width - 16, panel_height - 16),
                1,
                border_radius=14
            )

            texto_imperio = font_info.render("Ha ganado el Imperio", True, (255, 220, 80))
            self.ventana.blit(
                texto_imperio,
                (variables.ANCHO // 2 - texto_imperio.get_width() // 2, panel_y + 40),
            )

            texto_puntos = font_info.render(
                f"Puntuacion final: {puntuacion}", True, (255, 255, 255)
            )
            self.ventana.blit(
                texto_puntos,
                (variables.ANCHO // 2 - texto_puntos.get_width() // 2, panel_y + 95),
            )

            texto_nivel = font_info.render(
                f"Nivel jugado: {nivel}", True, (230, 230, 255)
            )
            self.ventana.blit(
                texto_nivel,
                (variables.ANCHO // 2 - texto_nivel.get_width() // 2, panel_y + 145),
            )

            texto_reiniciar = font_small.render(
                "Pulsa R para repetir el nivel", True, (255, 220, 80)
            )
            self.ventana.blit(
                texto_reiniciar,
                (variables.ANCHO // 2 - texto_reiniciar.get_width() // 2, panel_y + 215),
            )

            texto_menu = font_small.render(
                "Pulsa cualquier otra tecla para volver al menu",
                True,
                (220, 220, 220),
            )
            self.ventana.blit(
                texto_menu,
                (variables.ANCHO // 2 - texto_menu.get_width() // 2, panel_y + 255),
            )

            texto_salir = font_small.render(
                "Pulsa ESC para salir", True, (220, 220, 220)
            )
            self.ventana.blit(
                texto_salir,
                (variables.ANCHO // 2 - texto_salir.get_width() // 2, panel_y + 295),
            )

            pygame.display.flip()

    def pantalla_victoria(self, nivel, puntuacion):
        self.desbloquear_siguiente_nivel(nivel)
        self.audio.reproducir_musica(self.audio.VICTORY_MUSIC_FILES, "victoria")

        while True:
            self.clock.tick(60)

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

            self.ventana.blit(self.recursos.background_image, (0, 0))

            overlay = pygame.Surface((variables.ANCHO, variables.ALTO), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            self.ventana.blit(overlay, (0, 0))

            if self.recursos.victory_image is not None:
                self.ventana.blit(
                    self.recursos.victory_image,
                    (variables.ANCHO // 2 - self.recursos.victory_image.get_width() // 2, 50),
                )
            else:
                texto_win = self.recursos.font_victoria_titulo.render(
                    "NIVEL COMPLETADO", True, (80, 255, 120)
                )
                self.ventana.blit(
                    texto_win,
                    (variables.ANCHO // 2 - texto_win.get_width() // 2, 100),
                )

            panel_width = 700
            panel_height = 360
            panel_x = variables.ANCHO // 2 - panel_width // 2
            panel_y = 235

            panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            panel.fill((15, 15, 25, 185))
            self.ventana.blit(panel, (panel_x, panel_y))

            pygame.draw.rect(
                self.ventana,
                (255, 220, 80),
                (panel_x, panel_y, panel_width, panel_height),
                3,
                border_radius=18
            )

            pygame.draw.rect(
                self.ventana,
                (255, 255, 255),
                (panel_x + 8, panel_y + 8, panel_width - 16, panel_height - 16),
                1,
                border_radius=14
            )

            texto_puntos = self.recursos.font_victoria_info.render(
                f"Puntuacion final: {puntuacion}", True, (255, 255, 255)
            )
            self.ventana.blit(
                texto_puntos,
                (variables.ANCHO // 2 - texto_puntos.get_width() // 2, panel_y + 45),
            )

            texto_nivel = self.recursos.font_victoria_info.render(
                f"Nivel actual: {nivel}", True, (230, 230, 255)
            )
            self.ventana.blit(
                texto_nivel,
                (variables.ANCHO // 2 - texto_nivel.get_width() // 2, panel_y + 95),
            )

            if nivel < variables.MAX_NIVELES:
                texto_desbloqueado = self.recursos.font_victoria_info.render(
                    f"Has desbloqueado el nivel {min(nivel + 1, variables.MAX_NIVELES)}",
                    True,
                    (255, 220, 80)
                )
                self.ventana.blit(
                    texto_desbloqueado,
                    (
                        variables.ANCHO // 2 - texto_desbloqueado.get_width() // 2,
                        panel_y + 160,
                    ),
                )

                texto_siguiente = self.recursos.font_victoria_small.render(
                    "Pulsa N para pasar al siguiente nivel",
                    True,
                    (255, 220, 80)
                )
                self.ventana.blit(
                    texto_siguiente,
                    (
                        variables.ANCHO // 2 - texto_siguiente.get_width() // 2,
                        panel_y + 225,
                    ),
                )
            else:
                texto_fin = self.recursos.font_victoria_small.render(
                    "Has completado toda la aventura galactica",
                    True,
                    (255, 220, 80)
                )
                self.ventana.blit(
                    texto_fin,
                    (
                        variables.ANCHO // 2 - texto_fin.get_width() // 2,
                        panel_y + 225,
                    ),
                )

            texto_reiniciar = self.recursos.font_victoria_small.render(
                "Pulsa R para repetir este nivel",
                True,
                (220, 220, 220)
            )
            self.ventana.blit(
                texto_reiniciar,
                (
                    variables.ANCHO // 2 - texto_reiniciar.get_width() // 2,
                    panel_y + 275,
                ),
            )

            texto_salir = self.recursos.font_victoria_small.render(
                "Pulsa ESC para salir",
                True,
                (220, 220, 220)
            )
            self.ventana.blit(
                texto_salir,
                (
                    variables.ANCHO // 2 - texto_salir.get_width() // 2,
                    panel_y + 315,
                ),
            )

            pygame.display.flip()