'''
Upwind scheme
'''

#import numpy as np

def calcUpwind(pd, to_step):    #pd ... project data
    
    for n in range(1,to_step) : # for each timestep ...
        
        # a ... temporary variable for better readability
        # a = pd.v * pd.dt / (pd.dx * pd.dx)
        a = pd.CFL / pd.PE
        
        # Upwind scheme  
        # in case v==0.0 we can neglect the transport equation
        # so we don't need u[i+1] and can compute the last element
        if (pd.v == 0.0):
            pd.u_1[1:] = pd.u_0[1:]\
                          -pd.CFL * pd.u_0[1:]\
                          +pd.CFL* pd.u_0[0:-1]
        else:                        
            pd.u_1[1:-1] = (   pd.CFL +  a) * pd.u_0[0:-2]\
                          +(1 -pd.CFL -2*a) * pd.u_0[1:-1]\
                          +(             a) * pd.u_0[2:]
        
        #pd.u_n1 = pd.u_0
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
          
        pd.i_min += 1       # since first point can't be calculated, so its value is undefined
        pd.i_max -= 0