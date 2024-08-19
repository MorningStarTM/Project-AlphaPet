from const import *
import math

class Bullet:
    def __init__(self, x, y):
        self.image = BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10
    
    def update(self):
        self.rect.y -= self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)



class ImageEnemyBullet:
    def __init__(self, x, y, angle):
        self.original_image = BULLET_IMAGE
        self.angle = angle  # Angle at which the bullet is shot
        
        # Rotate the image based on the angle
        self.image = pygame.transform.rotate(self.original_image, -math.degrees(self.angle+2))
        self.rect = self.image.get_rect()
        self.rect.centerx = x + 5 
        self.rect.centery = y+10  # Adjust to center the image based on the rotated image

        self.speed = 10
        
        # Calculate the velocity components based on the angle
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed

    def update(self):
        # Move the bullet based on its velocity components
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class EnemyBullet:
    def __init__(self, x, y, angle):
        self.angle = angle  # Angle at which the bullet is shot
        self.rect = pygame.Rect(0, 0, 10, 10)  # Create a rect for collision detection
        self.rect.centerx = x
        self.rect.centery = y  # Center the rect based on the starting position

        self.speed = 10
        
        # Calculate the velocity components based on the angle
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed

    def update(self):
        # Move the bullet based on its velocity components
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def draw(self, screen):
        # Draw the bullet as a small yellow circle
        pygame.draw.circle(screen, (255, 255, 0), self.rect.center, 5)  



class DoubleBullet:
    def __init__(self, x, y):
        self.image = DOUBLE_BULLET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)