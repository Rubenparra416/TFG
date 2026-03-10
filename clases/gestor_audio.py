import pygame
from pathlib import Path


class GestorAudio:
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

    LEVEL2_MUSIC_FILES = [
        "assets/nivel2.ogg",
        "assets/musica/nivel2.mp3",
        "assets/level2.ogg",
        "assets/level2.mp3",
        "assets/musica/nivel2.ogg",
        "assets/musica/nivel1.mp3",
    ]

    LEVEL3_MUSIC_FILES = [
        "assets/nivel3.ogg",
        "assets/musica/nivel3.mp3",
        "assets/level3.ogg",
        "assets/level3.mp3",
        "assets/musica/nivel3.ogg",
        "assets/musica/nivel3.mp3",
    ]
    LEVEL4_MUSIC_FILES = [
        "assets/nivel4.ogg",
        "assets/musica/nivel4.mp3",
        "assets/level4.ogg",
        "assets/level4.mp3",
        "assets/musica/nivel4.ogg",
        "assets/musica/nivel4.mp3",
    ] 
    
    LEVEL5_MUSIC_FILES = [
        "assets/nivel5.ogg",
        "assets/musica/nivel5.mp3",
        "assets/level5.ogg",
        "assets/level5.mp3",
        "assets/musica/nivel5.ogg",
        "assets/musica/nivel5.mp3",
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

    def reproducir_musica(self, files, nombre, volume=0.35):
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