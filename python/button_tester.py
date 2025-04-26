import pygame

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Check for joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick connected.")
    pygame.quit()
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Detected joystick: {joystick.get_name()}")

running = True
while running:
    pygame.event.pump()  # Refresh joystick state

    # Loop through all buttons
    for i in range(joystick.get_numbuttons()):
        if joystick.get_button(i):
            print(f"Button {i} pressed!")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
