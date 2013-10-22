'''
    do all stuff related to plotting and matplotlib and so on
'''

from matplotlib import pyplot as plt
import numpy as np

from calc_modules.base import replaceBadValues

def drawPlot(pd):

    plt.clf()                       # clear plot

    fig = plt.figure()    
    
    plt.plot(pd.x, pd.u_00,'k-', label="orig. signal")   # plot initial shape (green)
    
    for m in pd.methods.itervalues():     # plot each method's results
    
        x_temp = np.nan_to_num(pd.x)
        #x_temp = np.reshape(x_temp,[x_temp,1])
        
        u_temp = replaceBadValues(m.u_final)
        
        legend_str = m.name + " " + m.legend_adder
                
        plt.plot(x_temp[m.i_min:m.i_max], u_temp[m.i_min:m.i_max], label=legend_str)
            
    plt.legend(loc=1, ncol=1, shadow=True)
    plt.ylim(pd.ylim_low, pd.ylim_high)
    
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
        