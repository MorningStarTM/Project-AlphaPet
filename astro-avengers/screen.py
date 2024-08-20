import pygame
import os
from player import Player
from enemyflight import EnemyFlight, DummyEnemyFlight, EnemyGroup
from decepticons import Decepticon, DecepticonGroup
from gla import Ammunition, Life, Shield, check_gla_collisions
from const import *
from scrappers import ScrapperGroup, Scrapper
from doubler import Doubler, DoublerGroup

# Initialize Pygame
pygame.init()

# Screen dimensions


# Load the background image
BACKGROUND_IMAGE = pygame.image.load("assets\\screen\\bg.png")

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((TOTAL_SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Astro Avenger")
        
        # Load the background image and create a flipped version
        self.bg_image = pygame.image.load("assets\\screen\\bg.png")
        self.bg_flipped = pygame.transform.flip(self.bg_image, False, True)
        
        # Initialize background positions
        self.bg_y1 = 0
        self.bg_y2 = -SCREEN_HEIGHT
        self.bg_speed = 2

    def draw_background(self):
        # Draw the original image
        self.screen.blit(self.bg_image, (0, self.bg_y1))
        # Draw the flipped image
        self.screen.blit(self.bg_flipped, (0, self.bg_y1 + SCREEN_HEIGHT))
        
        # Draw the original image again
        self.screen.blit(self.bg_image, (0, self.bg_y2))
        # Draw the flipped image again
        self.screen.blit(self.bg_flipped, (0, self.bg_y2 + SCREEN_HEIGHT))

    def move_background(self):
        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed
        
        if self.bg_y1 >= SCREEN_HEIGHT:
            self.bg_y1 = self.bg_y2 - SCREEN_HEIGHT
        if self.bg_y2 >= SCREEN_HEIGHT:
            self.bg_y2 = self.bg_y1 - SCREEN_HEIGHT

    def update_screen(self):
        self.move_background()
        self.draw_background()

"""def draw_hud(screen, player):
    hud_rect = pygame.Rect(GAME_SCREEN_WIDTH, 0, HUD_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, LIGHT_GRAY, hud_rect)

    # Draw health bar
    health_bar_rect = pygame.Rect(GAME_SCREEN_WIDTH + 10, 10, 180, 20)
    pygame.draw.rect(screen, (255, 0, 0), health_bar_rect)
    pygame.draw.rect(screen, (0, 255, 0), (GAME_SCREEN_WIDTH + 10, 10, player.life * 60, 20))

    # Draw shield bar
    shield_bar_rect = pygame.Rect(GAME_SCREEN_WIDTH + 10, 40, 180, 20)
    pygame.draw.rect(screen, (0, 0, 255), shield_bar_rect)
    pygame.draw.rect(screen, (0, 255, 255), (GAME_SCREEN_WIDTH + 10, 40, player.shield * 60, 20))

    # Draw missile count
    missile_text = pygame.font.SysFont(None, 24).render(f"Missiles: {player.missile_count}", True, BLACK)
    screen.blit(missile_text, (GAME_SCREEN_WIDTH + 10, 70))

    # Draw special bullet count (Placeholder for implementation)
    special_bullet_text = pygame.font.SysFont(None, 24).render("Special Bullets: 0", True, BLACK)
    screen.blit(special_bullet_text, (GAME_SCREEN_WIDTH + 10, 100))"""

def draw_hud(screen, player):
    # Create a semi-transparent surface for the HUD
    screen.blit(BACKGROUND_IMAGE, (SCREEN_WIDTH, 0))
    hud_surface = pygame.Surface((HUD_WIDTH, SCREEN_HEIGHT))
    hud_surface.set_alpha(128)  # Set transparency level (0-255)
    hud_surface.fill((174, 181, 191))  # Light gray background with transparency

    # Draw the HUD onto this surface
    # Draw a glassy gradient (optional)
    for i in range(HUD_WIDTH):
        shade = 200 + (i * 55 // HUD_WIDTH)
        pygame.draw.line(hud_surface, (shade, shade, shade), (i, 0), (i, SCREEN_HEIGHT))

    # Draw health bar
    health_bar_rect = pygame.Rect(10, 10, 180, 20)
    pygame.draw.rect(hud_surface, (255, 0, 0), health_bar_rect)
    pygame.draw.rect(hud_surface, (0, 255, 0), (10, 10, player.life * 60, 20))

    # Draw shield bar
    shield_bar_rect = pygame.Rect(10, 40, 180, 20)
    pygame.draw.rect(hud_surface, (0, 0, 255), shield_bar_rect)
    pygame.draw.rect(hud_surface, (0, 255, 255), (10, 40, player.shield * 60, 20))

    # Draw missile count
    missile_text = pygame.font.SysFont(None, 24).render(f"Missiles: {player.missile_count}", True, (0, 0, 0))
    hud_surface.blit(missile_text, (10, 70))

    # Draw special bullet count (Placeholder for implementation)
    special_bullet_text = pygame.font.SysFont(None, 24).render("Special Bullets: 0", True, (0, 0, 0))
    hud_surface.blit(special_bullet_text, (10, 100))

    # Finally, blit the HUD surface onto the main screen
    screen.blit(hud_surface, (GAME_SCREEN_WIDTH, 0))




def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    # Initialize the screen and game elements
    screen = Screen()
    player = Player()
    enemy_group = DecepticonGroup(player)  # Initialize with 3 Decepticons
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.fire_bullet()
                elif event.key in (pygame.K_SPACE, pygame.K_RCTRL):
                    player.launch_missile()

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_RIGHT]:
            dx = player.speed
        if keys[pygame.K_UP]:
            dy = -player.speed
        if keys[pygame.K_DOWN]:
            dy = player.speed
        player.move(dx, dy)
        
        # Update game elements
        player.update()
        enemy_group.update()  # Pass player position to enemies
        
        # Check for collisions
        for bullet in player.bullets[:]:
            for enemy in enemy_group.decepticons[:]:
                if enemy.collide(bullet):
                    player.bullets.remove(bullet)
                    break
        
        for missile in player.missiles[:]:
            for enemy in enemy_group.decepticons[:]:
                if enemy.collide(missile):
                    player.missiles.remove(missile)
                    break
        
        # Clear screen
        screen.screen.fill((0, 0, 0))
        
        # Update background and draw it
        screen.update_screen()
        
        # Draw game elements
        enemy_group.draw(screen.screen)
        player.draw(screen.screen)
        
        # Draw HUD
        draw_hud(screen.screen, player)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()





def main4():
    clock = pygame.time.Clock()
    screen = Screen()
    player = Player()
    running = True
    
    enemies = EnemyGroup(player)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RCTRL:
                    player.launch_missile()

        # Update player and enemies
        player.update()
        enemies.update()
        
        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_RIGHT]:
            dx = player.speed
        if keys[pygame.K_UP]:
            dy = -player.speed
        if keys[pygame.K_DOWN]:
            dy = player.speed
        player.move(dx, dy)

        # Check collisions between bullets/missiles and enemies
        for bullet in player.bullets[:]:
            for enemy in enemies.enemies[:]:
                if enemy.collide(bullet):
                    player.bullets.remove(bullet)
                    break
        
        for missile in player.missiles[:]:
            for enemy in enemies.enemies[:]:
                if enemy.collide(missile):
                    enemy.health -= 25
                    player.missiles.remove(missile)
                    break
        
        """for enemy in enemies.enemies[:]:
            if enemy.collide(player):
                enemy.bounce(player=player)"""
        
        for enemy in enemies.enemies[:]:
            if enemy.collide_player(player):
                return True


        # Update and draw the background
        screen.update_screen()
        
        # Clear the screen and redraw background
        screen.screen.fill((0, 0, 0))
        screen.draw_background()
        
        # Draw the enemies
        enemies.draw(screen=screen.screen)
        
        # Draw the player
        player.draw(screen.screen)

        # Draw the HUD
        draw_hud(screen.screen, player)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def main5():
    pygame.init()
    clock = pygame.time.Clock()
    
    # Initialize the screen and game elements
    screen = Screen()
    player = Player()
    enemy_group = DoublerGroup(player)  # Assuming you have this implemented
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RCTRL:
                    player.launch_missile()

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_RIGHT]:
            dx = player.speed
        if keys[pygame.K_UP]:
            dy = -player.speed
        if keys[pygame.K_DOWN]:
            dy = player.speed
        player.move(dx, dy)
        
        # Update game elements
        player.update()
        enemy_group.update()  # Update enemy group
        
        # Check for collisions
        for bullet in player.bullets:
            for enemy in enemy_group.enemies:
                if enemy.collide(bullet):
                    player.bullets.remove(bullet)
                    break
        
        for missile in player.missiles:
            for enemy in enemy_group.enemies:
                if enemy.collide(missile):
                    player.missiles.remove(missile)
                    break
        
        # Clear screen
        screen.screen.fill((0, 0, 0))
        
        # Update background and draw it
        screen.update_screen()
        
        # Draw game elements
        for enemy in enemy_group.enemies:
            enemy.draw(screen.screen)
        
        player.draw(screen.screen)
        
        # Draw HUD
        draw_hud(screen.screen, player)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def main6():
    pygame.init()
    clock = pygame.time.Clock()
    
    # Initialize the screen and game elements
    screen = Screen()
    player = Player()
    scrapper_group = ScrapperGroup(player)  # Initialize Scrapper group
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RCTRL:
                    player.launch_missile()

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_RIGHT]:
            dx = player.speed
        if keys[pygame.K_UP]:
            dy = -player.speed
        if keys[pygame.K_DOWN]:
            dy = player.speed
        player.move(dx, dy)
        
        # Update game elements
        player.update()
        scrapper_group.update()  # Update Scrapper group
        
        # Check for collisions
        
        
        # Check collisions with scrappers
        for scrapper in scrapper_group.enemies:
            if scrapper.collide(player):
                # Player health already reduced in Scrapper's collide method
                pass
        
        # Clear screen
        screen.screen.fill((0, 0, 0))
        
        # Update background and draw it
        screen.update_screen()
        
        # Draw game elements
        
        for scrapper in scrapper_group.enemies:
            scrapper.draw(screen.screen)
        
        player.draw(screen.screen)
        
        # Draw HUD
        draw_hud(screen.screen, player)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()