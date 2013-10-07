'''
Transport equation
implicit - Crank-Nicolson scheme
'''

from linalg_helper import solve_trid
import numpy as np
import scipy.sparse as sparse
import scipy.linalg as la


def calcCNtransport(pd, method, to_step):    #pd ... project data

    th = 0.75   # theta, Crank-Nicolson is stable for theta >= 0.5
    stable_calc = pd.CFL2 + 2.0*pd.NE
    print("stable_calc CN transp = ", stable_calc)
    
    pd.is_stable[method] = (stable_calc<=1) and (th >= 0.5) and (pd.PE < 2.0)
        
    pd.legend_adder[method] = "stable? " + str(pd.is_stable[method]) + \
                "\nCr = " + str(pd.CFL) + \
                "\nPE = " + str(pd.PE) + \
                "\nNE = " + str(pd.NE)
                
    size_u = np.size(pd.u_0)
    vec_one = np.ones(size_u)   # for better readability
    Diag_offsets = np.array( [-1, 0, 1] )
    
    # diffusion (equal to pure inplicit method!)
    #A_diag_main = np.ones(size_u) * (1.0 + 2.0*a)
    #A_diag_upper = np.ones(size_u) * (-1.0*a)
    #A_diag_lower = A_diag_upper
    
    # CN-transport eq.
    A_diag_lower = vec_one * (-0.5 *th * pd.CFL +    th *pd.NE        )
    A_diag_main  = vec_one * (                  -2.0*th *pd.NE    +1.0)
    A_diag_upper = vec_one * (+0.5 *th * pd.CFL +    th *pd.NE        )
                
    # full CN-equation:
    # A * u_1 = B * u_0
    # ==> leads to
    # u_1 = A_inv * B * u_0 = C * u_0
    A_data = np.array([A_diag_lower, A_diag_main, A_diag_upper])    
    A_band = sparse.dia_matrix( (A_data, Diag_offsets), shape=(pd.size_x,pd.size_x) )    
    # "todense" ... de-compress band matrix
    A_inv = la.inv( A_band.todense() )
    
    th_inv = 1.0-th
    
    B_diag_lower = vec_one * (-0.5*th_inv*pd.CFL  +    th_inv*pd.NE      )    
    B_diag_main  = vec_one * (                    -2.0*th_inv*pd.NE  +1.0)    
    B_diag_upper = vec_one * (+0.5*th_inv*pd.CFL  +    th_inv*pd.NE      )
    
    B_data = np.array([ B_diag_lower,B_diag_main,B_diag_upper,])
    B_band = sparse.dia_matrix( (B_data, Diag_offsets), shape=(pd.size_x,pd.size_x) )
    B = np.asarray(B_band.todense())
        
    #C = np.dot(A_inv,B_band.todense())
    #C = np.dot(A_inv,np.eye(size_u))
    C = A_inv
    C = np.asarray(C)   # to avoid problems in np.dot()
    
    local_u_0 = pd.u_0
    local_u_1 = pd.u_1
        
    for n in range(1,to_step) :
        local_u_0 = np.dot(B, local_u_0)
        local_u_1 = np.dot(C, local_u_0)  # only "pure implicit part!"
        
        local_u_1[0] = 0
        local_u_1[-1] = 0  # 'boundary conditions', just for now, ToDo
        
        local_u_0 = local_u_1     # calculated values are input values for the next step
        
        #pd.i_min += 1       # first point can't be calculated, so its value is undefined
        #pd.i_max -= 1       # last point can't be calculated, so its value is undefineddef calcCNtransport(pd, method, to_step):    #pd ... project data

    # reshape pd.u_1 to shape of pd.u_0
    pd.u_1 = local_u_1
    pd.u_0 = local_u_0
    
    
    