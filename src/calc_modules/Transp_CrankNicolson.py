"""
Transport equation
implicit - Crank-Nicolson scheme
"""

#from linalg_helper import solve_trid
import numpy as np
import scipy.sparse as sparse
import scipy.linalg as la


def calc_transp_CN(pd, m, to_step):    # pd ... project data

    th = 0.5   # theta, Crank-Nicolson is unconditionally stable for theta >= 0.5

    stable_calc = pd.CFL2 + 2.0*pd.NE
    
    m.is_stable = (stable_calc <= 1) and (th >= 0.5) and (pd.PE < 2.0)
        
    m.legend_adder = "\nNE = " + str(pd.NE) + \
                     "\nPE = " + str(pd.PE)
    
    u_0 = pd.u_00.copy()
    u_1 = pd.u_00.copy()
          
    size_u = np.size(u_0)
    vec_one = np.ones(size_u)   # for better readability
    diag_offsets = np.array( [-1, 0, 1] )

    # CN-transport eq.
    A_diag_lower = vec_one * (+0.5 *th * pd.CFL -    th *pd.NE        )
    A_diag_main  = vec_one * (                  +2.0*th *pd.NE    +1.0)
    A_diag_upper = vec_one * (-0.5 *th * pd.CFL -    th *pd.NE        )
                
    # full CN-equation:
    # A * u_1 = B * u_0
    # ==> leads to
    # u_1 = A_inv * B * u_0 = C * u_0
    A_data = np.array([A_diag_lower, A_diag_main, A_diag_upper])
    
    th_inv = 1.0-th

    u_right_side = pd.u_00.copy()
    try:
        for n in range(0, to_step):
            #u_right_side = np.dot(B_band, u_0)
            u_right_side[1:-1] = (+0.5*th_inv*pd.CFL  +    th_inv*pd.NE      ) * u_0[0:-2]\
                                +(                    -2.0*th_inv*pd.NE  +1.0) * u_0[1:-1]\
                                +(-0.5*th_inv*pd.CFL  +    th_inv*pd.NE      ) * u_0[2:]
            u_right_side[0] = pd.bc_upstream(n*pd.dt)
            u_right_side[-1] = pd.bc_downstream(n*pd.dt)

            u_1 = la.solve_banded((1, 1), A_data, u_right_side)

            # 'boundary conditions'
            u_1[0] = pd.bc_upstream(n*pd.dt)
            u_1[-1] = pd.bc_downstream(n*pd.dt)

            u_0 = u_1     # calculated values are input values for the next step
    except ValueError:
        # will occur in solve_banded when u_0_right contains infs or NaNs
        print("CrankNicolson calcualation was terminated because of infinity or undefined values.")

    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()


#################################
# backup:
#
# def calc_transp_CN(pd, m, to_step):    # pd ... project data
#
#     th = 1.0   # theta, Crank-Nicolson is stable for theta >= 0.5
#     stable_calc = pd.CFL2 + 2.0*pd.NE
#
#     m.is_stable = (stable_calc <= 1) and (th >= 0.5) and (pd.PE < 2.0)
#
#     m.legend_adder = "\nNE = " + str(pd.NE) + \
#                      "\nPE = " + str(pd.PE)
#
#     u_0 = pd.u_00.copy()
#     u_1 = pd.u_00.copy()
#
#     size_u = np.size(u_0)
#     vec_one = np.ones(size_u)   # for better readability
#     diag_offsets = np.array( [-1, 0, 1] )
#
#     # diffusion (equal to pure implicit method!)
#     #A_diag_main = np.ones(size_u) * (1.0 + 2.0*a)
#     #A_diag_upper = np.ones(size_u) * (-1.0*a)
#     #A_diag_lower = A_diag_upper
#
#     # CN-transport eq.
#     A_diag_lower = vec_one * (+0.5 *th * pd.CFL -    th *pd.NE        )
#     A_diag_main  = vec_one * (                  +2.0*th *pd.NE    +1.0)
#     A_diag_upper = vec_one * (-0.5 *th * pd.CFL -    th *pd.NE        )
#
#     # full CN-equation:
#     # A * u_1 = B * u_0
#     # ==> leads to
#     # u_1 = A_inv * B * u_0 = C * u_0
#     A_data = np.array([A_diag_lower, A_diag_main, A_diag_upper])
#     #A_band = sparse.dia_matrix( (A_data, diag_offsets), shape=(pd.size_x, pd.size_x) )
#     #A = A_band.todense()
#     # "todense" ... de-compress band matrix
#
#     th_inv = 1.0-th
#
#     B_diag_lower = vec_one * (+0.5*th_inv*pd.CFL  -    th_inv*pd.NE      )
#     B_diag_main  = vec_one * (                    +2.0*th_inv*pd.NE  +1.0)
#     B_diag_upper = vec_one * (-0.5*th_inv*pd.CFL  -    th_inv*pd.NE      )
#
#     B_data = np.array([ B_diag_lower, B_diag_main, B_diag_upper])
#     B_band = sparse.dia_matrix( (B_data, diag_offsets), shape=(pd.size_x, pd.size_x) )
#     #B = np.asarray(B_band.todense())
#
#     #A_inv = la.inv( A_band.todense() )
#     #C = np.dot(A_inv, B)
#     #C = np.dot(A_inv,np.eye(size_u))
#     #C = A_inv
#     #C = np.asarray(C)   # to avoid problems in np.dot()
#
#     u_right_side = pd.u_00.copy()
#     try:
#         for n in range(1, to_step):
#             #u_right_side = np.dot(B_band, u_0)
#             u_right_side[1:-1] =  (+0.5*th_inv*pd.CFL  +    th_inv*pd.NE      ) * u_0[0:-2]\
#                             +(                    -2.0*th_inv*pd.NE  +1.0) * u_0[1:-1]\
#                             +(-0.5*th_inv*pd.CFL  +    th_inv*pd.NE      ) * u_0[2:]
#             u_right_side[0] = pd.bc_upstream(n*pd.dt)
#             u_right_side[-1] = pd.bc_downstream(n*pd.dt)
#
#             #u_1 = np.dot(A_inv, np.dot(B, u_0))
#             #u_1 = np.dot(A_inv, u_right_side)
#             u_1 = la.solve_banded((1, 1), A_data, u_right_side)
#
#             # 'boundary conditions'
#             u_1[0] = pd.bc_upstream(n*pd.dt)
#             u_1[-1] = pd.bc_downstream(n*pd.dt)
#
#             u_0 = u_1     # calculated values are input values for the next step
#     except ValueError:
#         # will occur in solve_banded when u_0_right contains infs or NaNs
#         print("CrankNicolson calcualation was terminated because of infinity or undefined values.")
#
#     m.u_1 = u_1.copy()
#     m.u_final = u_1.copy()