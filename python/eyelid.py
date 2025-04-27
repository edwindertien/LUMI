import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 192
screen_height = 80
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
BACKGROUND = (127, 127, 127)
EYELID_COLOR = (0, 0, 0)  # Black eyelid color for visibility

# Eye parameters
eye_size = 5 * screen_height // 8
pupil_size = eye_size * 0.55
base_pupil_size = eye_size * 0.55
min_pupil_size = eye_size * 0.4
max_pupil_size = eye_size * 0.7

pupil_x = screen_width // 2
pupil_y = screen_height // 2

lid_mid = screen_height // 3
upper_value = 10  # For controlling the curve of the eyelid
eye_size_quarter = eye_size // 4  # A quarter of the eye size

# Function to calculate the cubic Bezier curve
def bezier_curve(P0, P1, P2, P3, num_points=100):
    points = []
    for t in range(num_points + 1):
        t = t / num_points  # Convert t to a range from 0 to 1
        x = (1 - t)**3 * P0[0] + 3 * (1 - t)**2 * t * P1[0] + 3 * (1 - t) * t**2 * P2[0] + t**3 * P3[0]
        y = (1 - t)**3 * P0[1] + 3 * (1 - t)**2 * t * P1[1] + 3 * (1 - t) * t**2 * P2[1] + t**3 * P3[1]
        points.append((x, y))
    return points

# Function to draw the eyelid using Bezier curve
def draw_eyelid(x, y):
    # Define the four control points for the Bezier curve
    P0 = (screen_width / 2, screen_height)  # Start point (bottom center)
    P1 = (x + screen_width / 2 + eye_size_quarter, y + upper_value)  # First control point
    P2 = (x + screen_width / 2 - eye_size_quarter, y + upper_value)  # Second control point
    P3 = (screen_width / 2, lid_mid)  # End point (middle of the lid)

    # Calculate the Bezier curve points
    curve_points = bezier_curve(P0, P1, P2, P3)

    # Draw the curve as a series of anti-aliased lines
    pygame.draw.aalines(screen, EYELID_COLOR, False, curve_points)

# Main loop
running = True
while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw the eyelid and the pupil
    draw_eyelid(pupil_x, pupil_y)
    pygame.draw.ellipse(screen, (0, 0, 0), (pupil_x - pupil_size // 2, pupil_y - pupil_size // 2, pupil_size, pupil_size))

    pygame.display.flip()

pygame.quit()
sys.exit()
