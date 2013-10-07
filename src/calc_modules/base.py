''' 
calculation/ base module
    define calcAdvection(method, pd)
        prepare stuff for the calculations, 
        call them and plot data into figures
'''

from matplotlib import pyplot as plt
import numpy as np
from numpy import fft 

from calc_modules.Advection_Upwind import calcUpwind
from calc_modules.Advection_LaxWendroff import calcLaxWendroff
from calc_modules.Advection_LeapFrog import calcLeapFrog
from calc_modules.Advection_CrankNicolson import calcCrankNicolson
from calc_modules.Diffusion_FTCS import calcFTCSdiffusion
from calc_modules.Transp_FTCS import calcFTCStransport
from calc_modules.Transp_Upwind import calcUpwindTransport
from calc_modules.Transp_LaxWendroff import calcLWtransport
from calc_modules.Transp_CrankNicolson import calcCNtransport

def replaceBadValues(vec):   
    BIG_NUMBER = 1e20
    BIG_NUMBER_NEG = -1 * 1e20
    
    sel_nan = [np.isnan(vec)]
    vec[sel_nan] = 0
    
    #sel_inf = [vec==np.inf]
    sel_inf = [vec>BIG_NUMBER]
    vec[sel_inf] = BIG_NUMBER
    
    #sel_neg_inf = [vec==-np.inf]
    sel_neg_inf = [vec<BIG_NUMBER_NEG]
    vec[sel_neg_inf] = BIG_NUMBER_NEG
        
    return vec


def calcBase(method, pd):
    ''' 
    prepare stuff for the calculations, 
    call them and plot data into figures
    '''
      
    pd.u_0 = pd.u_00                # reset data to input signal    
    plt.clf()                       # clear plot
    
    if method in pd.figures:  #get/create figure
        fig1 = pd.figures[method]
    else:
        fig1 = plt.figure()
        pd.figures[method] = fig1
            
    axarr = [0,0,0,0]
    axarr[0] = fig1.add_subplot(2,2,1)
    axarr[1] = fig1.add_subplot(2,2,2)
    axarr[2] = fig1.add_subplot(2,2,3)
    axarr[3] = fig1.add_subplot(2,2,4)
    
    axarr[0].plot(pd.x,pd.u_0,'g-')      # plot input signal; green
    
    # analytic solution
    # based on fourier transformation and script MalchereK: p.99 (eq.9.2)
    # add if pd.Ne = 0 => simply shift input signal
    # axarr[1].plot(pd.x+pd.c*pd.dt*pd.steps,pd.u_0,'r-') # simply shift input signal and plot it again; red

    t_f = pd.dt*pd.steps    # time final
    
    fft_coeff = fft.rfft(pd.u_00)
    #ifft_coeff = fft.fft(pd.u_00)
    
    #fft_coeff = fft_coeff[:-1]
    fft_freq = fft.fftfreq(len(pd.u_00), d=pd.dx)*2.0*np.pi
    fft_freq = fft_freq[:len(fft_coeff)]
    #k_vec = np.arange(len(fft_coeff))
    #coeff = enumerate(fft_coeff)
    
    fft_coeff = [val*np.exp(-1.0*(k*k)*pd.v*t_f)\
                for (k, val) in zip(fft_freq, fft_coeff)]
         
                
    #fft_coeff = [fft_coeff *\
    #        np.exp(-1.0*(k_vec) * pd.v*t_f\
    
    #fft_coeff = fft_coeff * np.exp(-1.0*(fft_freq*fft_freq) * pd.v*t_f)
    # + c*t
    #pd.u_0 = fft.irfft(fft_coeff)
    
    
    
    
     # simply shift input signal and plot it again; red
    #axarr[1].plot(pd.x+pd.c*t_f,pd.u_0,'r-')
    axarr[1].plot(pd.x+pd.c*t_f,fft.irfft(fft_coeff),'r-')
    
    
    
    
    
    
    
    
    pd.resetI_minmax()

    if method == 'upw':
        calcUpwind(pd, method, to_step=pd.steps)
    elif method == 'lw':  
        calcLaxWendroff(pd, method, to_step=pd.steps)
    elif method == 'lf':  
        calcLeapFrog(pd, method, to_step=pd.steps)
    elif method == 'cn':  
        calcCrankNicolson(pd, method, to_step=pd.steps)
    elif method == 'ftcs_diff':  
        calcFTCSdiffusion(pd, method, to_step=pd.steps)
    elif method == 'ftcs_transp':
        calcFTCStransport(pd, method, to_step=pd.steps)
    elif method == 'upw_transp':
        calcUpwindTransport(pd, method, to_step=pd.steps)
    elif method == 'lw_transp':
        calcLWtransport(pd, method, to_step=pd.steps)
    elif method == 'cn_transp':
        calcCNtransport(pd, method, to_step=pd.steps)
        
        
                                                     
    pd.x = np.nan_to_num(pd.x)
    pd.u_1 = replaceBadValues(pd.u_1)
    
    pd.x = np.reshape(pd.x,[pd.x.size,1])
    axarr[2].plot(pd.x[pd.i_min:pd.i_max],pd.u_1[pd.i_min:pd.i_max], 'b-') # plot calculated data; blue

        
    legend_str = "\ncalc = " + method + \
                "\n" + pd.legend_adder[method]
    axarr[3].plot([1], label=legend_str)
    axarr[3].legend(loc=1, ncol=3, shadow=True)
    
    for ax in axarr:
        ax.set_xlim(pd.xlim_low,pd.xlim_high)      # set figure boundaries
        ax.set_ylim(pd.ylim_low,pd.ylim_high)
    
    #pd.figures[method] = fig1
    
 
        
        
        
    
    
    
    