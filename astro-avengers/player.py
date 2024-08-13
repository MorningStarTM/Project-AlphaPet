from const import *
from bullet import Bullet
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
        self.max_vel = 5
        self.acceration = 0.1
        self.angle = 0
        self.vel = 0

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    
    def move_forward(self):
        self.vel = min(self.vel + self.acceration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceration, -self.max_vel/2)
        self.move()
    

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    """def move(self, dx, dy):
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
            self.rect.bottom = SCREEN_HEIGHT"""


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


def check_collisions(player, enemies, enemy_bullets):
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            player.life -= 1
            enemies.remove(enemy)
    
    for bullet in enemy_bullets:
        if player.rect.colliderect(bullet.rect):
            player.life -= 1
            enemy_bullets.remove(bullet)