'''
Transport equation
explicit - Upwind scheme
'''

def calcUpwindTransport(pd, method, to_step):    #pd ... project data

    Ne = pd.v * pd.dt / (pd.dx**2) # = pd.CFL / pd.PE 
    
    stable_calc = pd.CFL + 2.0*Ne
    pd.is_stable[method] = (stable_calc<=1)
    stable_calc = Ne
    pd.is_stable[method] = (stable_calc<=0.5)
    
    pd.legend_adder[method] = "stable? " + str(pd.is_stable[method]) + \
                "\nCr = " + str(pd.CFL) + \
                "\nPE = " + str(pd.PE) + \
                "\nNe = " + str(Ne)
                
                
    for n in range(1,to_step) : # for each timestep ...
        
        # FTCS scheme                    
        pd.u_1[1:-1] = (    +0.5*pd.CFL +1.0*Ne) * pd.u_0[0:-2]\
                      +(1.0             -2.0*Ne) * pd.u_0[1:-1]\
                      +(    -0.5*pd.CFL +1.0*Ne) * pd.u_0[2:]
            
        pd.u_1[0] = 0
        pd.u_1[-1] = 0  # 'boundary conditions', just for now, ToDo
        #pd.i_max -= 1
        #pd.i_min += 1       # since first point can't be calculated, so its value is undefined

        
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
        