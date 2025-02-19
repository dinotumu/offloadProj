#!/usr/bin/python3

# imports
import os
import csv
import time
import datetime
import subprocess
from os import listdir
from os.path import isfile, join

# stress-ng variables
STRESSNG_VALUES = [i for i in range(0,50,5)]
# print(STRESSNG_VALUES)
STRESSNG_CMD = "stress-ng -c 0 -l "

# Path to the files required by the program: Under the asssumption that PWD is offloadProj
PWD = os.getcwd()
SBC_PWD = PWD + '/sbc'
PATH_TO_FILE_DIR = SBC_PWD + '/data/train_data/'
PATH_SBC_OUTPUT = SBC_PWD + '/data/output/'
PATH_TO_CPUBWMON_FILE = SBC_PWD + '/data/cpu_bw_mon_now.csv'
PATH_TO_CSV_FILE = SBC_PWD + '/data'

# list of all the names of the input image files for the application
FILE_NAMES = [filename for filename in listdir(PATH_TO_FILE_DIR) if isfile(join(PATH_TO_FILE_DIR, filename))]
FILE_NAMES.sort()
# print(FILE_NAMES)

def create_csv_file():
    now = datetime.datetime.now()
    # for a custom filename to a csv file: "time_date.csv"
    DATE_TIME = str(now.hour) + '.' + str(now.minute) + '.' + str(now.second) + '_' + str(now.day) + '.' + str(now.month) + '.' + str(now.year) 
    
    # edit global variable "PATH_TO_CSV_FILE"
    global PATH_TO_CSV_FILE
    PATH_TO_CSV_FILE = PATH_TO_CPUBWMON_FILE + DATE_TIME + '.csv'
    with open(PATH_TO_CSV_FILE, 'w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['File Name', 'File Size', 'Average CPU Workload', 'Execution Time'])
# End of function create_csv_file()

def append_csv_file(row):
    with open(PATH_TO_CSV_FILE,'a') as csv_file:
        file_writer = csv.writer(csv_file)
        file_writer.writerow(row)
# End of function append_csv_file()


def data_collector():
    for stressng_value in STRESSNG_VALUES:
        stressng_command = STRESSNG_CMD + str(stressng_value)
        # print(stressng_command)
        
        # execute stress_ng command using subprocess: "$ stress-ng -c 0 -l 40" for 40% cpu stress
        # stressng_process = subprocess.Popen(stressng_command, shell=True)
        
        # wait time to make the cpu percenatge stable
        time.sleep(10)

        # for each stress-ng, execute all inputs
        for file_name in [1]:
            # get input_size
            input_size = os.path.getsize(PATH_TO_FILE_DIR + file_name)

            # Fetch average cpu utilization from the cpu_bw_mon_now.csv file
            with open(PATH_TO_CPUBWMON_FILE) as cpu_mon:
                average_cpu_workload = float(cpu_mon.readline()[:-1].split(',')[2])

            # initiate the start time to calculate the execution time of the desired application 
            start = time.time()
            
            # run the tesseract-ocr application with the input (from parameter)
            bash_command = 'tesseract ' + PATH_TO_FILE_DIR + file_name + ' ' + PATH_SBC_OUTPUT + file_name
            os.system(bash_command)

            # end time of the application
            end = time.time()
            execution_time = end - start
            
            # finally, write (input_size, average_cpu_workload, execution_time) to the csv file
            row = [file_name, input_size, average_cpu_workload, execution_time]
            append_csv_file(row)
        # End of 'for loop' for 'execute_input'

        # Terminate the stress-ng process after running for all the inputs for a particular (stressng_value) 
        # stressng_process.terminate()
        time.sleep(10)
        print('Process Terminated')

    # End of 'for loop' for 'stressng_values'
# End of function data_collector()



if __name__ == "__main__":
    create_csv_file()
    data_collector()
