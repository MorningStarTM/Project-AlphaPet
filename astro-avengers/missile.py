from const import *
import math


class Missile:
    def __init__(self, x, y, angle):
        self.original_image = MISSILE_IMAGE
        self.angle = angle  # Angle at which the bullet is shot
        
        # Rotate the image based on the angle
        self.image = pygame.transform.rotate(self.original_image, math.degrees(self.angle))
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.centery = y  # Adjust to center the image based on the rotated image

        self.speed = 10
        
        # Calculate the velocity components based on the angle
        self.vel_x = math.sin(self.angle) * self.speed
        self.vel_y = math.cos(self.angle) * self.speed

    def update(self):
        # Move the bullet based on its velocity components
        self.rect.x -= self.vel_x
        self.rect.y -= self.vel_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)