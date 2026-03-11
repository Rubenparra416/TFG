import pygame


class MissionManager:
    def __init__(self, font, color=(255, 255, 255)):
        self.font = font
        self.color = color
        self.misiones = []
        self.progreso = {}

    def cargar_nivel(self, nivel):
        self.misiones = self.crear_misiones_nivel(nivel)
        self.progreso = {
            "enemigos": 0,
            "powerups": 0,
            "golpes": 0,
            "segundos": 0,
        }

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

    def sumar(self, clave, cantidad=1):
        if clave in self.progreso:
            self.progreso[clave] += cantidad

    def set_valor(self, clave, valor):
        if clave in self.progreso:
            self.progreso[clave] = valor

    def mision_cumplida(self, mision, vida_jugador, puntuacion):
        mid = mision["id"]
        objetivo = mision["objetivo"]

        if mid == "enemigos":
            return self.progreso["enemigos"] >= objetivo
        elif mid == "powerups":
            return self.progreso["powerups"] >= objetivo
        elif mid == "sin_muchos_golpes":
            return self.progreso["golpes"] <= objetivo
        elif mid == "puntos":
            return puntuacion >= objetivo
        elif mid == "supervivencia":
            return self.progreso["segundos"] >= objetivo
        elif mid == "vida_final":
            return vida_jugador >= objetivo

        return False

    def todas_completadas(self, vida_jugador, puntuacion):
        for mision in self.misiones:
            if not self.mision_cumplida(mision, vida_jugador, puntuacion):
                return False
        return True

    def dibujar(self, ventana, vida_jugador, puntuacion, x=10, y=255):
        titulo = self.font.render("Misiones:", True, self.color)
        ventana.blit(titulo, (x, y))

        y_actual = y + 30

        for mision in self.misiones:
            cumplida = self.mision_cumplida(mision, vida_jugador, puntuacion)
            prefijo = "[OK]" if cumplida else "[ ]"

            mid = mision["id"]
            objetivo = mision["objetivo"]

            if mid == "enemigos":
                texto = f"{prefijo} {mision['texto']} ({self.progreso['enemigos']}/{objetivo})"
            elif mid == "powerups":
                texto = f"{prefijo} {mision['texto']} ({self.progreso['powerups']}/{objetivo})"
            elif mid == "sin_muchos_golpes":
                texto = f"{prefijo} {mision['texto']} ({self.progreso['golpes']}/{objetivo})"
            elif mid == "puntos":
                texto = f"{prefijo} {mision['texto']} ({puntuacion}/{objetivo})"
            elif mid == "supervivencia":
                texto = f"{prefijo} {mision['texto']} ({self.progreso['segundos']}/{objetivo})"
            elif mid == "vida_final":
                texto = f"{prefijo} {mision['texto']} ({vida_jugador}/{objetivo})"
            else:
                texto = f"{prefijo} {mision['texto']}"

            render = self.font.render(texto, True, self.color)
            ventana.blit(render, (x, y_actual))
            y_actual += 28