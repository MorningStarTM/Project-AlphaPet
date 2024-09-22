from const import *
import math

class Bullet:
    def __init__(self, x, y, flag=None):
        self.image = BULLET_IMAGE
        if flag == 1:
            self.image = DOUBLE_BULLET_IMAGE
        elif flag == 2:
            self.image = GOLDEN_BULLET_IMAGE

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10
    
    def update(self):
        self.rect.y -= self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


class PetBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)  # Increase size
        pygame.draw.circle(self.image, (221, 245, 66), (5, 5), 3)  # Change color to red
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle + 90
        self.speed = 40
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        radians = math.radians(self.angle)
        self.x += self.speed * math.cos(radians)
        self.y -= self.speed * math.sin(radians)
        self.rect.center = (self.x, self.y)
        
        # Debug print to check bullet position
        print(f"Bullet position: {self.rect.center}")

        if not (0 <= self.rect.x <= SCREEN_WIDTH and 0 <= self.rect.y <= SCREEN_HEIGHT):
            self.kill()



class AnimatedBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, images, speed=7):
        super().__init__()
        self.images = images  # List of bullet animation frames
        self.current_frame = 0  # Track current frame in animation
        self.image = self.images[self.current_frame]  # Initial image
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = speed
        self.animation_speed = 5  # Control the speed of the animation
        self.animation_counter = 0  # Counter to change frames
        self.x, self.y = x, y

    def update(self):
        # Update the animation frame
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.rect = self.image.get_rect(center=self.rect.center)

        # Move the bullet
        radians = math.radians(self.angle)
        dx = math.sin(radians) * self.speed
        dy = math.cos(radians) * self.speed
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)

        # Check if the bullet is off the screen and remove it
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)



class ImageEnemyBullet:
    def __init__(self, x, y, angle):
        self.original_image = ICE_BULLET
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


class DecepticonBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed=25, radius=5, color=(255, 0, 0)):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle  # Angle in radians at which the bullet will travel
        self.speed = speed  # Bullet speed
        self.radius = radius  # Bullet size (radius of the circle)
        self.color = color  # Bullet color
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
    
    def update(self):
        # Move the bullet in the direction of the angle
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.rect.center = (self.x, self.y)  # Update the rect position to the new coordinates
        
        # Remove the bullet if it goes off-screen
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.kill()  # Remove bullet from the group

    def draw(self, screen):
        # Draw the bullet as a simple filled circle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


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


    
class PredatorBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, player, images, speed=5, max_scale=2):
        super().__init__()
        self.images = images  # List of bullet animation frames
        self.current_frame = 0  # Track current frame in animation
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = speed
        self.animation_speed = 5  # Control the speed of the animation
        self.animation_counter = 0  # Counter to change frames
        self.x, self.y = x, y
        self.player = player  # Reference to the player for proximity scaling
        self.max_scale = max_scale  # Maximum scaling factor for the bullet
        self.time_alive = 0  # Track time since bullet was fired
        self.max_time = 180  # Time after which bullet reaches max size (frames)

    def update(self):
        # Update the animation frame
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
        
        # Scale the bullet based on proximity to the player or time
        self.time_alive += 1  # Increase time alive for time-based scaling
        self.scale_bullet()

        # Move the bullet
        radians = math.radians(self.angle)
        dx = math.sin(radians) * self.speed
        dy = math.cos(radians) * self.speed
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)

        # Check if the bullet is off the screen and remove it
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def scale_bullet(self):
        """Scale the bullet based on its proximity to the player or time."""
        if self.time_alive < self.max_time:
            # Scale based on time
            scale_factor = 1 + (self.time_alive / self.max_time) * (self.max_scale - 1)
        else:
            # Max scale reached
            scale_factor = self.max_scale
        
        # Scale the current frame
        scaled_image = pygame.transform.scale(self.image, 
                                              (int(self.rect.width * scale_factor), int(self.rect.height * scale_factor)))
        self.image = scaled_image
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
