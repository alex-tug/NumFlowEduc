"""
method data module
    define class MethodData()
        This class holds all data which exists once for each method of calculation
"""

import numpy as np

import config_file
from calc_modules.linalg_helper import discrete_integration
from calc_modules.base import replaceBadValues


class MethodData(object):
    def __init__(self, pd, method):

        self.name = method
        self.pd = pd

        self.u_n1 = np.zeros(pd.size_x)   # values at time t' = t-1
        self.u_1 = np.zeros(pd.size_x)    # new values; t' = t+1

        # check stability for each method
        self.is_stable = False
        self.legend_adder = ""  # additional legend-string, depending on chosen method

        # self.i_min and self.i_max define the boundaries of the area of useful data
        # in some methods this area becomes smaller with each step
        # self.i_min0 and self.i_max0 define the initial values 

        self.i_min0 = 0
        self.i_max0 = pd.size_x - 1

        self.reset_i_min_max()

        self.u_final = pd.u_00

    def reset_i_min_max(self):
        """ reset self.i_min and self.i_max to their initial values"""
        self.i_min = self.i_min0
        self.i_max = self.i_max0

    def calc(self):
        if self.name in config_file.modules:
            config_file.modules[self.name](self.pd, self, to_step=self.pd.steps)
        else:
            print "error in method/calc: method not found."

        self.u_final = replaceBadValues(self.u_final)

        self.legend_adder = "stable=" + str(self.is_stable) + self.legend_adder

    def get_area(self):
        return discrete_integration(self.u_final, self.pd.dx)

    def is_not_neg(self):
        return np.all(self.u_final > -1.0 * config_file.EPS)

    def is_nearly_zero(self):
        return np.all(abs(self.u_final) < config_file.EPS)

    def is_not_huge(self):
        return np.all(abs(self.u_final) < 100 * config_file.signal_max)



        

