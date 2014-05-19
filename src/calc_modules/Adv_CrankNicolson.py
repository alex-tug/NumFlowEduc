"""
Crank-Nicolson scheme
"""

import numpy as np
import scipy.sparse as sparse
import scipy.linalg as la


def calc_adv_CrankNicolson(pd, m, to_step):   # pd ... project data
    """
    Crank-Nicolson scheme according to:
        Malcherek, 'Num.Methoden d. Stroemungsmech.' Eq: 5.13, p.59
    and solver for tridiagonal matrix:
        H.Sormann, 'Numerische Methoden in der Physik', Chapter 2.6 p.39f

    NOT FINISHED!
    """
    
    th = 1.0   # theta, Crank-Nicolson is stable for theta >= 0.5
    
    m.is_stable = (th >= 0.5)

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
        
    #a = th/2.0 * pd.CFL
    #b = 1
    #c = th/2.0 * pd.CFL * (-1)

    a = th * ( 0.5*pd.CFL +1.0*pd.NE)
    b = th * (            -2.0*pd.NE) + 1.0
    c = th * (-0.5*pd.CFL +1.0*pd.NE)
    
    d = np.zeros(size)
    mat = np.zeros(size)

    d[0] = b
    for j in range(1, size):
        
        mat[j] = a / d[j-1]
        
        d[j] = b - mat[j] * c

    u_0 = pd.u_00.copy()
    u_1 = u_0.copy()
    
    for n in range(0, to_step):    # timesteps
        
        y = np.zeros(size)                        

        y[0] = u_0[0]        
        for i in range(1, size-1):
            y[i] = u_0[i] - mat[i] * y[i-1]
        
        u_1[size-1] = y[size-1] / d[size-1]
        for j in range(size-2, 0, -1):            
            u_1[j] = u_0[j] - mat[j] * y[j-1]

        #u_n1 = u_0
        u_0 = u_1     # calculated values are input values for the next step
    
        # 'boundary conditions'
        u_1[0] = pd.bc_upstream(n*pd.dt)
        u_1[-1] = pd.bc_downstream(n*pd.dt)

    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()


def calc_adv_CrankNicolson_old(pd, m, to_step):   # pd ... project data
    """
    Crank-Nicolson scheme
    according to: Malcherek, 'Num.Methoden d. Stroemungsmech.' Eq: 5.13, p.59

    NOT FINISHED!
    """
    
    th = 1.0   # theta, Crank-Nicolson is stable for theta >= 0.5
    
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

    #a = th * ( 0.5*pd.CFL +1.0*pd.NE)
    #b = th * (            -2.0*pd.NE) + 1.0
    #c = th * (-0.5*pd.CFL +1.0*pd.NE)

    #A_data = np.array([
    #                    np.ones(pd.size_x) * th/2.0 * pd.CFL,
    #                    np.ones(pd.size_x),
    #                    np.ones(pd.size_x) * th/2.0 * pd.CFL * (-1)
    #                    ])
    #better:
    A_data = np.array([
                        np.append(0.0, np.ones(pd.size_x -1) *        th * ( 0.5*pd.CFL +1.0*pd.NE)),
                            np.ones(pd.size_x)    * (1.0 + th * (            -2.0*pd.NE)),
                        np.append(np.ones(pd.size_x -1) *        th * (-0.5*pd.CFL +1.0*pd.NE), 0.0)
                        ])


    #A_offsets = np.array( [1, 0, -1] )
    #A_band = sparse.dia_matrix( (A_data, A_offsets), shape=(pd.size_x,pd.size_x) )
    #A_as_array = np.asarray(A_band)
    
    #print "A_band.todense() ", A_band.todense()
    
    # "todense" ... de-compress band matrix
    #A_band_inv = la.inv( A_band.todense() )
    
    #print "A_band_inv", A_band_inv
    
    #print "A_band ", A_band
    
    u_0_right = np.zeros(pd.size_x) 
    
    #print("{}".format(np.dot(A_band_inv, u_0_right)))
    
    u_0     = pd.u_00.copy()
    u_1     = u_0.copy()
    #u_n1    = u_1.copy()

    try:
        for n in range(1,to_step) : # timesteps

            # u_0_right is the right hand side of A_diag * u_1 = u_0_right which come from the CrankNicolson formula
            #u_0_right[1:-1] = u_0[1:-1]#\
                            #+ (th-1.0) / 2.0 * pd.CFL * u_0[2:]\
                            #- (th-1.0) / 2.0 * pd.CFL * u_0[0:-2]\
            u_0_right = u_0.copy()

            #print len(A_band)
            u_1 = la.solve_banded((1, 1), A_data, u_0_right)

            # quite slow ...

            #u_1 = np.dot(A_band_inv, u_0_right)

            #u_n1 = u_0.copy()
            u_0 = u_1.copy()     # calculated values are input values for the next step

            # 'boundary conditions'
            u_1[0] = pd.bc_upstream(n*pd.dt)
            u_1[-1] = pd.bc_downstream(n*pd.dt)
    except ValueError:
        # will occur in solve_banded when u_0_right contains infs or NaNs
        print("CrankNicolson calcualation was terminated because of infinity or undefined values.")

    finally:
        m.u_1 = u_1.copy()
        aa2 = u_1.copy()
        m.u_final = u_1.copy()