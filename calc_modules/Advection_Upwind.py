'''
Upwind scheme
'''

#import numpy as np

def calcUpwind(pd, to_step):    #pd ... project data
    
    for n in range(1,to_step) : # for each timestep ...
        
        # Upwind scheme              
        pd.u_1[1:] = pd.u_0[1:]\
                      -pd.CFL * pd.u_0[1:]\
                      +pd.CFL* pd.u_0[0:-1]\
        
        #pd.u_n1 = pd.u_0
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
          
        pd.i_min += 1       # since first point can't be calculated, so its value is undefined
        pd.i_max -= 0