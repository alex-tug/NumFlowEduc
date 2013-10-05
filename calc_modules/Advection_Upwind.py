'''
Upwind scheme
'''

#import numpy as np

def calcUpwind(pd, method, to_step):    #pd ... project data
    alpha = 1.0 # = upwind   
    # Ne ... Neumann's number
    Ne = pd.v * pd.dt / ((pd.dx)**2) # = pd.CFL / pd.PE 
    
    stable_calc = pd.CFL + 2.0*Ne
    pd.is_stable[method] = (stable_calc<=1)
    
    pd.legend_adder[method] = "stable? " + str(pd.is_stable[method]) + \
                "\nCr = " + str(pd.CFL) + \
                "\nPE = " + str(pd.PE) + \
                "\nCr(1+2/PE) = " + str(stable_calc)
                
    if pd.PE != 0.0:
        Ne = pd.CFL / pd.PE
    else:
        Ne = 0.0
    #print("type_a: ", type(a), a)
    #print("type: ", type(pd.u_1[1]))
    for n in range(1,to_step) : # for each timestep ...
                
        # alpha ... factor to determine which methods to use for differences
        # 1     ... backward differences
        # 0.5   ... central differences
        # 0     ... forward differences
        alpha = 0
        
        # Upwind scheme  
        # in case v==0.0 we can neglect the transport equation
        # so we don't need u[i+1] and can compute the last element
        
# old code: only backward differences
#        if (pd.v == 0.0):
#            pd.u_1[1:] = pd.u_0[1:]\
#                          -pd.CFL * pd.u_0[1:]\
#                          +pd.CFL* pd.u_0[0:-1]
        if (pd.v == 0.0): # still only backward differences
            pd.u_1[1:] = pd.u_0[1:]\
                          -pd.CFL * pd.u_0[1:]\
                          +pd.CFL* pd.u_0[0:-1]
        else:
            # a, b ... temporary variable for better readability
            # a = pd.v * pd.dt / (pd.dx * pd.dx)
            # a = pd.CFL / pd.PE
            b = 1.0 / pd.PE # ToDo: handle division by zero!
            pd.u_1[1:-1] = (    - alpha + b) * pd.CFL * pd.u_0[0:-2]\
                          +(  1 + pd.CFL * (1 - 2*alpha -2*b)) * pd.u_0[1:-1]\
                          +( -1 + alpha + b) * pd.CFL * pd.u_0[2:]
        
        #pd.u_n1 = pd.u_0
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
        
