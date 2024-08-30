import pygame, math

from settings import *
from colors import *

from PIL import Image

# PyGame Setup
pygame.init()

if FULLSCREEN:
    SCREEN = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
else:
    SCREEN = pygame.display.set_mode(RESOLUTION)

pygame.display.set_caption(WINDOW_NAME)
clock = pygame.time.Clock()

max_number = 2
depth = 2**6  # DECREASE TO INCREASE GENERATION SPEED BUT ALSO DECREASES QUALITY

# Calculate the scaling factor to maintain the aspect ratio
aspect_ratio = WIDTH / HEIGHT
scale_x = 4 / WIDTH
scale_y = 4 / HEIGHT / aspect_ratio


# Translate pixel coordinates to complex plane coordinates
def tl_to_center(coordinate: tuple[int, int]):
    return (
        (coordinate[0] - WIDTH / 2) * scale_x,
        (coordinate[1] - HEIGHT / 2) * scale_y,
    )


def iterate(z, c):
    # Iterating using complex number arithmetic
    return (z[0] ** 2 - z[1] ** 2 + c[0], 2 * z[0] * z[1] + c[1])


def check_point(c):
    z = (0, 0)

    for i in range(depth):
        z = iterate(z, c)
        magnitude = math.sqrt(z[0] ** 2 + z[1] ** 2)
        if magnitude > max_number:
            return False, i  # Return iteration count for coloring

    return True, depth


def get_shade_color(iterations):
    # Custom purple color scheme for the fractal shading
    return (
        int(128 + 127 * (iterations / depth)),  # Red component
        int(0),  # Green component
        int(128 + 127 * (1 - iterations / depth)),  # Blue component
    )


def main():
    running = True

    # Set the background color to LIGHT_PURPLE
    background_color = LIGHT_PURPLE
    SCREEN.fill(background_color)

    # Generate and draw fractals
    for i in range(WIDTH):
        for j in range(HEIGHT):
            pos = tl_to_center((i, j))
            is_in_set, iterations = check_point(pos)
            if is_in_set:
                SCREEN.set_at((i, j), BLACK)  # Fractal color (set to PURPLE)
            else:
                shade_color = get_shade_color(iterations)
                SCREEN.set_at((i, j), shade_color)  # Shading color

    img = Image.new("RGB", RESOLUTION)
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i, j] = SCREEN.get_at((i, j))[:-1]

    img.save("MandelbrotSet.png")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    SCREEN.fill(WHITE)
    main()
