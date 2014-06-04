"""
    do all stuff related to plotting and matplotlib and so on
"""

from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator   # , FormatStrFormatter
import numpy as np
# import config_file

from calc_modules.base import cut_too_big_values


def draw_plot(pd):
    """
        Plot all methods of this project and return one figure.

        There are some graphic options which might be moved
        to config_file or set from a gui or similar.
    """

    plt.clf()                       # clear plot

    fig = plt.figure()   
    ax = fig.add_axes([0.1, 0.1, 0.85, 0.85])
    
    # get index of lowest x-value greater than pd.xlim_low
    #x_i_min = np.argmax(pd.xlim_low < pd.x)
    # get index of highest x-value smaller than pd.xlim_high    
    #x_i_max = np.argmin(pd.xlim_high < pd.x) - 1
    #print x_i_min, " - ", x_i_max
    
    ax.plot(pd.x, pd.u_00, 'k-', label="orig. signal")   # plot initial shape (green)
    
    for m in pd.methods.itervalues():     # plot each method's results
    
        x_temp = np.nan_to_num(pd.x)
        
        u_temp = cut_too_big_values(m.u_final)
        
        legend_str = m.name     # + " " + m.legend_adder
                
        ax.plot(x_temp[m.i_min:m.i_max], u_temp[m.i_min:m.i_max], label=legend_str)
            
    ax.legend(bbox_to_anchor=(0.5, 0.6, 0.0, 0.0),
              loc=3, ncol=1, shadow=True, prop={'size': 24})
    #bbox_to_anchor=(0.5, 0.7, 0.0, 0.0),
    #ax.legend(loc=3, ncol=1, shadow=True, prop={'size': 24}, numpoints=1, scatterpoints = 1)

    plt.ylim(pd.y_lim_low, pd.y_lim_high)
    print "plt.xlim() 1: ", plt.xlim()
    print "new values: ", (pd.x_lim_low, pd.x_lim_high)
    plt.xlim(pd.x_lim_low, pd.x_lim_high)
    print "plt.xlim() 2: ", plt.xlim()
    #plt.set_xlim(pd.xlim_low, pd.xlim_high)

    plt.xlabel('x', fontsize=18)
    plt.ylabel('y', fontsize=18)
    
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(18) 
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(18) 
    
    return fig


def draw_stability_plot(stability_data):
    """
        this plots shows where the method is stable/unstable
    """

    plt.clf()   # clear plot

    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.85, 0.85])   # , label='axes1')

    points_green = []
    points_grey = []
    points_blue = []
    points_red = []

    for el in stability_data:
        if el[4] == 'True':     # el[4] = "is_not_null"
            # those points where every y-value is (nearly) zero
            points_grey.append([el[1], el[0]])

        elif el[5] == 'False':     # el[5] = "is_not_huge"
            # those points where some y-values are bigger than 10*signal_max (or smaller -10*signal_max)
            points_red.append([el[1], el[0]])

        elif el[3] == 'False':  # el[3] = "is_positive"
            # those points where the solution is stable but not every y-value is greater than zero
            points_blue.append([el[1], el[0]])

        else:
            # stable, positive, non-zero results :)
            points_green.append([el[1], el[0]])

    if points_grey:
        x, y = zip(*points_grey)
        ax.scatter(x, y, s=50, marker='s', facecolors='none', edgecolors='grey', label="f(x) ~ 0")

    if points_red:
        x, y = zip(*points_red)
        ax.scatter(x, y, s=50, marker='^', facecolors='none', edgecolors='r', label="instabil")

    if points_blue:
        x, y = zip(*points_blue)
        ax.scatter(x, y, s=50, marker='o', facecolors='none', edgecolors='b', label="tlw. negativ")

    if points_green:
        x, y = zip(*points_green)
        ax.scatter(x, y, s=50, marker='o', facecolors='g', edgecolors='g', label="positiv")

    plt.xlim(-0.1, 1.2)
    plt.ylim(-0.1, 1.2)
    ax.set_aspect('equal')
    #plt.axis('scaling')
    plt.grid()

    plt.xlabel('NE', fontsize=18)
    plt.ylabel('CFL', fontsize=18)

    # axis, formatting, ...
    #majorFormatter = FormatStrFormatter('%d')
    #minorLocator   = MultipleLocator(0.1)
    #majorLocator   = MultipleLocator(0.5)
    # ... Matplotlib reacts in a different way if you pass
    # these Locator-functions directly ...

    # ax.set_xticks(np.arange(0.0, 1.1, 0.5))
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.xaxis.set_minor_locator(MultipleLocator(0.1))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(MultipleLocator(0.1))

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(18)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(18)

    ax.get_xaxis().set_visible(True)
    ax.get_yaxis().set_visible(True)

    return fig

# some stuff to draw additional lines or change formatting etc.
# (may be deleted if not needed)

    # a = config_file.alpha

    # x_cut = np.linspace(0.0, 2.5)
    # x_cut_2 = np.linspace(0.0, 4.0)
    # x_cut_05 = np.linspace(0.0, 0.5)

    #y_1 = 2.0 * x_cut
    #y_2 = 2.0 + x_cut_2 * 0.0# - 2.0 * x_cut_05
    #y_2 = np.sqrt(1.0 - 2.0 * x_cut_05)
    #y_2 = [1.0/(1-2*a) * (2.0*i -1) for i in x_cut]
    #y_3 = [2*np.sqrt(i+0.5)-1 for i in x_cut]
    #y_4 = [-2.0*i + 1.0 for i in x_cut_2]

    #ax.plot(x_cut, y_1, 'k-', lw=2)
    #ax.plot(x_cut_2, y_2, 'k-', lw=2)
    #ax.plot(x_cut, y_3, 'k-', lw=2)

    #cfl_axis = np.linspace(0.0, 1.0)
    #ne_1 = [(-a)*i for i in cfl_axis]
    #ne_2 = [(-a)*i + 1 for i in cfl_axis]

    #ne_3 = [(0.5-a)*i +0.5 for i in cfl_axis]
    #ne_4 = [(0.5-a)*i for i in cfl_axis]
    #ne_4a = [(0.5-a)*i+i*i*0.5 for i in cfl_axis]

    #ne_5 = [(1-a)*i for i in cfl_axis]
    #ne_6 = [(1-a)*i+1 for i in cfl_axis]

    #ax.plot(ne_1, cfl_axis, 'b-', lw=2)
    #ax.plot(ne_2, cfl_axis, 'r-', lw=2)
    #ax.plot(ne_3, cfl_axis, 'k-', lw=2)
    #ax.plot(ne_4, cfl_axis, 'r-', lw=2)
    #ax.plot(ne_4a, cfl_axis, 'r-', lw=2)
    #ax.plot(ne_5, cfl_axis, 'k-', lw=2)
    #ax.plot(ne_6, cfl_axis, 'r.', lw=2)

    # bbox_props = dict(boxstyle="square, pad=0.3", fc="white", ec="k", lw=0.5)
    # arrow_props = dict(width=2, facecolor='black')

    # ax.annotate(r'$CFL = \sqrt{2 NE}$', xy=(0.3, 0.8),
    #             xytext=(0.05, 1.20),
    #             size=18,
    #             arrowprops=arrow_props
    #             )
    #
    # ax.annotate(r'$PE = 2$', xy=(0.35, 0.65),
    #             xytext=(0.80, 0.65),
    #             size=18,
    #             arrowprops=arrow_props,
    #             bbox=bbox_props
    #             )
    #
    # ax.annotate(r'$CFL = \sqrt{1-2NE}$', xy=(0.48, 0.3),
    #             xytext=(0.80, 0.50),
    #             size=18,
    #             arrowprops=arrow_props,
    #             bbox=bbox_props
    #             )
    # ax.annotate(r'$CFL = 2NE-1}$', xy=(0.70, 0.35),
    #             xytext=(0.9, 0.20),
    #             size=18,
    #             arrowprops=arrow_props,
    #             bbox=bbox_props
    #             )
    # ax.annotate(r'$0.5-0.5CFL$', xy=(0.36, 0.31),  # (0.60, 0.35)
    #             xytext=(0.6, 0.50),     # (0.8, 0.20)
    #             size=18,
    #             arrowprops=arrow_props,
    #             bbox=bbox_props
    #             )#r'$(0.5-\alpha)CFL+0.5$'

    # ax.annotate(r'$(1-\alpha)CFL$', xy=(0.7, 0.52),    # (0.43, 0.62)
    #             xytext=(0.1, 0.80),     # (0.8, 0.40)
    #             size=18,
    #             arrowprops=arrow_props,
    #             bbox=bbox_props
    #             )
    # ax.annotate(r'$(1-\alpha)CFL$', xy=(0.7, 0.52),    # (0.43, 0.62)
    #             xytext=(0.1, 0.80),     # (0.8, 0.40)
    #             size=18,
    #             arrowprops=arrow_props,
    #             bbox=bbox_props
    #             )



    #ax.legend(bbox_to_anchor=(0.5, 0.7, 0.05, 0.1),
    #          loc=3, ncol=1, shadow=True, prop={'size': 24}, numpoints=1, scatterpoints = 1)
    #ax.legend(bbox_to_anchor=(0.35, 1.0, 0.0, 0.0),
    #          loc=3, ncol=1, shadow=True, prop={'size': 24}, numpoints=1, scatterpoints = 1)
