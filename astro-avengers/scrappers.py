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
        self.attack_distance = 50  # Distance within which it attacks the player
        self.attack_damage = 10  # Damage dealt to the player

    def rotate_towards(self, target_rect):
        """Calculate the angle to face the target."""
        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        angle_to_target = math.degrees(math.atan2(dy, dx)) - 90  # Adjust for image orientation
        self.angle = angle_to_target % 360

    def move(self):
        """Move the scrapper according to its velocity and angle."""
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.rect.y -= vertical
        self.rect.x += horizontal

        # Ensure the scrapper stays within the screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update(self, player):
        """Update the scrapper's movement and rotation."""
        # Rotate to face the player
        self.rotate_towards(player.rect)

        # Move towards the player
        if self.vel < self.max_vel:
            self.vel += self.acceleration
        self.move()

        # Check for collision with player and attack if within range
        if self.collide(player):
            self.attack(player)  # Handle attack logic

    def draw(self, screen):
        """Draw the scrapper on the screen with rotation."""
        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

    def collide(self, player):
        """Check for collision with the player."""
        return self.rect.colliderect(player.rect)

    def attack(self, player):
        """Handle the attack on the player."""
        if self.collide(player):
            player.health -= self.attack_damage  # Reduce player's health
            # Optionally, remove the scrapper or take other actions
            self.rect.y = SCREEN_HEIGHT + self.rect.height  # Move off-screen or handle removal

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
