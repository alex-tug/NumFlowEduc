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
                  
    pd.is_stable[method] = True
        
    pd.legend_adder[method] = "stable? " + str(pd.is_stable[method]) + \
                "\nCr = " + str(pd.CFL) + \
                "\nPE = " + str(pd.PE)
                #                
                
    a = pd.v * pd.dt / (pd.dx*pd.dx)
    # diffusion (equal to pure inplicit method!)
    size_u = np.size(pd.u_0)
    A_diag_main = np.ones(size_u) * (1.0 + 2.0*a)
    A_diag_upper = np.ones(size_u) * (-1.0*a)
    A_diag_lower = A_diag_upper
                
    # full CN-equation:
    # A * u_1 = B * u_0
    # ==> leads to
    # u_1 = A_inv * B * u_0 = C * u_0
    A_data = np.array([ 
                        A_diag_upper,
                        A_diag_main,
                        A_diag_lower
                      ])
    
    Diag_offsets = np.array( [1, 0, -1] )
    A_band = sparse.dia_matrix( (A_data, Diag_offsets), shape=(pd.size_x,pd.size_x) )
    
    print "A_band.todense() ", A_band.todense()
    
    # "todense" ... de-compress band matrix
    A_band_inv = la.inv( A_band.todense() )
    
    print "A_band_inv", A_band_inv
    
    print "A_band ", A_band
    
    phi = (1.0-th)/th
    B_diag_main = np.ones(size_u) * (1.0 / pd.dt - 2.0*phi)
    B_diag_upper = np.ones(size_u) * (1.0*phi)
    B_diag_lower = B_diag_upper
                
    B_data = np.array([ 
                        B_diag_upper,
                        B_diag_main,
                        B_diag_lower
                      ])
    B_band = sparse.dia_matrix( (B_data, Diag_offsets), shape=(pd.size_x,pd.size_x) )
        
    C = np.dot(A_band_inv,B_band.todense())
    
    # reshape u_0: necessary to avoid problems in np.dot()
    local_u_0 = np.reshape(pd.u_0, [pd.u_0.size, 1])
    
    a_vec = pd.u_0
    
    for n in range(1,to_step) :
        
        local_u_1 = np.dot(C, local_u_0)  # only "pure implicit part!"
        
        local_u_1[0] = 0
        local_u_1[-1] = 0  # 'boundary conditions', just for now, ToDo
        
        local_u_0 = local_u_1     # calculated values are input values for the next step
        
        #pd.i_min += 1       # first point can't be calculated, so its value is undefined
        #pd.i_max -= 1       # last point can't be calculated, so its value is undefineddef calcCNtransport(pd, method, to_step):    #pd ... project data

    # reshape pd.u_1 to shape of pd.u_0
    b_vec = pd.u_1
    c_vec = local_u_1[:,1]
    pd.u_1 = local_u_1[:,:]
    d_vec = pd.u_1
    print(d_vec.size)


#def calcCNtransport_old(pd, method, to_step):    #pd ... project data
#
#    #th = 1.0   # theta, Crank-Nicolson is stable for theta >= 0.5
#    
#                
#    pd.is_stable[method] = True
#        
#    pd.legend_adder[method] = "stable? " + str(pd.is_stable[method]) + \
#                "\nCr = " + str(pd.CFL) + \
#                "\nPE = " + str(pd.PE)
#                #                
#                
#    a = pd.v * pd.dt / (pd.dx*pd.dx)
#    
#    size_u = np.size(pd.u_0)
#    
#    # advection
#    #diag_main = np.ones(size_u)
#    #diag_upper = np.ones(size_u-1) * pd.CFL * 0.5
#    #diag_lower = diag_upper * (-1.0)
#    
#    # diffusion (pure inplicit method!)
#    diag_main = np.ones(size_u) * (1.0 + 2.0*a)
#    diag_upper = np.ones(size_u-1) * (-1.0*a)
#    diag_lower = diag_upper
#    
#    for n in range(1,to_step) :
#        
##        pd.u_1 = solve_trid(diag_lower, diag_main, diag_upper, pd.u_0, size_u)
#                
#         
#        pd.u_0 = pd.u_1     # calculated values are input values for the next step
#         
#        pd.u_1[0] = 0
#        pd.u_1[-1] = 0  # 'boundary conditions', just for now, ToDo
#        #pd.i_min += 1       # first point can't be calculated, so its value is undefined
#        #pd.i_max -= 1       # last point can't be calculated, so its value is undefined