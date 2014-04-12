"""
Analytic solution for the Transport equation
"""

import numpy as np
from numpy import fft
from linalg_helper import return_next_power_of_two


def calc_transp_analytic(pd, m, to_step):  # pd ... project data
    """
    analytic solution using fft/ifft to calculate diffusion
    based on fourier transformation and script Malcherek: p.99 (eq.9.2)
    """
    m.is_stable = True

    m.legend_adder = "\nCr = " + str(round(pd.CFL, 3)) + \
                     "\nPE = " + str(round(pd.PE, 3))

    t_final = pd.dt * to_step   # time for which diffusion+advection takes effect

    # append zeros to avoid the signal from reentering on the upstream boudnary
    # and increase performance of fft
    orig_length = len(pd.u_00)
    additional_length = return_next_power_of_two(2.0 * orig_length) - orig_length
    u_0 = np.append(pd.u_00, np.zeros(additional_length))

    if pd.v != 0.0 or pd.c != 0.0:
        fft_coeff = fft.rfft(u_0)

        fft_freq = fft.fftfreq(len(u_0), d=pd.dx) * 2.0 * np.pi

        # apply diffusion and advection on fft-coefficients
        # k*k*pd.v      ... diffusion
        # 1j * k*pd.c   ... advection => time shifting of fourier transformation
        fft_coeff_final = [
            val  * np.exp(-1.0 * t_final * (k*k*pd.v  + 1j * k*pd.c))
            for (k, val) in zip(fft_freq, fft_coeff)
        ]

        u_final = fft.irfft(fft_coeff_final)
    else:
        u_final = u_0.copy()

    m.u_final = u_final[:orig_length]


##############################################
# backup:
#
# def calc_transp_analytic(pd, m, to_step):  # pd ... project data
#     """
#     analytic solution using fft/ifft to calculate diffusion
#     """
#     m.is_stable = True
#
#     m.legend_adder = "\nCr = " + str(round(pd.CFL, 3)) + \
#                      "\nPE = " + str(round(pd.PE, 3))
#
#     # analytic solution
#     # based on fourier transformation and script Malcherek: p.99 (eq.9.2)
#
#     t_final = pd.dt * to_step   # time for which siffusion+advection takes effect
#
#     u_0 = pd.u_00.copy()
#
#     # calculate diffusion first
#     # => so we can cut data which moved out of our borders - without loosing data
#     u_diff = u_0.copy()
#
#     # diffusion: do fft, scale coefficients, do ifft
#     if pd.v != 0.0:
#         fft_coeff = fft.rfft(u_0)
#
#         fft_freq = fft.fftfreq(len(u_0), d=pd.dx) * 2.0 * np.pi
#         # shift:
#         #fft_freq = fft_freq[:len(fft_coeff)]
#
#         # apply diffusion on fft-coefficients
#         # exponent = np.exp(-1.0 * (k * k) * pd.v * t_final)
#         # exponent = -1.0
#         # k * val * np.exp(exponent)
#         #fft_coeff_diff = [
#         #    val * np.exp(-1.0 * (k * k) * pd.v * t_final) + np.exp(-1j * k * 2.0 * np.pi * t_final)
#         #    for (k, val) in zip(fft_freq, fft_coeff)
#         #]
#
#         fft_coeff_diff = [
#             val  * np.exp(-1.0 * t_final * (k*k*pd.v  + 1j * k/2.0))
#             for (k, val) in zip(fft_freq, fft_coeff)
#         ]
#
#         #if (len(pd.x) % 2) != 0:  # odd number of elements
#         #    x_cut = pd.x[:(len(pd.x) - 1)]
#         #    m.i_max -= 1  # last point can't be calculated, so its value is undefined
#         #else:  # even nr. of el. => cut last value
#         #    x_cut = pd.x
#
#         u_diff = fft.irfft(fft_coeff_diff)  # fft_coeff_diff
#     else:
#         # no diffusion - simply keep u_diff == u_0
#         pass
#
#     # advection: shift u_diff-signal
#     u_adv = u_diff.copy()
#
#     #  i_shift ... nr. of dx-steps to shift the signal by advection
#     i_shift = int(round(t_final * pd.c / pd.dx, 0))
#
#     #if i_shift > 0:     # otherwise there is no advection to be calculated
#     if False:
#         # area_to_shift ... the area of u_diff which will we be in the observed area after shifting
#         area_to_shift = len(u_adv) - i_shift
#
#         # i_cut_off ... used in some formulas => for readability
#         i_cut_off = min(i_shift, len(u_adv))
#
#         if pd.c > 0.0:
#             t_f_cut = max(0, t_final - len(u_adv) * pd.dx / pd.c)
#         else:
#             t_f_cut = 0.0
#
#         if area_to_shift > 0:
#             # shift by i_shift positions
#             u_adv[i_shift:] = u_diff[:area_to_shift]
#         else:
#             # there is nothing from original area which keeps in observed area
#             pass
#
#         # now fill the area above i_shift with values from upstream boundary condition:
#         u_adv[:i_cut_off] = [
#             pd.bc_upstream(t) for t in np.linspace(t_final, t_f_cut, num=i_cut_off)
#         ]
#
#     m.u_final = u_adv.copy()