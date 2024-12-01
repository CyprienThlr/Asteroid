import pygame as pg

# Initialization
pg.init()

# Window settings
WIDTH, HEIGHT = int(800*1.618), 800
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ASTEROID")

# Colors
GRAY_1 = (197, 196, 201)
GRAY_2 = (61, 63, 67)

# Update
running = True

while running:

    current_time = pg.time.get_ticks()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Draw
    window.fill(GRAY_1)

    # Navbar
    pg.draw.rect(window, GRAY_2, (0, 0, WIDTH, 30))

    pg.display.update()

pg.quit()