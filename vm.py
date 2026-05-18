import math
from typing import Tuple

Vec3 = Tuple[float, float, float]


def length(v: Vec3) -> float:
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def kernel(point: Vec3, iterations: int = 5) -> float:
    """
    Mandelbulb-style fractal kernel.
    Takes a 3D point and returns a scalar field value.
    """

    x, y, z = point
    a_x, a_y, a_z = x, y, z

    for _ in range(iterations):
        r = length((a_x, a_y, a_z))

        # Avoid division by zero because math is petty
        if r == 0.0:
            break

        # Spherical coordinates
        theta = math.atan2(a_y, a_x) * 8.0
        phi = math.acos(a_z / r) * 8.0

        # Power scaling (the fractal part)
        r_powered = r ** 8.0

        # Convert back to Cartesian and offset by original point
        sin_phi = math.sin(phi)
        a_x = r_powered * sin_phi * math.cos(theta) + x
        a_y = r_powered * sin_phi * math.sin(theta) + y
        a_z = r_powered * math.cos(phi) + z

        # Escape condition
        if r_powered > 6.0:
            break

    # Implicit surface value
    return 4.0 - (a_x * a_x + a_y * a_y + a_z * a_z)

import numpy as np
import matplotlib.pyplot as plt

size = 300
scale = 2.0
image = np.zeros((size, size))

for i in range(size):
    for j in range(size):
        x = (i / size - 0.5) * scale
        y = (j / size - 0.5) * scale
        image[j, i] = kernel((x, y, 0.0))

plt.imshow(image, cmap="inferno")
plt.colorbar()
plt.title("Kernel Output Slice (z=0)")
plt.show()
