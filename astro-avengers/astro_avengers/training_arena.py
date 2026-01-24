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



if __name__ == "__main__":
    arena = Arena(fps=60)
    arena.navigation()