#!/usr/bin/python3

# imports
import os
import pandas as pd

# Path to the files required by the program: Under the asssumption that PWD is offloadProj
PWD = os.getcwd()
PWD = PWD + '/trainmodel_cloud_offloadProj'
PATH_TO_FILE = PWD + '/data/old_files'
PATH_TO_CSV_FILE = PWD + '/data/exec_time.csv'

exec_time_prediction = pd.read_csv(PATH_TO_CSV_FILE)
df = pd.DataFrame(exec_time_prediction,columns=['file_name', 'input_size', 'execution_time', 'average_cpu_workload'])
print (df)
