import pygame as pg
import math

# Initialization
pg.init()

# Colors
GRAY_1 = (197, 196, 201)
GRAY_2 = (61, 63, 67)
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
COLOR_TOP = BLACK
COLOR_BOTTOM = (0, 128, 255)

# Window settings
HEIGHT = 800
WIDTH = int(HEIGHT * 1.618)
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ASTEROID")
graph_view = False

# Simulation window settings
sim_height = 400
sim_width = int(sim_height * 1.618)
sim_x = 50
sim_y = 50

# Physic values
time_scale = 30
scale_factor = int(4761.9) / time_scale
g = 9.81 * scale_factor

# Lists
asteroids = []

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

def draw_vertical_gradient(surface, color_top, color_bottom, x, y, width, height):
    for i in range(height):
        ratio = i / height
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        color = (r, g, b)
        pg.draw.line(surface, color, (x, y + i), (x + width, y + i))

def is_inside_rect(pos, rect_x, rect_y, rect_width, rect_height):
    """Check if a position is inside a rectangle."""
    return rect_x <= pos[0] <= rect_x + rect_width and rect_y <= pos[1] <= rect_y + rect_height

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
                if is_inside_rect(mouse_pos, sim_x, sim_y, sim_width, sim_height):
                    mouse_pos_t = mouse_pos
                    line = True
            else:
                dx = mouse_pos[0] - mouse_pos_t[0]
                dy = mouse_pos[1] - mouse_pos_t[1]
                alpha_rad = -math.atan2(dy, dx)
                asteroids.append({
                    "pos_initial": mouse_pos_t,
                    "angle": alpha_rad,
                    "v0": 200 * scale_factor / time_scale,
                    "time": 0,
                })
                line = False

    screen.fill((GRAY_1))
    if not graph_view:
        draw_vertical_gradient(screen, COLOR_TOP, COLOR_BOTTOM, sim_x, sim_y, sim_width, sim_height)
        pg.draw.rect(screen, GREEN, (sim_x, sim_y + sim_height - 10, sim_width, 10))
    else:
        pg.draw.rect(screen, WHITE, (sim_x, sim_y, sim_width, sim_height))

    # Update asteroids
    for asteroid in list(asteroids):  # Use list copy to allow safe removal during iteration
        t = asteroid["time"]
        v0 = asteroid["v0"]
        angle = asteroid["angle"]
        x0, y0 = asteroid["pos_initial"]
        x = x0 + v0 * math.cos(angle) * t
        y = y0 - (-0.5 * g * t**2 + v0 * math.sin(angle) * t)

        # Remove asteroid if it goes out of bounds
        if not is_inside_rect((x, y), sim_x+5, sim_y+5, sim_width-5, sim_height-5):
            asteroids.remove(asteroid)
        else:
            if not graph_view:
                draw_asteroid(x, y)
            else:
                asteroid_graph_view(x, y)
            asteroid["time"] += clock.get_time() / 1000

    # Draw direction line
    if line:
        dx = mouse_pos[0] - mouse_pos_t[0]
        dy = mouse_pos[1] - mouse_pos_t[1]
        norme = (dx**2 + dy**2)**0.5
        end_x, end_y = mouse_pos_t
        line_color = WHITE if not graph_view else BLACK
        if norme != 0:
            dx_normalized = dx / norme
            dy_normalized = dy / norme
            distance = min(10000, sim_width - 1)  # Limit the line to the width of the rectangle
            end_x = max(sim_x, min(mouse_pos_t[0] + dx_normalized * distance, sim_x + sim_width))
            end_y = max(sim_y, min(mouse_pos_t[1] + dy_normalized * distance, sim_y + sim_height))
        pg.draw.line(screen, line_color, mouse_pos_t, (end_x, end_y), 1)
        alpha_rad = -math.atan2(dy, dx)
        alpa_deg = math.degrees(alpha_rad)
        print(alpa_deg)

    pg.display.update()
    clock.tick(60)

pg.quit()