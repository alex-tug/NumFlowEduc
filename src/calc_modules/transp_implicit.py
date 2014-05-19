"""
Transport equation
fully implicit scheme
"""

import numpy as np
from scipy import sparse
from scipy import linalg as la


def calc_transp_implicit(pd, m, to_step):    # pd ... project data
    """
        solve transport equation using fully implicit scheme
        each steps consists of solving A * u_1 = u_0
        were A is a banded matrix
    """

    m.is_stable = True  # implicit scheme is stable regardless of CFL, NE, PE, etc.

    u_0 = pd.u_00.copy()
    u_1 = pd.u_00.copy()

    b = (      0.5*pd.CFL     -pd.NE)
    a = (1.0              +2.0*pd.NE)
    c = (     -0.5*pd.CFL     -pd.NE)

    # A_data: data of banded matrix A
    A_data = np.array([
                    b * np.append(0.0, np.ones(pd.size_x - 1)),
                    a * np.ones(pd.size_x),
                    c * np.append(np.ones(pd.size_x -1), 0.0)
                    ])

    # include Dirichlet-boundary condition:
    #A_data[1][0] = 1
    #A_data[0][0] = 0
    #A_data[2][0] = 0
    #A_data[1][0] = 1

    #A_data[1][-1] = 1
    #A_data[2][-1] = 0

    try:
        for n in range(0, to_step):    # for each timestep
            # include Dirichlet-boundary condition:
            #u_0[0] = pd.bc_upstream(n*pd.dt)
            u_0[0:10] = u_0[13]
            #u_0[-1] = pd.bc_downstream(n*pd.dt)

            # fully implicit scheme
            u_1 = la.solve_banded((1, 1), A_data, u_0)
            #u_1[0:10] = u_0[11]   # pd.bc_upstream(n*pd.dt)

            u_0 = u_1     # calculated values are input values for the next step

    except ValueError:
        # will occur in solve_banded when u_0_right contains infs or NaNs
        print("Fully implicit calcualation was terminated because of infinity or undefined values.")

    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()