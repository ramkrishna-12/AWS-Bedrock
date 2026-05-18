import math
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple

Vec3 = Tuple[float, float, float]


def length(v: Vec3) -> float:
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])


def kernel(point: Vec3, iterations: int = 5) -> float:
    x, y, z = point
    a_x, a_y, a_z = x, y, z

    for _ in range(iterations):
        r = length((a_x, a_y, a_z))
        if r == 0.0:
            break

        theta = math.atan2(a_y, a_x) * 8.0
        phi = math.acos(a_z / r) * 8.0
        r_powered = r ** 8.0

        sin_phi = math.sin(phi)
        a_x = r_powered * sin_phi * math.cos(theta) + x
        a_y = r_powered * sin_phi * math.sin(theta) + y
        a_z = r_powered * math.cos(phi) + z

        if r_powered > 6.0:
            break

    return 4.0 - (a_x*a_x + a_y*a_y + a_z*a_z)


# ---------------- RAY MARCHER ---------------- #

WIDTH = 300
HEIGHT = 300
MAX_STEPS = 80
MAX_DIST = 6.0
SURFACE_EPS = 0.01

camera_pos = (0.0, 0.0, -3.0)
image = np.zeros((HEIGHT, WIDTH))

for y in range(HEIGHT):
    for x in range(WIDTH):
        # Normalized screen coordinates
        u = (x / WIDTH - 0.5) * 2.0
        v = (y / HEIGHT - 0.5) * 2.0

        # Ray direction
        ray_dir = (u, v, 1.0)
        ray_len = length(ray_dir)
        ray_dir = (
            ray_dir[0] / ray_len,
            ray_dir[1] / ray_len,
            ray_dir[2] / ray_len,
        )

        dist_traveled = 0.0
        hit = False

        for _ in range(MAX_STEPS):
            px = camera_pos[0] + ray_dir[0] * dist_traveled
            py = camera_pos[1] + ray_dir[1] * dist_traveled
            pz = camera_pos[2] + ray_dir[2] * dist_traveled

            d = kernel((px, py, pz))

            if d < SURFACE_EPS:
                hit = True
                break

            dist_traveled += max(d * 0.2, 0.01)
            if dist_traveled > MAX_DIST:
                break

        if hit:
            image[y, x] = 1.0 - dist_traveled / MAX_DIST
        else:
            image[y, x] = 0.0

# ---------------- DISPLAY ---------------- #

plt.imshow(image, cmap="inferno")
plt.title("Ray Marched Fractal")
plt.axis("off")
plt.show()
