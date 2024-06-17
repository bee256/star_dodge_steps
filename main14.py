# Schritt 18: Korrektur der Fehler mit dem Pausenmodus die in main11.py drin sind.
import random
import time
import pygame as pg
from os import path

pg.init()
pg.font.init()
WIN = pg.display.set_mode((1600, 900))
# WIN = pg.display.set_mode((0, 0), pg.FULLSCREEN)
info_display = pg.display.Info()
SCREEN_W = info_display.current_w
SCREEN_H = info_display.current_h
print(f"Screen width: {SCREEN_W}, height: {SCREEN_H}")
STAR_W = int(SCREEN_W / 150)
STAR_H = int(SCREEN_H / 70)
STAR_MASK = pg.mask.Mask((STAR_W, STAR_H))
STAR_MASK.fill()
STAR_VEL_MAX = round(SCREEN_H / 144)
STAR_VEL_MIN = round(SCREEN_H / 288)
print(f"Star width: {STAR_W}, height: {STAR_H}, velocity min/max: {STAR_VEL_MIN}/{STAR_VEL_MAX}")

FONT_SIZE_BASE = int(SCREEN_W / 40)
TIME_FONT = pg.font.Font(path.join('assets', 'fonts', 'StarJedi-DGRW.ttf'), FONT_SIZE_BASE)
LOST_FONT = pg.font.Font(path.join('assets', 'fonts', 'StarJedi-DGRW.ttf'), FONT_SIZE_BASE * 2)
SOUND_CRASH = pg.mixer.Sound(path.join('assets', 'sound', 'rubble_crash.wav'))
SOUND_HIT = pg.mixer.Sound(path.join('assets', 'sound', 'metal_trash_can_filled_2.wav'))
pg.mixer.music.load(path.join('assets', 'sound', 'planetary_paths.mp3'), 'planet_paths')
BG_IMG = pg.image.load(path.join('assets', 'images', 'background.jpeg'))
BG_IMG_SCALED = pg.transform.scale(BG_IMG, (SCREEN_W, SCREEN_H))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Additional Colors
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIGHT_BLUE = (0, 160, 255)

# Gray Shades
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)

# Custom Colors
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 182, 193)

STAR_COLOR_PALETTE = (WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, LIGHT_BLUE, LIGHT_GRAY, ORANGE, PURPLE, PINK)

# setup scrolling text
text = """This project is coded in a demo way
having everything in one file.
This is not good coding practice and
the whole game is refactored in bee256
GitHub project 'star dodge'!"""


def render_multiline_text(my_text):
    lines = my_text.splitlines()
    my_text_surfaces = []
    for line in lines:
        text_surface = TIME_FONT.render(line, True, WHITE)
        # Create a transparent surface for the text
        text_surface_with_alpha = pg.Surface((text_surface.get_width(), text_surface.get_height()), pg.SRCALPHA)
        text_surface_with_alpha.blit(text_surface, (0, 0))

        # Set the transparency level (0 is fully transparent, 255 is fully opaque)
        text_surface_with_alpha.set_alpha(32)
        my_text_surfaces.append(text_surface_with_alpha)

    return my_text_surfaces


text_surfaces = render_multiline_text(text)

text_y = SCREEN_H
scroll_speed = 2
line_height = text_surfaces[0].get_height() - 20


def draw_scrolling_text():
    global text_y

    # Draw each line with proper spacing
    y_offset = text_y
    for surface in text_surfaces:
        x_pos = (SCREEN_W - surface.get_width()) / 2
        WIN.blit(surface, (x_pos, y_offset))
        y_offset += line_height

    # Update the text's y-coordinate to scroll upwards
    text_y -= scroll_speed

    # If the text is off the top of the screen, reset it to start at the bottom
    if text_y < -text_surfaces[0].get_height() * len(text_surfaces):
        text_y = SCREEN_H


def draw_paused():
    paused_text = LOST_FONT.render("Paused!", 1, pg.Color(LIGHT_BLUE))
    WIN.blit(paused_text, (SCREEN_W / 2 - paused_text.get_width() / 2, SCREEN_H / 2 - paused_text.get_height() / 2))
    pg.display.flip()


def draw():
    WIN.blit(BG_IMG_SCALED, (0, 0))
    draw_scrolling_text()

    minutes = int(elapsed_time) // 60
    seconds = int(elapsed_time) % 60
    time_text = TIME_FONT.render(f"Time: {minutes:02d}:{seconds:02d}", 1, pg.Color(0, 160, 255))
    WIN.blit(time_text, (30, 10))

    color = 'green'
    if hits == 1:
        color = 'yellow'
    elif hits == 2:
        color = 'orange'
    elif hits >= 3:
        color = 'red'

    ship.draw(color)

    for star in stars:
        star.draw()

    hits_text = TIME_FONT.render(f"Hits: {hits}", 1, color)
    WIN.blit(hits_text, (SCREEN_W - hits_text.get_width() - 30, 10))

    if hits >= 3:
        lost_text = LOST_FONT.render("Raumschiff defekt!", 1, pg.Color(212, 0, 0))
        WIN.blit(lost_text, (SCREEN_W / 2 - lost_text.get_width() / 2, SCREEN_H / 2 - lost_text.get_height() / 2))

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

        self.ship_by_color = {}
        # the graphics loaded has a ship in grey color with RGB(100,100,100) → create colorful ships by replacing gray
        orig_color = pg.color.Color(100, 100, 100)
        color_set = ('green', 'yellow', 'orange', 'red')
        for col in color_set:
            self.ship_by_color[col] = self.ship_img.copy()
            new_color = pg.color.Color(col)
            pixel_array = pg.PixelArray(self.ship_by_color[col])
            pixel_array.replace(orig_color, new_color)

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

        # We scale each colored image after the color replacement and not before because of the antialiasing with smooth scale
        for col in color_set:
            self.ship_by_color[col] = pg.transform.smoothscale(self.ship_by_color[col], (self.width, self.height))

        self.mask = pg.mask.from_surface(self.ship_by_color['green'])
        self.x = round(screen.get_width() / 2 - self.width / 2)
        self.y = round(screen.get_height() - self.height - offset)
        print(f"Ship width: {self.width}, height: {self.height}, velocity: {self.__velocity}")

    def draw(self, color):
        self.screen.blit(self.ship_by_color[color], (self.x, self.y))

    def move_left(self):
        if self.x - self.__velocity >= 0:
            self.x -= self.__velocity

    def move_right(self):
        if self.x + self.__velocity + self.width <= self.screen.get_width():
            self.x += self.__velocity


class Star:
    """
    This class implements stars as rectangles with a random color from a color palette and moves them with a
    random velocity.

    Attributes:
        star_rect (pygame.Rect): the rectangle which is drawn on screen
        color: a randomly chosen color from a color palette
        velocity: a random chosen velocity from a certain range

    Methods:
        draw(): draw on screen
        move(): move the star vertically down the screen according to the velocity
        is_off_screen(): determines if the star has been moved outside the visible area of the screen
        is_near_ship(): determines if the star is close to the y coordinates of the ship
        collides_with_ship(): determines if the star collides with the ship
    """

    def __init__(self):
        star_x = random.randint(0, SCREEN_W - STAR_W)
        self.star_rect = pg.Rect(star_x, -STAR_H, STAR_W, STAR_H)
        self.color = STAR_COLOR_PALETTE[random.randint(0, len(STAR_COLOR_PALETTE) - 1)]
        self.velocity = random.randint(STAR_VEL_MIN, STAR_VEL_MAX)

    def draw(self):
        pg.draw.rect(WIN, self.color, self.star_rect)

    def move(self):
        self.star_rect.y += self.velocity

    def is_off_screen(self):
        if self.star_rect.y > SCREEN_H:
            return True
        return False

    def is_near_ship(self, ship):
        if self.star_rect.y + self.star_rect.height >= ship.y:
            return True
        return False

    def collides_with_ship(self, ship):
        if ship.mask.overlap(STAR_MASK, (self.star_rect.x - ship.x, self.star_rect.y - ship.y)):
            return True
        return False


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
hits = 0
is_paused = False
pause_start = 0

pg.mixer.music.play(loops=-1)
pg.mouse.set_visible(False)

while run:
    time_since_last_frame = clock.tick(60)
    star_create_timer += time_since_last_frame
    # print(f"Time since last frame: {time_since_last_frame}, Star timer: {star_create_timer}, Frame rate: {clock.get_fps():.2f}")

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                is_paused = not is_paused
                if is_paused:
                    pause_start = time.time()
                    draw_paused()
                else:
                    # Korrektur der Startzeit, wenn die Pause beendet wird
                    start_time += time.time() - pause_start

    if is_paused:
        continue

    elapsed_time = time.time() - start_time

    if star_create_timer > star_add_increment:
        for _ in range(3):
            star = Star()
            stars.append(star)

        # here we decrease star_add_increment, so that starts get created faster and faster, but not faster than a threshold
        star_add_increment = max(150, star_add_increment - 50)
        star_create_timer = 0

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        ship.move_left()
    if keys[pg.K_RIGHT]:
        ship.move_right()
    if keys[pg.K_ESCAPE]:
        break

    for star in stars.copy():
        star.move()
        if star.is_off_screen():
            stars.remove(star)
        elif star.is_near_ship(ship):
            if star.collides_with_ship(ship):
                stars.remove(star)
                is_hit = True
                break

    if is_hit:
        hits += 1
        if hits < 3:
            pg.mixer.Sound.play(SOUND_HIT)
            is_hit = False
        else:
            pg.mixer.Sound.play(SOUND_CRASH)
            pg.mixer.music.fadeout(2500)
            run = False

    draw()
    # end of game loop (while run)

if is_hit:
    # if we ended the loop with is hit it means that game is over
    pg.time.delay(3000)

pg.quit()



"""
self.star_count_time = 0
self.stars_on_screen_by_time = []

self.write_stars_by_time()

if elapsed_time >= self.star_count_time:
    self.stars_on_screen_by_time.append((elapsed_time, len(self.stars)))
    self.star_count_time = elapsed_time + 1


def write_stars_by_time(self):
    # Array of tuples
    # Specify the CSV file name
    filename = 'num_stars_by_time.csv'

    # Writing to the CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Optionally write a header
        writer.writerow(['Time', '# Stars'])
        # Write data
        for row in self.stars_on_screen_by_time:
            writer.writerow(row)

    print(f'Data successfully written to {filename}')

"""