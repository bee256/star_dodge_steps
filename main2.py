# Schritt 3: Spiel im Vollbildmodus bauen
# Schritt 4: Hintergrundbild laden

import pygame

# WIN = pygame.display.set_mode((1200, 800))
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
"""
info_display = pygame.display.Info()
SCREEN_W = info_display.current_w
SCREEN_H = info_display.current_h
print(f"Screen width: {SCREEN_W}, height: {SCREEN_H}")
"""

BG_IMG = pygame.image.load('background.jpeg')
# BG_IMG_SCALED = pygame.transform.scale(BG_IMG, (SCREEN_W, SCREEN_H))
WIN.blit(BG_IMG, (0, 0))
pygame.display.update()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

pygame.quit()

