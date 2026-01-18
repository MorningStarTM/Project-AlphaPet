import pygame
import os
from player import Player, check_collisions
from enemyflight import EnemyFlight, DummyEnemyFlight, EnemyGroup
from decepticons import Decepticon, DecepticonGroup
from gla import Ammunition, Life, Shield, check_gla_collisions
from const import *
from scrappers import ScrapperGroup, Scrapper
from doubler import Doubler, DoublerGroup
from pet import NewPet
from enemyColony import DiamondHead
from yellowBoss import YellowBoss
import math
from predator import Predator
import random
from gla import check_gla_collisions
from timing import GLATimer
from enemy_manager import EnemyManager

# Initialize Pygame
pygame.init()

# Screen dimensions


# Load the background image
BACKGROUND_IMAGE = pygame.image.load("assets\\screen\\Black_Wallpaper.jpg")

class Screen:
    def __init__(self):
        self.screen = pygame.display.set_mode((TOTAL_SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Astro Avenger")
        
        # Load the background image and create a flipped version
        self.bg_image = pygame.image.load("assets\\screen\\Black_Wallpaper.jpg")
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



def draw_hud(screen, player:Player, pet:NewPet):
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
    # Draw health bar (mixed green/red)
    health_bar_rect = pygame.Rect(10, 10, 180, 20)
    pygame.draw.rect(hud_surface, (255, 0, 0), health_bar_rect)  # Full red background
    health_width = int(player.health / 100 * 180)
    pygame.draw.rect(hud_surface, (0, 255, 0), (10, 10, health_width, 20))  # Green portion

    # Draw shield bar (mixed light blue/dark blue)
    shield_bar_rect = pygame.Rect(10, 40, 180, 20)
    pygame.draw.rect(hud_surface, (0, 0, 139), shield_bar_rect)  # Full dark blue background
    shield_width = int(player.shield / 400 * 180)
    pygame.draw.rect(hud_surface, (173, 216, 230), (10, 40, shield_width, 20))  # Light blue portion



    laser_bar_rect = pygame.Rect(10, 70, 180, 20)
    pygame.draw.rect(hud_surface, (50, 50, 50), laser_bar_rect)  # Background bar
    pygame.draw.rect(hud_surface, (232, 81, 94), (10, 70, int(pet.laser_bar / pet.laser_bar_full * 180), 20))
    
    # Label for laser bar
    laser_text = pygame.font.SysFont(None, 24).render(f"Laser: {int(pet.laser_bar)}", True, (0, 0, 0))
    hud_surface.blit(laser_text, (10, 95))


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
    pet = NewPet()
    enemy_group = Predator(player)  # Initialize with 3 Decepticons
    
    shake_timer = 0
    shake_duration = 30  # Frames to shake
    shake_magnitude = 10

    count = 0
    running = True

    while running:
        count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE:
                    player.launch_missile()
                elif event.key == pygame.K_LCTRL:
                    pet.shoot()
                elif event.key == pygame.K_TAB:
                    player.cycle_bullet_type()
                elif event.key == pygame.K_q:
                    player.cycle_missile_type()

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        moved = False
        opponent_moved = False

        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed


        if keys[pygame.K_LEFT]:
            pet.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            pet.rotate(right=True)
        if keys[pygame.K_UP]:
            moved = True
            pet.move_forward()
        if keys[pygame.K_DOWN]:
            moved = True
            pet.move_backward()

        if keys[pygame.K_b]:
            if not pet.shield_toggle:  # Prevent holding down the key from toggling repeatedly
                pet.toggle_shield()
            pet.shield_toggle = True
        else:
            pet.shield_toggle = False

        if keys[pygame.K_m]:
            pet.fire_laser(True)
        else:
            pet.fire_laser(False)
        player.move(dx, dy)
        pet.update()

        

        
        # Update game elements
        player.update()
        enemy_group.update()  # Pass player position to enemies

        
        # Check for collisions
        for bullet in player.bullets[:]:
            for enemy in enemy_group.enemies[:]:
                if enemy.collide(bullet):
                    player.bullets.remove(bullet)
                    break
        
                
        for missile in player.missiles[:]:
            for enemy in enemy_group.enemies[:]:
                if enemy.collide(missile):
                    player.missiles.remove(missile)
                    break

        
        for predator in enemy_group.enemies[:]:
            if predator.check_bullet_collisions():
                break

        for predator in enemy_group.enemies:
            pet.handle_enemy_laser_collision(predator.lasers)
        

        # Clear screen
        screen.screen.fill((0, 0, 0))
        
        # Update background and draw it
        screen.update_screen()
        
        # Draw game elements
        pet.draw(screen.screen)
        enemy_group.draw(screen.screen)
        player.draw(screen.screen)


        if pet.laser_active:
            pet.draw_laser(screen.screen, enemy_group.enemies)
        
        
        # Draw HUD
        draw_hud(screen.screen, player, pet)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()





def main7():
    pygame.init()
    clock = pygame.time.Clock()
    
    # Initialize the screen and game elements
    screen = Screen()
    player = Player()
    pet = NewPet()
    yellow_boss = YellowBoss(player)  # Initialize YellowBoss

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE:
                    player.launch_missile()
                elif event.key == pygame.K_LCTRL:
                    pet.shoot()
                elif event.key == pygame.K_TAB:
                    player.cycle_bullet_type()
                elif event.key == pygame.K_q:
                    player.cycle_missile_type()
                elif event.key == pygame.K_v:
                    player.launch_nuclear()

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        moved = False

        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed

        # Handle pet movement and shooting
        if keys[pygame.K_LEFT]:
            pet.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            pet.rotate(right=True)
        if keys[pygame.K_UP]:
            moved = True
            pet.move_forward()
        if keys[pygame.K_DOWN]:
            moved = True
            pet.move_backward()

        if keys[pygame.K_m]:
            pet.fire_laser(True)
        else:
            pet.fire_laser(False)

        # Update player and pet positions
        player.move(dx, dy)
        pet.update()

        # Update game elements
        player.update()
        yellow_boss.update()

        for wave in yellow_boss.vibration_waves[:]:
            if yellow_boss.check_vibration_collision(wave):
                player.health -= yellow_boss.vibration_damage
                yellow_boss.vibration_waves.remove(wave)
                print("Player Health : ", player.health)
            

        # Check for collisions with YellowBoss
        for bullet in player.bullets[:]:
            if yellow_boss.rect.colliderect(bullet.rect):
                player.bullets.remove(bullet)
                yellow_boss.health -= 5  # Reduce boss health on bullet collision
                if yellow_boss.health <= 0:
                    yellow_boss.trigger_explosion()

        for missile in player.missiles[:]:
            if yellow_boss.rect.colliderect(missile.rect):
                player.missiles.remove(missile)
                yellow_boss.health -= missile.damage  # Reduce boss health on missile collision
                if yellow_boss.health <= 0:
                    yellow_boss.trigger_explosion()
        
        for n_missile in player.nuclear[:]:
            if yellow_boss.rect.colliderect(n_missile.rect):
                player.nuclear.remove(n_missile)
                yellow_boss.health -= n_missile.damage  # Reduce boss health on missile collision
                if yellow_boss.health <= 0:
                    yellow_boss.trigger_explosion()
                    for protector in yellow_boss.protectors[:]:
                        protector.take_damage(100)
                        protector.trigger_explosion()


        for missile in player.missiles[:]:
            for protector in yellow_boss.protectors:
                    if protector.rect.colliderect(missile.rect):
                        protector.take_damage(15)
                        player.missiles.remove(missile)
                        break  # Bullet hits protector, no further checks
        
        for bullet in player.bullets[:]:
            for protector in yellow_boss.protectors:
                    if protector.rect.colliderect(bullet.rect):
                        protector.take_damage(5)
                        player.bullets.remove(bullet)
                        break  # Bullet hits protector, no further checks

        # Check for collisions between pet's laser and YellowBoss
        if pet.laser_active:
            distance_to_boss = math.hypot(pet.rect.centerx - yellow_boss.rect.centerx,
                                          pet.rect.centery - yellow_boss.rect.centery)
            if distance_to_boss <= SCREEN_HEIGHT:
                yellow_boss.health -= pet.laser_damage  # Reduce boss health by laser damage
                if yellow_boss.health <= 0:
                    yellow_boss.trigger_explosion()

        # Clear screen
        screen.screen.fill((0, 0, 0))
        
        # Update background and draw it
        screen.update_screen()
        
        # Draw game elements
        pet.draw(screen.screen)
        yellow_boss.draw(screen.screen)  # Draw YellowBoss
        player.draw(screen.screen)

        if pet.laser_active:
            all_targets = [yellow_boss] + yellow_boss.protectors
            pet.draw_laser(screen.screen, all_targets)
        # Pass YellowBoss as target

        # Draw HUD
        draw_hud(screen.screen, player, pet)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



def main4():
    clock = pygame.time.Clock()
    screen = Screen()
    player = Player()
    pet = NewPet()
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
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed
        player.move(dx, dy)

        # Handle pet movement and shooting
        if keys[pygame.K_LEFT]:
            pet.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            pet.rotate(right=True)
        if keys[pygame.K_UP]:
            moved = True
            pet.move_forward()
        if keys[pygame.K_DOWN]:
            moved = True
            pet.move_backward()

        if keys[pygame.K_m]:
            pet.fire_laser(True)
        else:
            pet.fire_laser(False)

        pet.update()

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

        # Handle shield collision with enemy bullets
        pet.handle_shield_collision(enemies)

        # Update and draw the background
        screen.update_screen()
        
        # Clear the screen and redraw background
        screen.screen.fill((0, 0, 0))
        screen.draw_background()
        
        # Draw the enemies
        enemies.draw(screen=screen.screen)
        
        # Draw the player
        player.draw(screen.screen)
        pet.draw(screen.screen)

        if pet.laser_active:
            pet.draw_laser(screen.screen, enemies.enemies)
        # Draw the HUD
        draw_hud(screen.screen, player, pet)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def main5():
    pygame.init()
    clock = pygame.time.Clock()
    
    # Initialize the screen and game elements
    screen = Screen()
    player = Player()
    pet = NewPet()
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
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed
        player.move(dx, dy)

        # Handle pet movement and shooting
        if keys[pygame.K_LEFT]:
            pet.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            pet.rotate(right=True)
        if keys[pygame.K_UP]:
            moved = True
            pet.move_forward()
        if keys[pygame.K_DOWN]:
            moved = True
            pet.move_backward()
        

        if keys[pygame.K_m]:
            pet.fire_laser(True)
        else:
            pet.fire_laser(False)

        pet.update()
        
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
        
        # Handle shield collision with enemy bullets
        pet.handle_shield_collision(enemy_group)
        
        # Clear screen
        screen.screen.fill((0, 0, 0))
        
        # Update background and draw it
        screen.update_screen()
        
        # Draw game elements
        for enemy in enemy_group.enemies:
            enemy.draw(screen.screen)
        
        player.draw(screen.screen)
        pet.draw(screen.screen)
        
        if pet.laser_active:
            pet.draw_laser(screen.screen, enemy_group.enemies)
        
        # Draw HUD
        draw_hud(screen.screen, player, pet)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def main6():
    pygame.init()
    clock = pygame.time.Clock()
    
    # Initialize the screen and game elements
    screen = Screen()
    player = Player()
    pet = player.pet #NewPet()
    scrapper_group = ScrapperGroup(player)  # Initialize Scrapper group
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE:
                    player.launch_missile()
                elif event.key == pygame.K_LCTRL:
                    pet.shoot()
                elif event.key == pygame.K_TAB:
                    player.cycle_bullet_type()
                elif event.key == pygame.K_q:
                    player.cycle_missile_type()
                elif event.key == pygame.K_v:
                    player.launch_nuclear()
                elif event.key == pygame.K_h:
                    player.launch_homing_missile(scrapper_group.enemies)

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed
        player.move(dx, dy)

        # Handle pet movement and shooting
        if keys[pygame.K_LEFT]:
            pet.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            pet.rotate(right=True)
        if keys[pygame.K_UP]:
            moved = True
            pet.move_forward()
        if keys[pygame.K_DOWN]:
            moved = True
            pet.move_backward()
        

        if keys[pygame.K_m]:
            pet.fire_laser(True)
        else:
            pet.fire_laser(False)

        pet.update()
        
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
        pet.draw(screen.screen)

        if pet.laser_active:
            pet.draw_laser(screen.screen, scrapper_group.enemies)
        
        # Draw HUD
        draw_hud(screen.screen, player, pet)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()




def main_predator():
    pygame.init()
    clock = pygame.time.Clock()
    
    # Initialize the screen and game elements
    screen = Screen()
    player = Player()
    pet = player.pet
    predator = YellowBoss(player)  # Directly use the Predator class
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE:
                    player.launch_missile()
                elif event.key == pygame.K_LCTRL:
                    pet.shoot()
                elif event.key == pygame.K_TAB:
                    player.cycle_bullet_type()
                elif event.key == pygame.K_q:
                    player.cycle_missile_type()
                elif event.key == pygame.K_v:
                    player.launch_nuclear()
                elif event.key == pygame.K_h:
                    player.launch_homing_missile(predator)


        # Handle player and pet movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed

        if keys[pygame.K_LEFT]:
            pet.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            pet.rotate(right=True)
        if keys[pygame.K_UP]:
            pet.move_forward()
        if keys[pygame.K_DOWN]:
            pet.move_backward()

        if keys[pygame.K_b]:
            if not pet.shield_toggle:
                pet.toggle_shield()
            pet.shield_toggle = True
        else:
            pet.shield_toggle = False

        if keys[pygame.K_m]:
            pet.fire_laser(True)
        else:
            pet.fire_laser(False)

        player.move(dx, dy)
        pet.update()

        # Update predator and player
        player.update()
        predator.update()

        # Check for collisions
        for bullet in player.bullets[:]:
            if not predator.is_dead and predator.collide(bullet):
                player.bullets.remove(bullet)

        for missile in player.missiles[:]:
            if not predator.is_dead and predator.collide(missile):
                player.missiles.remove(missile)

        for missile in player.nuclear[:]:
            if not predator.is_dead and predator.collide_missile(missile):
                player.nuclear.remove(missile)

        #pet.handle_enemy_laser_collision(predator.lasers)

        # Clear screen and update background
        screen.screen.fill((0, 0, 0))
        screen.update_screen()

        # Draw game elements
        pet.draw(screen.screen)
        predator.draw(screen.screen)
        player.draw(screen.screen)

        if pet.laser_active:
            pet.draw_laser(screen.screen, [predator])

        draw_hud(screen.screen, player, pet)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()





def main_doubler():
    pygame.init()
    clock = pygame.time.Clock()
    
    # Initialize the screen and game elements
    screen = Screen()
    player = Player()
    pet = NewPet()
    enemy_group = DoublerGroup(player)  # Use the DoublerGroup you provided
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE:
                    player.launch_missile()
                elif event.key == pygame.K_LCTRL:
                    pet.shoot()
                elif event.key == pygame.K_TAB:
                    player.cycle_bullet_type()
                elif event.key == pygame.K_q:
                    player.cycle_missile_type()

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed

        if keys[pygame.K_LEFT]:
            pet.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            pet.rotate(right=True)
        if keys[pygame.K_UP]:
            pet.move_forward()
        if keys[pygame.K_DOWN]:
            pet.move_backward()

        if keys[pygame.K_b]:
            if not pet.shield_toggle:
                pet.toggle_shield()
            pet.shield_toggle = True
        else:
            pet.shield_toggle = False

        if keys[pygame.K_m]:
            pet.fire_laser(True)
        else:
            pet.fire_laser(False)

        # Update positions
        player.move(dx, dy)
        player.update()
        pet.update()
        enemy_group.update()

        # Check collisions
        for bullet in player.bullets[:]:
            for enemy in enemy_group.enemies[:]:
                if enemy.collide(bullet):
                    player.bullets.remove(bullet)
                    break

        for missile in player.missiles[:]:
            for enemy in enemy_group.enemies[:]:
                if enemy.collide(missile):
                    player.missiles.remove(missile)
                    break

        for enemy in enemy_group.enemies:
            enemy.check_bullet_collisions() if hasattr(enemy, "check_bullet_collisions") else None
            # pet.handle_enemy_laser_collision(enemy.bullets) if hasattr(pet, "handle_enemy_laser_collision") else None  # Commented out: bullets don't have start_pos/end_pos

        # Handle shield collision with enemy bullets
        pet.handle_shield_collision(enemy_group)

        # Draw everything
        screen.screen.fill((0, 0, 0))
        screen.update_screen()

        pet.draw(screen.screen)
        enemy_group.draw(screen.screen)
        player.draw(screen.screen)

        if pet.laser_active:
            pet.draw_laser(screen.screen, enemy_group.enemies)

        draw_hud(screen.screen, player, pet)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



def main_decepticon():
    pygame.init()
    clock = pygame.time.Clock()
    
    # Initialize the screen and game elements
    screen = Screen()
    player = Player()
    pet = NewPet()
    yb = YellowBoss(player)
    d_group = DecepticonGroup(player)  # <-- Use DecepticonGroup here
    group_enemies = [d_group.enemies]
    single_enemies = [yb]


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE:
                    player.launch_missile()
                elif event.key == pygame.K_LCTRL:
                    pet.shoot()
                elif event.key == pygame.K_TAB:
                    player.cycle_bullet_type()
                elif event.key == pygame.K_q:
                    player.cycle_missile_type()
                elif event.key == pygame.K_h:
                    player.launch_homing_missile((group_enemies, single_enemies))
                elif event.key == pygame.K_v:
                    player.launch_nuclear()

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed
        

        if keys[pygame.K_LEFT]:
            pet.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            pet.rotate(right=True)
        if keys[pygame.K_UP]:
            pet.move_forward()
        if keys[pygame.K_DOWN]:
            pet.move_backward()

        if keys[pygame.K_b]:
            if not pet.shield_toggle:
                pet.toggle_shield()
            pet.shield_toggle = True
        else:
            pet.shield_toggle = False

        if keys[pygame.K_m]:
            pet.fire_laser(True)
        else:
            pet.fire_laser(False)

        # Update game state
        player.move(dx, dy)
        player.update()
        pet.update()
        d_group.update()
        yb.update()

        # Handle collisions
        for bullet in player.bullets[:]:
            for enemy in d_group.enemies[:]:  # <--- instead of group_enemies
                if enemy.collide(bullet):
                    player.bullets.remove(bullet)
                    break
            for boss in single_enemies:
                if hasattr(boss, "is_dead") and not boss.is_dead and boss.collide(bullet):
                    player.bullets.remove(bullet)
                    break


        for missile in player.missiles[:]:
            for enemy in d_group.enemies[:]:
                if enemy.collide_missile(missile):
                    player.missiles.remove(missile)
                    break
            for boss in single_enemies:
                if hasattr(boss, "is_dead") and not boss.is_dead and boss.collide_missile(missile):
                    player.missiles.remove(missile)
                    break


        
        for hmissile in player.home_missiles[:]:
            for enemy in d_group.enemies[:]:
                if enemy.collide_missile(hmissile):
                    player.home_missiles.remove(hmissile)
                    break
            for boss in single_enemies:
                if hasattr(boss, "is_dead") and not boss.is_dead and boss.collide_missile(hmissile):
                    player.home_missiles.remove(hmissile)
                    break
                for protector in boss.protectors:
                    if protector.rect.colliderect(hmissile.rect):
                        protector.take_damage(10)
                        player.home_missiles.remove(hmissile)
                        break  # Bullet hits protector, no further checks

        
        for nuclear in player.nuclear[:]:
            for boss in single_enemies:
                if hasattr(boss, "is_dead") and not boss.is_dead and boss.collide_missile(nuclear):
                    for protector in boss.protectors:
                        protector.take_damage(100)
                    player.nuclear.remove(nuclear)
                    break

        # Handle shield collision with enemy bullets
        pet.handle_shield_collision(d_group)

        # Draw everything
        screen.screen.fill((0, 0, 0))
        screen.update_screen()

        pet.draw(screen.screen)
        d_group.draw(screen.screen)
        yb.draw(screen.screen)
        player.draw(screen.screen)

        if pet.laser_active:
            pet.draw_laser(screen.screen, d_group.enemies)
        


        draw_hud(screen.screen, player, pet)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()





def main_combined():
    pygame.init()
    clock = pygame.time.Clock()

    # Initialize the screen and game elements
    screen = Screen()
    player = Player()
    pet = player.pet
    
    # Create group-based enemies
    #scrapper_group = ScrapperGroup(player)
    #doubler_group = DoublerGroup(player)
    decepticon_group = DecepticonGroup(player)
    
    # Create boss enemies
    #yellow_boss = YellowBoss(player)
    #diamond_head = DiamondHead(player)
    predator = Predator(player)

    group_enemies = [decepticon_group.enemies]
    single_enemies = [predator]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE:
                    player.launch_missile()
                elif event.key == pygame.K_LCTRL:
                    pet.shoot()
                elif event.key == pygame.K_TAB:
                    player.cycle_bullet_type()
                elif event.key == pygame.K_q:
                    player.cycle_missile_type()
                elif event.key == pygame.K_v:
                    player.launch_nuclear()
                elif event.key == pygame.K_h:
                    # 🚀 Launch homing missile with both groups and singles
                    player.launch_homing_missile((group_enemies, single_enemies))

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed

        if keys[pygame.K_LEFT]:
            pet.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            pet.rotate(right=True)
        if keys[pygame.K_UP]:
            pet.move_forward()
        if keys[pygame.K_DOWN]:
            pet.move_backward()

        if keys[pygame.K_b]:
            if not pet.shield_toggle:
                pet.toggle_shield()
            pet.shield_toggle = True
        else:
            pet.shield_toggle = False

        if keys[pygame.K_m]:
            pet.fire_laser(True)
        else:
            pet.fire_laser(False)

        # Update game objects
        player.move(dx, dy)
        player.update()
        pet.update()
        
        #scrapper_group.update()
        #doubler_group.update()
        decepticon_group.update()

        #yellow_boss.update()
        #diamond_head.update()
        predator.update()

        # Handle collisions (player bullets with enemies)
        for bullet in player.bullets[:]:
            for enemy_group in group_enemies:
                for enemy in enemy_group[:]:
                    if enemy.collide(bullet):
                        player.bullets.remove(bullet)
                        break
            for boss in single_enemies:
                if hasattr(boss, "is_dead") and not boss.is_dead and boss.collide(bullet):
                    player.bullets.remove(bullet)
                    break

        # Handle player missiles
        for missile in player.missiles[:]:
            for enemy_group in group_enemies:
                for enemy in enemy_group[:]:
                    if enemy.collide_missile(missile):
                        player.missiles.remove(missile)
                        break
            for boss in single_enemies:
                if hasattr(boss, "is_dead") and not boss.is_dead and boss.collide_missile(missile):
                    player.missiles.remove(missile)
                    break

        # Handle homing missiles
        for hmissile in player.home_missiles[:]:
            for enemy_group in group_enemies:
                for enemy in enemy_group[:]:
                    if enemy.collide_missile(hmissile):
                        player.home_missiles.remove(hmissile)
                        break
            for boss in single_enemies:
                if hasattr(boss, "is_dead") and not boss.is_dead and boss.collide_missile(hmissile):
                    player.home_missiles.remove(hmissile)
                    break

        # Handle nuclear missiles
        for missile in player.nuclear[:]:
            for enemy_group in group_enemies:
                for enemy in enemy_group[:]:
                    if enemy.collide_missile(missile):
                        player.nuclear.remove(missile)
                        break
            for boss in single_enemies:
                if hasattr(boss, "is_dead") and not boss.is_dead and boss.collide_missile(missile):
                    player.nuclear.remove(missile)
                    break

        # Update pet shield collisions with enemy bullets if needed
        for enemy_group in group_enemies:
            for enemy in enemy_group:
                if hasattr(enemy, "check_bullet_collisions"):
                    enemy.check_bullet_collisions()
                # if hasattr(pet, "handle_enemy_laser_collision"):
                #     pet.handle_enemy_laser_collision(enemy.bullets)  # Commented out: bullets don't have start_pos/end_pos

        # for boss in single_enemies:
        #     if hasattr(pet, "handle_enemy_laser_collision") and hasattr(boss, "bullets"):
        #         pet.handle_enemy_laser_collision(boss.bullets)  # Commented out: bullets don't have start_pos/end_pos

        # Handle shield collision with enemy bullets
        pet.handle_shield_collision(decepticon_group)

        # Clear screen
        screen.screen.fill((0, 0, 0))
        screen.update_screen()

        # Draw everything
        pet.draw(screen.screen)
        #scrapper_group.draw(screen.screen)
        #doubler_group.draw(screen.screen)
        decepticon_group.draw(screen.screen)

        #yellow_boss.draw(screen.screen)
        #diamond_head.draw(screen.screen)
        predator.draw(screen.screen)

        player.draw(screen.screen)

        if pet.laser_active:
            pet.draw_laser(screen.screen, decepticon_group.enemies + single_enemies)

        draw_hud(screen.screen, player, pet)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()




def main_gla():
    pygame.init()
    clock = pygame.time.Clock()

    screen = Screen()
    player = Player()
    pet = NewPet()
    gla_timer = GLATimer()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE:
                    player.launch_missile()
                elif event.key == pygame.K_LCTRL:
                    pet.shoot()
                elif event.key == pygame.K_TAB:
                    player.cycle_bullet_type()
                elif event.key == pygame.K_q:
                    player.cycle_missile_type()

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed

        if keys[pygame.K_LEFT]:
            pet.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            pet.rotate(right=True)
        if keys[pygame.K_UP]:
            pet.move_forward()
        if keys[pygame.K_DOWN]:
            pet.move_backward()

        player.move(dx, dy)
        pet.update()

        player.update()
        gla_timer.update()

        # Check for collisions
        check_gla_collisions(player, gla_timer.shields, gla_timer.lives, gla_timer.ammunitions)

        # Clear screen
        screen.screen.fill((0, 0, 0))
        screen.update_screen()

        # Draw game elements
        pet.draw(screen.screen)
        player.draw(screen.screen)
        gla_timer.draw(screen.screen)

        # Draw HUD
        draw_hud(screen.screen, player, pet)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()




def play_game():
    final_manager()


def final_manager():
    pygame.init()
    clock = pygame.time.Clock()

    screen = Screen()
    player = Player()
    pet = NewPet()
    # ... (setup pygame, screen, player, etc.)
    enemy_manager = EnemyManager(player)
    gla_timer = GLATimer()

    running = True
    while running:
        # handle input, etc.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    player.fire_bullet()
                elif event.key == pygame.K_SPACE:
                    player.launch_missile()
                elif event.key == pygame.K_LCTRL:
                    pet.shoot()
                elif event.key == pygame.K_TAB:
                    player.cycle_bullet_type()
                elif event.key == pygame.K_q:
                    player.cycle_missile_type()

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -player.speed
        if keys[pygame.K_d]:
            dx = player.speed
        if keys[pygame.K_w]:
            dy = -player.speed
        if keys[pygame.K_s]:
            dy = player.speed

        if keys[pygame.K_LEFT]:
            pet.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            pet.rotate(right=True)
        if keys[pygame.K_UP]:
            pet.move_forward()
        if keys[pygame.K_DOWN]:
            pet.move_backward()

        if keys[pygame.K_b]:
            if not pet.shield_toggle:
                pet.toggle_shield()
            pet.shield_toggle = True
        else:
            pet.shield_toggle = False

        if keys[pygame.K_m]:
            pet.fire_laser(True)
        else:
            pet.fire_laser(False)

        player.move(dx, dy)

        # Update everything
        player.update()
        pet.update()
        enemy_manager.update()  # This updates all active enemies/bosses

        gla_timer.update()

        # Check for collisions
        check_gla_collisions(player, pet, gla_timer.shields, gla_timer.lives, gla_timer.ammunitions)

        group_enemies = [enemy_manager.groups[g].enemies for g in enemy_manager.active_groups]
        single_enemies = [enemy_manager.bosses[b] for b in enemy_manager.active_bosses if not enemy_manager.bosses[b].is_dead]

        for bullet in player.bullets[:]:
            for enemy_group in group_enemies:
                for enemy in enemy_group[:]:
                    if enemy.collide(bullet):
                        player.bullets.remove(bullet)
                        break
            for boss in single_enemies:
                if hasattr(boss, "is_dead") and not boss.is_dead and boss.collide(bullet):
                    player.bullets.remove(bullet)
                    break

        for missile in player.missiles[:]:
            for enemy_group in group_enemies:
                for enemy in enemy_group[:]:
                    if enemy.collide_missile(missile):
                        player.missiles.remove(missile)
                        break
            for boss in single_enemies:
                if hasattr(boss, "is_dead") and not boss.is_dead and boss.collide_missile(missile):
                    player.missiles.remove(missile)
                    break

        # Add home_missiles, nuclear, etc in the same way if present in your player

        # --- Pet laser collision (if using laser) ---
          # Pet laser handles damage

        # --- Enemy bullets vs player/pet shields ---
        for enemy_group in group_enemies:
            for enemy in enemy_group:
                if hasattr(enemy, "check_bullet_collisions"):
                    enemy.check_bullet_collisions()
                if hasattr(pet, "handle_enemy_laser_collision") and hasattr(enemy, "bullets"):
                    pet.handle_enemy_laser_collision(enemy.bullets)
        for boss in single_enemies:
            if hasattr(pet, "handle_enemy_laser_collision") and hasattr(boss, "bullets"):
                pet.handle_enemy_laser_collision(boss.bullets)


        # Drawing
        screen.screen.fill((0, 0, 0))
        screen.update_screen()
        pet.draw(screen.screen)
        enemy_manager.draw(screen.screen)  # Draw all enemies/bosses
        player.draw(screen.screen)
        gla_timer.draw(screen.screen)
        # ...
        if pet.laser_active:
            all_targets = []
            for group in group_enemies:
                all_targets.extend(group)
            all_targets.extend(single_enemies)
            pet.draw_laser(screen.screen, all_targets)
        draw_hud(screen.screen, player, pet)

        pygame.display.flip()
        clock.tick(60)