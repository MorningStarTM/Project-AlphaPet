import re
import pygame
from astro_avengers.const import *
from astro_avengers.pet import NewPet
from astro_avengers.Utils.data_recorder import DataRecorder
from astro_avengers.Utils.command_ui import SimpleCommandUI


class Arena:
    """
    Common class to run different training cases.
    For now: navigation only (empty map).
    """
    def __init__(self, fps=60):
        pygame.init()
        self.fps = fps
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Training Area - Navigation")

        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 36)

        self.pet = NewPet()  # starts at your START_POS
        self.recorder = DataRecorder()
        self.recorder.save_every_n_frames = 4

    def _draw_status(self, command_text):
        # top-left HUD
        lines = [
            f"Command: {command_text}",
            "Controls: LEFT/RIGHT rotate, UP/DOWN move",
            "ENTER = finish + save CSV, ESC = quit (no save)",
        ]
        y = 10
        for line in lines:
            surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(surf, (10, y))
            y += 22

    def navigation(self):
        """
        Navigation scenario:
        - Empty map
        - Only pet
        - Collect trajectories until ENTER is pressed
        """
        running = True
        collecting = False
        command_text = ""

        cmd_ui = SimpleCommandUI(self.big_font)

        while running:
            dt_ms = self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not collecting:
                    res = cmd_ui.handle_event(event)
                    if res and res[0] == "set_command":
                        command_text = (res[1] or "").strip()
                    if res and res[0] == "start":
                        command_text = (res[1] or "").strip()
                        if command_text:
                            collecting = True
                            self.recorder.start_episode(command_text)

                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # quit without save
                            running = False
                        elif event.key == pygame.K_RETURN:
                            # finish + save
                            saved_path = self.recorder.save_csv()
                            print("Saved trajectory:", saved_path)
                            running = False

            self.screen.fill((0, 0, 0))  # empty map background

            if not collecting:
                # command selection screen
                title = self.big_font.render("Navigation Training", True, (255, 255, 255))
                self.screen.blit(title, (40, 10))
                cmd_ui.draw(self.screen)
                pygame.display.flip()
                continue

            # ========== collecting mode ==========
            keys = pygame.key.get_pressed()

            # Pet control (same style you already use in screen.py) :contentReference[oaicite:4]{index=4}
            if keys[pygame.K_LEFT]:
                self.pet.rotate(left=True)
            if keys[pygame.K_RIGHT]:
                self.pet.rotate(right=True)
            if keys[pygame.K_UP]:
                self.pet.move_forward()
            if keys[pygame.K_DOWN]:
                self.pet.move_backward()

            # update pet internal systems (bullets/shield timers etc.)
            self.pet.update()

            self.screen.fill((0, 0, 0))
            self.pet.draw(self.screen)
            self._draw_status(command_text)

            # --- NOW record (and screenshot) ---
            self.recorder.record(self.screen.copy(), self.pet, keys, dt_ms)

            pygame.display.flip()

        pygame.quit()



    def _obj_rect(self, obj):
        """
        Best-effort to get a pygame.Rect for collisions without changing existing classes.
        """
        r = getattr(obj, "rect", None)
        if r is not None:
            return r

        x = getattr(obj, "x", None)
        y = getattr(obj, "y", None)
        if x is None or y is None:
            return None

        img = getattr(obj, "image", None)
        if img is not None:
            w, h = img.get_width(), img.get_height()
        else:
            # fallback size if class doesn't expose image
            w, h = 32, 32

        return pygame.Rect(int(x), int(y), int(w), int(h))


    def _filter_items(self, gla_timer, target_kind: str):
        """
        target_kind: 'shield' | 'life' | 'ammo' | 'any'
        """
        if target_kind == "shield":
            return gla_timer.shields
        if target_kind == "life":
            return gla_timer.lives
        if target_kind == "ammo":
            return gla_timer.ammunitions
        # any
        return gla_timer.shields + gla_timer.lives + gla_timer.ammunitions


    def parse_catch_spec(self, command_text: str):
        """
        Examples it supports:
        "catch shield 5"
        "catch 10 ammo"
        "collect life x3"
        "catch ammunition 7"
        "catch gla 4"   -> kind='any', count=4
        "catch shield"  -> count defaults to 5
        """
        text = (command_text or "").lower()

        # kind
        kind = "any"
        if "shield" in text:
            kind = "shield"
        elif "life" in text or "health" in text:
            kind = "life"
        elif "ammo" in text or "ammunition" in text or "bullet" in text:
            kind = "ammo"
        elif "gla" in text:
            kind = "any"

        # count (first number found)
        m = re.search(r"\d+", text)
        count = int(m.group(0)) if m else 5

        # keep sane bounds
        if count < 1:
            count = 1
        if count > 999:
            count = 999

        return kind, count



    def catch_gla(self):
        """
        Catch GLA training task.
        - Empty map + pet
        - GLA items spawn fast (intervals overridden here)
        - User controls pet, must catch items (collision)
        - ENTER = finish + save CSV (+ images if your recorder saves obs_img)
        """
        import pygame
        from astro_avengers.timing import GLATimer  # do not edit timing.py

        running = True
        collecting = False
        command_text = ""

        # reuse your command UI (same as navigation)
        cmd_ui = SimpleCommandUI(self.big_font)

        # timer for GLA items
        gla_timer = GLATimer()

        # make items appear quickly (smaller = more frequent)
        gla_timer.spawn_interval_shield = 120
        gla_timer.spawn_interval_life = 90
        gla_timer.spawn_interval_ammunition = 45

        caught = 0

        while running:
            dt_ms = self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not collecting:
                    res = cmd_ui.handle_event(event)
                    if res and res[0] == "set_command":
                        command_text = (res[1] or "").strip()
                    if res and res[0] == "start":
                        command_text = (res[1] or "").strip()
                        if command_text:
                            target_kind, need_count = self.parse_catch_spec(command_text)

                            collecting = True
                            caught = 0
                            self.recorder.start_episode(command_text)

                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False  # quit without save
                        elif event.key == pygame.K_RETURN:
                            saved_path = self.recorder.save_csv()
                            print("Saved trajectory:", saved_path)
                            running = False

            # ---------- UI mode ----------
            if not collecting:
                self.screen.fill((0, 0, 0))
                title = self.big_font.render("Catch GLA Training", True, (255, 255, 255))
                self.screen.blit(title, (40, 10))
                cmd_ui.draw(self.screen)
                pygame.display.flip()
                continue

            # ---------- Collecting mode ----------
            keys = pygame.key.get_pressed()

            # pet control (same as navigation)
            if keys[pygame.K_LEFT]:
                self.pet.rotate(left=True)
            if keys[pygame.K_RIGHT]:
                self.pet.rotate(right=True)
            if keys[pygame.K_UP]:
                self.pet.move_forward()
            if keys[pygame.K_DOWN]:
                self.pet.move_backward()

            self.pet.update()

            # spawn/update items
            gla_timer.update()

            # collisions: pet vs target items
            pet_rect = self._obj_rect(self.pet)
            if pet_rect is not None:
                targets = self._filter_items(gla_timer, target_kind)

                # iterate backwards so we can pop/remove safely
                for i in range(len(targets) - 1, -1, -1):
                    item = targets[i]
                    item_rect = self._obj_rect(item)
                    if item_rect is not None and pet_rect.colliderect(item_rect):
                        targets.pop(i)
                        caught += 1

            # draw current frame FIRST
            self.screen.fill((0, 0, 0))
            gla_timer.draw(self.screen)
            self.pet.draw(self.screen)

            # HUD
            hud1 = self.font.render(f"Task: catch {target_kind} | Caught: {caught}/{need_count}", True, (255, 255, 255))
            hud2 = self.font.render("ENTER = finish + save, ESC = quit", True, (180, 180, 180))
            self.screen.blit(hud1, (10, 10))
            self.screen.blit(hud2, (10, 32))

            # record AFTER draw so screenshots aren’t black
            # (If your recorder expects .copy(), keep .copy())
            self.recorder.record(self.screen.copy(), self.pet, keys, dt_ms)

            pygame.display.flip()

            # optional: auto-finish when enough caught
            if caught >= need_count:
                saved_path = self.recorder.save_csv()
                print("Saved trajectory:", saved_path)
                running = False



if __name__ == "__main__":
    arena = Arena(fps=60)
    #arena.navigation()
    arena.catch_gla()