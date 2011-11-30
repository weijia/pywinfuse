from distutils.core import setup
from DistUtilsExtra.command import *

import fuse

setup(name='pywinfuse',
      version='.'.join(map(str, fuse.__version__)),
      license='GPL v2',
      url='http://pywinfuse.googlecode.com/',
      description='Support user mode filesystem based on dokan in python',

      packages=['pywinfuse', 'fuseparts'],
      package_dir={'pywinfuse': '.', 'fuseparts': 'fuseparts',},
      
      py_modules=['fuse'],
      data_files=[],
      requires=[],
      cmdclass = { "build" : build_extra.build_extra,
                   "build_help" :  build_help.build_help,
                   "build_icons" :  build_icons.build_icons },
)
