import random
import pygame
from astro_avengers.gla import Shield, Life, Ammunition



class GLATimer:
    def __init__(self):
        self.spawn_interval_shield = 800  # frames
        self.spawn_interval_life = 600    # frames
        self.spawn_interval_ammunition = 300  # frames

        self.shield_timer = 0
        self.life_timer = 0
        self.ammunition_timer = 0

        self.shields = []
        self.lives = []
        self.ammunitions = []


    def update(self):
        self.shield_timer += 1
        self.life_timer += 1
        self.ammunition_timer += 1

        if self.shield_timer >= self.spawn_interval_shield:
            self.shields.append(Shield())
            self.shield_timer = 0

        if self.life_timer >= self.spawn_interval_life:
            self.lives.append(Life())
            self.life_timer = 0

        if self.ammunition_timer >= self.spawn_interval_ammunition:
            self.ammunitions.append(Ammunition())
            self.ammunition_timer = 0

        # Update positions
        for shield in self.shields:
            shield.update()
        for life in self.lives:
            life.update()
        for ammunition in self.ammunitions:
            ammunition.update()
            

    def draw(self, screen):
        for shield in self.shields:
            shield.draw(screen)
        for life in self.lives:
            life.draw(screen)
        for ammunition in self.ammunitions:
            ammunition.draw(screen)



class UniverseTimer:
    def __init__(self, timeline=None):
        self.timeline = timeline if timeline is not None else self.default_timeline()
        self.timeline.sort(key=lambda event: event["time"])

        self.start_time_ms = pygame.time.get_ticks()
        self.timeline_pointer = 0

    def reset(self):
        self.start_time_ms = pygame.time.get_ticks()
        self.timeline_pointer = 0

    def update(self, enemy_manager):
        now_seconds = (pygame.time.get_ticks() - self.start_time_ms) / 1000
        while (
            self.timeline_pointer < len(self.timeline)
            and now_seconds >= self.timeline[self.timeline_pointer]["time"]
        ):
            event = self.timeline[self.timeline_pointer]
            event_type = event.get("type")
            name = event.get("name")

            if event_type == "wave":
                enemy_manager.spawn_wave(name)
            elif event_type == "boss":
                enemy_manager.trigger_boss(name)
            else:
                action = event.get("action")
                if action is not None:
                    action()

            self.timeline_pointer += 1

    @staticmethod
    def default_timeline():
        return [
            {"time": 1, "type": "wave", "name": "enemyflight"},
            {"time": 3, "type": "wave", "name": "scrappers"},
            {"time": 10, "type": "wave", "name": "doublers"},
            {"time": 30, "type": "wave", "name": "decepticons"},
            {"time": 350, "type": "boss", "name": "predator"},
            {"time": 600, "type": "boss", "name": "diamondhead"},
            {"time": 650, "type": "boss", "name": "yellowboss"},
        ]
