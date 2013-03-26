''' 
calculation/ base module
    define calcAdvection(method, pd)
        prepare stuff for the calculations, 
        call them and plot data into figures
'''

from matplotlib import pyplot as plt

from calc_modules.Advection_Upwind import calcUpwind
from calc_modules.Advection_LaxWendroff import calcLaxWendroff
from calc_modules.Advection_LeapFrog import calcLeapFrog
from calc_modules.Advection_CrankNicolson import calcCrankNicolson


def calcAdvection(method, pd):
    ''' 
    prepare stuff for the calculations, 
    call them and plot data into figures
    '''
      
    pd.u_0 = pd.u_00                # reset data to input signal
    
    plt.clf()                       # clear plot
    fig1 = plt.figure(method)       # doesn't work completely well yet...
    plt.plot(pd.x,pd.u_0,'g-')      # plot input signal; green
    plt.plot(pd.x+pd.c*pd.dt*pd.steps,pd.u_0,'r-') # simply shift input signal and plot it again; red

    pd.resetI_minmax()

    if method == 'upw':
        calcUpwind(pd, to_step=pd.steps)
    elif method == 'lw':  
        calcLaxWendroff(pd, to_step=pd.steps)
    elif method == 'lf':  
        calcLeapFrog(pd, to_step=pd.steps)
    elif method == 'cn':  
        calcCrankNicolson(pd, to_step=pd.steps)
    
    
    plt.plot(pd.x[pd.i_min:pd.i_max],pd.u_1[pd.i_min:pd.i_max], 'b-') # plot calculated data; blue
    plt.xlim(pd.xlim_low,pd.xlim_high)      # set figure boundaries
    plt.ylim(pd.ylim_low,pd.ylim_high)
    
    pd.figures[method] = fig1