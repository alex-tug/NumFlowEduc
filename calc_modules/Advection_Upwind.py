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
        
        
        # Upwind scheme  
        # in case v==0.0 we can neglect the transport equation
        # so we don't need u[i+1] and can compute the last element
        if (pd.v == 0.0):
            pd.u_1[1:] = (      pd.CFL) * pd.u_0[0:-1]\
                        +(1.0  -pd.CFL) * pd.u_0[1:]
            pd.i_max -= 0  
            
        else:                        
            pd.u_1[1:-1] = (    +(      -1.0)*pd.CFL -2.0*Ne) * pd.u_0[0:-2]\
                          +(1.0 +(alpha     )*pd.CFL +1.0*Ne) * pd.u_0[1:-1]\
                          +(    +(alpha -1.0)*pd.CFL +1.0*Ne) * pd.u_0[2:]
            pd.i_max -= 1  
        
        
        pd.i_min += 1       # since first point can't be calculated, so its value is undefined

                          
            #pd.u_1[1:-1] = (   pd.CFL +  a) * pd.u_0[0:-2]\
            #              +(1.0 -pd.CFL -2.0*a) * pd.u_0[1:-1]\
            #              +(          1.0*a) * pd.u_0[2:]
        
        #pd.u_n1 = pd.u_0
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
        