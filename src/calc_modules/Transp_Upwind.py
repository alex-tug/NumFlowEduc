"""
Transport equation
explicit - Upwind scheme
"""

#from linalg_helper import float_eq


def calc_transp_Upwind(pd, m, to_step):    # pd ... project data
    # alpha ... factor to determine which methods to use for differences
    # 1     ... backward differences
    # 0.5   ... central differences
    # 0     ... forward differences
    alpha = 1.0

    # Ne ... Neumann's number
    Ne = pd.v * pd.dt / (pd.dx**2)  # = pd.CFL / pd.PE
        
    stable_calc = pd.CFL + 2.0*Ne
    m.is_stable = (stable_calc<=1)
                    
    u_0 = pd.u_00.copy()
    u_1 = pd.u_00.copy()
    for n in range(0, to_step):     # for each timestep ...

        # Upwind scheme
        u_1[1:-1] = u_0[1:-1]\
            +((    +   alpha)* pd.CFL   +   Ne )  * u_0[0:-2]\
            +((  1 - 2*alpha)* pd.CFL   - 2*Ne )  * u_0[1:-1]\
            +(( -1 +   alpha)* pd.CFL   +   Ne )  * u_0[2:]
        
        # boundary conditions
        u_1[0] = pd.bc_upstream(n*pd.dt)
        u_1[-1] = pd.bc_downstream(n*pd.dt)
        
        u_0 = u_1     # calculated values are input values for the next step
        
    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()



# in case v==0.0 we could neglect the transport equation
# so we wouldn't need u[i+1] and could compute the last element...
#==============================================================================
#             # use 1st order upwind only u_1[1]
              # (can't be calculated using 2nd order upw.)
#            u_1[1:] = u_0[1:]\
#                          +pd.CFL * u_0[0:-1]\
#                          -pd.CFL * u_0[1:]
#
#             # second order upwind: (only advection!)
#             u_1[2:] =   u_0[2:]\
#                         -1.0 *0.5*pd.CFL* u_0[0:-2]\
#                         +4.0 *0.5*pd.CFL* u_0[1:-1]\
#                         -3.0 *0.5*pd.CFL* u_0[2:]
#==============================================================================