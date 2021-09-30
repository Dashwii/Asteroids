import pygame
import time
from datetime import datetime
import os
import math
import random

pygame.init()

FPS = 60
WIDTH, HEIGHT = 1200, 1000 # 1000, 800
MIDDLE_W, MIDDLE_H = WIDTH // 2, HEIGHT // 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
TITLE_FONT = pygame.font.Font(os.path.join("Assets", "Font", "upheavtt.ttf"), 150)
TEXT_FONT = pygame.font.Font(os.path.join("Assets", "Font", "upheavtt.ttf"), 80)
ENLARGED_TEXT_FONT = pygame.font.Font(os.path.join("Assets", "Font", "upheavtt.ttf"), 100)
LIVES_SCORE_FONT = pygame.font.Font(os.path.join("Assets", "Font", "upheavtt.ttf"), 40)
GAME_OVER_FONT = pygame.font.Font(os.path.join("Assets", "Font", "upheavtt.ttf"), 30)
SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_sprites", "spaceship_sprite.png")).convert(), (40, 60)) # 50, 70

BOOSTER_SPRITES = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_sprites", "booster_sprites", f"{i}")), (50, 50)) for i in os.listdir(os.path.join("Assets", "spaceship_sprites", "booster_sprites"))]
BULLET_SPRITES = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_sprites", "bullet_sprites", f"{i}")), (10, 20)) for i in os.listdir(os.path.join("Assets", "spaceship_sprites", "bullet_sprites"))]
ASTEROID_SPRITES = [pygame.image.load(os.path.join("Assets", "asteroid_sprites", f"{i}")) for i in os.listdir(os.path.join("Assets", "asteroid_sprites"))]


if __name__ == "__main__":
    print(os.listdir(os.path.join("Assets", "asteroid_sprites")))


