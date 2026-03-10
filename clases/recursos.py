import pygame

try:
    from clases import personaje, meteoritos
except ModuleNotFoundError:
    import clases.personaje as personaje
    import clases.meteoritos as meteoritos


class Recursos:
    def __init__(self):
        self.player_image = None
        self.meteor_image = None
        self.background_image = None
        self.enemy_image = None
        self.enemy_big_image = None
        self.title_image = None
        self.enemy_shooter_image = None
        self.victory_image = None
        self.game_over_image = None

        self.font_subtitulo = None
        self.font_nivel = None
        self.font_boton = None
        self.font_victoria_titulo = None
        self.font_victoria_info = None
        self.font_victoria_small = None

        self.cargar_imagenes()
        self.cargar_fuentes()

    def escalar_cuadrado(self, image, side):
        width, height = image.get_size()
        base = min(width, height)
        x = (width - base) // 2
        y = (height - base) // 2
        square = image.subsurface((x, y, base, base)).copy()
        return pygame.transform.smoothscale(square, (side, side))

    def cargar_imagenes(self):
        from clases import variables

        player_image = pygame.image.load("assets/milenario.png").convert_alpha()
        meteor_image = pygame.image.load("assets/meteorito.png").convert_alpha()
        background_image = pygame.image.load("assets/fondo.jpg").convert()
        enemy_base_image = pygame.image.load("assets/enemigo.png").convert_alpha()
        enemy_big_base_image = pygame.image.load("assets/enemigo2.png").convert_alpha()
        title_image = pygame.image.load("assets/titulo.png").convert_alpha()
        enemy_shooter_image = pygame.image.load("assets/boss.png").convert_alpha()

        victory_image = None
        try:
            victory_image = pygame.image.load("assets/victoria.png").convert_alpha()
            victory_image = pygame.transform.smoothscale(victory_image, (400, 200))
        except Exception as e:
            print("No se pudo cargar assets/victoria.png:", e)

        game_over_image = None
        try:
            game_over_image = pygame.image.load("assets/game_over.png").convert_alpha()
            game_over_image = pygame.transform.smoothscale(game_over_image, (400, 200))
        except Exception as e:
            print("No se pudo cargar assets/game_over.png:", e)

        background_image = pygame.transform.smoothscale(
            background_image, (variables.ANCHO, variables.ALTO)
        )

        self.player_image = self.escalar_cuadrado(
            player_image, personaje.Personaje.player_width
        )
        self.meteor_image = self.escalar_cuadrado(
            meteor_image, meteoritos.meteor_width
        )
        self.enemy_image = self.escalar_cuadrado(enemy_base_image, 60)
        self.enemy_big_image = self.escalar_cuadrado(enemy_big_base_image, 95)
        self.enemy_shooter_image = self.escalar_cuadrado(enemy_shooter_image, 130)
        self.title_image = pygame.transform.smoothscale(title_image, (1000, 350))

        self.victory_image = victory_image
        self.game_over_image = game_over_image
        self.background_image = background_image

    def cargar_fuentes(self):
        self.font_subtitulo = pygame.font.SysFont("arial", 32, bold=True)
        self.font_nivel = pygame.font.SysFont("arial", 28, bold=True)
        self.font_boton = pygame.font.SysFont("arial", 34, bold=True)
        self.font_victoria_titulo = pygame.font.SysFont("arial", 40, bold=True)
        self.font_victoria_info = pygame.font.SysFont("arial", 36, bold=True)
        self.font_victoria_small = pygame.font.SysFont("arial", 20, bold=True)