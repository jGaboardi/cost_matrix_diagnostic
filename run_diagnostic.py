#    GNU LESSER GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#        Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
#            Everyone is permitted to copy and distribute verbatim copies
#                of this license document, but changing it is not allowed.
#

"""run_diagnostic.py for --> `cost_matrix_diagnostic.py`

example call within ipython:
>>> run run_diagnostic.py 5

example call from command line:
>>> python run_diagnostic.py 5

This command with run the diagnostic script in the situation of 1 to 5 connectors being
used to create cost matrices. 5 total cost matrices will be compared in this sceanrio.
    
* sys.argv [1] = maximum connector density
"""

from cost_matrix_diagnostic import cost_matrix_diagnostic as cmd
import os 
import sys
import warnings

# Set connector density
connectors = list(range(1,int(sys.argv[1])+1))

# Set file paths
top_dir = os.path.dirname(os.path.realpath((' .')))
directory = top_dir + "/"
# Cost matrix information
matrix_directory = "test_matrices/"
matrix_file = "_Matrix.csv"
matrix_index_col=None
matrix_column_name="  Connectors"

# Instantiate object
situation = cmd.ConnectorScenario(connectors=connectors,
                                  head_directory=directory)
# Scenario list of dataframes
scenarios = situation.read_in_mtxs(mtx_dir=matrix_directory,
                                   mtx_file=matrix_file,
                                   index_name=matrix_index_col,
                                   column_name=matrix_column_name)
# Network Diagnostics
diags = situation.network_travel_time_comparision(with_diags=True,
                                                     print_diags=True,
                                                     save_diags=True,
                                                     diag_text_path=directory+"/",
                                                     diag_text_file="_Network_Diagnostics",
                                                     true_sp_mtxs=False)

# What If scenarios
what_if = situation.true_sp()
# What If Network Diagnostics
what_if_network_diags = situation.network_travel_time_comparision(with_diags=True,
                                                                  true_sp_mtxs=True)
what_if_network_diags = list(enumerate(what_if_network_diags, 1))
##########################################################################################