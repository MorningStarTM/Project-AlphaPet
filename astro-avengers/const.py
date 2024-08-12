import pygame
import os
from glob import glob


SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 1000


def scale_image(path, factor):
    image = pygame.image.load(path)
    new_width = int(image.get_width() * 0.35)  # Scale to 50% of original width
    new_height = int(image.get_height() * 0.35)  # Scale to 50% of original height
    return pygame.transform.scale(image, (new_width, new_height))


PLAYER_IMAGE = scale_image("assets\\Player_1\\ship_2.png", 0.3)

ENEMY_FLIGHT_IMAGE = pygame.image.load("assets\\enemy_1\\Turret09.png")

DECEPTICON_IMAGE = scale_image("assets\\enemy_1\\eship1.png", 0.3)



SCRAPPER_IMAGE = scale_image("assets\\colony\\B13.png", 0.3)

BULLET_IMAGE = pygame.image.load("assets\\bullet\\basicBullet.png")
MISSILE_IMAGE = pygame.image.load("assets\\bullet\\P05.png")
BLUE_BULLET_IMAGE = pygame.image.load("assets\\bullet\\bule_bullet.png")
GOLDEN_BULLET_IMAGE = pygame.image.load("assets\\bullet\\bullets_golden.png")

SHIELD_IMAGE = pygame.image.load("assets\\GLA\\shield.png")
LIFE_IMAGE = pygame.image.load("assets\\GLA\\ammunition.png")
AMMUNITION_IMAGE = pygame.image.load("assets\\GLA\\life.png")


HUD_WIDTH = 200  # Width of the HUD section

# Colors
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)


LIST_OF_EXPLOSION_IMAGE = [pygame.image.load(i) for i in glob("E:\\github_clone\\Project-AlphaPet\\astro-avengers\\assets\\explosion\\*")]




LEFT_SEGMENT = pygame.Rect(0, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT-100)
CENTER_SEGMENT = pygame.Rect(SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT-100)
RIGHT_SEGMENT = pygame.Rect(2 * SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT-100)

SEGMENTS = [LEFT_SEGMENT, CENTER_SEGMENT, RIGHT_SEGMENT]