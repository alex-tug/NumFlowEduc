'''
Lax Wendroff scheme
'''


def calcLaxWendroff(pd, to_step):   #pd ... project data
    
    for n in range(1,to_step) :
        
        #=======================================================================
        # original formula
        # pd.u_1 = zeros(pd.size_x)
        # for i in range(i_min,i_max) : 
        #    # original:
        #    pd.u_1[i] = pd.u_0[i]\
        #               -(pd.CFL/2.0)*(pd.u_0[i+1]-pd.u_0[i-1])\
        #               +((pd.CFL**2.0)/2.0) * (pd.u_0[i-1]-2.0*pd.u_0[i]+pd.u_0[i+1])
        #=======================================================================
          
        # new: transport equation
        # b ... temporary variable for better readability
        b = 2.0 * pd.v / (pd.c * pd.c * pd.dt)
        pd.u_1[1:-1] = \
                    + ( (pd.CFL + pd.CFL2 + b) /2.0) * pd.u_0[:-2]\
                    + (1 - pd.CFL2 - b)              * pd.u_0[1:-1]\
                    + ( (pd.CFL2 + b - pd.CFL) /2.0) * pd.u_0[2:]
                    
        #=======================================================================
        # old: only advection
        # pd.u_1[1:-1] = \
        #            + ( (pd.CFL + pd.CFL2) /2.0) * pd.u_0[:-2]\
        #            + (1 - pd.CFL2)              * pd.u_0[1:-1]\
        #            + ( (pd.CFL2 - pd.CFL) /2.0) * pd.u_0[2:]
        #=======================================================================
         
        #pd.u_n1 = pd.u_0
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
         
        pd.i_min += 1       # first point can't be calculated, so its value is undefined
        pd.i_max -= 1       # last point can't be calculated, so its value is undefined
