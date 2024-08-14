import pygame
import random
import math
from const import *


class Doubler:
    def __init__(self, player, segment):
        self.image = DOUBLER_IMAGE
        self.original_image = self.image.copy()  # Keep the original image for rotation
        self.rect = self.image.get_rect()
        self.segment = segment  # Segment that the enemy is restricted to
        self.player = player  # Store reference to the player
        self.rect.x = random.randint(segment.left, segment.right - self.rect.width)
        self.rect.y = 0  # Start at the top of the segment
        self.speed = 3  # Speed of the enemy
        self.health = 100  # Set initial health
        self.shoot_timer = 0
        self.shoot_interval = 60  # Time between shots in frames
        self.bullets = []
        self.explosion = None  # Explosion attribute
        self.is_dead = False  # Flag to mark the enemy as dead


