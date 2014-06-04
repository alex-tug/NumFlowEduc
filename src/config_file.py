"""
    config file
"""

import numpy as np

# ###########################################
# for main.py

folder_output = '../output/'

# define which parts of the code to use:
flag_print_simulation_plot = True
flag_write_simulation_as_csv = False

flag_print_stability_data_plot = True
flag_write_stability_data_as_csv = True


# vectors will be used to iterate over all possible combinations of parameter
# for description of parameters, see class ProjectData in data/project.py
temp_var = 1.0

dx_vec = [temp_var]

dt_vec = [temp_var]

c_vec = [i / 100.0 for i in np.arange(0, 101, 25)]
#c_vec = [0.2]

v_vec = [i * temp_var / 100.0 for i in np.arange(0, 101, 25)]
#v_vec = [0.05]

# don't use multiple values for 'step' if you want to create a stability plot,
# it would use a random one of those values for that plot
step_vec = [100]
#step_vec = [1, 5, 10, 20, 50, 100, 200]
#step_vec = [int(round(15.0/i, 0)) for i in dt_vec]     # keep 'real time' constant


#signal_vec =['step', 'wall', 'thinwall', 'tri', 'gauss', 'wave']
signal_vec = ['wall']
# 'step'... step
# 'tri' ... triangle
# 'wall'... block, like step up and step down
# 'thinwall' ... like wall, just thinner
# 'gauss' ... Gauss-function
# 'wave' ... sine-wave
# 'zero' ... f(x) := 0

bc_upstream_type = 'zero'
bc_downstream_type = 'zero'
# 'zero' ... f(t) := 0
# 'wave' ... sine-wave
# 'constant' ... constant level height=signal_max

# center of the signal created in class project
signal_center = 20.0
# maximum value of the signal created in class project
signal_max = 10.0

# methods used for flow-calculation
# possible values: see below


#method_vec = ['transp_ftcs', 'analytic', 'transp_upw', 'transp_implicit', 'transp_cn', 'transp_lw']
# 'transp_ftcs', 'transp_upw', 'transp_cn', 'transp_lw']

method_vec = ['analytic', 'transp_lw']


# special parameter for some methods:

    # for Crank Nicolson:
# th ... theta:
# 0 = fully explicit,
# 0.5=classic CrankNicolson
# 1 = fully implicit
th = 0.5

    # for generalized euler scheme (Forward Time)
# alpha = 0     ... forward differences = FTFS
# alpha = 0.5   ... central differences = FTCS
# alpha = 1     ... backward differences = upwind
alpha = 1.0


#
############################################

# drawings:

# minimum/maximum x-value for the area to be calculated
x_min = -10.0
x_max = 110.0
# limits for the graphics created in class project
x_lim_low = 0.0
x_lim_high = 100.0
y_lim_low = -0.1 * signal_max
y_lim_high = 1.2 * signal_max

#for graphical output:
#i_min = 1
#i_max = 40   # set i_max0 to zero to use max. possible range !


############################################
# for method.py

from calc_modules.transp_analytic import calc_transp_analytic

from calc_modules.adv_Upwind_1st import calc_adv_Upwind1st
from calc_modules.adv_Upwind_2nd import calc_adv_Upwind2nd
from calc_modules.adv_CrankNicolson import calc_adv_CrankNicolson_old
from calc_modules.transp_implicit import calc_transp_implicit

from calc_modules.transp_ftcs import calc_transp_ftcs
from calc_modules.transp_Upwind import calc_transp_Upwind
from calc_modules.transp_LeapFrog import calc_transp_LeapFrog
from calc_modules.transp_LaxWendroff import calc_transp_lw
from calc_modules.transp_CrankNicolson import calc_transp_cn

modules = {
    'analytic': calc_transp_analytic,

    'adv_upw_1st': calc_adv_Upwind1st,
    'adv_upw_2nd': calc_adv_Upwind2nd,
    'adv_cn': calc_adv_CrankNicolson_old,

    'transp_upw': calc_transp_Upwind,
    'transp_cn': calc_transp_cn,

    'transp_ftcs': calc_transp_ftcs,
    'transp_lf': calc_transp_LeapFrog,
    'transp_lw': calc_transp_lw,
    'transp_implicit': calc_transp_implicit,
}

#    
############################################

# for stability plot:
subfolder_plot_stability = 'csv_stability/'
stability_file_signature = '_'



# others:

# EPS ... used to check equality of two float variables
EPS = 1e-10
#
# HUGE_NUMBER ... used to approximate infinity (for stability check)
HUGE_NUMBER = 1e10