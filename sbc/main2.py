#!/usr/bin/python3

# imports
import os
import csv
import time
import datetime
import subprocess
from os import listdir
from os.path import isfile, join


# sbc variables
PWD = os.getcwd()
SBC_PWD = PWD + '/sbc'
PATH_SBC_OUTPUT = SBC_PWD + '/data/output/'
PATH_TO_CPUBWMON_FILE = SBC_PWD + '/data/cpu_bw_mon_now.csv'
PATH_TO_MAXBWMON_FILE = SBC_PWD + '/data/max_bw_mon_now.csv'
SBC_PREDICT = SBC_PWD + '/data/sbc_model.csv'

# remote variables
REMOTE_PREDICT = SBC_PWD + '/data/remote_model.csv'


# remote variables for ssh
REMOTE_SERVER_ADDRESS = '192.168.43.234'
REMOTE_USER_NAME = 'dinotumu'
REMOTE_PATH = '/home/' + REMOTE_USER_NAME + '/Documents/offloadProj/remote/'
REMOTE_INPUT_FILE_PATH = REMOTE_PATH + 'data/input/'
REMOTE_OUTPUT_FILE_PATH = REMOTE_PATH + 'data/output/'
TMP_SSH_DIR = str(subprocess.check_output('mktemp -d', shell=True))
TMP_SSH_DIR = TMP_SSH_DIR[2:len(TMP_SSH_DIR)-3]
PATH_SSH_CONFIG = TMP_SSH_DIR + '/ssh_config'
PATH_SSH_SOCKET = TMP_SSH_DIR + '/ssh_socket'


# Variables to store data
wl_sbc = []
wl_remote = []
wl_algo = []
total_time = []
workload_number = 1

# path to workload directory
PATH_WL_FOLDER = SBC_PWD + '/data/workloads/workload_' + str(workload_number)

# create input and output folders in remote server
now = datetime.datetime.now()
DATE_TIME = str(now.day) + '.' + str(now.month) + '.' + str(now.year) + '_' + str(now.hour) + '.' + str(now.minute) + '.' + str(now.second)


# Coefficients for SBC execution prediction time model
SBC_INTERCEPT = -0.4699124763 
SBC_COEFF_1 = 0.0000595278 # input_size
SBC_COEFF_2 = 0.0655410001 # average_cpu_workload

# Coefficients for remote execution prediction time model
R_INTERCEPT = 1.8309154981 
R_COEFF_1 = 0.0000420763 


















def start_docker():
    # start docker script on remote server
    # start_command = '"docker run -dt --cpus="4.0" --name tesseract-cn tesseract"'
    start_command = REMOTE_PATH + 'scripts/docker_start.sh'
    ssh_cmd = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + start_command
    os.system(ssh_cmd)

def stop_docker():
    # stop docker script on remote server
    # stop_command = '"docker stop tesseract-cn; docker rm tesseract-cn"'
    stop_command = REMOTE_PATH + 'scripts/docker_stop.sh'
    ssh_cmd = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + stop_command
    os.system(ssh_cmd)





def open_ssh_tunnel():
    open_ssh_command = 'sh ' + SBC_PWD + '/scripts/open_ssh_tunnel.sh' + ' ' + PATH_SSH_CONFIG + ' ' + PATH_SSH_SOCKET + ' ' + REMOTE_USER_NAME + ' ' + REMOTE_SERVER_ADDRESS
    os.system(open_ssh_command)

def close_ssh_tunnel():
    close_ssh_command = 'sh ' + SBC_PWD + '/scripts/close_ssh_tunnel.sh' + ' ' + PATH_SSH_CONFIG + ' ' + PATH_SSH_SOCKET + ' ' + REMOTE_SERVER_ADDRESS
    os.system(close_ssh_command)












def get_filenames():
    global PATH_WORKLOAD, FILE_NAMES, FILENAMES
    PATH_WORKLOAD = SBC_PWD + '/data/workloads/workload_' + str(workload_number) + '/'
    FILE_NAMES = [filename for filename in listdir(PATH_WORKLOAD) if isfile(join(PATH_WORKLOAD, filename))]
    FILENAMES = [filename for filename in listdir(PATH_WORKLOAD) if isfile(join(PATH_WORKLOAD, filename))]
    FILE_NAMES.sort()
    FILENAMES.sort()
    vaar = FILE_NAMES[9]
    FILENAMES.append(vaar)

def start_daemon():
    # start daemons on sbc
    cpu_bw_daemon = "/usr/bin/python3 " + PWD + "/sbc/src/cpu_bw_mon_d.py &"
    os.system(cpu_bw_daemon)

    # start bandwidth daemon
    max_bw_daemon = "/usr/bin/python3 " + PWD + "/sbc/src/max_bw_mon_d.py &"
    os.system(max_bw_daemon)





def sbc_only():
    # make output directories for 'SBC-Only case'
    sbc_output_folder_name = DATE_TIME + '_' + 'workload_' + str(workload_number)
    mkdir_sbc = 'mkdir ' + PATH_SBC_OUTPUT + sbc_output_folder_name
    # print(mkdir_sbc)
    os.system(mkdir_sbc)
    
    sbc_start = time.time()
    for filename in FILE_NAMES:
        tesseract_command = 'tesseract ' + PATH_WORKLOAD + filename + ' ' + PATH_SBC_OUTPUT + filename

        with open(PATH_TO_CPUBWMON_FILE) as cpu_mon:
            average_cpu_workload = float(cpu_mon.readline()[:-1].split(',')[2])

        start_task = time.time()
        os.system(tesseract_command)
        end_task = time.time()

        sbc_row = [average_cpu_workload, end_task - start_task]
        wl_sbc.append(sbc_row)

    sbc_end = time.time()
    print("SBC Only Time: ", sbc_end - sbc_start)

def remote_always():
    # make input and output directories for 'Remote-Always case'
    remote_folder_name = DATE_TIME + '_remote_' + 'workload_' + str(workload_number)
    mkdir_input_remote = 'mkdir ' + REMOTE_INPUT_FILE_PATH + remote_folder_name
    mkdir_output_remote = 'mkdir ' + REMOTE_OUTPUT_FILE_PATH + remote_folder_name
    ssh_mkdir_remote = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + '"' + mkdir_input_remote + '; ' + mkdir_output_remote + '"'
    # print(ssh_mkdir_remote)
    os.system(ssh_mkdir_remote)
    
    rem_start = time.time()

    for filename in FILENAMES:
        # set source and destination paths for scp command
        SOURCE_PATH = '"' + PATH_WL_FOLDER + '/' + filename + '"'
        DESTINATION_PATH = REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ':"' + REMOTE_INPUT_FILE_PATH + remote_folder_name + '"'
        
        # scp command to upload the input file in the remote server
        scp_cmd = 'scp -F "' + PATH_SSH_CONFIG + '" ' + SOURCE_PATH + ' ' + DESTINATION_PATH

        # arguments for the script file
        remote_docker_command_arg_0 = REMOTE_PATH + 'scripts/docker_run.sh'
        remote_docker_command_arg_1 = REMOTE_INPUT_FILE_PATH + remote_folder_name + '/' + filename
        remote_docker_command_arg_2 = filename
        remote_docker_command_arg_3 = REMOTE_OUTPUT_FILE_PATH + remote_folder_name + '/' 
        remote_docker_command_arg_4 = 'ocr_output_' + filename

        # docker run command with arguments
        remote_docker_command = '"sh ' + remote_docker_command_arg_0 + ' ' + remote_docker_command_arg_1 + ' '  + remote_docker_command_arg_2 + ' ' + remote_docker_command_arg_3 + ' ' + remote_docker_command_arg_4 + '"'
        
        # ssh command to run 'remote_docker_command' in the remote server
        ssh_cmd = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + remote_docker_command


        bw_start_time = time.time()
        os.system(scp_cmd)
        bw_end_time = time.time()

        remote_exec_start = time.time()
        os.system(ssh_cmd)
        remote_exec_end = time.time()


        remote_row = [bw_end_time - bw_start_time, remote_exec_end - remote_exec_start]
        # os.system(cd)
        wl_remote.append(remote_row)

    rem_end = time.time()
    print("Remote Execution Time: ", rem_end - rem_start)





def implemented_algo():
    # make input and output directories for 'Implemented-Algorithm case'
    algo_folder_name = DATE_TIME + '_algo_' + 'workload_' + str(workload_number)
    mkdir_input_algo = 'mkdir ' + REMOTE_INPUT_FILE_PATH + algo_folder_name
    mkdir_output_algo = 'mkdir ' + REMOTE_OUTPUT_FILE_PATH + algo_folder_name
    ssh_mkdir_algo = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + '"' + mkdir_input_algo + ';' + mkdir_output_algo + '"'
    # print(ssh_mkdir_algo)
    os.system(ssh_mkdir_algo)

    start_time = time.time()
    for filename in FILE_NAMES:
        
        # get input_size
        input_size = float(os.path.getsize(PATH_WL_FOLDER + '/' + filename))

        with open(PATH_TO_CPUBWMON_FILE) as cpu_mon:
            var = [float(i) for i in cpu_mon.readline()[:-1].split(',')]
            average_cpu_workload, up_bw_util = var[2], var[6]

        with open(PATH_TO_MAXBWMON_FILE) as bw_mon:
            up_max_bw = float(bw_mon.readline()[:-1].split(',')[2])


        SOURCE_PATH = '"' + PATH_WL_FOLDER + '/' + filename + '"'
        DESTINATION_PATH = REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ':"' + REMOTE_INPUT_FILE_PATH + algo_folder_name + '"'

        # scp command to upload the input file in the remote server
        scp_cmd = 'scp -F "' + PATH_SSH_CONFIG + '" ' + SOURCE_PATH + ' ' + DESTINATION_PATH

        # arguments for the script file
        remote_docker_command_arg_0 = REMOTE_PATH + 'scripts/docker_run.sh'
        remote_docker_command_arg_1 = REMOTE_INPUT_FILE_PATH + algo_folder_name + '/' + filename
        remote_docker_command_arg_2 = filename
        remote_docker_command_arg_3 = REMOTE_OUTPUT_FILE_PATH + algo_folder_name + '/' 
        remote_docker_command_arg_4 = 'ocr_output_' + filename

        # docker run command with arguments
        remote_docker_command = '"sh ' + remote_docker_command_arg_0 + ' ' + remote_docker_command_arg_1 + ' '  + remote_docker_command_arg_2 + ' ' + remote_docker_command_arg_3 + ' ' + remote_docker_command_arg_4 + '"'
        
        # ssh command to run 'remote_docker_command' in the remote server
        ssh_cmd = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + remote_docker_command





        t_sbc = SBC_COEFF_1 * input_size + SBC_COEFF_2 * average_cpu_workload + SBC_INTERCEPT
        t_remote = R_COEFF_1 * input_size + R_INTERCEPT
        t_upload = input_size/(up_max_bw - up_bw_util)

        # print(t_sbc, t_remote + t_upload)
        if (t_sbc > t_remote + t_upload):
            print("offloading " + filename)
            os.system(scp_cmd)
            os.system(ssh_cmd)
        
        else:
            print("executing " + filename + "locally")
            tesseract_command = 'tesseract ' + PATH_WORKLOAD + filename + ' ' + PATH_SBC_OUTPUT + filename
            os.system(tesseract_command)

    end_time = time.time()
    print("Implemented Algorithm Execution Time: ", end_time - start_time)
    # End of for loop


if __name__ == "__main__":
    # start background processes
    open_ssh_tunnel()
    start_docker()

    # execute workloads
    get_filenames()
    # sbc_only()
    remote_always()
    implemented_algo()

    # # stop background processes
    stop_docker()
    close_ssh_tunnel()

#     print(wl_sbc)
#     print(wl_remote)