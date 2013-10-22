'''
Transport equation
explicit - FTCS scheme
'''

def calcTranspFTCS(pd, m, to_step):    #pd ... project data

    Ne = pd.v * pd.dt / (pd.dx**2) # = pd.CFL / pd.PE 
    
    stable_calc = Ne
    m.is_stable = (stable_calc<=0.5)
        
    m.legend_adder = "stable=" + str(m.is_stable)# + \
                #"\nCr = " + str(round(pd.CFL, 2))# + \
                #"\nPE = " + str(pd.PE) + \
                #"\nNe = " + str(Ne)
                
       
    u_0 = pd.u_00.copy()
    u_1 = pd.u_00.copy()
        
    for n in range(1,to_step) : # for each timestep
        
        # FTCS scheme                    
        u_1[1:-1] =  (    +0.5*pd.CFL +1.0*Ne) * u_0[0:-2]\
                    +(1.0             -2.0*Ne) * u_0[1:-1]\
                    +(    -0.5*pd.CFL +1.0*Ne) * u_0[2:]
            
        u_1[0] = 0
        u_1[-1] = 0  # 'boundary conditions', just for now, ToDo
        #m.i_max -= 1
        #m.i_min += 1       # since first point can't be calculated, so its value is undefined

        
        u_0 = u_1     # calculated values are input values for the next step
    
    m.u_1 = u_1.copy()
    m.u_final = u_1.copy()
        