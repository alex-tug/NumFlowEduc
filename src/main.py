'''
This Tool is made to demonstrate strengths and weaknesses 
of several numerical methods for advection and diffusion calculation

Main Module:
    create sets of parameter,
    create ProjectData- and MethodData-instances,
    start calculations and export data
 '''

from itertools import product
import time as t

from data.project import ProjectData
from data.method import MethodData

from config import outputfolder,\
        dx_vec, dt_vec, c_vec, v_vec,\
        step_vec, signal_vec, method_vec

def main():
    t0 = t.time()
    
    # iterate over all combinations!
    for par in product(dx_vec, dt_vec, c_vec, v_vec, step_vec): 
        print "\n", par
            
        # ProjectData handles input data, figures, etc.
        pd = ProjectData(dx= par[0], dt = par[1], c = par[2], v = par[3], steps = par[4])
       
        try:
            for sig in signal_vec:
                pd.setSignal(sig)   # set input signal
                
                # iterate over all methods in method_vec
                for method in method_vec:
                    
                    pd.methods[method] = MethodData(pd, method)
                    
                    t1 = t.time()
                    pd.calc(method)
                    # calculate using chosen method                    
                    t2 = t.time()
                    print ("time per step - %s: %.2f ms" % (method, (t2-t1)/par[4]*1000))
                    
                # export results
                pd.printFig(out_path=outputfolder+'images/')
                pd.writeAsCSV(out_path=outputfolder+'csv/')
                    
                pd.del_fig()
        finally:
            # delete ProjectData instance and its figures now. Otherwise figures may be wrong
            del(pd)
            
    tn = t.time()
    print ("runtime main: %.3f s" % (tn-t0))


if __name__ == '__main__':
    main()