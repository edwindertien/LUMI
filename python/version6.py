import pygame
import random
import sys
import time
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

# Initialize pygame
pygame.init()

# Setup display
screenWidth, screenHeight = 192, 80
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("LUMI Eyes Control")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Eye parameters
eyeSize = 5 * screenHeight / 8
upperValue = eyeSize / 2
blink = False
dilate = False
pupilPosX = pupilPosY = 0
pupilSize = 0.55 * eyeSize
current_pupil_color = WHITE

# Blink parameters
blinkTimer = 0
nextBlinkTime = random.randint(4000, 15000)
blinkDuration = random.randint(5, 20)

# Pupil movement smoothing
prevEyeX, prevEyeY = 0, 0
eyeMoveThreshold = 200  # ms to consider eyes as focused
lastEyeMoveTime = 0
isFocusing = False

# Eyelid control
blinkSpeed = 0.1
eyelidPosition = 0
eyelidSpeed = 0.05

# Main loop flag
running = True

def draw_eyes(x, y, blink):
    global eyelidPosition
    
    lidMid = screenHeight / 2
    dLid = 0
    # Clamp pupil position to stay inside the eye boundaries
    if y > screenHeight:
        y = screenHeight
    if y < 0:
        y = 0
    if x < eyeSize / 2:
        x = eyeSize / 2
    if x > (screenWidth / 2 - eyeSize / 2):
        x = screenWidth / 2 - eyeSize / 2
    
    # Draw the eye (left and right)
    pygame.draw.circle(screen, current_pupil_color, (int(x), int(y)), int(pupilSize))
    pygame.draw.circle(screen, current_pupil_color, (int(x + screenWidth / 2), int(y)), int(pupilSize))

    # Eyelid logic: smooth blink and pupil-based eyelid shape
    if blink:
        eyelidPosition += blinkSpeed
    else:
        eyelidPosition -= blinkSpeed
    
    eyelidPosition = max(0, min(eyeSize / 2, eyelidPosition))

    # Left eyelid top and bottom
    pygame.draw.polygon(screen, BLACK, [(x - eyeSize / 2, y - eyeSize / 2 + eyelidPosition),
                                        (x + eyeSize / 2, y - eyeSize / 2 + eyelidPosition),
                                        (x + eyeSize / 2, y + eyeSize / 2 - eyelidPosition),
                                        (x - eyeSize / 2, y + eyeSize / 2 - eyelidPosition)])

    # Right eyelid top and bottom
    pygame.draw.polygon(screen, BLACK, [(x + screenWidth / 2 - eyeSize / 2, y - eyeSize / 2 + eyelidPosition),
                                        (x + screenWidth / 2 + eyeSize / 2, y - eyeSize / 2 + eyelidPosition),
                                        (x + screenWidth / 2 + eyeSize / 2, y + eyeSize / 2 - eyelidPosition),
                                        (x + screenWidth / 2 - eyeSize / 2, y + eyeSize / 2 - eyelidPosition)])

# Main loop
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == pygame.JOYBUTTONDOWN:
            dilate = joystick.get_button(10)
            if joystick.get_button(0):  # Button A
                current_pupil_color = GREEN  # Bright green
            if joystick.get_button(1):  # Button B
                current_pupil_color = RED  # Red
            if joystick.get_button(2):  # Button X
                current_pupil_color = BLUE  # Blue
            if joystick.get_button(3):  # Button Y
                current_pupil_color = YELLOW  # Yellow
            if joystick.get_button(8):  # Back button
                print("Back button pressed. Exiting...")
                running = False

    # Get joystick inputs for pupil position
    pupilPosX = joystick.get_axis(0) * (screenWidth / 2)  # Left/Right
    pupilPosY = joystick.get_axis(1) * screenHeight  # Up/Down

    # Blink control: periodically trigger blink
    if time.time() * 1000 > blinkTimer + nextBlinkTime:
        blinkTimer = time.time() * 1000
        nextBlinkTime = random.randint(4000, 15000)
        blinkDuration = random.randint(5, 20)

    if blinkDuration > 0:
        blink = True
        blinkDuration -= 1
    else:
        blink = False

    # Smooth eye movement
    eyeX = pupilPosX * 0.10 + prevEyeX * 0.90
    eyeY = pupilPosY * 0.10 + prevEyeY * 0.90

    prevEyeX = eyeX
    prevEyeY = eyeY

    # Draw eyes with the current pupil color and eyelid shape
    draw_eyes(eyeX, eyeY, blink)
    
    # Refresh display
    pygame.display.flip()
    pygame.time.wait(10)

# Quit pygame
pygame.quit()
sys.exit()
