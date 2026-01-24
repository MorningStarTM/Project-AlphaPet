import os
import csv
import time
from datetime import datetime

import pygame


class DataRecorder:
    """
    Records trajectory per-frame and writes to CSV.
    Also saves observation images and stores image path in CSV.
    """
    def __init__(self, out_dir="data/trajectories", img_format="png", save_every_n_frames=1):
        self.out_dir = out_dir
        self.img_format = img_format
        self.save_every_n_frames = int(save_every_n_frames) if save_every_n_frames else 1

        os.makedirs(self.out_dir, exist_ok=True)
        self.reset()

    def reset(self):
        self.command_text = ""
        self.episode_id = ""
        self.start_unix = 0.0
        self.rows = []
        self.frame_idx = 0

        self.episode_dir = ""
        self.images_dir = ""

    def start_episode(self, command_text: str):
        self.reset()
        self.command_text = (command_text or "").strip()
        self.start_unix = time.time()
        self.episode_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Folder per episode
        self.episode_dir = os.path.join(self.out_dir, f"nav_{self.episode_id}")
        self.images_dir = os.path.join(self.episode_dir, "images")
        os.makedirs(self.images_dir, exist_ok=True)

    def _save_obs_image(self, screen: pygame.Surface, frame_idx: int):
        """
        Saves current screen as an observation image.
        Returns relative path to store in CSV.
        """
        img_name = f"{frame_idx:06d}.{self.img_format}"
        img_path = os.path.join(self.images_dir, img_name)

        # PNG saving (fast enough for small frames, but can be heavy at 60fps)
        pygame.image.save(screen, img_path)

        # store relative path so dataset is portable
        rel_path = os.path.relpath(img_path, self.out_dir)
        return rel_path

    def record(self, screen: pygame.Surface, pet, keys, dt_ms: int):
        """
        Record a single timestep, including observation image (optionally every N frames).
        """
        self.frame_idx += 1
        t_rel = time.time() - self.start_unix

        act_left = 1 if keys[pygame.K_LEFT] else 0
        act_right = 1 if keys[pygame.K_RIGHT] else 0
        act_forward = 1 if keys[pygame.K_UP] else 0
        act_backward = 1 if keys[pygame.K_DOWN] else 0

        obs_img = ""
        if (self.frame_idx % self.save_every_n_frames) == 0:
            obs_img = self._save_obs_image(screen, self.frame_idx)

        row = {
            "episode_id": self.episode_id,
            "command": self.command_text,
            "frame": self.frame_idx,
            "t_rel_sec": f"{t_rel:.6f}",
            "dt_ms": int(dt_ms),

            # observation reference
            "obs_img": obs_img,

            # state (optional but useful)
            "x": float(pet.x),
            "y": float(pet.y),
            "angle_deg": float(pet.angle),

            # action
            "left": act_left,
            "right": act_right,
            "forward": act_forward,
            "backward": act_backward,
        }
        self.rows.append(row)

    def save_csv(self):
        if not self.rows:
            return None

        csv_path = os.path.join(self.episode_dir, "trajectory.csv")

        fieldnames = list(self.rows[0].keys())
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.rows)

        return csv_path
