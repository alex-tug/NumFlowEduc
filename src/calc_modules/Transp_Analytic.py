'''
Analytic solution for the Transport equation
'''

import numpy as np
from numpy import fft 

def calcTranspAnalytic(pd, m, to_step): #pd ... project data
    ''' 
    analytic solution using fft/ifft to calculate diffusion
    '''
    
    m.is_stable = True
        
    m.legend_adder =  "\nCr = " + str(round(pd.CFL,3)) + \
                      "\nPE = " + str(round(pd.PE,3))
    
    # analytic solution
    # based on fourier transformation and script Malcherek: p.99 (eq.9.2)

    t_f = pd.dt*pd.steps    # time final
    i_f = round(t_f*pd.c/pd.dx,0)  # how many dx-steps signal is shifted
    u_0 = pd.u_00.copy()
    u_0_adv = pd.u_00.copy()  
     
    # add if pd.Ne = 0 => simply shift input signal
    # advection: simply shift signal
    u_0_adv[i_f:len(u_0)] = u_0[:len(u_0)-i_f]
    u_0_adv[:i_f] = 0.0
    
    
    # diffusion: do fft, scale coefficients, do ifft
    if pd.v != 0.0:
        fft_coeff = fft.rfft(u_0_adv)
        #ifft_coeff = fft.fft(pd.u_00)
        
        #fft_coeff = fft_coeff[:-1]
        fft_freq = fft.fftfreq(len(u_0_adv), d=pd.dx)*2.0*np.pi
        fft_freq = fft_freq[:len(fft_coeff)]
        #k_vec = np.arange(len(fft_coeff))
        #coeff = enumerate(fft_coeff)
        
        fft_coeff = [val*np.exp(-1.0*(k*k)*pd.v*t_f)\
                    for (k, val) in zip(fft_freq, fft_coeff)]
             
        
    
        if (len(pd.x)%2) !=0:  #odd number off elements
            x_cut = pd.x[:(len(pd.x)-1)]
            m.i_max -= 1       # last point can't be calculated, so its value is undefined 
        else:   #even nr. of el. => cut last value
            x_cut = pd.x
            
        m.u_final = fft.irfft(fft_coeff)
    else:
        m.u_final = u_0_adv.copy()
    
   