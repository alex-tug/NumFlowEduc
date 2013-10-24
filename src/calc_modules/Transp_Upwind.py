'''
Transport equation
explicit - Upwind scheme
'''

def calcTranspUpwind(pd, m, to_step):    #pd ... project data
    alpha = 1.0 # = upwind   
    # Ne ... Neumann's number
    Ne = pd.v * pd.dt / ((pd.dx)**2) # = pd.CFL / pd.PE 
    
    stable_calc = pd.CFL + 2.0*Ne
    m.is_stable = (stable_calc<=1)
                    
    u_0 = pd.u_00.copy()
    u_1 = pd.u_00.copy()
    for n in range(1,to_step) : # for each timestep ...
                
        # alpha ... factor to determine which methods to use for differences
        # 1     ... backward differences
        # 0.5   ... central differences
        # 0     ... forward differences
        alpha = 0
        
        # Upwind scheme  
        # in case v==0.0 we can neglect the transport equation
        # so we don't need u[i+1] and can compute the last element
        
        if (pd.v == 0.0):   # ToDo: move this if out of the for-loop
            # first order upwind: (only advection!)
            u_1[1:] = u_0[1:]\
                          -pd.CFL * u_0[1:]\
                          +pd.CFL* u_0[0:-1]
            
#==============================================================================
#             # use 1st order upwind only u_1[1] (can't be calculated using 2nd order upw.)
#             u_1[1] = u_0[1] - pd.CFL * u_0[1]\
#                             + pd.CFL * u_0[0]
#         
#             # second order upwind: (only advection!)
#             u_1[2:] =   u_0[2:]\
#                         -1.0 *0.5*pd.CFL* u_0[0:-2]\
#                         +4.0 *0.5*pd.CFL* u_0[1:-1]\
#                         -3.0 *0.5*pd.CFL* u_0[2:]
#==============================================================================
            
        
        else:
            b = 1.0 / pd.PE # ToDo: handle division by zero!
            u_1[1:-1] = u_0[1:-1]\
                        +(    -   alpha   +   b )   * pd.CFL * u_0[0:-2]\
                        +(  1 - 2*alpha   - 2*b )   * pd.CFL * u_0[1:-1]\
                        +( -1 +   alpha   +   b )   * pd.CFL * u_0[2:]
        
        u_0 = u_1     # calculated values are input values for the next step
        
    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()
#        
#def calcUpwindTransport_old(pd, m, to_step):    #pd ... project data
#
#    Ne = pd.v * pd.dt / (pd.dx**2) # = pd.CFL / pd.PE 
#    
#    is_stable_1 = (pd.CFL + 2.0*Ne) <= 1.0          # p.102
#    is_stable_2 = ((1.0 - pd.CFL) * pd.PE ) <=2.0   # p.102
#
#    m.is_stable = is_stable_1 and is_stable_2
#    
#    m.legend_adder = "stable=" + str(m.is_stable) + \
#                "\nCr = " + str(round(pd.CFL, 2))# + \
#                #"\nPE = " + str(pd.PE) + \
#                #"\nNe = " + str(Ne)
#           
#    u_0 = pd.u_00.copy()
#    u_1 = pd.u_00.copy()   
#                
#    for n in range(1,to_step) : # for each timestep ...
#        
#        # FTCS scheme                    
#        u_1[1:-1] =  (    +0.5*pd.CFL +1.0*Ne) * u_0[0:-2]\
#                    +(1.0             -2.0*Ne) * u_0[1:-1]\
#                    +(    -0.5*pd.CFL +1.0*Ne) * u_0[2:]
#            
#        u_1[0] = 0
#        u_1[-1] = 0  # 'boundary conditions', just for now, ToDo
#        #pd.i_max -= 1
#        #pd.i_min += 1       # since first point can't be calculated, so its value is undefined
#
#        
#        u_0 = u_1     # calculated values are input values for the next step
#        
#    m.u_1 = u_1.copy()
#    m.u_final = u_1.copy()