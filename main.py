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
    
    #c_vec  = [0.6, 0.8, 1.0, 1.2, 1.4]
    c_vec  = [1.8]
    #c_vec  = range(0,2,21)
    
    #step_vec = [10,50,100,500,1000]
    step_vec = [1000]
    
    signal_vec =['wall', 'tri', 'gauss']
    
    #for step_val in step_vec:
    for par in product(dx_vec, dt_vec, c_vec, step_vec): # for all combinations!
        print par
        for sig in signal_vec:
            
            # ProjectData handles input data, figures, etc.
            pd = ProjectData(dx= par[0], dt = par[1], c = par[2], steps = par[3])
            
            # set input signal
            # 'step'... step from y=1 to y=0 at x=1
            # 'tri' ... triangle betwenn x=0 and x=1, peak y=1 at x=0.5
            # 'wall'... block, like step up and step down
            # 'gauss' ... Gauss-function
            pd.setSignal(sig)
            
            #calculate advection
            #pd.calcAll()
            t1 = t.time()
            calcLaxWendroff(pd)
            t2 = t.time()
            print ("time per step - LaxWendroff: %.6f s" % ((t2-t1)/par[3]))
            calcUpwind(pd)
            t3 = t.time()
            print ("time per step - Upwind: %.6f s" % ((t3-t2)/par[3]))
            
            # print all figures of this project
            pd.printFigAll(out_path)
            #pd.printFig(out_path, method='upw')
            
            # delete class and its figures now. Otherwise problems occured
            del(pd)
            t2 = t.time()
    tn = t.time()
    print ("runtime main: %.6f s" % (tn-t0))


if __name__ == '__main__':
    main()