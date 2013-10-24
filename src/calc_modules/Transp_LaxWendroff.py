'''
Transport equation
explicit - Lax-Wendroff scheme
'''

def calcTranspLW(pd, m, to_step):    #pd ... project data

    stable_calc = pd.CFL2 + 2.0*pd.v*pd.dt/((pd.dx)**2)
    m.is_stable = (stable_calc<=1)
                
#==============================================================================
#     if pd.PE != 0:
#         stab_str_transp = str(pd.CFL*(1.0+2.0/pd.PE))
#     else:
#         stab_str_transp = "NA"
#==============================================================================
    
    # a,b ... temporary variable for better readability
    a = 0.5 * stable_calc
    b = 0.5 * pd.CFL
    
    u_0 = pd.u_00.copy()
    u_1 = pd.u_00.copy()
    
    for n in range(1,to_step) :
        
        if pd.v == 0.0:
            #  only advection
            u_1[1:-1] +=  ( 1.0 + pd.CFL) *b  * u_0[:-2]\
                        +       - pd.CFL2     * u_0[1:-1]\
                        + (-1.0 + pd.CFL) *b  * u_0[2:]
        else:       
        
            u_1[1:-1] = u_0[1:-1]\
                        + ( 1.0*a  +1.0*b )    * u_0[:-2]\
                        + (-2.0*a         )    * u_0[1:-1]\
                        + ( 1.0*a  -1.0*b )    * u_0[2:]      
         
        u_0 = u_1     # calculated values are input values for the next step
         
        u_1[0] = 0
        u_1[-1] = 0  # 'boundary conditions', just for now, ToDo
        #m.i_min += 1       # first point can't be calculated, so its value is undefined
        #m.i_max -= 1       # last point can't be calculated, so its value is undefined
        
    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()