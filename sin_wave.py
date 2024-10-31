"""
 * author: Ohidul Islam
 * created on 30-10-2024-19h-02m
 * copyright 2024
"""

import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter

plt.rcParams["animation.ffmpeg_path"] = "C:/Program Files/ffmpeg/bin/ffmpeg.exe"

metadata = dict(title="Movie", artist="GoTigers")
writer = FFMpegWriter(fps=15, metadata=metadata)

fig, ax = plt.subplots()
ax.set_aspect("equal")
theta = np.linspace(0, 50 * pi, 2000)

# Set up the initial fixed circle in the center
x0, y0 = 0, 0
circle = plt.Circle((x0, y0), 0.1, color="blue", fill=True)
ax.add_patch(circle)
ax.set_xlim(-8, 30)
ax.set_ylim(-8, 8)

# Set radius for rotating circle
r = 5

# Create the rotating circle initially at an arbitrary point on the path
rot_cir = plt.Circle((r, 0), 0.2, color="r", fill=True)
ax.add_patch(rot_cir)

(trace_line,) = ax.plot([], [], "k-", lw=2)
(trace_curve,) = ax.plot([], [], "k-", lw=2)

(connect_center_to_outside,) = ax.plot([], [], "g-", lw=2)
(connect_circle_to_sin_curve,) = ax.plot([], [], "b-", lw=2)
x_data, y_data = [], []
theta_data = []
reverse_y_data = []


# Update function to move rot_cir around the center
def update(frame):
    connect_center_to_outside.set_data([], [])
    connect_circle_to_sin_curve.set_data([], [])
    # Calculate new x, y positions based on theta for each frame
    x = r * np.cos(theta[frame])
    y = r * np.sin(theta[frame])

    # Update the center of rot_cir
    rot_cir.set_center((x, y))
    connect_center_to_outside.set_data([x0, x], [y0, y])

    x_data.append(x)
    y_data.append(y)
    trace_line.set_data(x_data, y_data)

    reverse_y_data.insert(0, y)
    theta_data.append(2 * r + theta[frame])
    # theta_data.insert(0, 2 * r + theta[frame])
    trace_curve.set_data(theta_data, reverse_y_data)
    # plt.plot((x0, x), (y0, y), lw=2)

    connect_circle_to_sin_curve.set_data([x, 2 * r + theta[0]], [y, y])

    return (
        rot_cir,
        trace_line,
        connect_center_to_outside,
        trace_curve,
        connect_circle_to_sin_curve,
    )


# Create the animation
ani = animation.FuncAnimation(fig=fig, func=update, frames=len(theta), interval=30)
ani.save("sin.mp4", writer=writer)
plt.show()

# ani = animation.FuncAnimation(fig=fig, func=rotatating_circle, frames=40, interval=30)
# # writer.saving("test.mp4")
# # ani.save("projectile.mp4", writer=writer)
# plt.show()
