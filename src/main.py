"""
This Tool is made to demonstrate strengths and weaknesses
of several numerical methods for advection and diffusion calculation

Main Module:
    create sets of parameter,
    create ProjectData- and MethodData-instances,
    start calculations and export data
    (if flags in config_file are activated)
 """

from itertools import product
import time as t

from data.project import ProjectData
from data.method import MethodData
from io_handling.file_handling import export_stability_check_results, create_png
from io_handling.graphics import draw_stability_plot
import config_file


# parameter from config will be used as default
def main(dx_vec=config_file.dx_vec,
         dt_vec=config_file.dt_vec,
         c_vec=config_file.c_vec,
         v_vec=config_file.v_vec,
         step_vec=config_file.step_vec,
         signal_vec=config_file.signal_vec,
         method_vec=config_file.method_vec,
         output_folder=config_file.folder_output,
         ):
    t_0 = t.time()

    # check_vec ... will store information about the stability of each method
    #               for each CFL-NE-combination
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
                if not method in check_vec:
                    check_vec[method] = []

                pd.methods[method] = MethodData(pd, method)

                t_1 = t.time()
                # calculate using chosen method
                pd.calc(method)
                t_2 = t.time()

                print("\n  method: %s: area = %.2f" % (method, pd.methods[method].get_area()))
                print ("time - %s: %.2f ms" % (method, (t_2 - t_1) * 1000))
                print ("time per step - %s: %.2f ms" % (method, (t_2 - t_1) / par[4] * 1000))

                check_vec[method].append([
                    pd.CFL,
                    round(pd.NE, 2),
                    round(pd.PE, 2),
                    pd.methods[method].is_not_neg(),
                    pd.methods[method].is_nearly_zero(),
                    pd.methods[method].is_not_huge()
                ])

            # export results
            if config_file.flag_print_simulation_plot:
                pd.print_fig(out_path=output_folder + 'images/')
            if config_file.flag_write_simulation_as_csv:
                pd.write_as_csv(out_path=output_folder + 'csv/')

            pd.del_fig()
        finally:
            # Delete ProjectData instance and its figures now.
            # Otherwise figures may be wrong
            del pd

    for method in check_vec.keys():
        if config_file.flag_print_stability_data_plot:
            export_stability_check_results(output_folder + config_file.subfolder_plot_stability,
                                            config_file.stability_file_signature,
                                            method,
                                            check_vec[method])

        if config_file.flag_write_stability_data_as_csv:
            fig_stability = draw_stability_plot(check_vec[method])
            create_png(output_folder + config_file.subfolder_plot_stability,
                       'stability_' + method, fig_stability)

    t_n = t.time()
    print ("runtime main: %.3f s" % (t_n - t_0))


if __name__ == '__main__':
    # print sys.argv[1:]
    main()