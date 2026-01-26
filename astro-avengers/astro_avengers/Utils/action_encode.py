# action_codec.py

import numpy as np

class MultiBinaryActionCodec:
    """
    Encodes/decodes multi-key actions:
    action_vec = [LEFT, RIGHT, UP, DOWN, ...] where each element is 0/1.
    """

    def __init__(self, buttons):
        """
        buttons: list[str] e.g. ["LEFT","RIGHT","UP","DOWN"]
        """
        self.buttons = list(buttons)
        self.index = {b: i for i, b in enumerate(self.buttons)}
        self.n = len(self.buttons)

    def encode_from_keys(self, keys, pygame):
        """
        keys: pygame.key.get_pressed()
        returns: np.ndarray shape (n,), dtype uint8
        """
        a = np.zeros((self.n,), dtype=np.uint8)

        # Movement keys (add more if you add more buttons)
        if "LEFT" in self.index and keys[pygame.K_a]:
            a[self.index["LEFT"]] = 1
        if "RIGHT" in self.index and keys[pygame.K_d]:
            a[self.index["RIGHT"]] = 1
        if "UP" in self.index and keys[pygame.K_w]:
            a[self.index["UP"]] = 1
        if "DOWN" in self.index and keys[pygame.K_s]:
            a[self.index["DOWN"]] = 1

        if "SHOOT" in self.index and keys[pygame.K_LCTRL]:
            a[self.index["SHOOT"]] = 1
        if "SHIELD" in self.index and keys[pygame.K_c]:
            a[self.index["SHIELD"]] = 1
        if "LASER" in self.index and keys[pygame.K_x]:
            a[self.index["LASER"]] = 1

        return a

    def sanitize(self, a):
        """
        Resolve impossible combos, e.g. LEFT+RIGHT both pressed.
        a can be list/np array.
        """
        a = np.asarray(a, dtype=np.uint8).copy()

        # If both left and right pressed, cancel both (or choose one policy)
        li = self.index.get("LEFT", None)
        ri = self.index.get("RIGHT", None)
        if li is not None and ri is not None and a[li] == 1 and a[ri] == 1:
            a[li] = 0
            a[ri] = 0

        ui = self.index.get("UP", None)
        di = self.index.get("DOWN", None)
        if ui is not None and di is not None and a[ui] == 1 and a[di] == 1:
            a[ui] = 0
            a[di] = 0

        return a

    def apply_to_pet(self, pet, a):
        """
        Apply the action vector to your pet.
        """
        a = self.sanitize(a)

        if "LEFT" in self.index and a[self.index["LEFT"]]:
            pet.rotate(left=True)
        if "RIGHT" in self.index and a[self.index["RIGHT"]]:
            pet.rotate(right=True)
        if "UP" in self.index and a[self.index["UP"]]:
            pet.move_forward()
        if "DOWN" in self.index and a[self.index["DOWN"]]:
            pet.move_backward()

        if "SHOOT" in self.index and a[self.index["SHOOT"]]:
            pet.shoot()  # only if you have it
        if "SHIELD" in self.index and a[self.index["SHIELD"]]:
            pet.activate_shield()  # only if you have it
        if "LASER" in self.index:
            pet.fire_laser(bool(a[self.index["LASER"]]))  # hold to fire laser
        else:
            pet.fire_laser(False)
