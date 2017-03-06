#    GNU LESSER GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#        Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
#            Everyone is permitted to copy and distribute verbatim copies
#                of this license document, but changing it is not allowed.
#

"""cost_matrix_diagnostic.py
"""
import copy
import numpy as np
import pandas as pd
import warnings
from .__init__ import __author__, __license__, __version__

class ConnectorScenario:
    """
    This class creates an object for the analysis of a set of scenarios at a specific 
    spatial extent with regards to the number of 'connectors' utilized to 
    allocated population polygon centroids to a network for analysis.
    
    """
    
    def __init__(self,
                 connectors=None,
                 head_directory=None):
        """
        Attributes
        ==========
        connectors
        head_directory    
        
        """    
        self.connectors = connectors
        self.head_directory = head_directory


    def read_in_mtxs(self,
                     mtx_dir=None,
                     mtx_file=None,
                     index_name=None,
                     column_name=None):
        """
        Read in all cost matrices
        
        
        Parameters
        ==========
        mtx_dir         str
                        Directory where the matrices are stored
                        
        mtx_file        str
                        matrices' base file name
                        --> should be something like `1_Matrix.csv` for the cost matrix
                            containg values with 1 centroid connector being used.
                        
        index_name      str
                        
                        
        column_name     str
        
        Attributes
        ==========
        matrix_shape    tuple
                        dimension of the cost matrix
                        iXj (rowsXcolumns)
        
        Returns
        =======
        matrix_df_list      list
                            list of pandas dataframes (cost matrices)
    
    
        """
        mtx_dir = self.head_directory+mtx_dir
        matrix_df_list = []
        for count in self.connectors:
            connector_count = str(count)
            data_file = mtx_dir+connector_count+mtx_file
            matrix = pd.read_csv(data_file, index_col=0, header=None)
            if matrix.shape[0] == 1 or matrix.shape[1] == 1:
                warnings.warn("All cost matrices should be in iXj (rowsXcolumns) format.")
            matrix_df_list.append(matrix)
            if count != 0:
                if matrix.shape != matrix_df_list[count-1].shape:
                    warnings.warn("df"+str(count+1), matrix.shape,\
                                "!=", "df"+connector_count, matrix_df_list[count-1].shape)
                    raise Exception("Matrices used in comparision"\
                                    " are different dimensions")
        self.matrix_shape = matrix.shape
        self.matrix_df_list = matrix_df_list
        return self.matrix_df_list
     
     
    def network_travel_time_comparision(self,
                                        with_diags=True,
                                        print_diags=False,
                                        save_diags=False,
                                        diag_text_path=None,
                                        diag_text_file=None,
                                        true_sp_mtxs=False):
        """
        
        Parameters
        ==========
        with_diags      bool
                        Default == True
                        Print
                        
        print_diags     bool
                        Default == False
                        
        save_diags      bool
                        Default == False
                        
        diag_text_path  str
                        Default == None
                        
        diag_text_file  str
                        Default == None
        
        true_sp_mtxs    bool
                        Default == False
        
        Returns
        =======
        self.increases_each_scenario    list
                                        list of diafnostics by dataframes
        
        """
        if not self.matrix_df_list:
            raise Exception("`matrix_df_list` is needed to perform this operation`")
        if not true_sp_mtxs:
            dfs = copy.deepcopy(self.matrix_df_list)
        else:
            dfs = copy.deepcopy(self.true_SP_dfs_list)
        scenarios = range(len(dfs))
        self.increases_each_scenario = []
        for frame in scenarios:
            global_tt = dfs[frame].sum().sum()
            self.increases_each_scenario.append([])
            if frame == 0:
                self.increases_each_scenario[frame] = [0, 
                                                       [], 
                                                       global_tt]
            elif frame != 0:
                bool_array = dfs[frame-1] >= dfs[frame]
                increase_count = 0
                increase_tt = []
                for column in bool_array.columns:
                    for record in bool_array.index:
                        if bool_array[column][record] == False:
                            increase_count += 1
                            increase_tt.append(dfs[frame][column][record])
                self.increases_each_scenario[frame] = [increase_count, 
                                                       increase_tt, 
                                                       global_tt]
        # Run true_sp() on results?
        if increase_count > 0:
            should_run_true_sp_analyis = True
        else:
            should_run_true_sp_analyis = False           
        if should_run_true_sp_analyis:
            print("Should run the `true_sp()` analysis for potential decreases in cost.")
        if with_diags:
            # Total count of cost increases 
            df_count = range(len(self.increases_each_scenario))
            problem_count = sum([self.increases_each_scenario[df][0]\
                                                 for df in df_count])
            problem_list = list(enumerate([self.increases_each_scenario[df][0]\
                                                       for df in df_count], 1))
            # Total cost increases (minutes)
            increase_time = round(sum([sum(self.increases_each_scenario[df][1])\
                                                        for df in df_count]), 4)
            increase_time_list = list(enumerate(\
                                  [round(sum(self.increases_each_scenario[df][1]), 4)\
                                                              for df in df_count], 1))
            # Total travel time along the network in each scenario (minutes)
            total_time = [round(self.increases_each_scenario[df][2], 4)\
                                                     for df in df_count]
            total_time_list = list(enumerate(total_time, 1))
            
            diag_text = "\n\nAt the xxxxxxxxx"\
                         + " level of cost matrix calculation"\
                         + " between Post Offices (origins) and Block Group Centroids"\
                         + " (destinations) there are ** " + str(problem_count) \
                         + " ** instances of unexplained local increases in travel"\
                         + " time as connector density increases accounting for "\
                         + str(increase_time) + " minutes of network travel time."\
                         + " The instances of increase are broken down by count and"\
                         + " increased time as follows:\n"\
                         + "       e.g. [(connector, count)] -- "\
                         + str(problem_list) + "\n"\
                         + "       e.g. [(connector, time)]  -- "\
                         + str(increase_time_list) + "\n\n"\
                         + "As connectors are added the lowest cost travel time should"\
                         + " never increase from any origin destination, it should only"\
                         + " either decrease or remain constant.\n"
            
            # Add this if TOTAL time decreases as expected
            if [time != 0 and total_time[time-1] >= total_time[time]\
                for time in range(len(total_time))]:
                diag_text += "However, total network travel time DOES decrease each time"\
                             + " a connector is added:\n"\
                             + "       e.g. [(connector, total time)]  -- "\
                             + str(total_time_list)
            if print_diags:
                print(diag_text)
            if save_diags:
                diag_outfile = open(diag_text_path+diag_text_file+'.txt', 'w')
                diag_outfile.write(diag_text)
                diag_outfile.close()     
        return self.increases_each_scenario
        
        
    def true_sp(self):
        """
        Find the "true" shortest path 
    
        Returns
        =======
        true_SP_dfs_list    list
                            list of dataframes containing the updated shortest path
                            calculations
        
        """
        dfs = copy.deepcopy(self.matrix_df_list)
        scenarios = range(len(dfs))
        for frame in scenarios:
            if frame != 0:
                bool_array = dfs[frame-1] >= dfs[frame]
                for column in bool_array.columns:
                    for record in bool_array.index:
                        if bool_array[column][record] == False:
                            dfs[frame][column][record] = dfs[frame-1][column][record]
            dfs[frame].round(4)
        self.true_SP_dfs_list = dfs
        true_counter = 0
        for frame in scenarios:           
            bool_array = self.true_SP_dfs_list[frame] == self.matrix_df_list[frame]
            bool_list = list(bool_array.all(axis=0).values)\
                        + list(bool_array.all(axis=1).values)
            true_list = [True]*(self.matrix_shape[0]+self.matrix_shape[1])
            if bool_list != true_list:
                true_counter += 1
        if true_counter == 0:        
            print("Original matrices may already have been calculated as shortest path.")
        return self.true_SP_dfs_list
##########################################################################################        