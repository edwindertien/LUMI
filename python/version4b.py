import pygame
import random
import math
import sys

# Initialize
pygame.init()
pygame.mixer.init()

screen_width = 192
screen_height = 80
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
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
blink_progress = 0.0
blinking = False
blink_direction = 1
next_blink_time = pygame.time.get_ticks() + random.randint(4000, 7000)
blink_pause = 200
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

# Image and sound mapping
hat_images = {
    (0, 1): 'data/up.bmp',
    (0, -1): 'data/down.bmp',
    (-1, 0): 'data/left.bmp',
    (1, 0): 'data/right.bmp'
}
hat_sounds = {
    (0, 1): 'data/up.wav',
    (0, -1): 'data/down.wav',
    (-1, 0): 'data/left.wav',
    (1, 0): 'data/right.wav'
}
current_image = None
current_sound = None

def load_image(path):
    try:
        return pygame.image.load(path).convert()
    except:
        print(f"Failed to load image {path}")
        return None

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        print(f"Failed to load sound {path}")
        return None

def play_sound(sound):
    if sound:
        sound.play()

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
        (center_x, lid_y - 20 * (1-blink_amt)),
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
            if joystick.get_button(8):
                print("Back button pressed. Exiting...")
                running = False
            if joystick.get_button(0):
                current_pupil_color = (0, 255, 0)
            if joystick.get_button(1):
                current_pupil_color = (255, 0, 0)
            if joystick.get_button(2):
                current_pupil_color = (0, 0, 255)
            if joystick.get_button(3):
                current_pupil_color = (255, 255, 0)

        if event.type == pygame.JOYHATMOTION:
            hat = joystick.get_hat(0)
            if hat in hat_images:
                img_path = hat_images[hat]
                snd_path = hat_sounds[hat]
                current_image = load_image(img_path)
                current_sound = load_sound(snd_path)
                play_sound(current_sound)

    # Update pupil position based on joystick
    if joystick:
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)
        pupil_pos_x = left_eye_x + int(x_axis * eye_radius * 0.5)
        pupil_pos_y = eye_center_y + int(y_axis * eye_radius * 0.5)

        dilate = joystick.get_button(10)
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
                blink_direction = -1
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

    if current_image:
        screen.blit(current_image, (0, 0))

    draw_eye(left_eye_x, eye_center_y, blink_progress)
    draw_eye(right_eye_x, eye_center_y, blink_progress)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
