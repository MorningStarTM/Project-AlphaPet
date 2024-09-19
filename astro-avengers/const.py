import pygame
import os
from glob import glob

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
TOTAL_SCREEN_WIDTH = 1200
GAME_SCREEN_WIDTH = 1000
HUD_WIDTH = 200


def scale_image(path, factor=0.3):
    image = pygame.image.load(path)
    new_width = int(image.get_width() * factor)  # Scale to 50% of original width
    new_height = int(image.get_height() * factor)  # Scale to 50% of original height
    return pygame.transform.scale(image, (new_width, new_height))


PLAYER_IMAGE = scale_image("assets\\Player_1\\ship_2.png", 0.25)
PET_IMAGE = "assets\\Player_1\\ship_1.png"

ENEMY_FLIGHT_IMAGE = scale_image("assets\\enemy_1\\Turret09.png", 1.0)

DECEPTICON_IMAGE = scale_image("assets\\enemy_1\\eship1.png", 0.3)
DOUBLER_IMAGE = scale_image("assets\\enemy_1\\Turret07.png", 0.9)

WHITE_WALKER = scale_image("assets\\enemy_1\\white_walker.png", 0.5)
DIAMOND_HEAD = scale_image("assets\\enemy_1\\diamond_head.png", 0.5)
LASERER = scale_image("assets\\enemy_1\\laserer.png", 0.5)
FX100 = scale_image("assets\\enemy_1\\fx100.png", 0.3)
STR = scale_image("assets\\enemy_1\\str.png", 0.5)


SCRAPPER_IMAGE = scale_image("assets\\colony\\B13.png", 0.3)

BULLET_IMAGE = scale_image("assets\\bullet\\basicBullet.png",1.3)
DOUBLE_BULLET_IMAGE = pygame.image.load("assets\\bullet\\bullets_golden.png")
MISSILE_IMAGE = pygame.image.load("assets\\bullet\\P05.png")
ARC_MISSILE_IMAGE = pygame.image.load("assets\\bullet\\P03.png")
BLUE_BULLET_IMAGE = pygame.image.load("assets\\bullet\\bule_bullet.png")
GOLDEN_BULLET_IMAGE = pygame.image.load("assets\\bullet\\game.png")
ICE_BULLET = pygame.image.load("assets\\bullet\\ice.png")
ANIMATED_BULLET_IMAGES = [pygame.image.load('assets\\bullet\\a1.png'),
                        pygame.image.load('assets\\bullet\\a2.png'),
                        pygame.image.load('assets\\bullet\\a3.png')]

SHIELD_IMAGE = pygame.image.load("assets\\GLA\\shield.png")
LIFE_IMAGE = pygame.image.load("assets\\GLA\\ammunition.png")
AMMUNITION_IMAGE = pygame.image.load("assets\\GLA\\life.png")


HUD_WIDTH = 200  # Width of the HUD section

# Colors
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)
YELLOW = (192, 230, 28)
LASER_COLOR = (232, 81, 94)
ICE_LASER_COLOR = (160, 151, 219)
YELLOW_LASER = (217, 120, 17)

LIST_OF_EXPLOSION_IMAGE = [pygame.image.load(i) for i in glob("E:\\github_clone\\Project-AlphaPet\\astro-avengers\\assets\\explosion\\*")]


WAVE_COLOR = (179, 131, 2)

LEFT_SEGMENT = pygame.Rect(0, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT-100)
CENTER_SEGMENT = pygame.Rect(SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT-100)
RIGHT_SEGMENT = pygame.Rect(2 * SCREEN_WIDTH // 3, 0, SCREEN_WIDTH // 3, SCREEN_HEIGHT-100)

SEGMENTS = [LEFT_SEGMENT, CENTER_SEGMENT, RIGHT_SEGMENT]