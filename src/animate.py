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

from itertools import product

# import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

from data.project import ProjectData
from data.method import MethodData
import config_file as config


# animation function.  This is called sequentially
def animate(index, pd, lines):
    assert isinstance(pd, ProjectData)
    x = pd.x

    lines = []
    for method in pd.methods.itervalues():
        assert isinstance(method, MethodData)
        method.calc(to_step=index)
        y = method.u_final
        #y = np.sin(2 * np.pi * (x - 0.01 * index + 0.1 * j))
        method.line.set_data(x, y)
        lines.append(method.line)
    return lines


dx_vec = config.dx_vec
dt_vec = config.dt_vec
c_vec = config.c_vec
v_vec = config.v_vec
step_vec = config.step_vec
signal_vec = config.signal_vec
method_vec = config.method_vec
output_folder = config.folder_output

# iterate over all combinations!
for par in product(dx_vec, dt_vec, c_vec, v_vec, step_vec, signal_vec):
    print "\n", par

    # ProjectData handles input data, figures, etc.
    #global pd
    pd = ProjectData(dx=par[0], dt=par[1], c=par[2],
                     v=par[3], steps=par[4], signal=par[5])

    # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure()
    ax = plt.axes(xlim=(config.x_lim_low, config.x_lim_high), ylim=(config.y_lim_low, config.y_lim_high))
    lines = []
    # iterate over all methods in method_vec
    for method in method_vec:
        pd.methods[method] = MethodData(pd, method)

        tmp_line, = ax.plot([], [], lw=2)
        pd.methods[method].line = tmp_line
        lines.append(tmp_line)

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate,
                                   frames=100,
                                   interval=1,
                                   fargs=(pd, lines),
                                   blit=True)

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    anim.save(output_folder + '/video/basic_animation.mp4', fps=10, extra_args=['-vcodec', 'libx264'])
