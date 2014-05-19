"""
Leap Frog scheme
"""

#from Adv_Upwind_1st import calcAdvUpwind1st
import config_file


def calc_transp_LeapFrog(pd, m, to_step):   # pd ... project data

    # a ... temporary variable for better readability
    # a = pd.CFL / pd.PE
    # a = pd.v * pd.dt / (pd.dx * pd.dx)
    # a = pd.NE
    
    stable_calc = pd.CFL2 + 2.0*pd.NE
    m.is_stable = (stable_calc<=1)
    
    # store signal as u(t-1)
    u_n1 = pd.u_00.copy()    
    # calculate first step using Upwind:
    config_file.modules['transp_upw'](pd, m, to_step=2)
    
    # mind that m.u_01 is used now instaead of pd.u_00 !
    u_0 = m.u_1.copy()
    u_1 = m.u_1.copy()  # to be overwritten
    
    for n in range(0, to_step):
        # transport equation

        u_1[1:-1] =         1.0       * u_n1[1:-1]\
                    +( pd.CFL +2.0*pd.NE) * u_0[0:-2]\
                    +(        -4.0*pd.NE) * u_0[1:-1]\
                    +(-pd.CFL +2.0*pd.NE) * u_0[2:]
        
        # boundary conditions
        u_1[0] = pd.bc_upstream(n*pd.dt)
        u_1[-1] = pd.bc_downstream(n*pd.dt)

        u_n1 = u_0.copy()    # t becomes t-1
        u_0 = u_1.copy()     # calculated values are input values for the next step

    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()