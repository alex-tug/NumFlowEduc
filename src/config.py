'''
    config file
'''

############################################
# for main.py

outputfolder = '../output/'

# vectors will be used to iterate over all possible combinations of parameter
# for description of parameters, see class ProjectData in data/project.py


dx_vec = [0.2]

dt_vec = [0.01]    

c_vec  = [0.6]  
  
#v_vec  = [0.1, 0.01, 0.001, 0.0]
v_vec  = [0.1, 0.01, 0.0]

#step_vec = [10,50,100,500,1000]
step_vec = [4000]

#signal_vec =['step', 'wall', 'thinwall', 'tri', 'gauss', 'wave']
signal_vec =['step']
        # 'step'... step
        # 'tri' ... triangle
        # 'wall'... block, like step up and step down
        # 'thinwall' ... like wall, just thinner
        # 'gauss' ... Gauss-function
        # 'wave' ... sine-wave

# methods used for flow-calculation
# possible values: see below
method_vec = ['analytic', 'adv_upw_1st', 'adv_upw_2nd', 'transp_lw']
#method_vec = ['analytic', 'transp_cn']

#
############################################
############################################
# for method.py


from calc_modules.Transp_Analytic       import calcTranspAnalytic
from calc_modules.Adv_Upwind_1st        import calcAdvUpwind1st
from calc_modules.Adv_Upwind_2nd        import calcAdvUpwind2nd
#from calc_modules.Adv_LaxWendroff       import calcAdvLaxWendroff
from calc_modules.Adv_LeapFrog          import calcAdvLeapFrog
from calc_modules.Adv_CrankNicolson     import calcAdvCrankNicolson
from calc_modules.Diffusion_FTCS        import calcDiffusionFTCS
from calc_modules.Transp_FTCS           import calcTranspFTCS
from calc_modules.Transp_Upwind         import calcTranspUpwind
from calc_modules.Transp_LaxWendroff    import calcTranspLW
from calc_modules.Transp_CrankNicolson  import calcTranspCN

modules = {
    'analytic' : calcTranspAnalytic,
    
    'adv_upw_1st' : calcAdvUpwind1st,
    'adv_upw_2nd' : calcAdvUpwind2nd,
    'adv_lf' : calcAdvLeapFrog,
    'adv_cn' : calcAdvCrankNicolson,
    
    'diff_ftcs' : calcDiffusionFTCS,
    
    'transp_ftcs' : calcTranspFTCS,
    'transp_upw' : calcTranspUpwind,
    'transp_lw' : calcTranspLW,
    'transp_cn' : calcTranspCN,
    }
    
#    
############################################