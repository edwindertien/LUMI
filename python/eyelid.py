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

# Function to draw eyelid as a polygon
def draw_eyelid(x, y):
    points = [
        (screen_width / 2, screen_height),  # Bottom left
        (screen_width, screen_height),  # Bottom right
        (screen_width, lid_mid),  # Right side curve
        (x + screen_width / 2 + eye_size_quarter, y + upper_value),  # Bezier control point right
        (x + screen_width / 2 - eye_size_quarter, y + upper_value),  # Bezier control point left
        (screen_width / 2, lid_mid),  # Midpoint of the lid
    ]
    
    # Draw the eyelid as a polygon
    pygame.draw.polygon(screen, EYELID_COLOR, points)

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
