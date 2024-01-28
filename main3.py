# Schritt 5: Ein Rechteck als Raumschiff zeichnen
# Schritt 6: Mit Cursortasten animieren

import pygame

# WIN = pygame.display.set_mode((1200, 800))
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info_display = pygame.display.Info()
SCREEN_W = info_display.current_w
SCREEN_H = info_display.current_h
print(f"Screen width: {SCREEN_W}, height: {SCREEN_H}")
SHIP_WIDTH = SCREEN_W / 50
SHIP_HEIGHT = SHIP_WIDTH * 1.5
SHIP_VEL = SHIP_WIDTH / 8
print(f"Player width: {SHIP_WIDTH}, height: {SHIP_HEIGHT}, velocity: {SHIP_VEL}")

BG_IMG = pygame.image.load('background.jpeg')
BG_IMG_SCALED = pygame.transform.scale(BG_IMG, (SCREEN_W, SCREEN_H))


def draw(ship):
    WIN.blit(BG_IMG_SCALED, (0, 0))
    pygame.draw.rect(WIN, "red", ship)
    pygame.display.update()


run = True
ship = pygame.Rect(SCREEN_W / 2, SCREEN_H - SHIP_HEIGHT * 2, SHIP_WIDTH, SHIP_HEIGHT)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship.x - SHIP_VEL >= 0:
        ship.x -= SHIP_VEL
    if keys[pygame.K_RIGHT] and ship.x + SHIP_VEL + ship.width <= SCREEN_W:
        ship.x += SHIP_VEL
    if keys[pygame.K_ESCAPE]:
        break

    draw(ship)

pygame.quit()
