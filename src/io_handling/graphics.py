"""
    do all stuff related to plotting and matplotlib and so on
"""

from matplotlib import pyplot as plt
import numpy as np

from calc_modules.base import cut_too_big_values


def draw_plot(pd):

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
            
    ax.legend(bbox_to_anchor=(0.4, 0.9, 0.0, 0.0),
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

    plt.clf()   # clear plot

    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.85, 0.85], label='axes1')

    points_green = []
    points_blue = []
    points_red = []

    for el in stability_data:
        # print "el: ", el
        if el[4]:
            points_blue.append([el[1], el[0]])
        elif not el[3]:
            points_red.append([el[1], el[0]])
        else:
            points_green.append([el[1], el[0]])

    print "points_green: ", points_green
    print "points_blue: ", points_blue
    print "points_red: ", points_red

    if points_green:
        x, y = zip(*points_green)
        ax.plot(x, y, 'go')

    if points_blue:
        x, y = zip(*points_blue)
        ax.plot(x, y, 'bo')

    if points_red:
        x, y = zip(*points_red)
        ax.plot(x, y, 'ro')

    #ax.plot([0.01, 0.01, 0.99, 0.99], [0.01, 0.99, 0.01, 0.99], 'bo')

    plt.xlim(-0.1, 2.1)
    plt.ylim(-0.1, 2.1)
    plt.grid()

    plt.xlabel('NE', fontsize=18)
    plt.ylabel('CFL', fontsize=18)

    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(18)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(18)

    ax.get_xaxis().set_visible(True)
    ax.get_yaxis().set_visible(True)

    return fig


#    axarr = [0,0,0,0]
#    axarr[0] = fig1.add_subplot(2,2,1)
#    axarr[1] = fig1.add_subplot(2,2,2)
#    axarr[2] = fig1.add_subplot(2,2,3)
#    axarr[3] = fig1.add_subplot(2,2,4)
    
    
    
    
#    axarr[0].plot(pd.x,pd.u_0,'g-')      # plot input signal; green
              
            
    
    #axarr[2].plot(pd.x[pd.i_min:pd.i_max],pd.u_1[pd.i_min:pd.i_max], 'b-') # plot calculated data; blue

        
                
    #axarr[3].plot([1], label=legend_str)
    #axarr[3].legend(loc=1, ncol=3, shadow=True)
    
    #for ax in axarr:
    #    ax.set_xlim(pd.xlim_low,pd.xlim_high)      # set figure boundaries
    #    ax.set_ylim(pd.ylim_low,pd.ylim_high)