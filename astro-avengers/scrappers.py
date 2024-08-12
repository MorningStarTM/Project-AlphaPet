import pygame
import random
import math
from const import *


class Scrapper:
    def __init__(self):
        self.image = SCRAPPER_IMAGE
        self.original_image = self.image.copy()  # Keep the original image for rotation
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height  # Start above the screen
        self.speed = 3  # Speed of the scrapper
        self.angle = 0  # Initial angle for rotation
        self.vel = 0  # Initial velocity
        self.rotation_vel = 5  # Rotation velocity
        self.acceleration = 0.1  # Acceleration rate
        self.max_vel = 5  # Maximum velocity
    
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
        
        # Ensure angle stays within 0-360 degrees
        self.angle %= 360

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.rect.y -= vertical
        self.rect.x -= horizontal
        
        # Ensure the scrapper stays within the screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def update(self, player):
        # Calculate the direction to the player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        angle_to_player = math.atan2(dy, dx)

        # Rotate to face the player
        self.angle = math.degrees(angle_to_player+150) % 360

        # Move towards the player
        self.move_forward()

        # Check for collision with player
        if self.collide(player):
            self.bounce()  # Bounce backward upon collision

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)
        
    def collide(self, player):
        if self.rect.colliderect(player.rect):
            player.health -= 10  # Reduce player's health
            return True
        return False

class ScrapperGroup:
    def __init__(self):
        self.scrappers = [Scrapper() for _ in range(5)]  # Create a group with 5 scrappers

    def update(self, player):
        for scrapper in self.scrappers:
            scrapper.update(player)
            if scrapper.rect.top > SCREEN_HEIGHT:
                self.scrappers.remove(scrapper)
        
        # Optionally: Add more scrappers if needed
        while len(self.scrappers) < 5:
            self.scrappers.append(Scrapper())

    def draw(self, screen):
        for scrapper in self.scrappers:
            scrapper.draw(screen)
