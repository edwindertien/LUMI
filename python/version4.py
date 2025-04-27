import pygame
import math
import random
import sys

# Initialize
pygame.init()
pygame.mixer.init()

screen_width = 192
screen_height = 80
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('LUMI Eye Control')

clock = pygame.time.Clock()

# Colors
background_color = (127, 127, 127)
eyeball_color = (255, 255, 255)
pupil_color_default = (0, 255, 100)
current_pupil_color = pupil_color_default

# Eye parameters
eye_radius = int(5 * screen_height / 8)
eye_center_y = screen_height // 2
pupil_size = eye_radius * 0.55
min_pupil_size = eye_radius * 0.4
max_pupil_size = eye_radius * 0.7
dilation_speed = 0.1
contraction_speed = 0.05

left_eye_x = screen_width // 4
right_eye_x = 3 * screen_width // 4

# Blinking
blink_progress = 0.0  # 0.0 = fully open, 1.0 = fully closed
blinking = False
blink_direction = 1  # 1 = closing, -1 = opening
next_blink_time = pygame.time.get_ticks() + random.randint(4000, 7000)
blink_pause = 200  # milliseconds to stay closed
blink_paused = False
blink_pause_time = 0

# Joystick
pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Joystick detected:", joystick.get_name())
else:
    joystick = None
    print("No joystick detected!")

running = True
pupil_pos_x = left_eye_x
pupil_pos_y = eye_center_y

def draw_eye(center_x, center_y, blink_amt):
    # White eyeball
    pygame.draw.circle(screen, eyeball_color, (center_x, center_y), eye_radius)

    # Pupil
    pygame.draw.circle(screen, current_pupil_color, (int(pupil_pos_x), int(pupil_pos_y)), int(pupil_size))

    # Upper eyelid
    lid_y = center_y - int(eye_radius * (1 - blink_amt))
    points = [
        (center_x - eye_radius, 0),
        (center_x + eye_radius, 0),
        (center_x + eye_radius, lid_y),
        (center_x, lid_y - 20 * (1-blink_amt)),  # Soft curve shape
        (center_x - eye_radius, lid_y)
    ]
    pygame.draw.polygon(screen, background_color, points)

    # Lower eyelid
    lid_y2 = center_y + int(eye_radius * (1 - blink_amt))
    points = [
        (center_x - eye_radius, screen_height),
        (center_x + eye_radius, screen_height),
        (center_x + eye_radius, lid_y2),
        (center_x, lid_y2 + 20 * (1-blink_amt)),
        (center_x - eye_radius, lid_y2)
    ]
    pygame.draw.polygon(screen, background_color, points)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.JOYBUTTONDOWN:
            if joystick.get_button(8):  # Back button to exit
                print("Back button pressed. Exiting...")
                running = False
            if joystick.get_button(0):  # Button A
                current_pupil_color = (0, 255, 0)
            if joystick.get_button(1):  # Button B
                current_pupil_color = (255, 0, 0)
            if joystick.get_button(2):  # Button X
                current_pupil_color = (0, 0, 255)
            if joystick.get_button(3):  # Button Y
                current_pupil_color = (255, 255, 0)

    # Update pupil position based on joystick
    if joystick:
        x_axis = joystick.get_axis(0)  # Left-right
        y_axis = joystick.get_axis(1)  # Up-down
        pupil_pos_x = left_eye_x + int(x_axis * eye_radius * 0.5)
        pupil_pos_y = eye_center_y + int(y_axis * eye_radius * 0.5)

        dilate = joystick.get_button(10)  # Stick press for dilation
    else:
        dilate = False

    # Update pupil size
    if dilate:
        pupil_size += (max_pupil_size - pupil_size) * dilation_speed
    else:
        pupil_size += (min_pupil_size - pupil_size) * contraction_speed

    pupil_size = max(min(pupil_size, max_pupil_size), min_pupil_size)

    # Update blinking
    now = pygame.time.get_ticks()
    if blinking:
        if blink_paused:
            if now - blink_pause_time > blink_pause:
                blink_paused = False
                blink_direction = -1  # Start opening
        else:
            blink_progress += blink_direction * 0.05
            if blink_progress >= 1.0:
                blink_progress = 1.0
                blink_paused = True
                blink_pause_time = now
            if blink_progress <= 0.0:
                blink_progress = 0.0
                blinking = False
                next_blink_time = now + random.randint(4000, 7000)
    else:
        if now > next_blink_time:
            blinking = True
            blink_direction = 1

    # Draw
    screen.fill(background_color)

    draw_eye(left_eye_x, eye_center_y, blink_progress)
    draw_eye(right_eye_x, eye_center_y, blink_progress)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
