import pygame
from astro_avengers.const import SCREEN_WIDTH


class SimpleCommandUI:
    """
    In-game prompt overlay:
    - Press T to type a command (typed inside pygame window).
    - Press V to try voice (optional, uses speech_recognition if installed).
    - Press ENTER to start if a command exists.
    """
    def __init__(self, font):
        self.font = font
        self.mode = "idle"     # idle | typing | ready
        self.text = ""
        self.message = "Press T to type a command, V for voice. ENTER to start."

    def _draw_box(self, screen, x, y, w, h):
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        screen.blit(s, (x, y))
        pygame.draw.rect(screen, (200, 200, 200), (x, y, w, h), 2)

    def draw(self, screen):
        self._draw_box(screen, 40, 40, SCREEN_WIDTH - 80, 140)

        msg = self.font.render(self.message, True, (255, 255, 255))
        screen.blit(msg, (60, 60))

        cmd_label = self.font.render("Command:", True, (255, 255, 0))
        screen.blit(cmd_label, (60, 95))

        cmd_val = self.font.render(self.text if self.text else "(empty)", True, (255, 255, 255))
        screen.blit(cmd_val, (170, 95))

        hint = self.font.render("Typing: backspace to delete, ENTER to confirm.", True, (180, 180, 180))
        if self.mode == "typing":
            screen.blit(hint, (60, 125))

    def try_voice(self):
        """
        Optional voice recognition. If not available, return None.
        """
        try:
            import speech_recognition as sr
        except Exception:
            self.message = "speech_recognition not installed. Use T to type."
            return None

        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                self.message = "Listening... speak now."
                # (No blocking UI update here; simple approach)
                audio = r.listen(source, phrase_time_limit=4)
            text = r.recognize_google(audio)
            return text
        except Exception:
            self.message = "Voice failed. Use T to type."
            return None

    def handle_event(self, event):
        """
        Returns:
            ("set_command", cmd) or ("start", cmd) or None
        """
        if event.type != pygame.KEYDOWN:
            return None

        if self.mode == "idle":
            if event.key == pygame.K_t:
                self.mode = "typing"
                self.message = "Type your command, then press ENTER."
                return None
            if event.key == pygame.K_v:
                cmd = self.try_voice()
                if cmd:
                    self.text = cmd
                    self.mode = "ready"
                    self.message = "Command captured. Press ENTER to start."
                    return ("set_command", self.text)
                return None
            if event.key == pygame.K_RETURN:
                if self.text.strip():
                    return ("start", self.text)
                self.message = "No command yet. Press T to type or V for voice."
                return None

        if self.mode == "typing":
            if event.key == pygame.K_RETURN:
                self.mode = "ready" if self.text.strip() else "idle"
                self.message = "Command saved. Press ENTER to start." if self.text.strip() else "Command empty. Press T to type."
                return ("set_command", self.text)
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return None
            # basic text input (letters/numbers/space)
            if event.unicode and len(event.unicode) == 1:
                if event.unicode.isprintable():
                    self.text += event.unicode
            return None

        if self.mode == "ready":
            if event.key == pygame.K_RETURN:
                if self.text.strip():
                    return ("start", self.text)
                self.mode = "idle"
                self.message = "No command. Press T to type."
            if event.key == pygame.K_t:
                self.mode = "typing"
                self.message = "Edit your command, then press ENTER."
            return None

        return None

