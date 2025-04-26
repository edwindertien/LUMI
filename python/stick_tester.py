import pygame

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Check for joystick
if pygame.joystick.get_count() == 0:
    print("No joystick connected.")
    pygame.quit()
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Detected joystick: {joystick.get_name()}")
print(f"Number of buttons: {joystick.get_numbuttons()}")
print(f"Number of axes: {joystick.get_numaxes()}")
print(f"Number of hats: {joystick.get_numhats()}")

running = True
while running:
    pygame.event.pump()

    # Check buttons
    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i):
            print(f"Button {i} pressed!")

    # Check axes (joystick sticks)
    for i in range(joystick.get_numaxes()):
        axis = joystick.get_axis(i)
        if abs(axis) > 0.1:  # Small threshold to avoid noise
            print(f"Axis {i} moved: {axis:.2f}")

    # Check hats (D-pad)
    for i in range(joystick.get_numhats()):
        hat = joystick.get_hat(i)
        if hat != (0, 0):
            print(f"Hat {i} moved: {hat}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
