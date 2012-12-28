'''
This Tool is made to demonstrate strengths and weaknesses 
of several numerical methods for advection and diffusion calculation

Main Module
    set parameter, start calculations and print figures
'''

from itertools import product
import time as t

from calc_modules.base import calcAdvection
from data.project import ProjectData


def main():
    t0 = t.time()
    out_path = 'images/'
    
    # vectors will be used to iterate over all possible combinations of parameter
    # for description of parameters, see class ProjectData in data/project.py
    
    #dx_vec = [0.001, 0.002, 0.004]
    dx_vec = [0.002]
    
    dt_vec = [0.001]
    
    #c_vec  = [0.6, 1.5, 2.0, 2.8, 3.0]
    c_vec  = [1.5]
    
    #step_vec = [10,50,100,500,1000]
    step_vec = [10,50, 500]
    
    #signal_vec =['step', 'wall', 'thinwall', 'tri', 'gauss', 'wave']
    signal_vec =['step','wave']
    
    #method_vec = ['lw', 'upw', 'lf', 'cn']
    method_vec = ['upw', 'cn']                  # methods used for flow-calculation
    
    # iterate over all combinations!
    for par in product(dx_vec, dt_vec, c_vec, step_vec): 
        print "\n", par
            
        # ProjectData handles input data, figures, etc.
        pd = ProjectData(dx= par[0], dt = par[1], c = par[2], steps = par[3])
            
        # iterate over all signals in signal_vec
        for sig in signal_vec:
            pd.setSignal(sig)
            # set input signal
                # 'step'... step from y=1 to y=0 at x=1
                # 'tri' ... triangle betwenn x=0 and x=1, peak y=1 at x=0.5
                # 'wall'... block, like step up and step down
                # 'thinwall' ... wall from x=0.7 to x=0.72
                # 'gauss' ... Gauss-function
                # 'wave' ... sine-wave
            
            # iterate over all methods in method_vec
            for method in method_vec:
                t1 = t.time()
                calcAdvection(method, pd)
                # calculate advection using chosen method
                    # 'lw' ... LaxWendroff
                    # 'upw' ... Upwind     
                    # 'lf' ... Leapfrog   
                    # 'cn' ... CrankNicolson                
                t2 = t.time()
                print ("time per step - %s: %.2f ms" % (method, (t2-t1)/par[3]*1000))
                
                # print figure for this method
                pd.printFig(out_path=out_path, method=method)
            
        # delete ProjectData instance and its figures now. Otherwise figures may be wrong
        del(pd)
    tn = t.time()
    print ("runtime main: %.3f s" % (tn-t0))


if __name__ == '__main__':
    main()