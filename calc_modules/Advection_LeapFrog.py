'''
Leap Frog scheme
'''

from Advection_Upwind import calcUpwind

def calcLeapFrog(pd, to_step):  #pd ... project data
    
    # calculate first step using Upwind:
    calcUpwind(pd, to_step=2)
    
    for n in range(2,to_step) :
        # according to: Malcherek, Num.Methoden d. Stroemungsmech. Glchg: 5.10, S.58              
        pd.u_1[1:-1] =  \
                         pd.CFL * pd.u_0[0:-2]\
                       + 1      * pd.u_n1[1:-1]\
                       - pd.CFL * pd.u_0[2:]
        # either this calculation is wrong,
        # or this method is extremely unstable
        
        pd.u_n1 = pd.u_0    # t becomes t-1 
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
        
        pd.i_min += 1       # first point can't be calculated, so its value is undefined
        pd.i_max -= 1       # last point can't be calculated, so its value is undefined