"""
Transport equation
explicit - FTCS scheme
"""

def calc_transp_FTCS(pd, m, to_step):    # pd ... project data

    # Ne = pd.v * pd.dt / (pd.dx**2)  # = pd.CFL / pd.PE
    
    m.is_stable = (pd.NE<=0.5)  & (pd.NE > 0)
       
    u_0 = pd.u_00.copy()
    u_1 = pd.u_00.copy()
        
    for n in range(1, to_step):    # for each timestep
        
        # FTCS scheme
        u_1[1:-1] =  (    +0.5*pd.CFL +1.0*pd.NE) * u_0[0:-2]\
                    +(1.0             -2.0*pd.NE) * u_0[1:-1]\
                    +(    -0.5*pd.CFL +1.0*pd.NE) * u_0[2:]
            
        # boundary conditions
        u_1[0] = pd.bc_upstream(n*pd.dt)
        u_1[-1] = pd.bc_downstream(n*pd.dt)

        u_0 = u_1     # calculated values are input values for the next step
    
    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()