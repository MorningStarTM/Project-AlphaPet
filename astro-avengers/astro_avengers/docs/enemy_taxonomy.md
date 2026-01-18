
# Astro Avenger

## Enemy & Boss
### Enemy Taxonomy (High Level)

Enemies in Astro Avenger are divided into five functional categories:

* Basic Tracking Enemies – chase and shoot the player

* Fast Melee Swarm Enemies – rush and collide

* Segment-Restricted Tactical Enemies – area control

* Elite / Mini-Boss Enemies – lasers, missiles, patterns

* Boss-Class Enemies – multi-phase, multi-weapon threats

##  1. EnemyFlight (Basic Chaser)

Role: Entry-level ranged enemy
Threat Type: Continuous pressure

Behavior

* Spawns from top of screen

* Moves directly toward player

* Fires simple bullets at fixed intervals

Stats

* Health: 100

* Speed: Low–Medium

* Weapon: Single enemy bullet

Design Purpose

* Teaches player movement

* Forces constant repositioning

## 2. Decepticon (Segment-Bound Shooter)

Role: Tactical ranged enemy
Threat Type: Zone control

Behavior

* Restricted to screen segments (Left / Center / Right)

* Rotates to face the player

* Fires DecepticonBullets toward player

* Uses explosion animation on death

Stats

* Health: 100

* Speed: Medium

* Fire Rate: Medium

Design Purpose

* Prevents safe zones

* Encourages lateral movement

## 3. Doubler (Aggressive Tracker)

Role: Precision hunter
Threat Type: Pressure escalation

Behavior

* Actively tracks player direction

* Rotates dynamically

* Fires targeted bullets

* Uses explosion sequence on death

Stats

* Health: 100

* Speed: Medium

* Fire Interval: Short

Special

* Appears in groups

* Forces multi-target prioritization

## 4. Scrapper (Melee Swarm Enemy)

Role: Close-combat disruptor
Threat Type: Collision damage

Behavior

* Rushes player at high speed

* No ranged weapons

* On collision:

   * Bounces backward

   * Pushes player

* Spawns in arc formations

* Maintains distance from other scrappers

Stats

* Health: 50

* Speed: High

* Damage: Collision-based

Design Purpose

* Breaks defensive playstyles

* Punishes stationary players

## 5. DiamondHead (Elite Enemy / Mini-Boss)

Role: High-damage elite unit
Threat Type: Multi-weapon assault

Weapons

* Animated missiles

* Triple-shot bullet spread

* Ice laser beams

Behavior

* Horizontal tracking

* Periodic laser activation

* Missile barrages

* Explosion on defeat

Stats

* Health: 400

* Speed: Medium–High

* Laser Cooldown: Timed cycles

Design Purpose

* Skill check before boss fights

* Tests laser evasion + burst damage

## 6. Predator (Heavy Elite Enemy)

Role: Semi-boss enemy
Threat Type: Sustained battlefield dominance

Weapons

* Triple vertical lasers

* Predator bullets

* Downward dive attack

Behavior

* Smoothly tracks player X-axis

* Alternates between:

* Laser mode

* Bullet mode

* Periodically dives toward player

* Massive health pool

Stats

* Health: 2500

* Speed: Medium

* Laser Duration: Long

Design Purpose

* Endurance combat

* Forces shield + timing mastery

## BIG BOSS – YellowBoss
### Boss Identity

Name: YellowBoss\
Role: Final boss  
Threat Level: Extreme

Core Stats

* Health: 800

* Speed: Medium

* Multi-phase behavior

* Protector units active at start

#### Boss Weapons & Abilities
1. Twin Laser Cannons

* Fires two parallel vertical lasers

* Long screen coverage

* Continuous damage while active

2. Vibration Shockwaves

* Expanding circular waves

* Originate from boss center

* Damage player on contact

* Multiple waves can exist simultaneously

3. Protector Ships (4 Units)

Behavior

* Orbit boss in circular paths

* Shoot at the player independently

* Must be destroyed first

Purpose

* Shields boss from early burst damage

* Adds target-management complexity

#### Boss Phases (Implicit)
#### Phase 1

* Protectors active

* Limited laser usage

#### Phase 2

* Protectors destroyed

* Increased laser + wave frequency

#### Phase 3

* Aggressive vibration waves

* High laser uptime