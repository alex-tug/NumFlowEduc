'''
Lax Wendroff scheme
'''


def calcAdvLaxWendroff(pd, m, to_step):   #pd ... project data

    stable_calc = pd.CFL2 + 2.0*pd.v*pd.dt/((pd.dx)**2)
    m.is_stable = (stable_calc<=1)
        
    m.legend_adder = "stable=" + str(m.is_stable)# + \
                #"\nCr = " + str(round(pd.CFL, 2))# + \
                #"\nPE = " + str(pd.PE) + \
                #"\nCr(Cr+2/PE) = " + str(stable_calc)
                
                
    if pd.PE != 0:
        stab_str_transp = str(pd.CFL*(1.0+2.0/pd.PE))
    else:
        stab_str_transp = "NA"
    
    # b ... temporary variable for better readability
    b = 2.0 * pd.v / (pd.c * pd.c * pd.dt)
    print ("b = ", b)
    
    u_0 = pd.u_00.copy()
    u_1 = u_0.copy()
    
    for n in range(1,to_step) :          
        # transport equation
        u_1[1:-1] =   ( ( pd.CFL + pd.CFL2 + b) /2.0) * u_0[:-2]\
                    + (      1.0 - pd.CFL2 - b)       * u_0[1:-1]\
                    + ( (-pd.CFL + pd.CFL2 + b) /2.0) * u_0[2:]
                    
        u_0 = u_1     # calculated values are input values for the next step
         
        m.i_min += 1       # first point can't be calculated, so its value is undefined
        m.i_max -= 1       # last point can't be calculated, so its value is undefined

    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()
    
    
        #=======================================================================
        # original formula
        # pd.u_1 = zeros(pd.size_x)
        # for i in range(i_min,i_max) : 
        #    # original:
        #    pd.u_1[i] = pd.u_0[i]\
        #               -(pd.CFL/2.0)*(pd.u_0[i+1]-pd.u_0[i-1])\
        #               +((pd.CFL**2.0)/2.0) * (pd.u_0[i-1]-2.0*pd.u_0[i]+pd.u_0[i+1])
        #=======================================================================
        #=======================================================================
        # old: only advection
        #pd.u_1[1:-1] = \
        #            + ( (pd.CFL + pd.CFL2) /2.0) * pd.u_0[:-2]\
        #            + (1 - pd.CFL2)              * pd.u_0[1:-1]\
        #            + ( (pd.CFL2 - pd.CFL) /2.0) * pd.u_0[2:]
        #=======================================================================
         