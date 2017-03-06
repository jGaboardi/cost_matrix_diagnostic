#    GNU LESSER GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#        Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
#            Everyone is permitted to copy and distribute verbatim copies
#                of this license document, but changing it is not allowed.
#

try:
    import numpy
except:
    "Please install numpy"
try:
    import pandas
except:
    "Please install pandas"
    
import sys
import warnings
if sys.version_info[0] != 2 and sys.version_info[1] != 7:
    warnings.warn("The class defined in `cost_matrix_diagnostic.py` "
                  "may not be compatible with the version of Python being used. " 
                  "It is designed to be used with Python 2.7.x.")
                  
__author__   = 'James D. Gaboardi'
__version__  = '0.2', '03/2017'
__license__  = 'version 3 of the GNU Lesser General Public License' 
                  
        