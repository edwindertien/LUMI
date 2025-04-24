# import pygame
# import os
# import sys

# # Initialize pygame
# pygame.init()
# pygame.mixer.init()

# # Constants
# screen_width = 192
# screen_height = 80
# FPS = 60

# def draw_eyes(screen, eye_x, eye_y, pupil_size, blink):
#     # Eye size
#     eye_radius = eye_size // 2
    
#     # Draw the eyes
#     pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), eye_radius)  # Left eye
#     pygame.draw.circle(screen, (255, 255, 255), (eye_x + screen_width // 2, eye_y), eye_radius)  # Right eye
    
#     # Draw the pupils
#     pygame.draw.circle(screen, (0, 0, 0), (eye_x, eye_y), pupil_size)  # Left pupil
#     pygame.draw.circle(screen, (0, 0, 0), (eye_x + screen_width // 2, eye_y), pupil_size)  # Right pupil

#     # Blink effect
#     if blink:
#         pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(eye_x - eye_radius, eye_y - eye_radius, eye_radius * 2, eye_radius))  # Upper lid
#         pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(eye_x - eye_radius, eye_y, eye_radius * 2, eye_radius))  # Lower lid

# # Setup display
# screen = pygame.display.set_mode((screen_width * 2, screen_height), pygame.FULLSCREEN)
# pygame.display.set_caption("LUMI eye control")

# # Load resources from 'data' folder
# DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# # Sound files
# sound_files = [
#     "lumi-alarm.mp3", "lumi-yes.mp3", "lumi-yes1.mp3", "lumi-yes2.mp3",
#     "lumi-no.mp3", "lumi-no2.mp3", "lumi-startup.mp3", "lumi-shutdown.mp3"
# ]
# sounds = [pygame.mixer.Sound(os.path.join(DATA_DIR, f)) for f in sound_files]

# # Image files
# image_files = [
#     "lumi-battery.jpg", "lumi-classified.jpg", "lumi-map.jpg", "lumi-route.jpg",
#     "lumi-noconnection.jpg", "lumi-ok.jpg", "lumi-weather.jpg", "lumi-steps.jpg",
#     "lumi-warning.jpg"
# ]
# images = [pygame.image.load(os.path.join(DATA_DIR, f)) for f in image_files]

# # Joystick initialization
# pygame.joystick.init()
# joystick = None
# if pygame.joystick.get_count() > 0:
#     joystick = pygame.joystick.Joystick(0)
#     joystick.init()
#     print("Joystick initialized:", joystick.get_name())
# else:
#     print("No joystick found!")

# # Game loop
# running = True
# blink = False
# pupil_size = eye_size // 3
# eye_x = screen_width // 4
# eye_y = screen_height // 2

# # Main loop
# clock = pygame.time.Clock()
# running = True
# while running:
#     screen.fill((127, 127, 127))  # Background color

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#             running = False

#     # TODO: Add joystick input handling and eye drawing here
#         if event.type == pygame.JOYAXISMOTION:
#             x_pos = joystick.get_axis(0)
#             y_pos = joystick.get_axis(1)
#             eye_x = int(x_pos * screen_width // 2 + screen_width // 4)  # Scale to screen size
#             eye_y = int(y_pos * screen_height // 2 + screen_height // 2)
        
#         if event.type == pygame.JOYBUTTONDOWN:
#             if joystick.get_button(0):  # Button A - toggle blink
#                 blink = not blink
    
#     # Fill the screen with a background color
#     screen.fill((127, 127, 127))
    
#     # Draw the eyes
#     draw_eyes(screen, eye_x, eye_y, pupil_size, blink)

#     pygame.display.flip()
#     clock.tick(FPS)

# pygame.quit()
# sys.exit()
import pygame
import sys

# Initialize pygame and joystick module
pygame.init()
pygame.joystick.init()

# Check for joysticks
if pygame.joystick.get_count() == 0:
    print("No joysticks connected.")
    pygame.quit()
    sys.exit()

# Connect to the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Detected joystick: {joystick.get_name()} with {joystick.get_numaxes()} axes, {joystick.get_numbuttons()} buttons")

# Main loop to print input events
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                print(f"Axis {event.axis} moved to {event.value:.2f}")
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} released")
except KeyboardInterrupt:
    print("Exiting...")

pygame.quit()