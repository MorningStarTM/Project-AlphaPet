from const import *
from bullet import Bullet, ImageEnemyBullet
import math


class Pet:
    def __init__(self):
        self.image = PET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50)
        self.speed = 5
        self.bullets = []
        self.missiles = []
        self.life = 3
        self.ammunition = 500
        self.shield = False
        self.missile_count = 10
        self.health = 200
        
        self.max_vel = 6
        self.vel = 0
        self.rotation_vel = 5
        self.angle = 0
        self.x, self.y = self.rect.center
        self.acceration = 0.1