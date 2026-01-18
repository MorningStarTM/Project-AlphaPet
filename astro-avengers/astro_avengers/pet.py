from astro_avengers.const import *
from astro_avengers.bullet import Bullet, ImageEnemyBullet, PetBullet
import math

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
        self.START_POS = (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT-50)
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
        self.laser_damage = 5
        self.laser_bar_full = 100  # Full state of the laser bar
        self.laser_bar = self.laser_bar_full  # Current state of the laser bar
        self.laser_usage_rate = 1  # How fast the laser bar drains
        self.laser_recovery_rate = 0.5  

        # Shield-related properties
        self.shield_active = False
        self.shield_duration = 300  # How long the shield stays active (in frames)
        self.shield_timer = self.shield_duration  # Timer to control shield deactivation
        self.shield_color = (182, 221, 222)  # Gray color
        self.shield_radius = 70  # Radius for the shield's arc
        self.shield_thickness = 8  # Thickness of the shield
        self.shield_bar_full = 100  # The full state of the shield's time bar
        self.shield_bar = self.shield_bar_full  # Current state of the shield's time bar
        self.shield_toggle = False  

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

        # Draw laser if active
        #if self.laser_active:
        #    self.draw_laser(win)

        if self.shield_active:
            self.draw_shield(win)
        
        #self.draw_laser_bar(win)


    def draw_shield(self, win):
        """Draw the shield around the pet if it's active."""
        if self.shield_active:
            pygame.draw.circle(
                win, self.shield_color, (int(self.x), int(self.y)), 
                self.shield_radius, self.shield_thickness
            )

    def toggle_shield(self):
        """Toggles the shield on/off if the time bar is full."""
        if self.shield_bar >= self.shield_bar_full or self.shield_active:
            self.shield_active = not self.shield_active
            if self.shield_active:
                self.shield_timer = 0  # Reset the shield timer when activated
            print("Shield active:", self.shield_active)


    def activate_shield(self):
        """Activates the shield if the time bar is full."""
        if self.shield_bar >= self.shield_bar_full:
            self.shield_active = True
            self.shield_timer = 0  # Reset the shield timer

    def update_shield(self):
        """Handles the shield's state and deactivation based on time."""
        if self.shield_active:
            self.shield_timer += 1
            if self.shield_timer >= self.shield_duration:
                self.shield_active = False  # Deactivate shield after duration
                self.shield_bar = 0  # Reset shield bar after usage

        # Gradually refill the shield bar if it's not full
        if self.shield_bar < self.shield_bar_full:
            self.shield_bar += 1  # Refill the shield bar over time

    
    def handle_shield_collision(self, enemies):
        """Check if enemy bullets or lasers collide with the shield and remove them."""
        if self.shield_active:
            shield_rect = pygame.Rect(
                self.rect.centerx - self.shield_radius,
                self.rect.centery - self.shield_radius,
                self.shield_radius * 2,
                self.shield_radius * 2
            )

            # Check collision for enemy bullets
            for enemy in enemies.enemies[:]:
                for bullet in enemy.bullets[:]:
                    if shield_rect.colliderect(bullet.rect):
                        enemy.bullets.remove(bullet)
                        print("Bullet hit the shield!")



    def handle_kills(self, enemies):
        """Refill the shield bar when the pet or player kills enemies."""
        for enemy in enemies:
            if enemy.health <= 0:
                self.shield_bar += 20  # Increase shield bar for each enemy killed
                self.shield_bar = min(self.shield_bar, self.shield_bar_full)  # Cap the bar at max

    def handle_input(self, keys):
        """Handle player input, including shield activation."""
        if keys[pygame.K_b]:
            if not self.shield_toggle:  # Prevent holding down the key from toggling repeatedly
                self.toggle_shield()
            self.shield_toggle = True
        else:
            self.shield_toggle = False

    def handle_enemy_laser_collision(self, enemy_lasers):
        """
        Handles enemy lasers colliding with the pet's shield and stops them at the shield's boundary.
        """
        if self.shield_active:
            # Define the shield's boundary as a circle around the pet
            shield_center = self.rect.center
            shield_radius = self.shield_radius

            for laser in enemy_lasers:
                # Laser start and end positions
                laser_start = laser.start_pos  # Starting position of the laser
                laser_end = laser.end_pos  # Current end position of the laser

                # Calculate the intersection between the laser and the shield
                intersection = self.get_laser_shield_intersection(shield_center, shield_radius, laser_start, laser_end)

                # If the laser intersects the shield, truncate it at the intersection point
                if intersection:
                    laser.end_pos = intersection

    
    def get_laser_shield_intersection(self, shield_center, shield_radius, laser_start, laser_end):
        """Calculate the intersection point between the laser and the shield circle.
        
        If the laser intersects the shield, return the point where it hits the shield.
        Otherwise, return None.
        """
        cx, cy = shield_center  # Center of the shield (pet position)
        lx1, ly1 = laser_start  # Start of the laser
        lx2, ly2 = laser_end  # End of the laser

        # Vector from the laser start to end
        dx, dy = lx2 - lx1, ly2 - ly1

        # Quadratic coefficients
        a = dx**2 + dy**2
        b = 2 * (dx * (lx1 - cx) + dy * (ly1 - cy))
        c = (lx1 - cx)**2 + (ly1 - cy)**2 - shield_radius**2

        # Solve the quadratic equation for t
        discriminant = b**2 - 4 * a * c
        if discriminant >= 0:
            # There are two possible intersection points
            t1 = (-b - math.sqrt(discriminant)) / (2 * a)
            t2 = (-b + math.sqrt(discriminant)) / (2 * a)

            # Check if either t is in the range [0, 1], which means the intersection is on the laser segment
            if 0 <= t1 <= 1:
                intersection_x = lx1 + t1 * dx
                intersection_y = ly1 + t1 * dy
                return (intersection_x, intersection_y)
            elif 0 <= t2 <= 1:
                intersection_x = lx1 + t2 * dx
                intersection_y = ly1 + t2 * dy
                return (intersection_x, intersection_y)

        # No intersection
        return None

    """def draw_laser(self, win):
        #Draws the laser from the pet to the edge of the screen.
        radians = math.radians(self.angle+180)  # Convert angle to radians
        # Calculate the end position of the laser based on angle
        laser_end_x = self.x + math.sin(radians) * self.laser_length
        laser_end_y = self.y + math.cos(radians) * self.laser_length
        pygame.draw.line(win, self.laser_color, (self.x, self.y), (laser_end_x, laser_end_y), self.laser_width)"""
    
    def draw_laser(self, win, enemies):
        """Draw the laser from the pet and check for collisions with enemies or the shield."""
        radians = math.radians(self.angle + 180)  # Convert angle to radians

        # Calculate the end position of the laser based on angle
        laser_end_x = self.x + math.sin(radians) * self.laser_length
        laser_end_y = self.y + math.cos(radians) * self.laser_length

        # If shield is active, check if the laser hits the shield
        if self.shield_active:
            laser_end_x, laser_end_y = self.get_laser_shield_intersection(
                (self.x, self.y), self.shield_radius, (self.x, self.y), (laser_end_x, laser_end_y)
            )

        # Draw the laser
        pygame.draw.line(win, self.laser_color, (self.x, self.y), (laser_end_x, laser_end_y), self.laser_width)

        # Check for collisions with enemies
        self.check_laser_collision(enemies, (self.x, self.y), (laser_end_x, laser_end_y))

        

    """def check_laser_collision(self, enemies, laser_start, laser_end):
        Check if the laser hits any enemies and reduce their health.
        for enemy in enemies:
            # Check if the laser line intersects the enemy's rect
            if enemy.rect.clipline(laser_start, laser_end):
                enemy.health -= self.laser_damage

                # If enemy's health is zero or less, destroy the enemy
                if enemy.health <= 0:
                    enemies.remove(enemy)  # Remove the enemy from the game"""
    
    def check_laser_collision(self, enemies, laser_start, laser_end):
        """Pixel-perfect check if the laser hits any enemies or protectors and reduces their health."""
        laser_dx = laser_end[0] - laser_start[0]
        laser_dy = laser_end[1] - laser_start[1]
        laser_length = int(math.hypot(laser_dx, laser_dy))
        steps = laser_length

        for enemy in enemies[:]:
            # Ensure the object has .rect, .mask, and .health
            if not hasattr(enemy, 'rect') or not hasattr(enemy, 'mask') or not hasattr(enemy, 'health'):
                continue

            for i in range(steps):
                check_x = int(laser_start[0] + (laser_dx * i / steps))
                check_y = int(laser_start[1] + (laser_dy * i / steps))

                offset_x = check_x - enemy.rect.left
                offset_y = check_y - enemy.rect.top

                if 0 <= offset_x < enemy.rect.width and 0 <= offset_y < enemy.rect.height:
                    try:
                        if enemy.mask.get_at((offset_x, offset_y)):
                            enemy.health -= self.laser_damage
                            if hasattr(enemy, 'vanish') and enemy.health <= 0:
                                enemy.vanish()  # protectorShip
                            elif enemy.health <= 0:
                                enemies.remove(enemy)  # Mark as dead, group will remove!
                                if hasattr(enemy, "trigger_explosion"):
                                    enemy.trigger_explosion()
                            break
                    except IndexError:
                        continue

    """def check_laser_collision(self, enemies, laser_start, laser_end):
        Pixel-perfect check if the laser hits any enemies and reduce their health
        laser_dx = laser_end[0] - laser_start[0]
        laser_dy = laser_end[1] - laser_start[1]
        laser_length = int(math.hypot(laser_dx, laser_dy))
        steps = laser_length  # One check per pixel

        for enemy in enemies[:]:  # Copy to allow safe removal
            if not hasattr(enemy, "mask"):
                continue  # Skip if enemy has no mask (safety)

            for i in range(steps):
                # Get the current point along the laser line
                check_x = int(laser_start[0] + (laser_dx * i / steps))
                check_y = int(laser_start[1] + (laser_dy * i / steps))

                offset_x = check_x - enemy.rect.left
                offset_y = check_y - enemy.rect.top

                # Ensure offset is within bounds of the enemy's mask
                if (0 <= offset_x < enemy.rect.width) and (0 <= offset_y < enemy.rect.height):
                    try:
                        if enemy.mask.get_at((offset_x, offset_y)):
                            enemy.health -= self.laser_damage
                            if enemy.health <= 0:
                                enemies.remove(enemy)
                            break  # Stop checking this enemy after a hit
                    except IndexError:
                        continue  # Just in case something slips through"""



    def check_laser_shield_collision(self, laser_start, laser_end):
        """Check if the laser hits the shield and stop the laser at the shield's edge."""
        # Calculate the distance from the pet to the laser end point
        laser_distance = math.sqrt((laser_end[0] - self.x) ** 2 + (laser_end[1] - self.y) ** 2)
        
        # If the laser end point is inside the shield radius, adjust it to stop at the shield
        if laser_distance < self.shield_radius:
            angle_to_laser = math.atan2(laser_end[1] - self.y, laser_end[0] - self.x)
            laser_end_x = self.x + math.cos(angle_to_laser) * self.shield_radius
            laser_end_y = self.y + math.sin(angle_to_laser) * self.shield_radius
            return laser_end_x, laser_end_y

        return laser_end  # No collision, return original end point


    def handle_enemy_laser_collision_(self, enemy_lasers):
        """Handle enemy lasers colliding with the shield."""
        for laser in enemy_lasers:
            laser_start = laser.start_pos  # Starting point of the laser
            laser_end = laser.end_pos  # Current end point of the laser

            # If shield is active, check for collision with shield
            if self.shield_active:
                new_laser_end_x, new_laser_end_y = self.get_laser_shield_intersection(
                    (self.x, self.y), self.shield_radius, laser_start, laser_end
                )

                # Update the laser's endpoint to stop at the shield if it collides
                laser.end_pos = (new_laser_end_x, new_laser_end_y)

            # If laser is now short (due to shield collision), remove it
            if math.dist(laser.start_pos, laser.end_pos) < self.shield_radius:
                enemy_lasers.remove(laser)  # Remove laser as it hit the shield



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
        self.update_shield()

        if not self.laser_active and self.laser_bar < self.laser_bar_full:
            self.laser_bar += self.laser_recovery_rate
            self.laser_bar = min(self.laser_bar, self.laser_bar_full)

    def fire_laser(self, is_firing):
        if is_firing and self.laser_bar > 0:
            self.laser_active = True
            self.laser_bar -= self.laser_usage_rate
            self.laser_bar = max(self.laser_bar, 0)  # Ensure it doesn't go below 0
        else:
            self.laser_active = False  # Force laser to stop when empty

        # If laser bar is empty, prevent firing
        if self.laser_bar <= 0:
            self.laser_active = False




    def draw_laser_bar(self, win):
        bar_width = 100
        bar_height = 10
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 15

        # Background bar
        pygame.draw.rect(win, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        # Current laser level
        pygame.draw.rect(win, (232, 81, 94), (bar_x, bar_y, int((self.laser_bar / self.laser_bar_full) * bar_width), bar_height))




def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center
    )
    win.blit(rotated_image, new_rect.topleft)