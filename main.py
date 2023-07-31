import pygame
from pygame.locals import *
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Function to rotate a 3D point around the origin
def rotate_point(point, angle_x, angle_y, angle_z):
    x, y, z = point
    sin_x, cos_x = math.sin(angle_x), math.cos(angle_x)
    sin_y, cos_y = math.sin(angle_y), math.cos(angle_y)
    sin_z, cos_z = math.sin(angle_z), math.cos(angle_z)

    new_x = x * cos_y - z * sin_y
    new_z = x * sin_y + z * cos_y
    x, z = new_x, new_z

    new_x = x * cos_x - y * sin_x
    new_y = x * sin_x + y * cos_x
    x, y = new_x, new_y

    new_y = y * cos_z - z * sin_z
    new_z = y * sin_z + z * cos_z
    y, z = new_y, new_z

    return x, y, z

# Function to draw a rotating 3D cube with perspective
def draw_cube(screen, angle_x, angle_y, angle_z):
    cube_size = 100
    cube_points = [
        (-cube_size, -cube_size, -cube_size),
        (-cube_size, -cube_size, cube_size),
        (-cube_size, cube_size, -cube_size),
        (-cube_size, cube_size, cube_size),
        (cube_size, -cube_size, -cube_size),
        (cube_size, -cube_size, cube_size),
        (cube_size, cube_size, -cube_size),
        (cube_size, cube_size, cube_size),
    ]

    rotated_points = [rotate_point(point, angle_x, angle_y, angle_z) for point in cube_points]

    # Connect the points to draw the cube edges
    for i in range(4):
        point1 = rotated_points[i]
        point2 = rotated_points[i + 4]
        pygame.draw.line(screen, WHITE, perspective_projection(point1), perspective_projection(point2))

        point1 = rotated_points[i]
        point2 = rotated_points[(i + 1) % 4]
        pygame.draw.line(screen, WHITE, perspective_projection(point1), perspective_projection(point2))

        point1 = rotated_points[i + 4]
        point2 = rotated_points[((i + 1) % 4) + 4]
        pygame.draw.line(screen, WHITE, perspective_projection(point1), perspective_projection(point2))

# Function for perspective projection
def perspective_projection(point):
    x, y, z = point
    fov = 256  # Field of view
    distance = 200  # Distance from the viewer to the screen

    scale = fov / (z + distance)
    screen_x = x * scale + SCREEN_WIDTH // 2
    screen_y = y * scale + SCREEN_HEIGHT // 2

    return screen_x, screen_y

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tesseract")
    clock = pygame.time.Clock()

    angle_x, angle_y, angle_z = 0, 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Increment the angle to make the cube spin
        angle_z += 0.01

        screen.fill(BLACK)
        draw_cube(screen, angle_x, angle_y, angle_z)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()