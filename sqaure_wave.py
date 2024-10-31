"""
 * author: Ohidul Islam
 * created on 31-10-2024-00h-00m
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


# variables
x0, y0 = 0, 0
R = 6
N = 5
w_scale = 0.5

# setup plots
fig, ax = plt.subplots()
ax.set_aspect("equal")
theta = np.linspace(0, 20 * pi, 1000)

# center main circle dot
circle = plt.Circle((x0, y0), 0.3, color="k", fill=True)
ax.add_patch(circle)
ax.set_xlim(-20, 40)
ax.set_ylim(-20, 20)

# need a rotating circle on the outer path
rot_cir = plt.Circle((0, 0), 0.5, color="r", fill=True)
ax.add_patch(rot_cir)

(trace_curve,) = ax.plot([], [], "k-", lw=2)  # trace the final sin curve
(connect_center_to_boundary,) = ax.plot(
    [], [], "g-", lw=2
)  # line from each cricles center to its boundary
(connect_circle_to_sin_curve,) = ax.plot(
    [], [], "b-", lw=2
)  # line from rotating circle to sin curve


theta_data = []
reverse_y_data = []

main_circles = []
main_circles_lines = []


# Update function
def update(frame):
    # remove the circles in each frame
    for temp_circle in main_circles:
        temp_circle.remove()
    main_circles.clear()

    # remove lines in each frame
    for lines in main_circles_lines:
        lines.remove()
        # print(lines)
    main_circles_lines.clear()

    connect_center_to_boundary.set_data([], [])
    connect_circle_to_sin_curve.set_data([], [])
    x, y = 0, 0

    # main loop
    for i in np.arange(N):
        prevx, prevy = x, y
        n = 2 * i + 1

        r = R * 4 / (n * pi)
        x += r * np.cos(w_scale * n * theta[frame])
        y += r * np.sin(w_scale * n * theta[frame])

        # Update the center of rot_cir
        main_circle = plt.Circle((prevx, prevy), r, color="g", fill=False)
        ax.add_patch(main_circle)
        main_circles.append(main_circle)
        rot_cir.set_center((x, y))

        #
        line = ax.plot([prevx, x], [prevy, y], "g-", lw=2)[0]
        # print(type(line))
        main_circles_lines.append(line)

    reverse_y_data.insert(0, y)
    translate_x = 10
    theta_data.append(translate_x + theta[frame])
    # # theta_data.insert(0, 2 * r + theta[frame])
    trace_curve.set_data(theta_data, reverse_y_data)
    connect_circle_to_sin_curve.set_data([x, translate_x], [y, y])

    return (
        rot_cir,
        connect_center_to_boundary,
        trace_curve,
        connect_circle_to_sin_curve,
    )


# animation
ani = animation.FuncAnimation(fig=fig, func=update, frames=len(theta), interval=1)
ani.save("square_wave.mp4", writer=writer)
plt.show()
