'''
    some functions for numerical calculation
'''

import numpy as np
   
def solveTrid(lower, main, upper, v_inhom, n):
    # a, b, c ... vectors of the tridiagonal matrix
    #           b ... main diagonal
    # v_inhom ... inhomogeneous vector
    # n ... order of the system
    
    # u,y ... temporary vectors
    u = np.zeros(n)
    y = np.zeros(n)
    
    # x ... return vector
    x = np.zeros(n)
        
    y[0] = v_inhom[0]
    u[0] = main[0]
    
    if u[0] == 0.0: 
        return 0
    
    for j in range(1, n):
        m = lower[j-1]/u[j-1]
        u[j] = main[j]-m*upper[j-1]
        
        if u[j] == 0.0:
            return 0
        
        y[j] = v_inhom[j] - m*y[j-1]
    
    x[n-1] = y[n-1] / u[n-1]
    
    for j in range(n-2,0,-1):
        x[j] = (y[j]-upper[j]*x[j+1])/u[j]
        
    return x
        

def discreteIntegration(y, stepsize=1.0):
    '''
        wrap ,method for discrete integration
    '''

    return np.trapz(y, dx=stepsize)
    


        