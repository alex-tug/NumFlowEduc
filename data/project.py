'''
project module
    define class ProjectData()
        this class holds all input and output data for the flow-calculations
'''

import numpy as np
from matplotlib import pyplot as plt

from io_handling.file_handling import makeSurePathExists

class ProjectData():
    # this class holds all input and output data for the flow-calculations
    
    def __init__(self,  dx= 0.002, dt = 0.001, c = 1.0, steps = 50):
        
        self.dx = dx                        # dx ... spatial resolution
        self.x = np.arange(-10,15, dx)      # vector of all x-values;  (from, to, resolution)
        self.size_x = np.size(self.x)       # number of x-values
        #print "self.size_x", self.size_x
        self.dt = dt                        # dt ... temporal resolution
        self.c = c                          # c  ... velocity of flow
        self.steps = steps                  # number of steps to be calculated 
        #print "self.steps", self.steps      # (full spatial shift = c * dt/dx * steps = CFL * steps)
        
        self.u_n1 = np.zeros(self.size_x)   # values at time t' = t-1
        self.u_0 = np.zeros(self.size_x)    # values before calculation, will be set to u_1 after each step
        self.u_1 = np.zeros(self.size_x)    # new values; t' = t+1
        self.u_00 = np.zeros(self.size_x)   # to keep a copy of input signal
        self.signal_shape = ''              # shape of input signal
        
        self.CFL = self.c*self.dt/self.dx   # Courant number, Upwind and LaxWendroff are stable for CFL <= 1
        print("CFL = {}".format(self.CFL))
        self.CFL2 = self.CFL**2.0           # just for easy reading formulas
        
        self.figures = {'lw':plt.figure('lw'), \
                        'upw':plt.figure('upw'), \
                        'lf':plt.figure('lf'), \
                        'cn':plt.figure('cn')}  # store a figure for each method, doesn't work complete well...
                                            
        self.xlim_low = -4                  # boundaries for the figures
        self.xlim_high = 10
        self.ylim_low = -0.5
        self.ylim_high = 1.5
        
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
        for fig in self.figures.itervalues():  plt.close(fig)
        print("closed figures")
        
        
    def __str__(self):
        return 'dx = {!s} dt = {!s} c = {!s} steps = {!s}'\
                    .format(self.dx, self.dt, self.c, self.steps)
        
    
    def resetI_minmax(self):
        ''' reset self.i_min and self.i_max to their initial values'''
        
        self.i_min = self.i_min0
        self.i_max = self.i_max0
        
    def setSignal(self, shape):
        ''' write input signal into u_00 using chosen shape'''
        if shape != '':
            self.signal_shape = shape
            if shape == 'step':
                for i in range(self.xlim_low,self.size_x) :
                    if self.x[i]<1 :
                        self.u_00[i] = 1.0
                    else :
                        self.u_00[i] = 0.0
                        
            elif shape == 'tri':    # triangle
                for i in range(self.xlim_low,self.size_x) :
                    if self.x[i]<0.5 :
                        self.u_00[i] = 2 * self.x[i]
                    elif self.x[i]<1.0 :
                        self.u_00[i] = 2*(1.0 - self.x[i])
                    else :
                        self.u_00[i] = 0.0
                        
            elif shape == 'wall':
                for i in range(self.xlim_low,self.size_x) :
                    if self.x[i]<0.5 :
                        self.u_00[i] = 0.0
                    elif self.x[i]<1.0 :
                        self.u_00[i] = 1.0
                    else :
                        self.u_00[i] = 0.0
                        
            elif shape == 'thinwall':
                for i in range(self.xlim_low,self.size_x) :
                    if self.x[i]<0.7 :
                        self.u_00[i] = 0.0
                    elif self.x[i]<0.72 :
                        self.u_00[i] = 1.0
                    else :
                        self.u_00[i] = 0.0
            
            elif shape == 'gauss':
                sigma = 0.15
                mue = 0.5
                for i in range(self.xlim_low,self.size_x) :
                    if self.x[i]<1.0 :
                        self.u_00[i] = 0.5  * 1.0/(sigma * np.sqrt(2 * np.pi)) \
                                            * np.exp( - 0.5 * ((self.x[i]-mue)/sigma)**2 )
                    else :
                        self.u_00[i] = 0.0
                        
            elif shape == 'wave':
                amp = 0.5
                fact = 2.0
                phase = 0.5
                offset = 0.5
                for i in range(self.xlim_low,self.size_x) :
                    if self.x[i]<1.0 :
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
    
    
    def printFig(self, out_path='images/', method='lw'):
        ''' 
        print figure of chosen method(default='lw') 
        as .png to out_path(default='images/') 
        '''
        
        out_filename = '{0}-{1}-cfl_{2:.2f}-steps_{3}'\
                        .format(method, self.signal_shape, self.CFL, self.steps)
        
        makeSurePathExists(out_path)
        
        #self.fig_lw.savefig(out_path + out_filename + '.eps')
        self.figures[method].savefig(out_path + out_filename + '.png')
        
        print("plotted {!s} to {!s}".format(out_filename + '.png', out_path))
    