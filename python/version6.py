import pygame
import sys
import random
import os

# Initialize
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

# Screen setup
screen_width, screen_height = 192, 80
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("LUMI eye control")

clock = pygame.time.Clock()

blink = False
blink_timer = 0
next_blink_time = random.randint(4000, 15000)  # Random interval between blinks (ms)
blink_duration = 0  # Duration of a blink (frames)

# Colors
WHITE = (255, 255, 255)
BACKGROUND = (127, 127, 127)
EYE_COLOR = (0, 255, 100)
current_pupil_color = (0, 255, 100)  # Default greenish color

# Joystick setup
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    print("No joystick found!")
    sys.exit()

# Load images
image_folder = "data"
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
    path = os.path.join(image_folder, name)
    if os.path.exists(path):
        img = pygame.image.load(path).convert()
        images.append(img)
    else:
        print(f"Image not found: {path}")
        images.append(None)

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

# POV control
image_number = 0  # 0 = no image, 1-8 = images

def draw_eyes(x, y, blink_now):
    # Left Eye
    pygame.draw.ellipse(screen, current_pupil_color, (x - eye_size//2, y - eye_size//2, eye_size, eye_size))
    # Right Eye
    pygame.draw.ellipse(screen, current_pupil_color, (x + screen_width//2 - eye_size//2, y - eye_size//2, eye_size, eye_size))
    
    # Pupils
    pygame.draw.ellipse(screen, (0, 0, 0), (x - pupil_size//2, y - pupil_size//2, pupil_size, pupil_size))
    pygame.draw.ellipse(screen, (0, 0, 0), (x + screen_width//2 - pupil_size//2, y - pupil_size//2, pupil_size, pupil_size))

    # Draw eyelids dynamically following the pupil position
    eyelid_height = 10  # Eyelid curvature adjustment, change this to control the arc

    # Left Eyelid (dynamic polygon)
    pygame.draw.polygon(screen, (0, 0, 0), [
        (x - eye_size//2, y - eye_size//2 + eyelid_height),  # Top left
        (x - pupil_size//2, y - eye_size//2 + eyelid_height),  # Near pupil left
        (x - pupil_size//2, y - eye_size//2 - eyelid_height),  # Near pupil bottom left
        (x - eye_size//2, y - eye_size//2 - eyelid_height)   # Bottom left
    ])
    
    # Right Eyelid (dynamic polygon)
    pygame.draw.polygon(screen, (0, 0, 0), [
        (x + screen_width//2 - eye_size//2, y - eye_size//2 + eyelid_height),  # Top right
        (x + screen_width//2 + pupil_size//2, y - eye_size//2 + eyelid_height),  # Near pupil right
        (x + screen_width//2 + pupil_size//2, y - eye_size//2 - eyelid_height),  # Near pupil bottom right
        (x + screen_width//2 - eye_size//2, y - eye_size//2 - eyelid_height)   # Bottom right
    ])

def draw_image(img):
    if img is None:
        return
    img = pygame.transform.scale(img, (screen_width // 2, screen_height))
    screen.blit(img, (0, 0))
    screen.blit(img, (screen_width // 2, 0))

# Main loop
running = True
start_time = pygame.time.get_ticks()

while running:
    screen.fill(BACKGROUND)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
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

    if event.type == pygame.JOYBUTTONDOWN:
        if event.button == 0:
            current_pupil_color = (0, 255, 0)
        elif event.button == 1:
            current_pupil_color = (255, 0, 0)
        elif event.button == 2:
            current_pupil_color = (0, 0, 255)
        elif event.button == 3:
            current_pupil_color = (255, 255, 0)
        elif event.button == 8:
            print("Back button pressed. Exiting...")
            running = False
        elif event.button == 10:  # DILATE
            dilate = True
        elif event.button == 5:  # EYELID button (choose correct mapping later)
            blink = True  # Manual blink

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
    if image_number == 0:
        draw_eyes(int(pupil_x), int(pupil_y), blink)
    else:
        if 1 <= image_number <= len(images):
            draw_image(images[image_number - 1])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
