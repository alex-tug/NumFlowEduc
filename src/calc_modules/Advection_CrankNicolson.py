'''
Crank-Nicolson scheme
'''

import numpy as np
import scipy.sparse as sparse
import scipy.linalg as la

def calcCrankNicolson(pd, method, to_step): #pd ... project data
    ''' 
    Crank-Nicolson scheme according to: 
        Malcherek, 'Num.Methoden d. Stroemungsmech.' Eq: 5.13, p.59
    and solver for tridiagonal matrix: 
        H.Sormann, 'Numerische Methoden in der Physik', Chapter 2.6 p.39f
    
    NOT FINISHED!
    '''
    
    th = 1.0   # theta, Crank-Nicolson is stable for theta >= 0.5
    
    pd.is_stable[method] = (th>=0.5)
        
    pd.legend_adder[method] = "stable? " + str(pd.is_stable[method]) + \
                "\nCr = " + str(pd.CFL) + \
                "\nPE = " + str(pd.PE) + \
                "\nth = " + str(th)
    
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
        
    size = pd.size_x    # just for better readability
        
    a = th/2.0 * pd.CFL
    b = 1
    c = th/2.0 * pd.CFL * (-1)
    
    d = np.zeros(size)
    m = np.zeros(size)

    d[0] = b
    for j in range(1, size-1):
        
        m[j] = a / d[j-1]
        
        d[j] = b - m[j] * c

    for n in range(1, to_step) : # timesteps
        
        y = np.zeros(size)                        

        y[0] = pd.u_0[0]        
        for i in range(1, size-1):
            y[i] = pd.u_0[i] - m[i] * y[i-1]
            #if i < 4: print i, "  y[i]: ", y[i]
        
        #print "y[size-1]: ", y[size-1], "  n=", n, "  th=", th
        #print "d[size-1]: ", d[size-1]
        
        pd.u_1[size-1] = y[size-1] / d[size-1]
        for j in range(size-2, 0, -1):            
            pd.u_1[j] = pd.u_0[j] - m[j] * y[j-1]


        pd.u_n1 = pd.u_0
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
        
        pd.i_min += 1       # first point can't be calculated, so its value is undefined
        pd.i_max -= 1       # last point can't be calculated, so its value is undefined 
        
        
def calcCrankNicolson_old(pd, to_step): #pd ... project data
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
    
    #===========================================================================
    # A_band = np.zeros( (3,pd.size_x) )
    # A_band[0,1:] =       th/2.0 * pd.CFL * np.ones(pd.size_x-1)
    # A_band[1,:] = np.ones(pd.size_x)
    # A_band[2,:-1] = -1 * th/2.0 * pd.CFL * np.ones(pd.size_x-1)
    # # upper left corner is zero because this upper diagonal is one position smaller than the main diagonal
    # A_band[0,0] = 0.
    # A_band[2,-1] = 0.     # same as upper left corner
    #===========================================================================
    
    #better:
    A_data = np.array([ 
                        np.ones(pd.size_x) * th/2.0 * pd.CFL,
                        np.ones(pd.size_x),
                        np.ones(pd.size_x) * th/2.0 * pd.CFL * (-1)
                      ])
    
    A_offsets = np.array( [1, 0, -1] )
    A_band = sparse.dia_matrix( (A_data, A_offsets), shape=(pd.size_x,pd.size_x) )
    
    print "A_band.todense() ", A_band.todense()
    
    # "todense" ... de-compress band matrix
    A_band_inv = la.inv( A_band.todense() )
    
    print "A_band_inv", A_band_inv
    
    print "A_band ", A_band
    
    u_0_right = np.zeros(pd.size_x) 
    
    #print("{}".format(np.dot(A_band_inv, u_0_right)))
    
    for n in range(1,to_step) : # timesteps
                        
        # u_0_right is the right hand side of A_diag * u_1 = u_0_right which come from the CrankNicolson formula
        u_0_right[1:-1] = pd.u_0[1:-1]\
                        + (th-1.0) / 2.0 * pd.CFL * pd.u_0[2:]\
                        - (th-1.0) / 2.0 * pd.CFL * pd.u_0[0:-2]\
        
        #print len(A_band)
        #pd.u_1 = la.solve_banded((1, 1), A_band, u_0_right)        
        # quite slow ...        
        
        pd.u_1 = np.dot(A_band_inv, u_0_right)
        
        pd.u_n1 = pd.u_0
        pd.u_0 = pd.u_1     # calculated values are input values for the next step
        
        pd.i_min += 1       # first point can't be calculated, so its value is undefined
        pd.i_max -= 1       # last point can't be calculated, so its value is undefined 