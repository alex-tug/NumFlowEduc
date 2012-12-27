'''
Created on 22.12.2012

@author: Alex
'''
from itertools import product
import time as t

from calc_modules.Advection_LaxWendroff import calcLaxWendroff
from calc_modules.Advection_Upwind import calcUpwind
from data.project import ProjectData


def main():
    t0 = t.time()
    out_path = 'images/'
    
    #dx_vec = [0.001, 0.002, 0.004]
    dx_vec = [0.002]
    
    dt_vec = [0.0010]
    #dt_vec = [0.001]
    
    #c_vec  = [0.6, 1.5, 2.0, 2.8, 3.0]
    c_vec  = [0.2, 1.5, 1.8, 2.0]
    #c_vec  = range(0,2,21)
    
    #step_vec = [10,50,100,500,1000]
    step_vec = [2000]
    
    #signal_vec =['step', 'wall', 'thinwall', 'tri', 'gauss', 'wave']
    signal_vec =['step', 'wall', 'thinwall', 'tri', 'gauss', 'wave']
    
    #for step_val in step_vec:
    for par in product(dx_vec, dt_vec, c_vec, step_vec): # for all combinations!
        print "\n", par
            
        # ProjectData handles input data, figures, etc.
        pd = ProjectData(dx= par[0], dt = par[1], c = par[2], steps = par[3])
            
        for sig in signal_vec:
            # set input signal
            # 'step'... step from y=1 to y=0 at x=1
            # 'tri' ... triangle betwenn x=0 and x=1, peak y=1 at x=0.5
            # 'wall'... block, like step up and step down
            # 'thinwall' ... wall from x=0.7 to x=0.72
            # 'gauss' ... Gauss-function
            # 'wave' ... sine-wave
            pd.setSignal(sig)
            
            #calculate advection
            #pd.calcAll()
            t1 = t.time()
            calcLaxWendroff(pd)
            t2 = t.time()
            print ("time per step - LaxWendroff: %.2f ms" % ((t2-t1)/par[3]*1000))
            calcUpwind(pd)
            t3 = t.time()
            print ("time per step - Upwind: %.2f ms" % ((t3-t2)/par[3]*1000))
            
            # print all figures of this project
            pd.printFigAll(out_path)
            #pd.printFig(out_path, method='upw')
            
            # delete class and its figures now. Otherwise problems occured
        del(pd)
        t2 = t.time()
    tn = t.time()
    print ("runtime main: %.3f s" % (tn-t0))


if __name__ == '__main__':
    main()