# Upwind scheme

from numpy import mod, zeros
from matplotlib import pyplot as plt


def calcUpwind(pd): #pd ... project data
  
    pd.u_0 = pd.u_00    # reset signal       
    pd.u_1 = pd.u_01    
    
    fig1 = plt.figure('upw')         
    plt.plot(pd.x,pd.u_0,'g-')
    plt.plot(pd.x+pd.c*pd.dt*pd.steps,pd.u_0,'r-')        
    
    i_min = 1
    i_max = pd.size_x-1
    
    for n in range(1,pd.steps) :
        #if mod(n,100) == 0: print "step: ", n
        
        pd.u_1 = zeros(pd.size_x)
        for i in range(i_min,i_max) : 
            pd.u_1[i] = pd.u_0[i]-pd.CFL*(pd.u_0[i]-pd.u_0[i-1])
        
        pd.u_0 = pd.u_1    
        i_min += 1
        i_max -= 0 
    
    #print i_min, i_max
    #print size(x[i_min:i_max])
    plt.plot(pd.x[i_min:i_max],pd.u_1[i_min:i_max])
    plt.xlim(pd.xlim_low,pd.xlim_high)
    plt.ylim(pd.ylim_low,pd.ylim_high)
    
    pd.figures['upw'] = fig1