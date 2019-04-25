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
# print(TMP_SSH_DIR, PATH_SSH_CONFIG, PATH_SSH_SOCKET)


# Variables to store data
wl_sbc = []
wl_remote = []
wl_algo = []
total_time = []

##################################################################################################################

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


##################################################################################################################



def start_docker():
    # start docker script on remote server
    # start_command = '"docker run -dt --cpus="4.0" --name tesseract-cn tesseract"'
    start_command = REMOTE_PATH + 'scripts/docker_start.sh'
    ssh_cmd = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + start_command
    os.system(ssh_cmd)

def stop_docker():
    # Try running a command on container
    # try_command = 'docker exec -t tesseract-cn "touch /home/app/dino.txt"'
    # try_cmd = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + try_command
    try2_command = 'docker exec -t tesseract-cn "ls /home/app"'
    try2_cmd = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + try2_command
    # os.system(try_cmd)
    os.system(try2_cmd)

    # stop docker script on remote server
    stop_command = '"docker stop tesseract-cn; docker rm tesseract-cn"'
    # stop_command = REMOTE_PATH + 'scripts/docker_stop.sh'
    ssh_cmd = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + stop_command
    os.system(ssh_cmd)




##################################################################################################################


def open_ssh_tunnel():
    open_ssh_command = 'sh ' + SBC_PWD + '/scripts/open_ssh_tunnel.sh' + ' ' + PATH_SSH_CONFIG + ' ' + PATH_SSH_SOCKET + ' ' + REMOTE_USER_NAME + ' ' + REMOTE_SERVER_ADDRESS
    os.system(open_ssh_command)

def close_ssh_tunnel():

    # exec_command = '"ls -al; ls -al /root/offloadProj"'
    # ssh_cmd = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + exec_command
      
    # SOURCE_PATH = '"/home/dinotumu/Downloads/Final.pdf"'
    # DESTINATION_PATH = REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ':"/root/"'
    # scp_cmd = 'scp -F "' + PATH_SSH_CONFIG + '" ' + SOURCE_PATH + ' ' + DESTINATION_PATH
    # os.system(scp_cmd)

    close_ssh_command = 'sh ' + SBC_PWD + '/scripts/close_ssh_tunnel.sh' + ' ' + PATH_SSH_CONFIG + ' ' + PATH_SSH_SOCKET + ' ' + REMOTE_SERVER_ADDRESS
    os.system(close_ssh_command)


##################################################################################################################


def execute_workload(workload_number):

    # define workload specific variables

    # path to workload directory
    PATH_WL_FOLDER = SBC_PWD + '/data/workloads/workload_' + str(workload_number)

    # create input and output folders in remote server
    now = datetime.datetime.now()
    DATE_TIME = str(now.day) + '.' + str(now.month) + '.' + str(now.year) + '_' + str(now.hour) + '.' + str(now.minute) + '.' + str(now.second)

    # make output directories for 'SBC-Only case'
    sbc_output_folder_name = DATE_TIME + '_' + 'workload_' + str(workload_number)
    mkdir_sbc = 'mkdir ' + PATH_SBC_OUTPUT + sbc_output_folder_name
    # print(mkdir_sbc)
    os.system(mkdir_sbc)
    
    # make input and output directories for 'Remote-Always case'
    remote_folder_name = DATE_TIME + '_remote_' + 'workload_' + str(workload_number)
    mkdir_input_remote = 'mkdir ' + REMOTE_INPUT_FILE_PATH + remote_folder_name
    mkdir_output_remote = 'mkdir ' + REMOTE_OUTPUT_FILE_PATH + remote_folder_name
    ssh_mkdir_remote = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + '"' + mkdir_input_remote + '; ' + mkdir_output_remote + '"'
    # print(ssh_mkdir_remote)
    os.system(ssh_mkdir_remote)

    # make input and output directories for 'Implemented-Algorithm case'
    algo_folder_name = DATE_TIME + '_algo_' + 'workload_' + str(workload_number)
    mkdir_input_algo = 'mkdir ' + REMOTE_INPUT_FILE_PATH + algo_folder_name
    mkdir_output_algo = 'mkdir ' + REMOTE_OUTPUT_FILE_PATH + algo_folder_name
    ssh_mkdir_algo = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + '"' + mkdir_input_algo + ';' + mkdir_output_algo + '"'
    # print(ssh_mkdir_algo)
    os.system(ssh_mkdir_algo)

    # # 
    # # run sbc-only: start
    # # 
    # sbc_start = time.time()

    # for filename in FILE_NAMES:
    #     tesseract_command = 'tesseract ' + PATH_WORKLOAD + filename + ' ' + PATH_SBC_OUTPUT + filename
    #     st_task = time.time()
    #     os.system(tesseract_command)
    #     # print(workload_number, filename)
    #     ed_task = time.time()

    #     wl_sbc.append(ed_task - st_task)

    # sbc_end = time.time()
    # sbc_time = sbc_end - sbc_start
    # total_time.append(sbc_time)	
    # # 
    # # run sbc-only: end
    # # 


    # # 
    # # run remote-always: start
    # # 
    # remote_start = time.time()
    # for filename in FILE_NAMES:

    #     # set source and destination paths for scp command
    #     SOURCE_PATH = '"' + PATH_WL_FOLDER + '/' + filename + '"'
    #     DESTINATION_PATH = REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ':"' + REMOTE_INPUT_FILE_PATH + remote_folder_name + '"'
        
    #     # scp command to upload the input file in the remote server
    #     scp_cmd = 'scp -F "' + PATH_SSH_CONFIG + '" ' + SOURCE_PATH + ' ' + DESTINATION_PATH
    #     # print(scp_cmd)

    #     bw_start_time = time.time()
    #     os.system(scp_cmd)
    #     bw_end_time = time.time()

    #     # arguments for the script file
    #     remote_docker_command_arg_0 = REMOTE_PATH + 'scripts/docker_run.sh'
    #     remote_docker_command_arg_1 = REMOTE_INPUT_FILE_PATH + remote_folder_name + '/' + filename
    #     remote_docker_command_arg_2 = filename
    #     remote_docker_command_arg_3 = REMOTE_OUTPUT_FILE_PATH + remote_folder_name + '/' 
    #     remote_docker_command_arg_4 = 'ocr_output_' + filename

    #     # docker run command with arguments
    #     remote_docker_command = '"sh ' + remote_docker_command_arg_0 + ' ' + remote_docker_command_arg_1 + ' '  + remote_docker_command_arg_2 + ' ' + remote_docker_command_arg_3 + ' ' + remote_docker_command_arg_4 + '"'
        
    #     # ssh command to run 'remote_docker_command' in the remote server
    #     ssh_cmd = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + remote_docker_command
    #     # print(ssh_cmd)
    #     remote_exec_start = time.time()
    #     os.system(ssh_cmd)
    #     remote_exec_end = time.time()
    #     wl_remote.append((bw_end_time - bw_start_time) + (remote_exec_end - remote_exec_start))
    # remote_end = time.time()
    # remote_time = remote_end - remote_start
    # total_time.append(remote_time)	
    # # 
    # # run remote-always: end
    # # 


    # 
    # run algo: start
    # 
    de_start = time.time()
    for filename in FILE_NAMES:
        # get input_size
        input_size = float(os.path.getsize(PATH_WL_FOLDER + '/' + filename))

        # t_sbc
        with open(SBC_PREDICT) as sbc:
            coeff1, coeff2, coeff3 = [float(i) for i in sbc.readline()[:-1].split(',')]

        with open(PATH_TO_CPUBWMON_FILE) as cpu_mon:
            var = [float(i) for i in cpu_mon.readline()[:-1].split(',')]
            average_cpu_workload, up_bw_util = var[2], var[6]

        t_sbc = coeff1 * average_cpu_workload + coeff2 * input_size + coeff3

        # t_remote
        with open(REMOTE_PREDICT) as remote:
            r_coeff1, r_coeff2 = [float(i) for i in remote.readline()[:-1].split(',')]

        t_remote = r_coeff1 * input_size + r_coeff2

        # t_upload
        with open(PATH_TO_MAXBWMON_FILE) as bw_mon:
            up_max_bw = float(bw_mon.readline()[:-1].split(',')[2])

        t_upload = input_size/(up_max_bw - up_bw_util)
        print(t_sbc, t_remote, t_upload)

        if (t_sbc > t_remote + t_upload):
            print("executing " + filename + "here")
            tesseract_command = 'tesseract ' + PATH_WORKLOAD + filename + ' ' + PATH_SBC_OUTPUT + filename
            os.system(tesseract_command)
        else:
            print("offloading " + filename)
            SOURCE_PATH = '"' + PATH_WL_FOLDER + '/' + filename + '"'
            DESTINATION_PATH = REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ':"' + REMOTE_INPUT_FILE_PATH + remote_folder_name + '"'

            # scp command to upload the input file in the remote server
            scp_cmd = 'scp -F "' + PATH_SSH_CONFIG + '" ' + SOURCE_PATH + ' ' + DESTINATION_PATH
            # print(scp_cmd)
            os.system(scp_cmd)


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
            # print(ssh_cmd)
            os.system(ssh_cmd)


    de_end = time.time()
    de_time = de_end - de_start
    # 
    # run algo: end
    # 

    # print observations
    # print("SBC-only: ", sbc_time)
    # print("Remote-always: ", remote_time)
    print("Using implemented algorithm: ", de_time)

if __name__ == "__main__":



    # # start background processes
    # # start_daemon()
    # open_ssh_tunnel()
    # start_docker()

    # # execute workloads
    # # for workload_number in range(1,2):
    workload_number = 1
    get_filenames(workload_number)
    execute_workload(workload_number)

    # # stop background processes
    # stop_docker()
    # close_ssh_tunnel()


    # print(wl_sbc)
    # print(wl_remote)