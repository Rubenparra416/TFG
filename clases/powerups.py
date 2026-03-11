import random
import pygame


class PowerUpManager:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

        self.defs = {
            "speed": {
                "label": "Velocidad +",
                "duracion_ms": 9000,
                "color": (90, 220, 255),
                "letter": "V",
            },
            "double": {
                "label": "Doble disparo",
                "duracion_ms": 9000,
                "color": (120, 255, 120),
                "letter": "D",
            },
            "chaos": {
                "label": "Disparo caotico",
                "duracion_ms": 7000,
                "color": (255, 160, 70),
                "letter": "C",
            },
        }

        self.items = []
        self.active_until = {
            "speed": 0,
            "double": 0,
            "chaos": 0,
        }
        self.ultimo_powerup = None

    def reset(self):
        self.items.clear()
        for key in self.active_until:
            self.active_until[key] = 0
        self.ultimo_powerup = None

    def is_active(self, kind, now_ticks):
        return self.active_until.get(kind, 0) > now_ticks

    def get_speed_bonus(self, now_ticks):
        return 3 if self.is_active("speed", now_ticks) else 0

    def try_spawn_from_enemy(self, enemy_rect, enemy_type="normal"):
        """
        Probabilidad de soltar powerup al destruir enemigo.
        """
        prob = 0.30 if enemy_type == "grande" else 0.18

        if random.random() > prob:
            return

        kind = random.choice(list(self.defs.keys()))

        rect = pygame.Rect(
            enemy_rect.centerx - 20,
            enemy_rect.centery - 20,
            40,
            40
        )

        self.items.append({
            "tipo": kind,
            "rect": rect,
            "speed": 2
        })

        print(f"PowerUp creado: {kind} en ({rect.x}, {rect.y})")

    def spawn_debug(self, kind="double"):
        """
        Crea un powerup para pruebas con la tecla O.
        """
        rect = pygame.Rect(self.ancho // 2 - 20, 100, 40, 40)
        self.items.append({
            "tipo": kind,
            "rect": rect,
            "speed": 2
        })
        print(f"PowerUp debug creado: {kind}")

    def update_and_collect(self, player_hitbox, now_ticks):
        for item in self.items[:]:
            item["rect"].y += item["speed"]

            if item["rect"].top > self.alto:
                self.items.remove(item)
                continue

            if player_hitbox.colliderect(item["rect"]):
                kind = item["tipo"]
                duracion = self.defs[kind]["duracion_ms"]
                self.active_until[kind] = max(self.active_until[kind], now_ticks) + duracion
                self.ultimo_powerup = kind
                self.items.remove(item)
                print("PowerUp recogido:", kind)

    def draw_items(self, surface):
        font = pygame.font.SysFont(None, 26)

        for item in self.items:
            tipo = item["tipo"]
            color = self.defs[tipo]["color"]
            letra = self.defs[tipo]["letter"]

            pygame.draw.ellipse(surface, color, item["rect"])
            pygame.draw.ellipse(surface, (255, 255, 255), item["rect"], 3)

            texto = font.render(letra, True, (0, 0, 0))
            texto_rect = texto.get_rect(center=item["rect"].center)
            surface.blit(texto, texto_rect)

    def draw_last_powerup_hud(self, surface, font, x, y, now_ticks):
        if self.ultimo_powerup is None:
            return

        restante_ms = self.active_until[self.ultimo_powerup] - now_ticks
        if restante_ms <= 0:
            return

        data = self.defs[self.ultimo_powerup]

        texto = font.render(
            f"PowerUp: {data['label']} ({restante_ms / 1000:.1f}s)",
            True,
            data["color"]
        )

        texto_rect = texto.get_rect(topright=(x, y))
        surface.blit(texto, texto_rect)

    def draw_debug_count(self, surface, font):
        texto = font.render(
            f"Powerups en pantalla: {len(self.items)}",
            True,
            (255, 0, 0)
        )
        surface.blit(texto, (10, 300))