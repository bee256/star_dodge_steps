# Schritt 10: Game bei Kollision beenden
import random
import time
import pygame

pygame.font.init()
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
STAR_W = int(SCREEN_W / 150)
STAR_H = int(SCREEN_H / 70)
STAR_VEL = 8
print(f"Star width: {STAR_W}, height: {STAR_H}, velocity: {STAR_VEL}")


FONT = pygame.font.SysFont("comicsans", 100)
BG_IMG = pygame.image.load('background.jpeg')
BG_IMG_SCALED = pygame.transform.scale(BG_IMG, (SCREEN_W, SCREEN_H))


def draw():
    WIN.blit(BG_IMG_SCALED, (0, 0))

    # time_text = FONT.render(f"Time: {elapsed_time} sec", 1, "white")
    time_text = FONT.render(f"Time: {round(elapsed_time)} sec", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", ship)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()


# Main Program
run = True
ship = pygame.Rect(SCREEN_W / 2, SCREEN_H - SHIP_HEIGHT * 2, SHIP_WIDTH, SHIP_HEIGHT)
clock = pygame.time.Clock()
start_time = time.time()
elapsed_time = 0

# Sterne
star_add_increment = 1500       # gibt den Zeitabstand in Millisekunden an, in der wir neuen Sterne auf den Bildschirm bringen
star_create_timer = 0           # gibt die absolute Zeit an, wenn wir neue Sterne auf den Bildschirm bringen
stars = []                      # Die Liste, in der wir alle Sterne abspeichern, die wir generiert haben (und wo wir sie auch rauslöschen)
is_hit = False

while run:
    time_since_last_frame = clock.tick(60)
    star_create_timer += time_since_last_frame
    elapsed_time = time.time() - start_time
    # print(f"Time since last frame: {time_since_last_frame}, Star timer: {star_create_timer}, Frame rate: {clock.get_fps():.2f}")

    if star_create_timer > star_add_increment:
        for _ in range(3):
            star_x = random.randint(0, SCREEN_W - STAR_W)
            star = pygame.Rect(star_x, -STAR_H, STAR_W, STAR_H)
            stars.append(star)

        star_add_increment = max(150, star_add_increment - 50)
        star_create_timer = 0

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

    for star in stars.copy():
        star.y += STAR_VEL
        if star.y > SCREEN_H:
            stars.remove(star)
        elif star.y + star.height >= ship.y:        # nachschauen, ob die Unterkante des Sterns in Höhe des Schiffes ist
            if star.colliderect(ship):              # berühren sich Stern und Schiff?
                stars.remove(star)
                is_hit = True
                break

    if is_hit:
        lost_text = FONT.render("Das Raumschiff ist konkret defekt!", 1, "red")
        # WIN.blit(lost_text, (SCREEN_W/2, SCREEN_H/2))
        WIN.blit(lost_text, (SCREEN_W/2 - lost_text.get_width()/2, SCREEN_H/2 - lost_text.get_height()/2))

        pygame.display.update()
        pygame.time.delay(20000)
        break

    draw()

pygame.quit()
