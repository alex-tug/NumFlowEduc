'''
Advection
explicit - Upwind scheme - first order
'''

def calc_adv_Upwind1st(pd, m, to_step):    #pd ... project data

    stable_calc = pd.CFL
    m.is_stable = (stable_calc<=1)
                    
    u_0 = pd.u_00.copy()
    u_1 = pd.u_00.copy()
    if (pd.v == 0.0):
        for n in range(1,to_step) : # for each timestep:        
               
            # first order upwind scheme: (only advection!)
            u_1[1:] = u_0[1:]\
                        -pd.CFL * u_0[1:]\
                        +pd.CFL * u_0[0:-1]
                        
            # 'boundary conditions'
            u_1[0] = pd.bc_upstream(n*pd.dt)
            
            u_0 = u_1     # calculated values are input values for the next step
        
    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()
