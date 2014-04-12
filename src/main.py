"""
This Tool is made to demonstrate strengths and weaknesses
of several numerical methods for advection and diffusion calculation

Main Module:
    create sets of parameter,
    create ProjectData- and MethodData-instances,
    start calculations and export data
 """
import sys

from itertools import product
import time as t
#import numpy as np

from data.project import ProjectData
from data.method import MethodData
from io_handling.file_handling import create_png, export_stability_check_results
from io_handling.graphics import draw_stability_plot

import config_file as config # import outputfolder,\
#dx_vec, dt_vec, c_vec, v_vec,\
# step_vec, signal_vec, method_vec

# parameter from config will be used as default
def main(dx_vec=config.dx_vec,
         dt_vec=config.dt_vec,
         c_vec=config.c_vec,
         v_vec=config.v_vec,
         step_vec=config.step_vec,
         signal_vec=config.signal_vec,
         method_vec=config.method_vec,
         output_folder=config.folder_output,
        ):
    t_0 = t.time()

    check_vec = {}

    # iterate over all combinations!
    for par in product(dx_vec, dt_vec, c_vec, v_vec, step_vec, signal_vec):
        print "\n", par

        # ProjectData handles input data, figures, etc.
        pd = ProjectData(dx=par[0], dt=par[1], c=par[2],
                         v=par[3], steps=par[4], signal=par[5])

        try:
            # iterate over all methods in method_vec
            for method in method_vec:
                if not check_vec.has_key(method):
                    check_vec[method] = []

                pd.methods[method] = MethodData(pd, method)

                #t_1 = t.time()
                pd.calc(method)
                # calculate using chosen method
                #t_2 = t.time()
                #print ("time per step - %s: %.2f ms" % (method, (t_2-t_1)/par[4]*1000))

                print("method: %s: area = %.2f" % (method, pd.methods[method].get_area()))

                check_vec[method].append([
                                        pd.CFL,
                                        round(pd.NE, 2),
                                        round(pd.PE, 2),
                                        pd.methods[method].is_not_neg(),
                                        pd.methods[method].is_nearly_zero(),
                                        pd.methods[method].is_not_huge()
                ])

            # export results
            pd.print_fig(out_path=output_folder + 'images/')
            #pd.write_as_csv(out_path=output_folder + 'csv/')

            pd.del_fig()
        finally:
            # delete ProjectData instance and its figures now. 
            # Otherwise figures may be wrong
            del pd

    signature = "temp_"
    #'{0}-dx_{1:.3f}-dt_{2:.3f}-steps_{3}' \
    #.format(pd.signal_shape, self.dx, self.dt, self.steps)
    export_stability_check_results(output_folder + 'csv_stability/', signature, check_vec)
    for method in check_vec.keys():
        fig_stability = draw_stability_plot(check_vec[method])
        create_png(output_folder + 'images/', 'stability_' + method, fig_stability)

    t_n = t.time()
    print ("runtime main: %.3f s" % (t_n - t_0))


if __name__ == '__main__':
    print sys.argv[1:]
    main()