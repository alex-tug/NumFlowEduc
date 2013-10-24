'''
method data module
    define class MethodData()
        This class holds all data which exists once for each method of calculation
'''

import numpy as np

from config import modules
from calc_modules.linalg_helper import discreteIntegration


class MethodData(object):
    
    def __init__(self, pd, method):

        self.name = method  
        self.pd = pd
        
        self.u_n1 = np.zeros(pd.size_x)   # values at time t' = t-1
        self.u_1 = np.zeros(pd.size_x)    # new values; t' = t+1
        
        # check stability for each method
        self.is_stable = False
        self.legend_adder = "" # additional legend-string, depending on chosen method
        
        # self.i_min and self.i_max define the boundaries of the area of useful data
        # in some methods this area becomes smaller with each step
        # self.i_min0 and self.i_max0 define the initial values 
        self.i_min0 = 1
        self.i_max0 = pd.size_x-1        
        self.resetI_minmax()
        
        self.u_final = pd.u_00
        
    def resetI_minmax(self):
        ''' reset self.i_min and self.i_max to their initial values'''
        self.i_min = self.i_min0
        self.i_max = self.i_max0
        
    def calc(self):
        if self.name in modules:
            modules[self.name](self.pd, self, to_step=self.pd.steps)
        else:
            print "error in method/calc: method not found."
        
        self.legend_adder = "stable=" + str(self.is_stable) + self.legend_adder
            
    def getArea(self):
        return discreteIntegration(self.u_final, self.pd.dx)

        

