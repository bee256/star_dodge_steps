# Schritt 3: Spiel im Vollbildmodus bauen
# Schritt 4: Hintergrundbild laden
import pygame
from random import randint

# WIN = pygame.display.set_mode((1200, 800))
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Wenn wir das Spiel im Fullscreen laufen lassen, müssen wir die Objekte, die wir auf den Bildschirm bringen
# an die unterschiedlichen Bildschirmgrössen anpassen. Auch weiter unten wird die Grösse des Bildschirms in der
# pygame.transform.scale() funktion verwendet.
info_display = pygame.display.Info()
SCREEN_W = info_display.current_w
SCREEN_H = info_display.current_h
print(f"Screen width: {SCREEN_W}, height: {SCREEN_H}")

BG_IMG = pygame.image.load('background.jpeg')
BG_IMG_SCALED = pygame.transform.scale(BG_IMG, (SCREEN_W, SCREEN_H))
WIN.blit(BG_IMG_SCALED, (0, 0))

# Hier wird ein Objekt der pygame.time.Clock() Klasse instanziert. Dieses ist für das Timing der Schleife unten
# notwendig und sorgt dafür, dass das Spiel auf unterschiedlichen Computer gleich schnell läuft.
# → Siehe die Erklärung von ChatGPT unten
clock = pygame.time.Clock()

run = True

while run:
    # Experimentiert mit den Werten in clock.tick()
    clock.tick(60)
    # Kommentiert WIN.blit(BG_IMG_SCALED, (0, 0)) ein, was ändert sich?
    # WIN.blit(BG_IMG_SCALED, (0, 0))

    # Zufallsfarben erzeugen
    red = randint(0, 255)
    green = randint(0, 255)
    blue = randint(0, 255)
    # Zufallsposition erzeugen
    x = randint(5, SCREEN_W - 5)
    y = randint(5, SCREEN_H - 5)
    # Ein kleines "Kreischen" auf dem Bildschirm zeichnen
    pygame.draw.circle(WIN, center=(x, y), color=(red, green, blue), radius=10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    pygame.display.update()

pygame.quit()

"""
Erklärung von ChatGPT 4:

In Pygame, einem beliebten Framework zur Spieleentwicklung mit Python, ist pygame.time.Clock eine sehr nützliche Klasse,
die benutzt wird, um die Zeit zu kontrollieren. Das ist besonders wichtig in Spielen, da es hilft, die Spielgeschwindigkeit
konstant zu halten, unabhängig davon, wie schnell oder langsam ein individueller Computer ist.

pygame.time.Clock
Die Klasse pygame.time.Clock wird genutzt, um eine Uhr zu erstellen, die dabei hilft, die Framerate (Bildwiederholrate)
eines Spiels zu regulieren. Eine Instanz dieser Klasse bietet mehrere Methoden, aber die wichtigste ist tick().

clock.tick()
Die Methode clock.tick(framerate) wird in der Hauptspiel-Schleife (game loop) verwendet, um sicherzustellen,
dass das Spiel mit einer bestimmten Framerate läuft. Hier ein paar Details:

Parameter: framerate ist die maximale Anzahl von Frames pro Sekunde (FPS), die das Spiel erreichen soll. Zum Beispiel
sorgt clock.tick(60) dafür, dass das Spiel nicht mehr als 60 Frames pro Sekunde zeichnet.
Rückgabewert: Die Methode gibt die Anzahl der Millisekunden zurück, die seit dem letzten Aufruf der Methode vergangen sind.
Dies kann verwendet werden, um Animationen oder andere Zeitabhängige Aktionen zu steuern.

Verwendung in einer Gameschleife
Hier ist ein einfaches Beispiel, wie pygame.time.Clock und clock.tick() in einer typischen Spielschleife verwendet werden können:

import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Spiellogik hier einfügen
    
    pygame.display.flip()
    # Reguliert die Framerate auf 60 FPS
    ms_per_frame = clock.tick(60)

pygame.quit()
In diesem Code:

clock.tick(60) wird am Ende jeder Iteration der Schleife aufgerufen, was das Spiel dazu bringt, zu warten, bis 1/60 Sekunde
vergangen ist, bevor die nächste Iteration beginnt. Dies stabilisiert die Framerate auf etwa 60 FPS.
Der Rückgabewert ms_per_frame kann benutzt werden, um zu berechnen, wie viel Zeit tatsächlich für einen Frame aufgewendet wurde,
was nützlich ist, wenn man Spielereignisse oder Animationen zeitlich steuern muss.
Die Verwendung von pygame.time.Clock und clock.tick() ist also eine effektive Methode, um eine gleichmäßige Spielerfahrung
über verschiedene Systeme hinweg sicherzustellen.
"""
