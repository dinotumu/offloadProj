#!/usr/bin/python3

# imports
import os
import csv
import time
import subprocess
import datetime
from os import listdir
from os.path import isfile, join

# define variables
# Path to the files required by the program: Here, PWD is offloadProj
PWD = os.getcwd() + '/remote'
PATH_OUTPUT = PWD + '/data/output/'
PATH_IMAGE_FILE = PWD + '/data/train_data/'
PATH_DATASET_FILE = PWD + '/data/remote_train_dataset/'


now = datetime.datetime.now()
DATE_TIME = str(now.day) + '.' + str(now.month) + '.' + str(now.year) + '_' + str(now.hour) + '.' + str(now.minute) + '.' + str(now.second)
output_folder_name = PATH_OUTPUT + DATE_TIME + '_train'
mkdir_folder = 'mkdir ' + output_folder_name
os.system(mkdir_folder)


# list of all the names of the input image files for the application
FILE_NAMES = [filename for filename in listdir(PATH_IMAGE_FILE) if isfile(join(PATH_IMAGE_FILE, filename))]
# FILE_NAMES = FILE_NAMES[0:3]

def create_csv_file():
    # for a custom filename to a csv file: "date_time.csv"
    # edit global variable "PATH_DATASET_FILE"
    global PATH_DATASET_FILE
    PATH_DATASET_FILE = PATH_DATASET_FILE + DATE_TIME + '.csv'
    # print(PATH_DATASET_FILE)
    with open(PATH_DATASET_FILE, 'w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['file_name', 'time_stamp', 'input_size', 'execution_time'])
# End of function create_csv_file()


def execute_input(filename):
    start = time.time()

    # command to run the bash script which contains docker instructions

    docker_command_arg_0 = PWD + '/scripts/docker_run.sh'
    docker_command_arg_1 = PATH_IMAGE_FILE + filename
    docker_command_arg_2 = filename
    docker_command_arg_3 = output_folder_name
    docker_command_arg_4 = 'ocr_output_' + filename

    docker_command = 'sh ' + docker_command_arg_0 + ' ' + docker_command_arg_1 + ' ' + docker_command_arg_2 + ' ' + docker_command_arg_3 + ' ' + docker_command_arg_4
    print(docker_command)
    
    # execute bash command using os.system
    os.system(docker_command)

    end = time.time()
    exec_time = end - start
    return exec_time
# End of function execute_input()


def data_collector():

    # start docker container    
    start_command = 'sh ' + PWD + '/scripts/docker_start.sh'
    os.system(start_command)

    t_start = time.time()

    # For each file name in the list, run the tesseract docker container 
    for filename in FILE_NAMES:
        PATH_WITH_FILENAME = PATH_IMAGE_FILE + filename

        # get input_size
        input_size = os.path.getsize(PATH_WITH_FILENAME)

        # note time stamp before starting the execution
        time_stamp = time.time()

        # invoke execute_input(file_name); get (execution_time) as return value
        execution_time = execute_input(filename)

        # finally, write (input_size, average_cpu_workload, execution_time) to the csv file
        row = [filename, time_stamp, input_size, execution_time]
        
        # Append the csv file with values
        with open(PATH_DATASET_FILE,'a') as csv_file:
            file_writer = csv.writer(csv_file)
            file_writer.writerow(row)
    
    # End of 'for loop' for 'execute_input'
    t_end = time.time()
    print(t_end - t_start)

    # stop docker container    
    stop_command = 'sh ' + PWD + '/scripts/docker_stop.sh'
    os.system(stop_command)

# End of function data_collector()


if __name__ == "__main__":
    create_csv_file()
    data_collector()