# Schritt 5: Ein Rechteck als Raumschiff zeichnen
# Schritt 6: Mit Cursortasten animieren

import pygame

# WIN = pygame.display.set_mode((1200, 800))
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info_display = pygame.display.Info()
SCREEN_W = info_display.current_w
SCREEN_H = info_display.current_h
print(f"Screen width: {SCREEN_W}, height: {SCREEN_H}")
PLAYER_WIDTH = SCREEN_W / 50
PLAYER_HEIGHT = PLAYER_WIDTH * 1.5
PLAYER_VEL = PLAYER_WIDTH / 8
print(f"Player width: {PLAYER_WIDTH}, height: {PLAYER_HEIGHT}, velocity: {PLAYER_VEL}")

BG_IMG = pygame.image.load('background.jpeg')
BG_IMG_SCALED = pygame.transform.scale(BG_IMG, (SCREEN_W, SCREEN_H))


def draw(player):
    WIN.blit(BG_IMG_SCALED, (0, 0))
    pygame.draw.rect(WIN, "red", player)
    pygame.display.update()


run = True
player = pygame.Rect(SCREEN_W / 2, SCREEN_H - PLAYER_HEIGHT * 2, PLAYER_WIDTH, PLAYER_HEIGHT)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
        player.x -= PLAYER_VEL
    if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= SCREEN_W:
        player.x += PLAYER_VEL
    if keys[pygame.K_ESCAPE]:
        break

    draw(player)

pygame.quit()
