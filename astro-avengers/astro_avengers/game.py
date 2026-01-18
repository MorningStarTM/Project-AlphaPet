# main_game.py
import sys
import pygame

from astro_avengers.screen import Screen, draw_hud
from astro_avengers.player import Player
from astro_avengers.pet import NewPet

from astro_avengers.enemy_manager import EnemyManager
from astro_avengers.timing import GLATimer
from astro_avengers.gla import check_gla_collisions


def clamp_fps(clock, fps=60):
    dt = clock.tick(fps)
    return dt / 1000.0


def iter_enemy_projectiles(enemy):
    """
    Normalize projectiles across your different enemy implementations.

    Returns a list of "projectile objects" that at least have:
      - rect (pygame.Rect)
    And optionally:
      - update(), draw()
    """
    projs = []

    # Many enemies use pygame.sprite.Group() named bullets
    if hasattr(enemy, "bullets"):
        b = enemy.bullets
        if isinstance(b, pygame.sprite.Group):
            projs.extend(list(b.sprites()))
        elif isinstance(b, list):
            projs.extend(b)

    # Some bosses/enemies have missiles list (DiamondHead has missiles)
    if hasattr(enemy, "missiles"):
        m = enemy.missiles
        if isinstance(m, list):
            projs.extend(m)

    # Some enemies have lasers stored differently; you already handle lasers by
    # directly reducing player health inside enemy.draw_laser(). So we won't treat
    # lasers as projectiles here.

    return projs


def damage_player_if_hit_by_projectiles(player, pet, enemies):
    """
    Applies damage if player is hit by enemy bullets/missiles.
    Also lets pet shield remove bullets when active (per your pet implementation).
    """
    # Pet shield collision needs a "group-like" object with .enemies list
    # Your pet.handle_shield_collision expects enemies.enemies and enemy.bullets
    # So we will call it for group types only when possible in main loop (below).

    # Direct hit on player from any enemy projectile
    for enemy in enemies:
        for proj in iter_enemy_projectiles(enemy):
            if hasattr(proj, "rect") and player.rect.colliderect(proj.rect):
                # lightweight, consistent damage
                player.health -= 2

                # remove projectile safely
                if isinstance(getattr(enemy, "bullets", None), pygame.sprite.Group):
                    enemy.bullets.remove(proj)
                else:
                    # list-style projectiles
                    if hasattr(enemy, "bullets") and isinstance(enemy.bullets, list) and proj in enemy.bullets:
                        enemy.bullets.remove(proj)
                    if hasattr(enemy, "missiles") and isinstance(enemy.missiles, list) and proj in enemy.missiles:
                        enemy.missiles.remove(proj)


def handle_player_projectiles_vs_enemies(player, pet, active_group_enemies, active_single_enemies):
    """
    Player bullets/missiles damage enemies.
    Pet bullets damage enemies.
    Pet laser damages enemies (your pet.draw_laser already reduces health and removes dead enemies).
    """

    # ---- Player bullets ----
    for bullet in player.bullets[:]:
        hit = False

        # group enemies
        for enemy_list in active_group_enemies:
            for e in enemy_list[:]:
                if hasattr(e, "collide") and e.collide(bullet):
                    hit = True
                    break
            if hit:
                break

        # bosses (single enemies)
        if not hit:
            for boss in active_single_enemies:
                if hasattr(boss, "is_dead") and boss.is_dead:
                    continue
                if hasattr(boss, "collide") and boss.collide(bullet):
                    hit = True
                    break

        if hit and bullet in player.bullets:
            player.bullets.remove(bullet)

    # ---- Player missiles ----
    for missile in player.missiles[:]:
        hit = False

        for enemy_list in active_group_enemies:
            for e in enemy_list[:]:
                # some enemies only have collide(), some may have collide_missile()
                if hasattr(e, "collide_missile"):
                    if e.collide_missile(missile):
                        hit = True
                        break
                elif hasattr(e, "collide"):
                    if e.collide(missile):
                        hit = True
                        break
            if hit:
                break

        if not hit:
            for boss in active_single_enemies:
                if hasattr(boss, "is_dead") and boss.is_dead:
                    continue
                if hasattr(boss, "collide_missile"):
                    if boss.collide_missile(missile):
                        hit = True
                        break
                elif hasattr(boss, "collide"):
                    if boss.collide(missile):
                        hit = True
                        break

        if hit and missile in player.missiles:
            player.missiles.remove(missile)

    # ---- Pet bullets (sprite group) ----
    for pb in list(pet.bullets.sprites()):
        hit = False
        for enemy_list in active_group_enemies:
            for e in enemy_list[:]:
                if hasattr(e, "rect") and e.rect.colliderect(pb.rect):
                    if hasattr(e, "health"):
                        e.health -= 10
                    hit = True
                    break
            if hit:
                break

        if not hit:
            for boss in active_single_enemies:
                if hasattr(boss, "rect") and boss.rect.colliderect(pb.rect):
                    if hasattr(boss, "health"):
                        boss.health -= 10
                    hit = True
                    break

        if hit:
            pb.kill()

    # ---- Pet laser ----
    # Damage is handled inside pet.draw_laser(win, enemies),
    # so we just ensure we pass the correct targets in draw step.


def collect_active_targets(enemy_manager):
    """
    Returns:
      - group_enemies: list[list[enemy]]
      - single_enemies: list[enemy] (bosses)
      - all_enemies_flat: list[enemy]
    """
    group_enemies = []
    for gname in enemy_manager.active_groups:
        g = enemy_manager.groups[gname]
        if hasattr(g, "enemies"):
            group_enemies.append(g.enemies)

    single_enemies = []
    for bname in enemy_manager.active_bosses:
        b = enemy_manager.bosses[bname]
        # some bosses have is_dead
        if hasattr(b, "is_dead") and b.is_dead:
            continue
        single_enemies.append(b)

    all_enemies_flat = []
    for glist in group_enemies:
        all_enemies_flat.extend(glist)
    all_enemies_flat.extend(single_enemies)

    return group_enemies, single_enemies, all_enemies_flat


def reset_game():
    screen = Screen()
    player = Player()
    pet = NewPet()
    enemy_manager = EnemyManager(player)
    gla_timer = GLATimer()
    return screen, player, pet, enemy_manager, gla_timer


def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen, player, pet, enemy_manager, gla_timer = reset_game()

    running = True
    paused = False
    game_over = False

    # Small helper so shield toggle doesn’t spam
    shield_toggle_latch = False

    while running:
        dt = clamp_fps(clock, fps=60)

        # -------- events --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

                if game_over and event.key == pygame.K_r:
                    screen, player, pet, enemy_manager, gla_timer = reset_game()
                    game_over = False
                    paused = False

                if not paused and not game_over:
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

        keys = pygame.key.get_pressed()

        if not paused and not game_over:
            # -------- movement/input --------
            dx = dy = 0
            if keys[pygame.K_a]:
                dx -= player.speed
            if keys[pygame.K_d]:
                dx += player.speed
            if keys[pygame.K_w]:
                dy -= player.speed
            if keys[pygame.K_s]:
                dy += player.speed
            player.move(dx, dy)

            # pet rotate/move
            if keys[pygame.K_LEFT]:
                pet.rotate(left=True)
            if keys[pygame.K_RIGHT]:
                pet.rotate(right=True)
            if keys[pygame.K_UP]:
                pet.move_forward()
            if keys[pygame.K_DOWN]:
                pet.move_backward()

            # pet shield toggle (single press)
            if keys[pygame.K_b]:
                if not shield_toggle_latch:
                    pet.toggle_shield()
                shield_toggle_latch = True
            else:
                shield_toggle_latch = False

            # pet laser hold
            pet.fire_laser(bool(keys[pygame.K_m]))

            # -------- update --------
            player.update()
            pet.update()
            enemy_manager.update()
            gla_timer.update()

            # GLA pickups (correct signature: player, shields, lives, ammunitions)
            check_gla_collisions(player, pet, gla_timer.shields, gla_timer.lives, gla_timer.ammunitions)

            # -------- collision sets --------
            group_enemies, single_enemies, all_enemies = collect_active_targets(enemy_manager)

            # Player/Pet attacks → enemies
            handle_player_projectiles_vs_enemies(player, pet, group_enemies, single_enemies)

            # Pet shield removes bullets from GROUP enemies (your pet code expects enemies.enemies)
            for gname in enemy_manager.active_groups:
                grp = enemy_manager.groups[gname]
                # only if group has .enemies and enemies have .bullets groups
                if hasattr(grp, "enemies"):
                    pet.handle_shield_collision(grp)

            # Enemy projectiles → player
            damage_player_if_hit_by_projectiles(player, pet, all_enemies)

            # Some enemies have internal bullet collision checks (Predator does)
            for e in all_enemies:
                if hasattr(e, "check_bullet_collisions"):
                    e.check_bullet_collisions()

            # -------- game over condition --------
            if player.health <= 0:
                game_over = True

        # -------- draw --------
        screen.screen.fill((0, 0, 0))
        screen.update_screen()

        # Draw entities
        pet.draw(screen.screen)
        enemy_manager.draw(screen.screen)
        player.draw(screen.screen)
        gla_timer.draw(screen.screen)

        # Pet laser render + damage (pass every active target)
        if pet.laser_active:
            _, _, all_enemies = collect_active_targets(enemy_manager)
            pet.draw_laser(screen.screen, all_enemies)

        # HUD
        draw_hud(screen.screen, player, pet)

        # overlays
        if paused:
            font = pygame.font.SysFont(None, 64)
            txt = font.render("PAUSED", True, (255, 255, 255))
            screen.screen.blit(txt, (screen.screen.get_width() // 2 - txt.get_width() // 2, 200))

        if game_over:
            font = pygame.font.SysFont(None, 64)
            txt = font.render("GAME OVER", True, (255, 80, 80))
            screen.screen.blit(txt, (screen.screen.get_width() // 2 - txt.get_width() // 2, 200))

            font2 = pygame.font.SysFont(None, 32)
            txt2 = font2.render("Press R to Restart | Close window to quit", True, (255, 255, 255))
            screen.screen.blit(txt2, (screen.screen.get_width() // 2 - txt2.get_width() // 2, 270))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()