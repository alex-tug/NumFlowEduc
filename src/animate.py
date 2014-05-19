__author__ = 'Ace'

"""
Some of the following code is based on a Tutorial by Jake Vanderplas:
http://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/

Matplotlib Animation Example

author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

import config_file

n = 5   # number of lines

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
lines = []
for i in range(n):
    line, = ax.plot([], [], lw=2)
    lines.append(line)
#lines = [ax.plot([], [], lw=2) for i in range(n)]


# initialization function: plot the background of each frame
def init():
    for line in lines:
        line.set_data([], [])
    return lines


# animation function.  This is called sequentially
def animate(i):
    x = np.linspace(0, 10, 1000)
    j = 0
    for line in lines:
        y = np.sin(2 * np.pi * (x - 0.01 * i + 0.1 * j))
        line.set_data(x, y)
        j += 1
    return lines

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save(config_file.folder_output + '/video/basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
