from const import *
from bullet import Bullet, ImageEnemyBullet
from missile import Missile
import math

class Player:
    def __init__(self):
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5
        self.bullets = []
        self.missiles = []
        self.life = 3
        self.ammunition = 500
        self.shield = False
        self.missile_count = 10
        self.health = 100
        

    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        # Ensure the player stays within the screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


    def fire_bullet(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.append(bullet)

    def launch_missile(self):
        if self.missile_count != 0:
            missile = Missile(self.rect.centerx, self.rect.top)
            self.missiles.append(missile)
            self.missile_count -= 1

    
    def update(self):
        # Update bullets
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        
        # Update missiles
        for missile in self.missiles:
            missile.update()
            if missile.rect.bottom < 0:
                self.missiles.remove(missile)
                


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)
        for missile in self.missiles:
            missile.draw(screen)


class AdvancedPlayer:
    def __init__(self):
        self.image = PLAYER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5
        self.bullets = []
        self.missiles = []
        self.life = 3
        self.ammunition = 500
        self.shield = False
        self.missile_count = 10
        self.health = 100
        
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

    def get_rect(self):
        car_rect = self.image.get_rect(topleft=(self.x, self.y))
        rotated_rect = pygame.Rect(car_rect)
        rotated_rect.center = car_rect.center
        return rotated_rect
    
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

    def update(self):
        #self.move()  # Update player position

        # Update bullets
        for bullet in self.bullets:
            bullet.update()
            # Remove bullet if it goes off-screen
            if bullet.rect.bottom < 0 or bullet.rect.top > SCREEN_HEIGHT or bullet.rect.right < 0 or bullet.rect.left > SCREEN_WIDTH:
                self.bullets.remove(bullet)


    def draw(self, win):
        blit_rotate_center(win, self.image, (self.x, self.y), self.angle)
        for bullet in self.bullets:
            bullet.draw(win)
        




def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center
    )
    win.blit(rotated_image, new_rect.topleft)


def check_collisions(player, enemies):
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            player.life -= 1
            
    