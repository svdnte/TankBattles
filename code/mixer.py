import pygame.mixer

from support import *


pygame.mixer.music.set_volume(0.8)


def set_music(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)


def set_main_music():
    set_music("../data/sounds/music/main.mp3")


def set_battle_music():
    set_music("../data/sounds/music/battle.mp3")


def set_volume(volume: float):
    pygame.mixer.music.set_volume(volume)


btn_sound = pygame.mixer.Sound("../data/sounds/effects/button.mp3")
btn_sound.set_volume(0.3)
def play_button_sound():
    btn_sound.play()