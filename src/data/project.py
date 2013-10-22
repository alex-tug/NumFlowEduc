'''
project module
    define class ProjectData()
        This class holds all those data for the flow-calculations which are
            not specific to one method of calculation
        For each set of parameter there is one ProcetData class witch holds
            a list of MethodData classes - one for each CalcModule in use
'''

import numpy as np
from matplotlib import pyplot as plt

from io_handling.file_handling import createPNG, createCSV
from io_handling.graphics import drawPlot

class ProjectData(object):
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
                                            # (full spatial shift = c * dt/dx * steps = CFL * steps)
        self.center_i = 20.0                # center of signal at t=0
        self.center_f = self.center_i +\
            self.c*self.dt*self.steps       # center of signal at t=t_max (of analytic solution)
        
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
        
        self.methods = {}
        self.fig = None                     # one figure for all methods
          
          
        self.signal_max = 10.0
        self.xlim_low = 0                 # boundaries for the figures
        self.xlim_high = 100
        self.ylim_low  = self.xlim_low -0.1 * self.signal_max
        self.ylim_high =                1.2 * self.signal_max
        
                

    def __del__(self):
        ''' destructor, ensure that all objects are completely eliminated '''
        
        for m in self.methods.itervalues():  
            if m is not None:
                del m
                
        plt.close('all')
        print("closed figures and classes")
        
        
    def __str__(self):
        return 'dx = {!s} dt = {!s} c = {!s} steps = {!s}'\
                    .format(self.dx, self.dt, self.c, self.steps)

    def del_fig(self):
        plt.clf()
        if self.fig is not None: 
            plt.close('all')
            del self.fig
            self.fig = None
        
#        if method in self.figures:
#            if plt is not None:
#                if self.figures[method] is not None:
#                    plt.close(self.figures[method])
#                    del self.figures[method]
    
        
    def setSignal(self, shape):
        ''' write input signal into u_00 using chosen shape'''
        if shape != '':
            self.signal_shape = shape
            shape_max = self.signal_max
            center = self.center_i
            
            if shape == 'step':
                for i in range(self.xlim_low, self.size_x) :
                    if self.x[i]<center :
                        self.u_00[i] = shape_max
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
                #f_max = 1 / (sigma * sqrt(2*pi))
                #sigma = 1.0 / (shape_max * np.sqrt(2*np.pi))
                sigma = np.sqrt(shape_max)
                mue = center
                for i in range(self.xlim_low, self.size_x) :
                    self.u_00[i] = shape_max \
                                * np.exp( - 0.5 * ((self.x[i]-mue)/sigma)**2 )
                        
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
                        
    
    def calc(self, method):
        if method in self.methods:
            self.methods[method].calc()
        
    def calcAll(self):
        for m in self.methods: m.calc()
    
    def createFig(self):
        self.fig = drawPlot(self)
        
    def getFig(self):
        if self.fig is None:
            self.createFig()
        return self.fig
    
    def printFig(self, out_path='', method=''):
        ''' 
        print figure of chosen method
        as .png to out_path(default='images/') 
        '''
            
        out_filename = '{0}-PE_{1:.1f}-dx_{2:.3f}-dt_{3:.3f}-c_{4:.2f}-v_{5}-steps_{6}'\
                        .format(self.signal_shape, self.PE, self.dx, self.dt, self.c, self.v, self.steps)
        
        #if (method in self.figures) and (out_path != ''):
        createPNG(out_path, out_filename, self.getFig())
        print("plotted {!s} to {!s}".format(out_filename + '.png', out_path))
        #else:
        #    print("printFig: figure for method '{!s}' not found!".format(method))
        
    
    def writeAsCSV(self, out_path=''):
        ''' 
        export data of chosen method
        as .csv to out_path(default='images/') 
        '''
            
        out_filename = '{0}-PE_{1:.1f}-dx_{2:.3f}-dt_{3:.3f}-c_{4:.2f}-v_{5}-steps_{6}'\
                        .format(self.signal_shape, self.PE, self.dx, self.dt, self.c, self.v, self.steps)
                
        if (out_path != ''):
            createCSV(out_path, out_filename, self)            
            
            print("wrote {!s} to {!s}".format(out_filename + '.csv', out_path))
        else:
            print("writeAsCSV: outup path not correct!")
        
            
        
            
    