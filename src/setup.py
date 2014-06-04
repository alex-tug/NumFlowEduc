from distutils.core import setup
#import py2exe

from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy as np

# from distutils.filelist import findall
# import os
# import matplotlib
# matplotlibdatadir = matplotlib.get_data_path()
# matplotlibdata = findall(matplotlibdatadir)
# matplotlibdata_files = []
#
# for f in matplotlibdata:
#     dirname = os.path.join('matplotlibdata', f[len(matplotlibdatadir)+1:])
#     matplotlibdata_files.append((os.path.split(dirname)[0], [f]))


ext  =  [Extension( "transp_LaxWendroff_cython",
                    sources=["calc_modules/transp_LaxWendroff_cython.pyx"] )]

# cythonize("transp_LaxWendroff_cython.pyx"),

setup(
    cmdclass={'build_ext': build_ext},
    include_dirs=[np.get_include()],
    ext_modules=ext,
    requires=['numpy', 'matplotlib', 'scipy', 'Cython']
)
    # console=['main.py'],
#                        'includes': 'matplotlib.numerix.random_array',
# setup(
#     ext_modules = cythonize("transp_LaxWendroff_cython.pyx"),
#     options={
#              'py2exe': {
#                         'packages' : ['matplotlib', 'pytz'],
#                         'excludes': ['_gtkagg', '_tkagg'],
#                         'dll_excludes': [ 'MSVCP90.dll',
#                                          'libgdk-win32-2.0-0.dll',
#                                          'libgobject-2.0-0.dll',
#                                          'libgdk_pixbuf-2.0-0.dll',]
#                        }
#             },
#     data_files=matplotlibdata_files,
#     requires=['numpy', 'matplotlib', 'scipy', 'Cython']
# )