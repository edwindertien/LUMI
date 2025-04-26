import pygame
import sys
import random

# Initialize
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

# Screen setup
screen_width, screen_height = 192, 80
screen = pygame.display.set_mode((screen_width, screen_height))
# screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

pygame.display.set_caption("LUMI eye control")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BACKGROUND = (127, 127, 127)
EYE_COLOR = (0, 255, 100)

# Joystick setup
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print("No joystick found!")
    sys.exit()

# Eye parameters
eye_size = 5 * screen_height // 8
pupil_size = eye_size * 0.55
base_pupil_size = eye_size * 0.55
min_pupil_size = eye_size * 0.4
max_pupil_size = eye_size * 0.7

pupil_x = screen_width // 4
pupil_y = screen_height // 2

prev_pupil_x = pupil_x
prev_pupil_y = pupil_y

eye_offset_x = 0
eye_offset_y = 0

blink = False
blink_timer = 0
next_blink_time = random.randint(4000, 15000)
blink_duration = 0

last_eye_move_time = 0
eye_move_threshold = 200  # ms
is_focusing = False

def draw_eyes(x, y, blink_now):
    # Left Eye
    pygame.draw.ellipse(screen, EYE_COLOR, (x - eye_size//2, y - eye_size//2, eye_size, eye_size))
    # Right Eye
    pygame.draw.ellipse(screen, EYE_COLOR, (x + screen_width//2 - eye_size//2, y - eye_size//2, eye_size, eye_size))
    # Pupils
    pygame.draw.ellipse(screen, (0, 0, 0), (x - pupil_size//2, y - pupil_size//2, pupil_size, pupil_size))
    pygame.draw.ellipse(screen, (0, 0, 0), (x + screen_width//2 - pupil_size//2, y - pupil_size//2, pupil_size, pupil_size))

# Main loop
running = True
start_time = pygame.time.get_ticks()

while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time_now = pygame.time.get_ticks()

    # Joystick input
    target_x = pupil_x
    target_y = pupil_y
    dilate = False

    if joystick.get_numaxes() >= 2:
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)
        target_x = int((x_axis + 1) * screen_width / 4)
        target_y = int((y_axis + 1) * screen_height / 2)

    if joystick.get_numbuttons() > 0:
        dilate = joystick.get_button(0)  # Button A for DILATE (adjust if needed)

    # Smooth eye movement
    pupil_x = 0.9 * pupil_x + 0.1 * (target_x + eye_offset_x)
    pupil_y = 0.9 * pupil_y + 0.1 * (target_y + eye_offset_y)

    # Focus detection
    if abs(pupil_x - prev_pupil_x) > 0.5 or abs(pupil_y - prev_pupil_y) > 0.5:
        last_eye_move_time = time_now
        is_focusing = False
    else:
        if time_now - last_eye_move_time > eye_move_threshold:
            is_focusing = True

    prev_pupil_x = pupil_x
    prev_pupil_y = pupil_y

    # Random blinking
    if time_now - blink_timer > next_blink_time:
        blink_timer = time_now
        next_blink_time = random.randint(4000, 15000)
        blink_duration = random.randint(5, 20)

    if blink_duration > 0:
        blink_duration -= 1
        blink = True
    else:
        blink = False

    # Pupil size adjustment
    if dilate:
        pupil_size += (max_pupil_size - pupil_size) * 0.1
    elif is_focusing:
        pupil_size += (min_pupil_size - pupil_size) * 0.05
    else:
        pupil_size += (base_pupil_size - pupil_size) * 0.05

    pupil_size = max(min_pupil_size, min(max_pupil_size, pupil_size))

    # Draw
    draw_eyes(int(pupil_x), int(pupil_y), blink)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
