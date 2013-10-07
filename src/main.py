'''
This Tool is made to demonstrate strengths and weaknesses 
of several numerical methods for advection and diffusion calculation

Main Module
    set parameter, start calculations and print figures
 '''

from itertools import product
import time as t

from calc_modules.base import calcBase
from data.project import ProjectData


def main():
    t0 = t.time()
    outputfolder = '../output/'
    
    # vectors will be used to iterate over all possible combinations of parameter
    # for description of parameters, see class ProjectData in data/project.py
    
    #dx_vec = [0.001, 0.002, 0.004]
    dx_vec = [0.1]    
    dt_vec = [0.01]    
    #c_vec  = [0.6, 1.5, 2.0, 2.8, 3.0]
    c_vec  = [0.3, 0.6]    
    v_vec  = [0.01]
    
    #step_vec = [10,50,100,500,1000]
    step_vec = [300,1000]
    
    #signal_vec =['step', 'wall', 'thinwall', 'tri', 'gauss', 'wave']
    signal_vec =['wave']
    
    #method_vec = ['lw', 'upw', 'lf', 'cn', 'ftcs_diff', 'ftcs_transp', _
    #                   'upw_transp', 'lw_transp', 'cn_transp']
    method_vec = ['upw_transp']                  # methods used for flow-calculation

    
    # iterate over all combinations!
    for par in product(dx_vec, dt_vec, c_vec, v_vec, step_vec): 
        print "\n", par
            
        # ProjectData handles input data, figures, etc.
        pd = ProjectData(dx= par[0], dt = par[1], c = par[2], v = par[3], steps = par[4])
       
        try:
            for sig in signal_vec:
                pd.setSignal(sig)
                # set input signal
                    # 'step'... step
                    # 'tri' ... triangle
                    # 'wall'... block, like step up and step down
                    # 'thinwall' ... like wall, just thinner
                    # 'gauss' ... Gauss-function
                    # 'wave' ... sine-wave
                
                # iterate over all methods in method_vec
                for method in method_vec:
                    t1 = t.time()
                    calcBase(method, pd)
                    # calculate advection using chosen method
                        # 'lw' ... LaxWendroff
                        # 'upw' ... Upwind     
                        # 'lf' ... Leapfrog   
                        # 'cn' ... CrankNicolson 
                        # 'ftcs_diff' ... calcFTCSdiffusion
                        # 'ftcs_transp' ... calcFTCStransport
                        # 'upw_transp'
                        # 'lw_transp'
                        # 'cn_transp'
                    
                    t2 = t.time()
                    print ("time per step - %s: %.2f ms" % (method, (t2-t1)/par[4]*1000))
                    
                    # print figure for this method
                    pd.printFig(out_path=outputfolder+'images/', method=method)
                    pd.writeAsCSV(out_path=outputfolder+'csv/', method=method)
                    
                    pd.del_fig(method)
        finally:
            # delete ProjectData instance and its figures now. Otherwise figures may be wrong
            del(pd)
            
    tn = t.time()
    print ("runtime main: %.3f s" % (tn-t0))


if __name__ == '__main__':
    main()