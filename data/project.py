'''
Created on 22.12.2012

@author: Alex
'''

import numpy as np
from matplotlib import pyplot as plt

from io_handling.file_handling import makeSurePathExists
from calc_modules.Advection_LaxWendroff import calcLaxWendroff
from calc_modules.Advection_Upwind import calcUpwind

class ProjectData():
    
    def __init__(self,  dx= 0.002, dt = 0.001, c = 1.0, steps = 50):
        
        self.dx = dx
        self.x = np.arange(-2,5, dx)
        self.size_x = np.size(self.x)
        self.dt = dt
        self.c = c
        self.steps = steps

        self.u_0 = np.zeros(self.size_x)
        self.u_1 = np.zeros(self.size_x)
        self.u_00 = np.zeros(self.size_x)
        self.u_01 = np.zeros(self.size_x)
        self.signal_shape = ''
        
        self.CFL = self.c*self.dt/self.dx   
        print("CFL = {}".format(self.CFL))
        
        self.figures = {'lw':plt.figure('lw'), 'upw':plt.figure('upw')}
        self.xlim_low = 0
        self.xlim_high = 3
        self.ylim_low = -0.5
        self.ylim_high = 1.5
        
    def __del__(self):
        for fig in self.figures.itervalues():  plt.close(fig)
        print("closed figures")
        
        
    def __str__(self):
        return 'dx = {!s} dt = {!s} c = {!s} steps = {!s}'.format(self.dx, self.dt, self.c, self.steps)
        
    def setSignal(self, shape):
        if shape != '':
            self.signal_shape = shape
            if shape == 'step':
                for i in range(0,self.size_x) :
                    if self.x[i]<1 :
                        self.u_00[i] = 1.0
                    else :
                        self.u_00[i] = 0.0
                        
            elif shape == 'tri':    # triangle
                for i in range(0,self.size_x) :
                    if self.x[i]<0.5 :
                        self.u_00[i] = 2 * self.x[i]
                    elif self.x[i]<1.0 :
                        self.u_00[i] = 2*(1.0 - self.x[i])
                    else :
                        self.u_00[i] = 0.0
                        
            elif shape == 'wall':
                for i in range(0,self.size_x) :
                    if self.x[i]<0.5 :
                        self.u_00[i] = 0.0
                    elif self.x[i]<1.0 :
                        self.u_00[i] = 1.0
                    else :
                        self.u_00[i] = 0.0
            
            elif shape == 'gauss':
                sigma = 0.15
                mue = 0.5
                for i in range(0,self.size_x) :
                    if self.x[i]<1.0 :
                        self.u_00[i] = 0.5 * 1.0/(sigma * np.sqrt(2 * np.pi)) * np.exp( - 0.5 * ((self.x[i]-mue)/sigma)**2 )
                    else :
                        self.u_00[i] = 0.0
        
    
    def calcAll(self):
        calcLaxWendroff(self)
        calcUpwind(self)
    
    def printFigAll(self, out_path='images/'):        
        self.printFig(out_path, method='lw')
        self.printFig(out_path, method='upw')
    
    
    def printFig(self, out_path='images/', method='lw'):
        
        out_filename = '{0}-{1}-cfl_{2:.2f}-steps_{3}'.format(method, self.signal_shape, self.CFL, self.steps)
        
        makeSurePathExists(out_path)
        
        if method == 'lw':            
            #self.fig_lw.savefig(out_path + out_filename + '.eps')
            self.figures['lw'].savefig(out_path + out_filename + '.png')
            
            print("plotted {!s} to {!s}".format(out_filename + '.png', out_path))
            
        elif method == 'upw':
            #self.fig_upw.savefig(out_path + out_filename + '.eps')
            self.figures['upw'].savefig(out_path + out_filename + '.png')
            
            print("plotted {!s} to {!s}".format(out_filename + '.png', out_path))
    
    