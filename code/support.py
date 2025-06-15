import io

import pygame
import os
import sys
import random
from datetime import datetime
import sqlite3
from time import sleep

version = 0.2


def get_data():
    global SCALE
    try:
        with open(r'../data/scale.txt', 'r', encoding='utf8') as file:
            data = file.readline()
            SCALE = float(data)
    except io.UnsupportedOperation:
        print('Не удалось открыть текстовый файл с данными, возможно, он пуст')
        SCALE = 1


get_data()

SCALE = SCALE

FPS = 60
SIZE = WIDTH, HEIGHT = 1200 * SCALE, 800 * SCALE
WIDTH2, HEIGHT2 = HEIGHT, HEIGHT


intro_text = [
    "ТРЕНИРОВКА",
    "КАМПАНИЯ",
    "МАГАЗИН"
    # "СОЗДАТЬ УРОВЕНЬ",
    # "НАСТРОЙКИ",
    # "ПОМОЩЬ"
]


tile_images_paths = {
    'wall': (
        r'../data/images/object_images/metal_box/metal_box.png',
        r'../data/images/object_images/metal_box/metal_box1.png',
    ),
    'sand': (
        r'../data/images/object_images/sand/sand1.png',
        r'../data/images/object_images/sand/sand2.png',
        r'../data/images/object_images/sand/sand3.png'
    )
}

game_background = r'../data/images/game_background.png'
bullet_image = r'../data/images/bullet.png'
explosion_image = r'../data/images/explosion.png'
shop_background = r'../data/images/shop_background.jpg'


TILE_SIZE = int(50 * SCALE)
VELOCITY = TILE_SIZE / FPS * SCALE


directions = ['N', 'S', 'W', 'E']

GAME_NAME = "TANK BATTLES"

MAIN_FONT = '../data/fonts/ft40.ttf'

# COLORS
BG_COLOR = "#231E21"
TITLE_COLOR = "#F9F9F9"
GREEN_COLOR = "#0EB23C"
GRAY_COLOR = "#B7B7B5"
DARK_GRAY_COLOR = "#939392"