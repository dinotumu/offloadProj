#!/usr/bin/python3

# imports
import os
import csv
import time
import datetime
import subprocess
from os import listdir
from os.path import isfile, join


# define variables

# Path to the files required by the program: Here, PWD is offloadProj
PWD = os.getcwd()
PWD = PWD + '/trainmodel_cloud_offloadProj'
PATH_OCR_OUTPUT = PWD + '/data/ocr_output/'
PATH_TO_FILE_DIR = PWD + '/data/test_images/'
PATH_TO_CSV_FILE = PWD + '/data/csv_remote_exec_time/'

# list of all the names of the input image files for the application
# FILE_NAMES = [filename for filename in listdir(PATH_TO_FILE_DIR) if isfile(join(PATH_TO_FILE_DIR, filename))]
FILE_NAMES = ['001.png']
FILE_NAMES.sort()
# print(FILE_NAMES)


def create_csv_file():
    now = datetime.datetime.now()
    # for a custom filename to a csv file: "time_date.csv"
    DATE_TIME = str(now.hour) + '.' + str(now.minute) + '.' + str(now.second) + '_' + str(now.day) + '.' + str(now.month) + '.' + str(now.year) 
    
    # edit global variable "PATH_TO_CSV_FILE"
    global PATH_TO_CSV_FILE
    PATH_TO_CSV_FILE = PATH_TO_CSV_FILE + DATE_TIME + '.csv'
    # print(PATH_TO_CSV_FILE)
    with open(PATH_TO_CSV_FILE, 'w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['file_name', 'time_stamp', 'input_size', 'execution_time'])
# End of function create_csv_file()


def execute_input(filename):
    # Run bash script which executes docker commands
    start = time.time()

    # command to run the bash script which contains docker instructions
    # Arg 0 is PWD + '/scripts/run_app_on_docker.sh'
    # Arg 1 is PATH_TO_FILE_DIR 
    # Arg 2 is filename
    bash_command = 'sh ' + PWD + '/scripts/run_app_on_docker.sh' + ' ' + PATH_TO_FILE_DIR + ' ' + filename + ' ' + PATH_OCR_OUTPUT
    # print(bash_command)
    
    # execute bash command using subprocess
    # app_on_docker_process = 
    subprocess.Popen(bash_command, shell=True)
    # print(app_on_docker_process)

    end = time.time()
    exec_time = end - start
    return exec_time
# End of function execute_input()


def append_csv_file(row):
    with open(PATH_TO_CSV_FILE,'a') as csv_file:
        file_writer = csv.writer(csv_file)
        file_writer.writerow(row)
# End of function append_csv_file()


def data_collector():
    # For each file name in the list, run the tesseract docker container 
    for filename in FILE_NAMES:
        PATH_TO_FILE = PATH_TO_FILE_DIR + filename

        # get input_size
        input_size = os.path.getsize(PATH_TO_FILE)

        # note time stamp before starting the execution
        time_stamp = time.time()

        # invoke execute_input(file_name); get (execution_time) as return value
        execution_time = execute_input(filename)

        # finally, write (input_size, average_cpu_workload, execution_time) to the csv file
        row = [filename, time_stamp, input_size, execution_time]
        append_csv_file(row)
    # End of 'for loop' for 'execute_input'

# End of function data_collector()


if __name__ == "__main__":
    create_csv_file()
    data_collector()