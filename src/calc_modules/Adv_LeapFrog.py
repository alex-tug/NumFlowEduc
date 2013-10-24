'''
Leap Frog scheme
'''

from Transp_Upwind import calcTranspUpwind

def calcAdvLeapFrog(pd, m, to_step):  #pd ... project data
    
    stable_calc = pd.CFL2 + 2.0*pd.v*pd.dt/((pd.dx)**2)
    m.is_stable = (stable_calc<=1)
    
    #m.legend_adder = "stable=" + str(m.is_stable)# + \
                #"\nCr = " + str(round(pd.CFL, 2)) + \
                #"\nPE = " + str(pd.PE) + \
                #"\nCr(Cr+2/PE) = " + str(stable_calc)
    
    # calculate first step using Upwind:
    calcTranspUpwind(pd, to_step=2)
    # ToDo: This won't work anymore!
    
    u_0 = pd.u_00.copy()
    u_1 = pd.u_00.copy()
    u_n1 = m.u_n1.copy()
    
    for n in range(2,to_step) :
        # new: trasport equation
        # a ... temporary variable for better readability
        # a = pd.v * pd.dt / (pd.dx * pd.dx)
        a = pd.CFL / pd.PE
        
        u_1[1:-1] =        1.0                * u_n1[1:-1]\
                    +pd.CFL * ( 1 +2.0/pd.PE) * u_0[0:-2]\
                    +pd.CFL * (   -4.0/pd.PE) * u_0[1:-1]\
                    +pd.CFL * (-1 +2.0/pd.PE) * u_0[2:]
        
                      
        # old: according to: Malcherek, Num.Methoden d. Stroemungsmech. Glchg: 5.10, S.58
        # without diffusion
        #pd.u_1[1:-1] =  \
        #                 pd.CFL * pd.u_0[0:-2]\
        #               + 1      * pd.u_n1[1:-1]\
        #               - pd.CFL * pd.u_0[2:]
        # either this calculation is wrong,
        # or this method is extremely unstable
        
        u_n1 = pd.u_0    # t becomes t-1 
        u_0 = pd.u_1     # calculated values are input values for the next step
        
        m.i_min += 1       # first point can't be calculated, so its value is undefined
        m.i_max -= 1       # last point can't be calculated, so its value is undefined
    
    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()