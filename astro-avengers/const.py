import pygame
import os
from glob import glob

PLAYER_IMAGE = pygame.image.load("assets\\Player_1\\ship02P0000.png")
ENEMY_FLIGHT_IMAGE = pygame.image.load("assets\\enemy_1\\Turret09.png")
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 1000
BULLET_IMAGE = pygame.image.load("assets\\bullet\\bullet.png")
MISSILE_IMAGE = pygame.image.load("assets\\bullet\\P05.png")
SHIELD_IMAGE = pygame.image.load("assets\\GLA\\shield.png")
LIFE_IMAGE = pygame.image.load("assets\\GLA\\ammunition.png")
AMMUNITION_IMAGE = pygame.image.load("assets\\GLA\\life.png")


HUD_WIDTH = 200  # Width of the HUD section

# Colors
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)


LIST_OF_EXPLOSION_IMAGE = [pygame.image.load(i) for i in glob("E:\\github_clone\\Project-AlphaPet\\astro-avengers\\assets\\explosion\\*")]
