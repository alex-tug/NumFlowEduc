'''
    config file
'''

############################################
# for main.py

outputfolder = '../output/'

# vectors will be used to iterate over all possible combinations of parameter
# for description of parameters, see class ProjectData in data/project.py

#dx_vec = [1.0, 0.5, 0.2, 0.1]
dx_vec = [0.5]
dt_vec = [0.01]    
#c_vec  = [0.6, 1.5, 2.0, 2.8, 3.0]
c_vec  = [0.2]    
v_vec  = [0.1]

#step_vec = [10,50,100,500,1000]
step_vec = [5000]

#signal_vec =['step', 'wall', 'thinwall', 'tri', 'gauss', 'wave']
signal_vec =['wall']
        # 'step'... step
        # 'tri' ... triangle
        # 'wall'... block, like step up and step down
        # 'thinwall' ... like wall, just thinner
        # 'gauss' ... Gauss-function
        # 'wave' ... sine-wave

# methods used for flow-calculation
# possible values: see below
method_vec = ['analytic', 'ftcs_transp', 'lw_transp', 'cn_adv', 'cn_transp']

#
############################################
############################################
# for method.py


from calc_modules.Transp_Analytic import calcTranspAnalytic
#from calc_modules.Advection_Upwind import calcUpwind
from calc_modules.Advection_LaxWendroff     import calcAdvLaxWendroff
from calc_modules.Advection_LeapFrog        import calcAdvLeapFrog
from calc_modules.Advection_CrankNicolson   import calcAdvCrankNicolson
from calc_modules.Diffusion_FTCS            import calcDiffusionFTCS
from calc_modules.Transp_FTCS               import calcTranspFTCS
from calc_modules.Transp_Upwind             import calcTranspUpwind
from calc_modules.Transp_LaxWendroff        import calcTranspLW
from calc_modules.Transp_CrankNicolson      import calcTranspCN

modules = {
    'analytic' : calcTranspAnalytic,
    'lw_adv' : calcAdvLaxWendroff,
    'lf_adv' : calcAdvLeapFrog,
    'cn_adv' : calcAdvCrankNicolson,
    'ftcs_diff' : calcDiffusionFTCS,
    'ftcs_transp' : calcTranspFTCS,
    'upw_transp' : calcTranspUpwind,
    'lw_transp' : calcTranspLW,
    'cn_transp' : calcTranspCN,
    }
    
#    
############################################