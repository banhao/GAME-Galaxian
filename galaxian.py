#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: chat GPT -4
# Instructor: banhao@gmail.com
# Version:
# Issue Date: September 19, 2023
# Release Note: 


import pygame
import random
import math

# Initialize pygame
pygame.init()

# Configuration
BACKGROUND_COLOR = (0, 0, 0)
ENEMY_COLOR = (255, 255, 255)
BULLET_COLOR = (255, 255, 255)
SHIP_COLOR = (0, 0, 255)
NUM_ENEMIES = 5
ENEMY_BULLET_CHANCE = 0.01

SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY_EVENT, 2000)  # spawns an enemy every 2 seconds

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Enemy properties
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 30
ENEMY_SPEED = 3
ENEMY_AMPLITUDE = 100

# Bullet properties
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 7
SPRAY_SPREAD = 5

# Laser properties
LASER_WIDTH = 10
LASER_HEIGHT = HEIGHT
LASER_SPEED = 15

# Spaceship properties
SHIP_WIDTH = 60
SHIP_HEIGHT = 20
SHIP_SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxian Style Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([ENEMY_WIDTH, ENEMY_HEIGHT], pygame.SRCALPHA)
        self.draw_bee()
        self.rect = self.image.get_rect()
        self.start_x = random.randint(0, WIDTH - ENEMY_WIDTH)
        self.rect.x = self.start_x
        self.rect.y = random.randint(0, HEIGHT - ENEMY_HEIGHT)
        self.angle = random.uniform(0, math.pi * 2)

    def draw_bee(self):
        pygame.draw.ellipse(self.image, ENEMY_COLOR, [0, 10, ENEMY_WIDTH, ENEMY_HEIGHT - 20])
        stripe_width = ENEMY_WIDTH // 3
        for i in range(3):
            if i % 2 == 1:
                pygame.draw.rect(self.image, (0, 0, 0), [i * stripe_width, 10, stripe_width, ENEMY_HEIGHT - 20])
        pygame.draw.arc(self.image, (200, 200, 200), [0, 0, ENEMY_WIDTH // 2, ENEMY_HEIGHT // 2], 0, math.pi, 3)
        pygame.draw.arc(self.image, (200, 200, 200), [ENEMY_WIDTH // 2, 0, ENEMY_WIDTH // 2, ENEMY_HEIGHT // 2], 0, math.pi, 3)

    def update(self):
        self.angle += 0.05
        offset_x = ENEMY_AMPLITUDE * math.sin(self.angle)
        offset_y = ENEMY_AMPLITUDE * math.cos(self.angle)
        self.rect.x = (self.start_x + offset_x) % WIDTH
        self.rect.y = (self.rect.y + ENEMY_SPEED) % HEIGHT

        if random.random() < ENEMY_BULLET_CHANCE:
            bullet = Bullet(self.rect.centerx, self.rect.bottom)
            bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, shooter="enemy", dx=0, dy=BULLET_SPEED):
        super().__init__()
        self.shooter = shooter
        self.image = pygame.Surface([BULLET_WIDTH, BULLET_HEIGHT])
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = dx
        self.dy = dy

    def update(self):
        if self.shooter == "enemy":
            self.rect.y += self.dy
        else:
            self.rect.x += self.dx
            self.rect.y -= self.dy
        if self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.shooter = "player"  # Add this line
        self.image = pygame.Surface([LASER_WIDTH, LASER_HEIGHT], pygame.SRCALPHA)
        pygame.draw.line(self.image, BULLET_COLOR, (LASER_WIDTH // 2, 0), (LASER_WIDTH // 2, LASER_HEIGHT), LASER_WIDTH)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y

    def update(self):
        self.rect.y -= LASER_SPEED
        if self.rect.bottom < 0:
            self.kill()

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BULLET_WIDTH, BULLET_HEIGHT])
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.y < 0:
            self.kill()

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([SHIP_WIDTH, SHIP_HEIGHT], pygame.SRCALPHA)
        self.draw_rocket()
        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH - SHIP_WIDTH) / 2
        self.rect.y = HEIGHT - SHIP_HEIGHT - 10
        self.bullet_type = "spray"

    def draw_rocket(self):
        # Body of the airplane
        pygame.draw.rect(self.image, SHIP_COLOR, [SHIP_WIDTH // 4, SHIP_HEIGHT // 4, SHIP_WIDTH // 2, SHIP_HEIGHT // 2])
        # Wings of the airplane
        pygame.draw.polygon(self.image, SHIP_COLOR, [(SHIP_WIDTH // 4, SHIP_HEIGHT // 2), (0, 3 * SHIP_HEIGHT // 4), (SHIP_WIDTH // 4, 3 * SHIP_HEIGHT // 4)])
        pygame.draw.polygon(self.image, SHIP_COLOR, [(3 * SHIP_WIDTH // 4, SHIP_HEIGHT // 2), (SHIP_WIDTH, 3 * SHIP_HEIGHT // 4), (3 * SHIP_WIDTH // 4, 3 * SHIP_HEIGHT // 4)])
        # Tail of the airplane
        pygame.draw.polygon(self.image, SHIP_COLOR, [(SHIP_WIDTH // 2, 0), (SHIP_WIDTH // 2 - SHIP_WIDTH // 8, SHIP_HEIGHT // 4), (SHIP_WIDTH // 2 + SHIP_WIDTH // 8, SHIP_HEIGHT // 4)])


    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= SHIP_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += SHIP_SPEED
        self.rect.x = max(0, min(WIDTH - SHIP_WIDTH, self.rect.x))

    def shoot(self):
        if self.bullet_type == "spray":
            spread_angles = [-30, 0, 30]  # angles covering 120 degrees
            for angle in spread_angles:
                dx = BULLET_SPEED * math.sin(math.radians(angle))
                dy = BULLET_SPEED * math.cos(math.radians(angle))
                bullet = Bullet(self.rect.centerx, self.rect.top, "player", dx, dy)
                bullets.add(bullet)
        elif self.bullet_type == "laser":
            bullets.add(Laser(self.rect.centerx, 0))

    def toggle_bullet_type(self):
        if self.bullet_type == "spray":
            self.bullet_type = "laser"
        else:
            self.bullet_type = "spray"

def game_over_screen():
    font = pygame.font.SysFont('Arial', 36)
    text_surface = font.render('GAME OVER', True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Indicate game should not restart
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # Indicate game should restart


enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
spaceship = Spaceship()

for i in range(NUM_ENEMIES):
    enemy = Enemy()
    enemies.add(enemy)

running = True
clock = pygame.time.Clock()

#AUTOMATIC_SHOOT_EVENT = pygame.USEREVENT + 2
#pygame.time.set_timer(AUTOMATIC_SHOOT_EVENT, 1000)  # spaceship shoots every 0.5 seconds

while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                spaceship.toggle_bullet_type()
        #if event.type == AUTOMATIC_SHOOT_EVENT:
        #    spaceship.shoot()
            if event.key == pygame.K_SPACE:
                spaceship.shoot()
        if event.type == SPAWN_ENEMY_EVENT:
            enemy = Enemy()
            enemies.add(enemy)

    screen.fill(BACKGROUND_COLOR)

    enemies.update()
    bullets.update()
    spaceship.update(keys)

    enemies.draw(screen)
    bullets.draw(screen)
    screen.blit(spaceship.image, spaceship.rect)
    
    # Check bullet collisions with enemies
    enemy_bullet_collisions = pygame.sprite.groupcollide(enemies, bullets, True, True, pygame.sprite.collide_mask)
    for enemy in enemy_bullet_collisions:
        # You can add score or other effects here for each destroyed enemy
        pass

    # Check bullet collisions with spaceship (only consider enemy bullets)
    enemy_bullets = [bullet for bullet in bullets if bullet.shooter == "enemy"]
    spaceship_bullet_collisions = pygame.sprite.spritecollide(spaceship, enemy_bullets, False, pygame.sprite.collide_mask)
    if spaceship_bullet_collisions:
        spaceship.kill()
        # Show the game over screen and check if the game should restart
        if game_over_screen():
            # Logic to restart the game
            enemies.empty()
            bullets.empty()
            spaceship = Spaceship()
            for i in range(NUM_ENEMIES):
                enemy = Enemy()
                enemies.add(enemy)
            continue
        else:
            running = False
    # Check direct collisions between enemies and spaceship
    if pygame.sprite.spritecollide(spaceship, enemies, True, pygame.sprite.collide_mask):
        spaceship.kill()
        # Show the game over screen and check if the game should restart
        if game_over_screen():
            # Logic to restart the game
            enemies.empty()
            bullets.empty()
            spaceship = Spaceship()
            for i in range(NUM_ENEMIES):
                enemy = Enemy()
                enemies.add(enemy)
            continue
        else:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

