"""
Analytic solution for the Transport equation
"""

import numpy as np
from numpy import fft


def calc_transp_analytic(pd, m, to_step):  # pd ... project data
    """
    analytic solution using fft/ifft to calculate diffusion
    """
    m.is_stable = True

    m.legend_adder = "\nCr = " + str(round(pd.CFL, 3)) + \
                     "\nPE = " + str(round(pd.PE, 3))

    # analytic solution
    # based on fourier transformation and script Malcherek: p.99 (eq.9.2)

    t_final = pd.dt * to_step   # time for which siffusion+advection takes effect

    u_0 = pd.u_00.copy()

    # calculate diffusion first
    # => so we can cut data which moved out of our borders - without loosing data
    u_diff = u_0.copy()

    # diffusion: do fft, scale coefficients, do ifft
    if pd.v != 0.0:
        fft_coeff = fft.rfft(u_0)
        #ifft_coeff = fft.fft(pd.u_00)

        #fft_coeff = fft_coeff[:-1]
        fft_freq = fft.fftfreq(len(u_0), d=pd.dx) * 2.0 * np.pi
        fft_freq = fft_freq[:len(fft_coeff)]
        #k_vec = np.arange(len(fft_coeff))
        #coeff = enumerate(fft_coeff)

        # apply diffusion on fft-coefficients
        fft_coeff = [
            val * np.exp(-1.0 * (k * k) * pd.v * t_final)
            for (k, val) in zip(fft_freq, fft_coeff)
        ]

        if (len(pd.x) % 2) != 0:  # odd number of elements
            x_cut = pd.x[:(len(pd.x) - 1)]
            m.i_max -= 1  # last point can't be calculated, so its value is undefined
        else:  # even nr. of el. => cut last value
            x_cut = pd.x

        u_diff = fft.irfft(fft_coeff)
    else:
        # no diffusion - simply keep u_diff == u_0
        pass

    # advection: shift u_diff-signal
    u_adv = u_diff    # .copy()

    #  i_shift ... nr. of dx-steps to shift the signal by advection
    i_shift = int(round(t_final * pd.c / pd.dx, 0))

    # area_to_shift ... the area of u_diff which will we be in the observed area after shifting
    area_to_shift = len(u_adv) - i_shift

    # i_cut_off ... used in some formulas => for readability
    i_cut_off = min(i_shift, len(u_adv))

    if pd.c > 0.0:
        t_f_cut = max(0, t_final - len(u_adv) * pd.dx / pd.c)
    else:
        t_f_cut = 0.0

    if area_to_shift > 0:
        # shift by i_shift positions
        u_adv[i_shift:] = u_diff[:area_to_shift]
    else:
        # there is nothing from original area which keeps in observed area
        pass

    # now fill the area above i_shift with values from upstream boundary condition:
    u_adv[:i_cut_off] = [
        pd.bc_upstream(t) for t in np.linspace(t_final, t_f_cut, num=i_cut_off)
    ]



    if i_shift < len(u_0):
        u_adv[i_shift:len(u_0)] = u_0[:len(u_0) - i_shift]
    # apply boundary condition
    u_adv[:i_cut_off] = \
        [pd.bc_upstream(t) for t in np.linspace(t_final, t_f_cut, i_cut_off)]





    #
    # def calc_transp_analytic(pd, m, to_step):  # pd ... project data
    #     """
    #     analytic solution using fft/ifft to calculate diffusion
    #     """
    #
    #     m.is_stable = True
    #
    #     m.legend_adder = "\nCr = " + str(round(pd.CFL, 3)) + \
    #                      "\nPE = " + str(round(pd.PE, 3))
    #
    #     # analytic solution
    #     # based on fourier transformation and script Malcherek: p.99 (eq.9.2)
    #
    #     t_final = pd.dt * to_step  # time final
    #     i_final = int(round(t_final * pd.c / pd.dx, 0))  # how many dx-steps signal is being shifted
    #     u_0 = pd.u_00.copy()
    #     u_adv = pd.u_00.copy()
    #
    #     i_cut_off = min(i_final, len(u_0))  # used in some formulas => for readability
    #     if pd.c > 0.0:
    #         t_f_cut = max(0, t_final - len(u_0) * pd.dx / pd.c)  # similar
    #     else:
    #         t_f_cut = 0.0
    #
    #     # add if pd.Ne = 0 => simply shift input signal
    #     # advection: simply shift signal
    #     if i_final < len(u_0):
    #         u_adv[i_final:len(u_0)] = u_0[:len(u_0) - i_final]
    #     # apply boundary condition
    #     u_adv[:i_cut_off] = \
    #         [pd.bc_upstream(t) for t in np.linspace(t_final, t_f_cut, i_cut_off)]
    #
    #     # diffusion: do fft, scale coefficients, do ifft
    #     if pd.v != 0.0:
    #         fft_coeff = fft.rfft(u_adv)
    #         #ifft_coeff = fft.fft(pd.u_00)
    #
    #         #fft_coeff = fft_coeff[:-1]
    #         fft_freq = fft.fftfreq(len(u_adv), d=pd.dx) * 2.0 * np.pi
    #         fft_freq = fft_freq[:len(fft_coeff)]
    #         #k_vec = np.arange(len(fft_coeff))
    #         #coeff = enumerate(fft_coeff)
    #
    #         fft_coeff = [
    #                         val * np.exp(-1.0 * (k * k) * pd.v * t_final)
    #                         for (k, val) in zip(fft_freq, fft_coeff)
    #                     ]
    #
    #         if (len(pd.x) % 2) != 0:  # odd number of elements
    #             x_cut = pd.x[:(len(pd.x) - 1)]
    #             m.i_max -= 1  # last point can't be calculated, so its value is undefined
    #         else:  # even nr. of el. => cut last value
    #             x_cut = pd.x
    #
    #         m.u_final = fft.irfft(fft_coeff)
    #     else:
    #         m.u_final = u_adv.copy()