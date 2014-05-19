"""
Transport equation
explicit - Lax-Wendroff scheme
"""


def calc_transp_LW(pd, m, to_step):

<<<<<<< HEAD
    # a,b ... temporary variable for better readability
    a = 0.5 * pd.CFL2 + pd.NE
    b = 0.5 * pd.CFL

    stable_calc = 2.0 * a
=======
    stable_calc = pd.CFL2 + 2.0*pd.v*pd.dt/(pd.dx **2)
>>>>>>> ff862db... - improved analytic solution using fft and shift-theorem
    m.is_stable = (stable_calc<=1)
                
#==============================================================================
#     if pd.PE != 0:
#         stab_str_transp = str(pd.CFL*(1.0+2.0/pd.PE))
#     else:
#         stab_str_transp = "NA"
#==============================================================================

    u_0 = pd.u_00.copy()
    u_1 = pd.u_00.copy()
    
<<<<<<< HEAD
    for n in range(0, to_step):
=======
    for n in range(1, to_step):
>>>>>>> ff862db... - improved analytic solution using fft and shift-theorem
        
        if pd.v == 0.0:
            #  only advection
            u_1[1:-1] += ( 1.0 + pd.CFL) *b  * u_0[:-2]\
<<<<<<< HEAD
                        +(     - pd.CFL2)   * u_0[1:-1]\
                        +(-1.0 + pd.CFL) *b  * u_0[2:]
        else:       
        
            u_1[1:-1] =  (     a  +b    ) * u_0[:-2]\
                        +(-2.0*a    +1.0) * u_0[1:-1]\
                        +(     a  -b    ) * u_0[2:]
=======
                        +      - pd.CFL2     * u_0[1:-1]\
                        +(-1.0 + pd.CFL) *b  * u_0[2:]
        else:       
        
            u_1[1:-1] = u_0[1:-1]\
                        +( 1.0*a  +1.0*b )    * u_0[:-2]\
                        +(-2.0*a         )    * u_0[1:-1]\
                        +( 1.0*a  -1.0*b )    * u_0[2:]
>>>>>>> ff862db... - improved analytic solution using fft and shift-theorem
         
        # boundary conditions
        u_1[0] = pd.bc_upstream(n*pd.dt)
        u_1[-1] = pd.bc_downstream(n*pd.dt)
        
        u_0 = u_1     # calculated values are input values for the next step

    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()