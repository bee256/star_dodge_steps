# Schritt 14: ein "echtes" Raumschiff verwenden → das Raumschiff in eine Klasse umbauen
import random
import time
import pygame as pg
from os import path

pg.init()
pg.font.init()
WIN = pg.display.set_mode((1200, 800))
# WIN = pg.display.set_mode((0, 0), pg.FULLSCREEN)
info_display = pg.display.Info()
SCREEN_W = info_display.current_w
SCREEN_H = info_display.current_h
print(f"Screen width: {SCREEN_W}, height: {SCREEN_H}")
STAR_W = int(SCREEN_W / 150)
STAR_H = int(SCREEN_H / 70)
STAR_MASK = pg.mask.Mask((STAR_W, STAR_H))
STAR_MASK.fill()
STAR_VEL = 8
print(f"Star width: {STAR_W}, height: {STAR_H}, velocity: {STAR_VEL}")

FONT_SIZE_BASE = int(SCREEN_W / 40)
TIME_FONT = pg.font.Font(path.join('assets', 'fonts', 'StarJedi-DGRW.ttf'), FONT_SIZE_BASE)
LOST_FONT = pg.font.Font(path.join('assets', 'fonts', 'StarJedi-DGRW.ttf'), FONT_SIZE_BASE * 2)
SOUND_HIT = pg.mixer.Sound(path.join('assets', 'sound', 'metal_trash_can_filled_2.wav'))
pg.mixer.music.load(path.join('assets', 'sound', 'planetary_paths.mp3'), 'planet_paths')
BG_IMG = pg.image.load(path.join('assets', 'images', 'background.jpeg'))
BG_IMG_SCALED = pg.transform.scale(BG_IMG, (SCREEN_W, SCREEN_H))


def draw():
    WIN.blit(BG_IMG_SCALED, (0, 0))

    minutes = int(elapsed_time) // 60
    seconds = int(elapsed_time) % 60
    time_text = TIME_FONT.render(f"Time: {minutes:02d}:{seconds:02d}", 1, pg.Color(0, 160, 255))
    WIN.blit(time_text, (30, 10))

    ship.draw()

    for star in stars:
        pg.draw.rect(WIN, "white", star)

    pg.display.update()


class Ship:
    """
    This class creates a ship from a graphic file, scales according to the size of the surface it shall be drawn on,
    animates the ship and draws it.

    Attributes:
        screen (pygame.Surface): Surface where the ship is drawn on
        ship_img (pygame.Surface): The image to be drawn will be scaled during construction
        width (float): width of the ship
        height (float): height of the ship
        mask (pygame.mask): The mask of the ship (taken from the image) for collision detection
        x (int): x coordinate of the ship's surrounding rectangle
        y (int): y coordinate of the ship's surrounding rectangle

    Methods:
        draw(): draw on screen
        move_left(): move the ship to the left (will not move off-screen)
        move_right(): move the ship to the right (will not move off-screen)
    """

    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.ship_img = pg.image.load(path.join('assets', 'images', 'space_ship.png'))

        # calculate aspect ratio
        image_aspect = self.ship_img.get_height() / self.ship_img.get_width()
        # use a reasonable width in relation so screen
        self.width = round(screen.get_width() / 28)
        # height is then derived using the aspect ratio
        self.height = round(self.width * image_aspect)
        # the speed in which we move the ship is in relation to the size and thus relates to the screen as well
        self.__velocity = round(self.width / 8)
        # now size the ship image and assign back to the same attribute
        self.ship_img = pg.transform.smoothscale(self.ship_img, (self.width, self.height))
        offset = self.height / 2

        self.mask = pg.mask.from_surface(self.ship_img)
        self.x = round(screen.get_width() / 2 - self.width / 2)
        self.y = round(screen.get_height() - self.height - offset)
        print(f"Ship width: {self.width}, height: {self.height}, velocity: {self.__velocity}")

    def draw(self):
        self.screen.blit(self.ship_img, (self.x, self.y))

    def move_left(self):
        if self.x - self.__velocity >= 0:
            self.x -= self.__velocity

    def move_right(self):
        if self.x + self.__velocity + self.width <= self.screen.get_width():
            self.x += self.__velocity


# Main Program
run = True
ship = Ship(WIN)
clock = pg.time.Clock()
start_time = time.time()
elapsed_time = 0

# Sterne timer und array
star_add_increment = 1500       # gibt den Zeitabstand in Millisekunden an, in der wir neuen Sterne auf den Bildschirm bringen
star_create_timer = 0           # gibt die absolute Zeit an, wenn wir neue Sterne auf den Bildschirm bringen
stars = []                      # Die Liste, in der wir alle Sterne abspeichern, die wir generiert haben (und wo wir sie auch rauslöschen)
is_hit = False

pg.mixer.music.play(loops=-1)
pg.mouse.set_visible(False)

while run:
    time_since_last_frame = clock.tick(60)
    star_create_timer += time_since_last_frame
    elapsed_time = time.time() - start_time
    # print(f"Time since last frame: {time_since_last_frame}, Star timer: {star_create_timer}, Frame rate: {clock.get_fps():.2f}")

    if star_create_timer > star_add_increment:
        for _ in range(3):
            star_x = random.randint(0, SCREEN_W - STAR_W)
            star = pg.Rect(star_x, -STAR_H, STAR_W, STAR_H)
            stars.append(star)

        star_add_increment = max(150, star_add_increment - 50)
        star_create_timer = 0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        ship.move_left()
    if keys[pg.K_RIGHT]:
        ship.move_right()
    if keys[pg.K_ESCAPE]:
        break

    for star in stars.copy():
        star.y += STAR_VEL
        if star.y > SCREEN_H:
            stars.remove(star)
        elif star.y + star.height >= ship.y:        # nachschauen, ob die Unterkante des Sterns in Höhe des Schiffes ist
            if ship.mask.overlap(STAR_MASK, (star.x - ship.x, star.y - ship.y)):      # berühren sich Stern und Schiff?
                stars.remove(star)
                is_hit = True
                break

    if is_hit:
        lost_text = LOST_FONT.render("Raumschiff defekt!", 1, "red")
        # WIN.blit(lost_text, (SCREEN_W/2, SCREEN_H/2))
        WIN.blit(lost_text, (SCREEN_W/2 - lost_text.get_width()/2, SCREEN_H/2 - lost_text.get_height()/2))
        pg.display.update()
        pg.mixer.Sound.play(SOUND_HIT)
        pg.mixer.music.fadeout(2500)
        pg.time.delay(3000)
        break

    draw()

pg.quit()
