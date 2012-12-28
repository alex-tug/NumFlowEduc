'''
Crank-Nicolson scheme
'''

import numpy as np
import scipy.linalg as la


def calcCrankNicolson(pd, to_step): #pd ... project data
    ''' 
    Crank-Nicolson scheme
    according to: Malcherek, 'Num.Methoden d. Stroemungsmech.' Eq: 5.13, p.59
    
    NOT FINISHED!
    '''
    
    th = 0.75   # theta, Crank-Nicolson is stable for theta >= 0.5
    
    # A ... Band(!)-Matrix which comes from the CrankNicolson formula
    # A:
    #    1            th/2*CFL         0            ...            0
    #  -th/2*CFL         1           th/2*CFL        0             0
    #    0            -th/2*CFL        1           th/2*CFL        0
    #    ...
    #    ...                                                    th/2*CFL  
    #    0            ...................          -th/2*CFL       1 
    
    # A stored as Band matrix:    (otherwise its huge!)
    # A_band:
    #        0          th/2*CFL       th/2*CFL     ...       th/2*CFL       th/2*CFL 
    #        1             1              1         ...          1              1
    #     -th/2*CFL    -th/2*CFL      -th/2*CFL     ...      -th/2*CFL          0
    
    A_band = np.zeros( (3,pd.size_x) )
    A_band[0,1:] =       th/2.0 * pd.CFL * np.ones(pd.size_x-1)
    A_band[1,:] = np.ones(pd.size_x)
    A_band[2,:-1] = -1 * th/2.0 * pd.CFL * np.ones(pd.size_x-1)
    # upper left corner is zero because this upper diagonal is one position smaller than the main diagonal
    A_band[0,0] = 0.
    A_band[2,-1] = 0.     # same as upper left corner
    
    #print "A_band", A_band
    
    u_0_right = np.zeros(pd.size_x) 
    
    for n in range(1,to_step) :
                        
        # u_0_right is the right hand side of A_diag * u_1 = u_0_right which come from the CrankNicolson formula
        u_0_right[1:-1] = pd.u_0[1:-1]\
                        + (th-1) / 2.0 * pd.CFL * pd.u_0[2:]\
                        - (th-1) / 2.0 * pd.CFL * pd.u_0[0:-2]\
        
        #print len(A_band)
        pd.u_1 = la.solve_banded((1, 1), A_band, u_0_right)        
        # quite slow ...        
        
        pd.u_n1 = pd.u_0
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
        
        pd.i_min += 1       # first point can't be calculated, so its value is undefined
        pd.i_max -= 1       # last point can't be calculated, so its value is undefined 