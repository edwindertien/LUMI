import pygame
import os
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

# Screen settings
SCREEN_WIDTH = 192
SCREEN_HEIGHT = 80
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("LUMI Eye Control")

# Colors
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
DEFAULT_PUPIL_COLOR = (0, 255, 100)

# Eye settings
eye_size = (5 * SCREEN_HEIGHT) // 8
pupil_size = eye_size * 0.55
min_pupil_size = eye_size * 0.4
max_pupil_size = eye_size * 0.7
pupil_color = DEFAULT_PUPIL_COLOR

# Eyelid settings
upper_lid_value = eye_size // 2
lid_speed = 2  # Smooth blink speed
is_blinking = False
blink_timer = 0
next_blink_time = random.randint(3000, 7000)
blink_duration = 0

# Load images
image_names = [
    "lumi-battery.jpg",
    "lumi-classified.jpg",
    "lumi-map.jpg",
    "lumi-route.jpg",
    "lumi-noconnection.jpg",
    "lumi-ok.jpg",
    "lumi-weather.jpg",
    "lumi-steps.jpg",
    "lumi-warning.jpg"
]

images = []
for name in image_names:
    img_path = os.path.join("data", name)
    images.append(pygame.image.load(img_path))

# Load sounds
sample_names = [
    "lumi-alarm.mp3",
    "lumi-yes.mp3",
    "lumi-yes1.mp3",
    "lumi-yes2.mp3",
    "lumi-no.mp3",
    "lumi-no2.mp3",
    "lumi-startup.mp3",
    "lumi-shutdown.mp3"
]

samples = []
for name in sample_names:
    snd_path = os.path.join("data", name)
    samples.append(pygame.mixer.Sound(snd_path))

# Link images to sound samples
link = [1, 4, 1, 5, 1, 5, 1, 4, 0]
last_sample_played = -1

# Joystick setup
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print("No joystick found.")
    sys.exit()

# Pupil position
pupil_x = SCREEN_WIDTH // 4
pupil_y = SCREEN_HEIGHT // 2

# Hat input
current_image_index = 0
image_delay = 0

# Clock
clock = pygame.time.Clock()

running = True

def draw_eyelid(x, y, width, height, upper_opening):
    lid_mid = height // 2

    points_upper = [
        (x, 0),
        (x + width, 0),
        (x + width, lid_mid),
        (x + width * 0.75, y - upper_opening),
        (x + width * 0.25, y - upper_opening),
        (x, lid_mid)
    ]

    points_lower = [
        (x, height),
        (x + width, height),
        (x + width, lid_mid),
        (x + width * 0.75, y + upper_opening),
        (x + width * 0.25, y + upper_opening),
        (x, lid_mid)
    ]

    pygame.draw.polygon(screen, GREY, points_upper)
    pygame.draw.polygon(screen, GREY, points_lower)

def draw_eye(x_offset):
    # Eye white
    pygame.draw.ellipse(screen, WHITE, (x_offset + pupil_x - eye_size // 2, pupil_y - eye_size // 2, eye_size, eye_size))

    # Pupil
    pygame.draw.ellipse(screen, pupil_color, (x_offset + pupil_x - pupil_size // 2, pupil_y - pupil_size // 2, pupil_size, pupil_size))

    # Eyelids
    draw_eyelid(x_offset, pupil_y, SCREEN_WIDTH // 2, SCREEN_HEIGHT, upper_lid_value)

# Main loop
while running:
    screen.fill(GREY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.JOYBUTTONDOWN:
            if joystick.get_button(0):  # A button
                pupil_color = (0, 255, 0)
            if joystick.get_button(1):  # B button
                pupil_color = (255, 0, 0)
            if joystick.get_button(2):  # X button
                pupil_color = (0, 0, 255)
            if joystick.get_button(3):  # Y button
                pupil_color = (255, 255, 0)
            if joystick.get_button(8):  # Back button
                running = False

        if event.type == pygame.JOYHATMOTION:
            hat_x, hat_y = joystick.get_hat(0)
            if hat_x != 0 or hat_y != 0:
                hat_pos = (hat_y + 1) * 3 + (hat_x + 1)
                if 1 <= hat_pos <= len(images):
                    current_image_index = hat_pos
                    if link[current_image_index-1] < len(samples):
                        if last_sample_played != current_image_index:
                            samples[link[current_image_index-1]].play()
                            last_sample_played = current_image_index

    # Joystick control for pupil position
    x_axis = joystick.get_axis(0) if joystick else 0
    y_axis = joystick.get_axis(1) if joystick else 0
    pupil_x = int(((x_axis + 1) / 2) * (SCREEN_WIDTH // 2))
    pupil_y = int(((y_axis + 1) / 2) * SCREEN_HEIGHT)

    # Smooth blink logic
    if pygame.time.get_ticks() - blink_timer > next_blink_time:
        is_blinking = True
        blink_duration = random.randint(5, 20)
        blink_timer = pygame.time.get_ticks()
        next_blink_time = random.randint(4000, 8000)

    if is_blinking:
        upper_lid_value -= lid_speed
        if upper_lid_value <= 0:
            upper_lid_value = 0
            blink_duration -= 1
            if blink_duration <= 0:
                is_blinking = False
    else:
        if upper_lid_value < eye_size // 2:
            upper_lid_value += lid_speed
            if upper_lid_value > eye_size // 2:
                upper_lid_value = eye_size // 2

    # Draw left and right eyes
    draw_eye(0)
    draw_eye(SCREEN_WIDTH // 2)

    # Draw overlay image if active
    if current_image_index != 0 and 1 <= current_image_index <= len(images):
        img = images[current_image_index - 1]
        img = pygame.transform.scale(img, (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        screen.blit(img, (0, 0))
        screen.blit(img, (SCREEN_WIDTH // 2, 0))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
