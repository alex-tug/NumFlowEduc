'''
Advection
explicit - Upwind scheme - second order
'''

def calcAdvUpwind2nd(pd, m, to_step):    #pd ... project data

    stable_calc = pd.CFL
    m.is_stable = (stable_calc<=1)
                    
    u_0 = pd.u_00.copy()
    u_1 = pd.u_00.copy()
    if (pd.v == 0.0):
        for n in range(1,to_step) : # for each timestep ...        
            # Upwind scheme          
                
            # use 1st order upwind only u_1[1] (can't be calculated using 2nd order upw.)
            u_1[1] = u_0[1] - pd.CFL * u_0[1]\
                            + pd.CFL * u_0[0]
        
            # second order upwind: (only advection!)
            u_1[2:] =   u_0[2:]\
                        -1.0 *0.5*pd.CFL* u_0[0:-2]\
                        +4.0 *0.5*pd.CFL* u_0[1:-1]\
                        -3.0 *0.5*pd.CFL* u_0[2:]
                        
            u_1[0] = 0    # 'boundary conditions', just for now, ToDo
            
            u_0 = u_1     # calculated values are input values for the next step
        
    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()