#!/usr/bin/python3

import os
import time
from os import listdir
from os.path import isfile, join

# define variables
PWD = os.getcwd()
SBC_PWD = PWD + '/sbc'
PATH_OCR_OUTPUT = SBC_PWD + '/data/ocr_output/'
PATH_TO_CPUBWMON_FILE = SBC_PWD + '/data/cpu_bw_mon_now.csv'
PATH_TO_MAXBWMON_FILE = SBC_PWD + '/data/max_bw_mon_now.csv'






def start_daemon():
    # start daemons on sbc
    cpu_bw_daemon = "/usr/bin/python3 " + PWD + "/sbc/src/cpu_bw_mon_d.py &"
    os.system(cpu_bw_daemon)
    max_bw_daemon = "/usr/bin/python3 " + PWD + "/sbc/src/max_bw_mon_d.py &"
    os.system(max_bw_daemon)
    # print(PWD, SBC_PWD, cpu_bw_daemon, max_bw_daemon)


def get_filenames(workload_number):
    global PATH_WORKLOAD, FILE_NAMES
    PATH_WORKLOAD = SBC_PWD + '/data/workloads/workload_' + str(workload_number) + '/'
    # print(PATH_WORKLOAD)
    FILE_NAMES = [filename for filename in listdir(PATH_WORKLOAD) if isfile(join(PATH_WORKLOAD, filename))]
    FILE_NAMES.sort()
    # print(FILE_NAMES)


def start_docker():
    # start docker script on remote server
    # ssh to remote server



    # execute start docker script
    start_command = 'docker run -dt --cpus="4.0" --name tesseract-cn tesseract'
    os.system(start_command)


def stop_docker():
    # stop docker script on remote server
    # ssh to remote server


    # execute start docker script
    stop_command = 'docker stop tesseract-cn; docker rm tesseract-cn'
    os.system(stop_command)


def sbc_execution():
    pass


def remote_execution():
    pass


def decision_engine():
    pass


def execute_workload():

    # print(PATH_WORKLOAD)
    # print(FILE_NAMES)

    # run sbc-only
    sbc_start = time.time()

    for filename in FILE_NAMES:
        tesseract_command = 'tesseract ' + PATH_WORKLOAD + filename + ' ' + PATH_OCR_OUTPUT + filename
        os.system(tesseract_command)

    sbc_end = time.time()
    sbc_time = sbc_end - sbc_start


    # run remote-always
    remote_start = time.time()

    for filename in FILE_NAMES:

        # send input file to remote server # execute using tesseract in the docker # get the output back
        remote_run_command = 'sh ' + SBC_PWD + '/scripts/run.sh'
        os.system(remote_run_command)

        # tesseract_command = 'tesseract ' + PATH_WORKLOAD + filename + ' ' + PATH_OCR_OUTPUT + filename
        # os.system(tesseract_command)

    remote_end = time.time()
    remote_time = remote_end - remote_start

    # run algorithm
    de_start = time.time()


    de_end = time.time()
    de_time = de_end - de_start






    # print observations
    print("SBC-only: ", sbc_time)
    print("Remote-always: ", remote_time)
    print("Using implemented algorithm: ", de_time)

if __name__ == "__main__":
    # start_daemons()
    # start_docker()

    for workload_number in range(1,4):
        get_filenames(workload_number)
        execute_workload()
    
    # stop_docker()
    # generate_test_summary()