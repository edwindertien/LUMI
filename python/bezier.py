import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from scipy.special import comb

# Function to calculate a Bézier curve
def bezier_curve(p0, p1, p2, p3, t):
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3

# Define the control points for the Bézier curve (start, control1, control2, end)
p0 = np.array([0, 0])    # Starting point
p1 = np.array([1, 2])    # First control point
p2 = np.array([2, 2])    # Second control point
p3 = np.array([3, 0])    # End point

# Generate points on the Bézier curve
t_values = np.linspace(0, 1, 100)
curve_points = np.array([bezier_curve(p0, p1, p2, p3, t) for t in t_values])

# Define the other polygon vertices (the straight edges)
other_points = np.array([[3, 0], [3, -2], [0, -2]])

# Combine the points to create the full polygon
polygon_points = np.vstack([curve_points, other_points])

# Create the polygon path and patch
path = Path(polygon_points)
patch = PathPatch(path, facecolor='lightblue', edgecolor='black', lw=2)

# Plot the result
fig, ax = plt.subplots()
ax.add_patch(patch)
ax.set_xlim(-1, 4)
ax.set_ylim(-3, 3)
ax.set_aspect('equal', 'box')
ax.grid(True)
plt.title("Polygon with One Bézier Curve Edge")
plt.show()
