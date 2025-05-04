import pygame
import numpy as np

# Function to calculate a Bézier curve
def bezier_curve(p0, p1, p2, p3, t):
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3

# Initialize Pygame
pygame.init()

# Define the screen dimensions and create a display surface
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Polygon with Bézier Curve Edge")

# Define the control points for the Bézier curve
p0 = np.array([50, 250])   # Starting point
p1 = np.array([150, 100])  # First control point
p2 = np.array([250, 100])  # Second control point
p3 = np.array([350, 250])  # End point

# Generate points on the Bézier curve
t_values = np.linspace(0, 1, 100)
curve_points = np.array([bezier_curve(p0, p1, p2, p3, t) for t in t_values])

# Define the other polygon vertices (the straight edges)
other_points = np.array([[350, 250], [350, 350], [50, 350]])

# Combine the points to create the full polygon
polygon_points = np.vstack([curve_points, other_points])

# Set up colors
light_blue = (173, 216, 230)
blue = (0, 0, 255)
black = (0, 0, 0)

# Run the Pygame main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the Bézier curve as a series of lines between points
    for i in range(1, len(curve_points)):
        pygame.draw.line(screen, blue, tuple(curve_points[i-1]), tuple(curve_points[i]), 2)

    # Draw the straight edges of the polygon
    for i in range(1, len(other_points)):
        pygame.draw.line(screen, blue, tuple(other_points[i-1]), tuple(other_points[i]), 2)

    # Draw and fill the polygon
    pygame.draw.polygon(screen, light_blue, polygon_points.tolist())
    pygame.draw.polygon(screen, black, polygon_points.tolist(), 2)  # Black outline for the polygon

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
