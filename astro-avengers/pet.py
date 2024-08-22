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


    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    
    def move_forward(self):
        self.vel = self.max_vel
        self.move()

    def move_backward(self):
        self.vel = -self.max_vel
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def car_collide(self, other_car):
        # Check for pixel-level collision with another car
        offset = (int(other_car.x - self.x), int(other_car.y - self.y))
        overlap = self.get_mask().overlap(other_car.get_mask(), offset)
        return overlap is not None
    

    def shoot(self):
        """Create a bullet and add it to the list of bullets."""
        if self.ammunition > 0:
            bullet = ImageEnemyBullet(self.x, self.y, math.radians(self.angle))
            self.bullets.append(bullet)
            self.ammunition -= 1  # Decrease ammunition count