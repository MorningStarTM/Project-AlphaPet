from const import *
from bullet import Bullet, ImageEnemyBullet, PetBullet
import math

class NewPet2(pygame.sprite.Sprite):
    def __init__(self, scale_factor=0.9):
        super().__init__()
        # Load and scale the image
        original_image = pygame.image.load(PET_IMAGE).convert_alpha()
        self.original_image = pygame.transform.scale(original_image, (int(original_image.get_width() * scale_factor), int(original_image.get_height() * scale_factor)))
        self.image = self.original_image
        self.max_vel = 5
        self.vel = 0
        self.rotation_vel = 3
        self.angle = 0
        self.START_POS = (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT)
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.radar_visible = True
        self.rect = self.image.get_rect(center=self.START_POS)
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 100

        self.bullets = pygame.sprite.Group()

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
        self.angle %= 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


    def get_health(self):
        return self.health

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)
        self.bullets.draw(win)  # Ensure bullets are drawn

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

        self.x = max(0 + self.rect.width // 2, min(SCREEN_WIDTH - self.rect.width // 2, self.x))
        self.y = max(0 + self.rect.height // 2, min(SCREEN_HEIGHT - self.rect.height // 2, self.y))

        self.rect.center = (self.x, self.y)
        
        

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel * 0.5
        self.move()
   

    def shoot(self):
        bullet = PetBullet(self.x, self.y, self.angle)
        self.bullets.add(bullet)
        print("Bullet shot!")  # Debug print

    def update_bullets(self):
        self.bullets.update()

    def handle_collision(self, buildings):
        if pygame.sprite.spritecollide(self, buildings, False, pygame.sprite.collide_mask):
            #self.vel = 0
            self.bounce()
            self.move()

    def update(self):
        self.update_bullets()



class NewPet(pygame.sprite.Sprite):
    def __init__(self, scale_factor=0.4):
        super().__init__()
        # Load and scale the image
        original_image = pygame.image.load(PET_IMAGE).convert_alpha()
        self.original_image = pygame.transform.scale(original_image, (int(original_image.get_width() * scale_factor), int(original_image.get_height() * scale_factor)))
        self.image = self.original_image
        self.max_vel = 5
        self.vel = 0
        self.rotation_vel = 3
        self.angle = 0
        self.START_POS = (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT)
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.radar_visible = True
        self.rect = self.image.get_rect(center=self.START_POS)
        self.mask = pygame.mask.from_surface(self.image)
        self.health = 100

        self.bullets = pygame.sprite.Group()
        self.laser_active = False  # Track if laser is being fired
        self.laser_color = (232, 81, 94)  # Laser color as specified
        self.laser_width = 5  # Thickness of the laser
        self.laser_length = SCREEN_HEIGHT  # Length of the laser
        self.laser_damage = 8  

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
        self.angle %= 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        print(self.angle)

    def get_health(self):
        return self.health

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)
        self.bullets.draw(win)  # Ensure bullets are drawn

        # Draw laser if active
        #if self.laser_active:
        #    self.draw_laser(win)

    """def draw_laser(self, win):
        #Draws the laser from the pet to the edge of the screen.
        radians = math.radians(self.angle+180)  # Convert angle to radians
        # Calculate the end position of the laser based on angle
        laser_end_x = self.x + math.sin(radians) * self.laser_length
        laser_end_y = self.y + math.cos(radians) * self.laser_length
        pygame.draw.line(win, self.laser_color, (self.x, self.y), (laser_end_x, laser_end_y), self.laser_width)"""
    
    def draw_laser(self, win, enemies):
        """Draw the laser from the pet and check for collisions with enemies."""
        radians = math.radians(self.angle + 180)  # Convert angle to radians

        # Calculate the end position of the laser based on angle
        laser_end_x = self.x + math.sin(radians) * self.laser_length
        laser_end_y = self.y + math.cos(radians) * self.laser_length

        # Draw the laser
        pygame.draw.line(win, self.laser_color, (self.x, self.y), (laser_end_x, laser_end_y), self.laser_width)

        # Check for collisions with enemies
        self.check_laser_collision(enemies, (self.x, self.y), (laser_end_x, laser_end_y))

    def check_laser_collision(self, enemies, laser_start, laser_end):
        """Check if the laser hits any enemies and reduce their health."""
        for enemy in enemies:
            # Check if the laser line intersects the enemy's rect
            if enemy.rect.clipline(laser_start, laser_end):
                enemy.health -= self.laser_damage
                print(f"Laser hit! {enemy.__class__.__name__} health: {enemy.health}")
                
                # If enemy's health is zero or less, destroy the enemy
                if enemy.health <= 0:
                    print(f"{enemy.__class__.__name__} destroyed!")
                    enemies.remove(enemy)  # Remove the enemy from the game

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

        self.x = max(0 + self.rect.width // 2, min(SCREEN_WIDTH - self.rect.width // 2, self.x))
        self.y = max(0 + self.rect.height // 2, min(SCREEN_HEIGHT - self.rect.height // 2, self.y))

        self.rect.center = (self.x, self.y)
        
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel * 0.5
        self.move()

    def shoot(self):
        bullet = PetBullet(self.x, self.y, self.angle)
        self.bullets.add(bullet)
        print("Bullet shot!")  # Debug print

    def update_bullets(self):
        self.bullets.update()

    def handle_collision(self, buildings):
        if pygame.sprite.spritecollide(self, buildings, False, pygame.sprite.collide_mask):
            self.bounce()
            self.move()

    def update(self):
        self.update_bullets()

    def fire_laser(self, is_firing):
        """Activates or deactivates the laser."""
        self.laser_active = is_firing





def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center
    )
    win.blit(rotated_image, new_rect.topleft)