
# 🚀 Astro Avenger — Game-Driven Research Environment

Astro Avenger is a Python–Pygame based 2D space-combat game that also serves as a research platform for experimenting with AI behavior, human–machine interaction, and reinforcement-learning-inspired mechanics.

The project blends classic arcade gameplay with modular enemy dynamics, multi-agent interactions, and advanced combat systems (lasers, shields, bosses), making it suitable both as a playable game and a testbed for AI research.

## 🎮 Game Overview

You control a player spacecraft assisted by an intelligent companion pet ship, battling multiple enemy factions and bosses in a vertically scrolling space environment.

### Core Gameplay Features

* Smooth vertical scrolling background

* Player ship with:

    * Multiple bullet types

    * Missiles

    * Health & lives

* AI-controlled Pet Ship with:

    * Independent movement

    * Rotational control

    * Laser weapon

    * Rechargeable shield system

* Diverse enemy types:

    * Scrappers

    * Decepticons

    * Doublers

    * Predator boss

    * DiamondHead boss

    * YellowBoss (laser & vibration waves)

* Explosions, animations, health bars, HUD


## 🧠 Research Motivation

This project is not just a game.

Astro Avenger is designed as a controlled simulation environment to study:

* Human–AI cooperation (Player + Pet dynamics)

* Agent behavior design

* Combat decision-making

* Multi-agent interaction patterns

* Foundations for Reinforcement Learning (RL) environments

Future research directions include:

* RL-controlled enemies

* Language-guided agents

* Behavior cloning from player data

* Transition to 3D environments (Unity / PyBullet)


## 🏗️ Folder Structure
```bash
astro_avengers/
│
├── assets/                  # Images, sprites, bullets, explosions
│
├── player.py                # Player ship logic
├── enemyManager.py 
├── enemyflight.py           # Basic enemy flight logic
├── scrappers.py             # Scrapper enemy group
├── doubler.py               # Doubler enemy group
├── decepticons.py           # Decepticon enemy group
├── predator.py              # Predator boss
├── enemyColony.py           # DiamondHead boss
├── yellowBoss.py            # YellowBoss (laser + waves)
│
├── bullet.py                # All bullet & projectile types
├── missile.py               # Missile logic
├── explosion.py             # Explosion animations
├── gla.py                   # Shield, life, ammo pickups
├── screen.py                # Main game loop & rendering
├── timing.py 
├── const.py                 # Constants & assets
├── game.py                  # Entry point
│
└── README.md
```

## 🕹️ Controls
### Player
| **Key** | **Action** |
|---------|-------------|
| W A S D | Move Player |
|Right Ctrl | Fire Bullet |
|Space | Fire Missile |
|Tab	| Change bullet type |
|Q	| Change missile type|


### Pet Ship
| **Key** |	**Action** |
|---------|-------------|
|← / →	| Rotate pet|
|↑ / ↓	| Move pet |
|Left Ctrl	| Shoot|
|M	| Fire laser |
|B	| Activate shield |


## 🖥️ Requirements

* Python 3.8+
* Pygame

Install dependencies:
```bash
pip install pygame
```

▶️ How to Run the Game
1. Clone the repository:
```bash
git clone https://github.com/MorningStarTM/Project-AlphaPet.git
cd astro-avengers
```


2. Ensure asset paths are correct inside const.py

3. Run the game:
```bash
python -m astro_avengers.game
```


## 👤 Author

Ernest (K. J. Ernest Paul)\
Machine Learning Engineer | AI Research Enthusiast\
Focus: RL, Agent Systems, Human–AI Interaction

## 📜 License

This project is released for research and educational purposes.
Commercial use requires permission.