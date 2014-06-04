"""
project module
    define class ProjectData()
        This class holds all those data for the flow-calculations which are
            not specific to one method of calculation
        For each set of parameter there is one ProcetData class witch holds
            a list of MethodData classes - one for each CalcModule in use
"""

import numpy as np
from matplotlib import pyplot as plt

from io_handling.file_handling import create_png, create_csv
from io_handling.graphics import draw_plot

import config_file


class ProjectData(object):
    """ this class holds all input and output data for the flow calculation """

    def __init__(self, dx=0.002, dt=0.001, c=1.0, v=1.0, steps=50, signal='gauss'):

        self.dx = dx  # dx ... spatial resolution

        self.x_min = config_file.x_min
        self.x_max = config_file.x_max
        self.x = np.arange(self.x_min, self.x_max, dx)  # vector of all x-values;  (from, to, resolution)
        self.size_x = np.size(self.x)  # number of x-values
        #print "self.size_x", self.size_x
        self.dt = dt  # dt ... temporal resolution
        self.c = c  # c  ... velocity of flow
        self.v = v  # v  ... coefficient for transport equation
        self.steps = steps  # number of steps to be calculated
        # (full spatial shift = c * dt/dx * steps = CFL * steps)
        self.center_i = config_file.signal_center  # center of signal at t=0
        self.center_f = self.center_i + \
                        self.c * self.dt * self.steps  # center of signal at t=t_max (of analytic solution)

        self.u_00 = np.zeros(self.size_x)  # to keep a copy of input signal
        self.signal_shape = ''  # shape of input signal

        self.CFL = self.c * self.dt / self.dx  # Courant number, Upwind and LaxWendroff are stable for CFL <= 1
        print("CFL = {}".format(self.CFL))
        self.CFL2 = self.CFL ** 2.0  # just for easy reading formulas
        if self.v != 0:  # avoid division by zero
            self.PE = self.c * self.dx / self.v  # Peclet number
        else:
            self.PE = 0.0

        self.NE = self.v * self.dt / (self.dx ** 2)

        self.methods = {}
        # all methods will be drawn into the same figure
        self.fig = None

        self.signal_max = config_file.signal_max

        # boundaries of the figures
        self.x_lim_low = config_file.x_lim_low
        self.x_lim_high = config_file.x_lim_high
        self.y_lim_low = config_file.y_lim_low
        self.y_lim_high = config_file.y_lim_high

        self.set_signal(signal)

        # boundary conditions (these are functions!)
        self.bc_upstream_type = config_file.bc_upstream_type
        self.bc_downstream_type = config_file.bc_downstream_type

    def __del__(self):
        """ destructor, ensure that all objects are completely eliminated """

        for m in self.methods.itervalues():
            if m is not None:
                del m

        plt.close('all')
        print("closed figures and classes")

    def __str__(self):
        return 'dx = {!s} dt = {!s} c = {!s} steps = {!s}' \
            .format(self.dx, self.dt, self.c, self.steps)

    def del_fig(self):
        plt.clf()
        if self.fig is not None:
            plt.close('all')
            del self.fig
            self.fig = None

    def bc_upstream(self, t):  # wrapper for boundary condition - upstream
        return self.boundary_condition(t, str_type=self.bc_upstream_type)

    def bc_downstream(self, t):  # wrapper for boundary condition
        return self.boundary_condition(t, str_type=self.bc_downstream_type)

    def boundary_condition(self, t, str_type):
        """ functions for boundary condition (upstream and downstrem) """
        if str_type == 'zero':
            return 0.0

        elif str_type == 'wave':
            fact = 1.0 / 10.0
            offset = self.signal_max * 0.5
            return self.signal_max * 0.5 * np.sin(fact * t * (2 * np.pi)) + offset

        elif str_type == 'constant':
            return self.signal_max

        else:
            return 0.0

    def set_signal(self, shape):
        """ write input signal into u_00 using chosen shape"""
        if shape != '':
            self.signal_shape = shape
            shape_max = self.signal_max
            center = self.center_i

            if shape == 'step':
                for i in range(0, self.size_x):
                    if self.x[i] < center:
                        self.u_00[i] = shape_max
                    else:
                        self.u_00[i] = 0.0

            elif shape == 'tri':  # triangle
                for i in range(0, self.size_x):
                    self.u_00[i] = max(0.0, shape_max - abs(center - self.x[i]))

            elif shape == 'wall':
                thickness = shape_max
                for i in range(0, self.size_x):
                    if abs(self.x[i] - center) < (thickness * 0.5):
                        # maybe add "+ config_file.EPS" into abs(...) to
                        # exclude one point on one end of the shape
                        # and include one point on the other end of the shape
                        self.u_00[i] = shape_max
                    else:
                        self.u_00[i] = 0.0

            elif shape == 'thinwall':
                #thickness = shape_max / 10.0
                thickness = 4.0 * self.dx
                for i in range(0, self.size_x):
                    if abs(self.x[i] - center) < thickness * 0.5:
                        self.u_00[i] = shape_max
                    else:
                        self.u_00[i] = 0.0

            elif shape == 'gauss':
                #f_max = 1 / (sigma * sqrt(2*pi))
                #sigma = 1.0 / (shape_max * np.sqrt(2*np.pi))
                sigma = np.sqrt(shape_max)
                mue = center
                for i in range(0, self.size_x):
                    self.u_00[i] = shape_max \
                                   * np.exp(- 0.5 * ((self.x[i] - mue) / sigma) ** 2)

            elif shape == 'wave':
                amp = 0.5 * shape_max
                offset = 0.5 * shape_max
                wavelength = 10.0
                fact = 1.0 / wavelength
                phase = 0.25 * wavelength
                for i in range(0, self.size_x):
                    if self.x[i] < center:
                        self.u_00[i] = amp * np.sin(fact * (self.x[i] - phase) * (2 * np.pi)) + offset
                    else:
                        self.u_00[i] = 0.0

            elif shape == 'zero':
                for i in range(0, self.size_x):
                    self.u_00[i] = 0.0

    def calc(self, method):
        if method in self.methods:
            self.methods[method].calc()

    def calc_all(self):
        for m in self.methods:
            m.calc()

    def create_fig(self):
        self.fig = draw_plot(self)

    def get_fig(self):
        if self.fig is None:
            self.create_fig()
        return self.fig

    def print_fig(self, out_path='', method=''):
        """
        print figure of chosen method
        as .png to out_path(default='images/')
        """

        out_filename = '{0}-dx_{2:.3f}-dt_{3:.3f}-CFL_{4:.2f}-Ne_{5:.2f}-PE_{1:.2f}-steps_{6}' \
            .format(self.signal_shape, self.PE, self.dx, self.dt, self.CFL, self.NE, self.steps)

        #if (method in self.figures) and (out_path != ''):
        my_fig = self.get_fig()
        create_png(out_path, out_filename, my_fig)
        print("plotted {!s} to {!s}".format(out_filename + '.png', out_path))
        #else:
        #    print("printFig: figure for method '{!s}' not found!".format(method))

    def write_as_csv(self, out_path=''):
        """
        export data of chosen method
        as .csv to out_path(default='images/')
        """

        out_filename = '{0}-dx_{2:.3f}-dt_{3:.3f}-CFL_{4:.2f}-Ne_{5:.2f}-PE_{1:.2f}-steps_{6}' \
            .format(self.signal_shape, self.PE, self.dx, self.dt, self.CFL, self.NE, self.steps)

        if out_path != '':
            create_csv(out_path, out_filename, self)
            print("wrote {!s} to {!s}".format(out_filename + '.csv', out_path))
        else:
            print("write_as_csv: output path not correct!")