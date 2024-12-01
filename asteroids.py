import pygame as pg
import math

pg.init()

asteroids = []
time_scale = 30
scale_factor = int(4761.9) / time_scale
g = 9.81 * scale_factor
WIDTH, HEIGHT = int(800 * 1.618), 800
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ASTEROID")
graph_view = False

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
COLOR_TOP = BLACK
COLOR_BOTTOM = (0, 128, 255)

def draw_asteroid(x, y):
    pg.draw.circle(screen, GRAY, (int(x), int(y)), 7)

def asteroid_graph_view(x, y):
    x1s = x-5
    x2s = x
    x1e = x+5
    x2e = x
    y1s = y
    y2s = y+5
    y1e = y
    y2e = y-5
    pg.draw.line(screen, BLACK, (x1s, y1s), (x1e, y1e), 1)
    pg.draw.line(screen, BLACK, (x2s, y2s), (x2e, y2e), 1)

def draw_vertical_gradient(surface, color_top, color_bottom):
    height = surface.get_height() - 30
    width = surface.get_width()

    for y in range(height):
        ratio = y / height
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        color = (r, g, b)
        pg.draw.line(surface, color, (0, y), (width, y))

running = True
line = False
clock = pg.time.Clock()

while running:
    mouse_pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_g:
                graph_view = not graph_view

        if event.type == pg.MOUSEBUTTONDOWN:
            if not line:
                mouse_pos_t = mouse_pos
                line = True
            else:
                dx = mouse_pos[0] - mouse_pos_t[0]
                dy = mouse_pos[1] - mouse_pos_t[1]
                alpha_rad = -math.atan2(dy, dx)
                asteroids.append({
                    "pos_initial": mouse_pos_t,
                    "angle": alpha_rad,
                    "v0": 1000,
                    "time": 0
                })
                line = False

    if not graph_view:
        pg.draw.rect(screen, GREEN, (0, 770, WIDTH, 30))
        draw_vertical_gradient(screen, COLOR_TOP, COLOR_BOTTOM)
    else:
        screen.fill((WHITE))

    for asteroid in asteroids:
        t = asteroid["time"]
        v0 = asteroid["v0"]
        angle = asteroid["angle"]
        x0, y0 = asteroid["pos_initial"]
        x = x0 + v0 * math.cos(angle) * t
        y = y0 - (-0.5 * g * t**2 + v0 * math.sin(angle) * t)

        if y < HEIGHT:
            if not graph_view:
                draw_asteroid(x, y)
            else:
                asteroid_graph_view(x, y)
            asteroid["time"] += clock.get_time() / 1000

    if line:
        dx = mouse_pos[0] - mouse_pos_t[0]
        dy = mouse_pos[1] - mouse_pos_t[1]
        norme = (dx**2 + dy**2)**0.5
        end_x, end_y = mouse_pos_t
        line_color = WHITE if not graph_view else BLACK
        if norme != 0:
            dx_normalized = dx / norme
            dy_normalized = dy / norme
            distance = 10000
            end_x = mouse_pos_t[0] + dx_normalized * distance
            end_y = mouse_pos_t[1] + dy_normalized * distance
        pg.draw.line(screen, line_color, mouse_pos_t, (end_x, end_y), 1)

    pg.display.update()
    clock.tick(60)

pg.quit()
