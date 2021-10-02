import pygame
import time
from datetime import datetime
import os
import math
import random

pygame.init()

FPS = 60
WIDTH, HEIGHT = 1200, 1000
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

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "starbg.png")), (1200, 1000)).convert()
SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_sprites", "spaceship_sprite.png")), (40, 60)).convert_alpha()
STAR_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "star.png")), (60, 75)).convert_alpha()
HEART_SPRITE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "heart.png")), (45, 40)).convert_alpha()
BOOSTER_SPRITES = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_sprites", "booster_sprites", f"{i}")), (50, 50)).convert_alpha() for i in os.listdir(os.path.join("Assets", "spaceship_sprites", "booster_sprites"))]
BULLET_SPRITES = [pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship_sprites", "bullet_sprites", f"{i}")), (10, 20)).convert_alpha() for i in os.listdir(os.path.join("Assets", "spaceship_sprites", "bullet_sprites"))]
ASTEROID_SPRITES = [pygame.image.load(os.path.join("Assets", "asteroid_sprites", f"{i}")).convert_alpha() for i in os.listdir(os.path.join("Assets", "asteroid_sprites"))]


if __name__ == "__main__":
    print(os.listdir(os.path.join("Assets", "asteroid_sprites")))
