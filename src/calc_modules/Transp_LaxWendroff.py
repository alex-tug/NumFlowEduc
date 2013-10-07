'''
Transport equation
explicit - Lax-Wendroff scheme
'''

def calcLWtransport(pd, method, to_step):    #pd ... project data

    stable_calc = pd.CFL2 + 2.0*pd.v*pd.dt/((pd.dx)**2)
    pd.is_stable[method] = (stable_calc<=1)
        
    pd.legend_adder[method] = "stable? " + str(pd.is_stable[method]) + \
                "\nCr = " + str(pd.CFL) + \
                "\nPE = " + str(pd.PE) + \
                "\nCr(Cr+2/PE) = " + str(stable_calc)
                
                
    if pd.PE != 0:
        stab_str_transp = str(pd.CFL*(1.0+2.0/pd.PE))
    else:
        stab_str_transp = "NA"
    print ("stab_str_transp = ", stab_str_transp)
    
    # a,b ... temporary variable for better readability
    a = 0.5 * stable_calc
    b = 0.5 * pd.CFL
    print ("b = ", b)
    
    for n in range(1,to_step) :
        
        pd.u_1[1:-1] = ( 1.0*a  +1.0*b      ) * pd.u_0[0:-2]\
                      +(-2.0*a          +1.0) * pd.u_0[1:-1]\
                      +( 1.0*a  -1.0*b      ) * pd.u_0[2:]      
         
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
         
        pd.u_1[0] = 0
        pd.u_1[-1] = 0  # 'boundary conditions', just for now, ToDo
        #pd.i_min += 1       # first point can't be calculated, so its value is undefined
        #pd.i_max -= 1       # last point can't be calculated, so its value is undefined