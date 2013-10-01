'''
Leap Frog scheme
'''

from Advection_Upwind import calcUpwind

def calcLeapFrog(pd, method, to_step):  #pd ... project data
    
    stable_calc = pd.CFL2 + 2.0*pd.v*pd.dt/((pd.dx)**2)
    pd.is_stable[method] = (stable_calc<=1)
    
    pd.legend_adder[method] = "stable? " + str(pd.is_stable[method]) + \
                "\nCr = " + str(pd.CFL) + \
                "\nPE = " + str(pd.PE) + \
                "\nCr(Cr+2/PE) = " + str(stable_calc)
    
    # calculate first step using Upwind:
    calcUpwind(pd, to_step=2)
    
    for n in range(2,to_step) :
        # new: trasport equation
        # a ... temporary variable for better readability
        # a = pd.v * pd.dt / (pd.dx * pd.dx)
        a = pd.CFL / pd.PE
        
        pd.u_1[1:-1] =        1.0                * pd.u_n1[1:-1]\
                       +pd.CFL * ( 1 +2.0/pd.PE) * pd.u_0[0:-2]\
                       +pd.CFL * (   -4.0/pd.PE) * pd.u_0[1:-1]\
                       +pd.CFL * (-1 +2.0/pd.PE) * pd.u_0[2:]
        
                      
        # old: according to: Malcherek, Num.Methoden d. Stroemungsmech. Glchg: 5.10, S.58
        # without diffusion
        #pd.u_1[1:-1] =  \
        #                 pd.CFL * pd.u_0[0:-2]\
        #               + 1      * pd.u_n1[1:-1]\
        #               - pd.CFL * pd.u_0[2:]
        # either this calculation is wrong,
        # or this method is extremely unstable
        
        pd.u_n1 = pd.u_0    # t becomes t-1 
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
        
        pd.i_min += 1       # first point can't be calculated, so its value is undefined
        pd.i_max -= 1       # last point can't be calculated, so its value is undefined