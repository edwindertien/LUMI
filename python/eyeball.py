import pygame
import sys

# Initialize pygame
pygame.init()

# Screen setup
screen_width, screen_height = 192, 80
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Static Eye with Eyelids")

# Colors
WHITE = (255, 255, 255)
BACKGROUND = (127, 127, 127)
EYE_COLOR = (0, 255, 100)
PUPIL_COLOR = (0, 0, 0)
EYELID_COLOR = (0, 0, 0)

# Eye parameters
eye_size = 5 * screen_height // 8
pupil_size = eye_size * 0.55
base_pupil_size = eye_size * 0.55
min_pupil_size = eye_size * 0.4
max_pupil_size = eye_size * 0.7

pupil_x = screen_width // 4
pupil_y = screen_height // 2

# Eyelid parameters
eyelid_height = 10  # Height for the eyelid curve
eyelid_offset = 15  # Vertical offset for eyelid shape

# Draw eyes, pupils, and eyelids
def draw_eyes_and_eyelids():
    # Left Eye (Ellipse)
    pygame.draw.ellipse(screen, EYE_COLOR, (pupil_x - eye_size//2, pupil_y - eye_size//2, eye_size, eye_size))
    # Right Eye (Ellipse)
    pygame.draw.ellipse(screen, EYE_COLOR, (pupil_x + screen_width//2 - eye_size//2, pupil_y - eye_size//2, eye_size, eye_size))
    
    # Pupils (smaller circles inside the eyes)
    pygame.draw.ellipse(screen, PUPIL_COLOR, (pupil_x - pupil_size//2, pupil_y - pupil_size//2, pupil_size, pupil_size))
    pygame.draw.ellipse(screen, PUPIL_COLOR, (pupil_x + screen_width//2 - pupil_size//2, pupil_y - pupil_size//2, pupil_size, pupil_size))

    # Left Eyelid (polygon)
    left_eyelid_points = [
        (pupil_x - eye_size//2, pupil_y - eye_size//2 + eyelid_height),  # Top left
        (pupil_x - pupil_size//2, pupil_y - eye_size//2 + eyelid_height),  # Near pupil left
        (pupil_x - pupil_size//2, pupil_y - eye_size//2 - eyelid_offset),  # Near pupil bottom left
        (pupil_x - eye_size//2, pupil_y - eye_size//2 - eyelid_offset)   # Bottom left
    ]
    pygame.draw.polygon(screen, EYELID_COLOR, left_eyelid_points)

    # Right Eyelid (polygon)
    right_eyelid_points = [
        (pupil_x + screen_width//2 - eye_size//2, pupil_y - eye_size//2 + eyelid_height),  # Top right
        (pupil_x + screen_width//2 + pupil_size//2, pupil_y - eye_size//2 + eyelid_height),  # Near pupil right
        (pupil_x + screen_width//2 + pupil_size//2, pupil_y - eye_size//2 - eyelid_offset),  # Near pupil bottom right
        (pupil_x + screen_width//2 - eye_size//2, pupil_y - eye_size//2 - eyelid_offset)   # Bottom right
    ]
    pygame.draw.polygon(screen, EYELID_COLOR, right_eyelid_points)

    # Debugging: Draw the points of the eyelids for visualization
    for point in left_eyelid_points:
        pygame.draw.circle(screen, (255, 0, 0), point, 3)  # Draw red dots at the polygon points

    for point in right_eyelid_points:
        pygame.draw.circle(screen, (255, 0, 0), point, 3)  # Draw red dots at the polygon points

# Main loop
running = True
while running:
    screen.fill(BACKGROUND)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Draw the static eyes, pupils, and eyelids
    draw_eyes_and_eyelids()

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
