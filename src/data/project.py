'''
project module
    define class ProjectData()
        this class holds all input and output data for the flow-calculations
'''

import numpy as np
from matplotlib import pyplot as plt
import csv
import os

from io_handling.file_handling import createPNG, createCSV

class ProjectData():
    # this class holds all input and output data for the flow-calculations
    
    def __init__(self,  dx=0.002, dt=0.001, c=1.0, v=1.0, steps=50):
        
        self.dx = dx                        # dx ... spatial resolution
        self.x_max = 100
        self.x = np.arange(0,self.x_max, dx) # vector of all x-values;  (from, to, resolution)
        self.size_x = np.size(self.x)       # number of x-values
        #print "self.size_x", self.size_x
        self.dt = dt                        # dt ... temporal resolution
        self.c = c                          # c  ... velocity of flow
        self.v = v                          # v  ... coefficient for transport equation
        self.steps = steps                  # number of steps to be calculated 
        #print "self.steps", self.steps     # (full spatial shift = c * dt/dx * steps = CFL * steps)
        
        self.u_n1 = np.zeros(self.size_x)   # values at time t' = t-1
        self.u_0 = np.zeros(self.size_x)    # values before calculation, will be set to u_1 after each step
        self.u_1 = np.zeros(self.size_x)    # new values; t' = t+1
        self.u_00 = np.zeros(self.size_x)   # to keep a copy of input signal
        self.signal_shape = ''              # shape of input signal
        
        self.CFL = self.c*self.dt/self.dx   # Courant number, Upwind and LaxWendroff are stable for CFL <= 1
        print("CFL = {}".format(self.CFL))
        self.CFL2 = self.CFL**2.0           # just for easy reading formulas
        if self.v != 0:                     # avoid division by zero
            self.PE = self.c*self.dx/self.v # Peclet number
        else:
            self.PE = 0.0
        
        self.NE = self.v *self.dt / (self.dx**2)
        
        self.figures = {} # each method will add its figure
          
        # check stybility for each method
        self.is_stable = {}
          
        self.xlim_low = 0                 # boundaries for the figures
        self.xlim_high = 100
        self.ylim_low = -1.1
        self.ylim_high = 2.0
        
        self.legend_adder = {} # additional legend-string, depending on chosen method
        
        #self.uu = np.zeros((self.size_x, self.steps))    # nonsense^^
        
        # self.i_min and self.i_max define the boundaries of the area of useful data
        # in some methods this area becomes smaller with each step
        # self.i_min0 and self.i_max0 define the initial values, 
        # to which i_min and i_max will be reseted before calculation
        self.i_min0 = 1
        self.i_max0 = self.size_x-1         
        self.resetI_minmax()

    def __del__(self):
        ''' destructor, ensure that all figure are completely eliminated '''
        for fig in self.figures.itervalues():  
            if plt is not None:
                plt.close(fig)
        plt.close('all')
        print("closed figures")
        
        
    def __str__(self):
        return 'dx = {!s} dt = {!s} c = {!s} steps = {!s}'\
                    .format(self.dx, self.dt, self.c, self.steps)

    def del_fig(self, method):
        plt.clf()
        if method in self.figures:
            if plt is not None:
                if self.figures[method] is not None:
                    plt.close(self.figures[method])
                    del self.figures[method]
    
    def resetI_minmax(self):
        ''' reset self.i_min and self.i_max to their initial values'''
        self.i_min = self.i_min0
        self.i_max = self.i_max0
        
    def setSignal(self, shape):
        ''' write input signal into u_00 using chosen shape'''
        if shape != '':
            self.signal_shape = shape
            shape_max = 1.0
            center = 20.0
            
            if shape == 'step':
                for i in range(self.xlim_low, self.size_x) :
                    if self.x[i]<center :
                        self.u_00[i] = 1.0
                    else :
                        self.u_00[i] = 0.0
                        
            elif shape == 'tri':    # triangle
                for i in range(self.xlim_low, self.size_x) :
                    self.u_00[i] = max(0.0, shape_max - abs(center - self.x[i]))

                        
            elif shape == 'wall':
                thickness = 2.0
                for i in range(self.xlim_low, self.size_x) :
                    if abs(self.x[i]-center)<thickness*0.5:
                        self.u_00[i] = shape_max
                    else :
                        self.u_00[i] = 0.0
                        
            elif shape == 'thinwall':
                thickness = 0.2
                for i in range(self.xlim_low, self.size_x) :
                    if abs(self.x[i]-center)<thickness*0.5:
                        self.u_00[i] = shape_max
                    else :
                        self.u_00[i] = 0.0
            
            elif shape == 'gauss':
                # f_max = 1 / (sigma * sqrt(2*pi))
                sigma = 1.0 / (shape_max * np.sqrt(2*np.pi))
                mue = center
                for i in range(self.xlim_low, self.size_x) :
                    #if self.x[i]<5.0 :
                    self.u_00[i] = shape_max \
                                * np.exp( - 0.5 * ((self.x[i]-mue)/sigma)**2 )
                    #else :
                    #    self.u_00[i] = 0.0
                        
            elif shape == 'wave':
                amp = shape_max
                fact = 0.5
                phase = 0.5
                offset = 0.5
                for i in range(self.xlim_low, self.size_x) :
                    if self.x[i]<center :
                        self.u_00[i] = amp * np.sin(fact*(self.x[i]-phase)*(2*np.pi)) + offset
                    else :
                        self.u_00[i] = 0.0
        
    
    #===========================================================================
    # def calcAll(self):
    #    calcLaxWendroff(self)
    #    calcUpwind(self)
    #===========================================================================
    
    #===========================================================================
    # def printFigAll(self, out_path='images/'):        
    #    self.printFig(out_path, method='lw')
    #    self.printFig(out_path, method='upw')
    #===========================================================================
    
    
    def printFig(self, out_path='', method=''):
        ''' 
        print figure of chosen method
        as .png to out_path(default='images/') 
        '''
            
        out_filename = '{0}-{1}-PE_{2:.1f}-dx_{3:.3f}-dt_{4:.3f}-c_{5:.2f}-v_{6}-steps_{7}'\
                        .format(method, self.signal_shape, self.PE, self.dx, self.dt, self.c, self.v, self.steps)
        
        if (method in self.figures) and (out_path != ''):
            createPNG(out_path, out_filename, self.figures[method])
            print("plotted {!s} to {!s}".format(out_filename + '.png', out_path))
        else:
            print("printFig: figure for method '{!s}' not found!".format(method))
        
    
    def writeAsCSV(self, out_path='', method=''):
        ''' 
        export data of chosen method
        as .csv to out_path(default='images/') 
        '''
            
        out_filename = '{0}-{1}-PE_{2:.1f}-dx_{3:.3f}-dt_{4:.3f}-c_{5:.2f}-v_{6}-steps_{7}'\
                        .format(method, self.signal_shape, self.PE, self.dx, self.dt, self.c, self.v, self.steps)
                
        if (method in self.figures) and (out_path != ''):
            createCSV(out_path, out_filename, method, self.x, self.u_1)            
            
            print("wrote {!s} to {!s}".format(out_filename + '.csv', out_path))
        else:
            print("writeAsCSV: data for method '{!s}' not found!".format(method))
        
            
        
            
    