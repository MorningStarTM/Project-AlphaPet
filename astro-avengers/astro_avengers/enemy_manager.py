# enemy_manager.py
import pygame
from astro_avengers.timing import UniverseTimer

class EnemyManager:
    def __init__(self, player):
        self.player = player

        # Enemy groups and single bosses
        from astro_avengers.scrappers import ScrapperGroup
        from astro_avengers.doubler import DoublerGroup
        from astro_avengers.decepticons import DecepticonGroup
        from astro_avengers.enemyColony import DiamondHead
        from astro_avengers.yellowBoss import YellowBoss
        from astro_avengers.predator import Predator
        from astro_avengers.enemyflight import EnemyGroup

        # Register all types (can add more in the future)
        self.groups = {
            "enemyflight": EnemyGroup(player),
            "scrappers": ScrapperGroup(player),
            "doublers": DoublerGroup(player),
            "decepticons": DecepticonGroup(player)
        }
        # Single-instance bosses
        self.bosses = {
            "yellowboss": YellowBoss(player),
            "predator": Predator(player),
            "diamondhead":DiamondHead(player)
            # add more bosses here
        }

        # You can control "waves" and boss entry with state/logic here
        self.active_groups = []
        self.active_bosses = []

        self.timeline = [
            {"time": 3, "action": lambda: self.spawn_wave("scrappers")},
            {"time": 10, "action": lambda: self.spawn_wave("doublers")},
            {"time": 30, "action": lambda: self.spawn_wave("decepticons")},
            {"time": 650, "action": lambda: self.trigger_boss("yellowboss")},
            {"time": 350, "action": lambda: self.trigger_boss("predator")},
            {"time": 600, "action": lambda: self.trigger_boss("diamondhead")},
            # Add as many as you want
        ]
        self.timeline.sort(key=lambda x: x["time"])
        self.start_time = pygame.time.get_ticks()  # milliseconds
        self.timeline_pointer = 0
        self.universe_timer = UniverseTimer()

    def spawn_wave(self, group_name):
        """Activate a wave (group) by name."""
        if group_name in self.groups and group_name not in self.active_groups:
            self.active_groups.append(group_name)

    def trigger_boss(self, boss_name):
        """Activate a boss by name."""
        if boss_name in self.bosses and boss_name not in self.active_bosses:
            self.active_bosses.append(boss_name)

    def update(self):
        # Check and trigger timeline events
        now_seconds = (pygame.time.get_ticks() - self.start_time) / 1000
        while (self.timeline_pointer < len(self.timeline) and 
               now_seconds >= self.timeline[self.timeline_pointer]["time"]):
            self.timeline[self.timeline_pointer]["action"]()
            self.timeline_pointer += 1
        
        for group_name in self.active_groups:
            grp = self.groups[group_name]
            if hasattr(grp, "update"):
                grp.update()

        for boss_name in self.active_bosses:
            boss = self.bosses[boss_name]
            if hasattr(boss, "update"):
                boss.update()

        # keep your timer logic last (or first, doesn’t matter)
        self.universe_timer.update(self)


    def draw(self, screen):
        for group in self.active_groups:
            self.groups[group].draw(screen)
        for boss in self.active_bosses:
            self.bosses[boss].draw(screen)

    def get_all_enemies(self):
        """Return flat list of all active enemies (for collision, etc)."""
        enemies = []
        for group in self.active_groups:
            enemies.extend(self.groups[group].enemies)
        for boss in self.active_bosses:
            enemies.append(self.bosses[boss])
        return enemies

    # Add more methods for enemy attack coordination, event triggers, etc.
