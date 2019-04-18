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


# remote variables for ssh
REMOTE_SERVER_ADDRESS = '192.168.0.80'
REMOTE_USER_NAME = 'dinotumu'
REMOTE_PATH = '/home/' + REMOTE_USER_NAME + '/Documents/offloadProj/remote/'
REMOTE_INPUT_FILE_PATH = REMOTE_PATH + 'data/input/'
REMOTE_OUTPUT_FILE_PATH = REMOTE_PATH + 'data/output/'

# HOST_PATH=/home/dinotumu/Documents/offloadProj/sbc/data/workloads/workload_1/10.png # the second script argument


TMP_SSH_DIR = str(subprocess.check_output('mktemp -d', shell=True))
TMP_SSH_DIR = TMP_SSH_DIR[2:len(TMP_SSH_DIR)-3]
PATH_SSH_CONFIG = TMP_SSH_DIR + '/ssh_config'
PATH_SSH_SOCKET = TMP_SSH_DIR + '/ssh_socket'

# print(TMP_SSH_DIR, PATH_SSH_CONFIG, PATH_SSH_SOCKET)







wl_sbc_all = []
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
    # print(FILE_NAMES)



##################################################################################################################



def start_docker():
    # start docker script on remote server
    start_command = '"docker run -i --cpus="4.0" --name tesseract-cn tesseract"'
    ssh_cmd = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + start_command
    os.system(ssh_cmd)

def stop_docker():
    # stop docker script on remote server
    stop_command = '"docker stop tesseract-cn; docker rm tesseract-cn"'
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
    # sbc_output_folder_name = DATE_TIME + '_' + 'workload_' + str(workload_number)
    # mkdir_sbc = 'mkdir ' + PATH_SBC_OUTPUT + sbc_output_folder_name
    # print(mkdir_sbc)
    # os.system(mkdir_sbc)
    
    # make input and output directories for 'Remote-Always case'
    remote_folder_name = DATE_TIME + '_remote_' + 'workload_' + str(workload_number)
    mkdir_input_remote = 'mkdir ' + REMOTE_INPUT_FILE_PATH + remote_folder_name
    mkdir_output_remote = 'mkdir ' + REMOTE_OUTPUT_FILE_PATH + remote_folder_name
    ssh_mkdir_remote = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + '"' + mkdir_input_remote + '; ' + mkdir_output_remote + '"'
    # print(ssh_mkdir_remote)
    os.system(ssh_mkdir_remote)

    # make input and output directories for 'Implemented-Algorithm case'
    # algo_folder_name = DATE_TIME + '_algo_' + 'workload_' + str(workload_number)
    # mkdir_input_algo = 'mkdir ' + REMOTE_INPUT_FILE_PATH + algo_folder_name
    # mkdir_output_algo = 'mkdir ' + REMOTE_OUTPUT_FILE_PATH + algo_folder_name
    # ssh_mkdir_algo = 'ssh -F "'+ PATH_SSH_CONFIG +'" ' + REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ' -T ' + '"' + mkdir_input_algo + ';' + mkdir_output_algo + '"'
    # print(ssh_mkdir_algo)
    # os.system(ssh_mkdir_algo)



    wl_sbc = []
    wl_remote = []
    wl_algo = []


    # 
    # run sbc-only: start
    # 
    # sbc_start = time.time()

    # for filename in FILE_NAMES:
    #     tesseract_command = 'tesseract ' + PATH_WORKLOAD + filename + ' ' + PATH_OCR_OUTPUT + filename
    #     st_task = time.time()
    #     os.system(tesseract_command)
    #     # print(workload_number, filename)
    #     ed_task = time.time()

    #     wl_sbc.append(ed_task - st_task)
    #     # wl.append(filename)

    # sbc_end = time.time()
    # sbc_time = sbc_end - sbc_start
    # wl_sbc_all.append(wl_sbc)
    # total_time.append(sbc_time)	
    # 
    # run sbc-only: end
    # 






    # 
    # run remote-always: start
    # 
    remote_start = time.time()
    for filename in FILE_NAMES:

        # set source and destination paths for scp command
        SOURCE_PATH = '"' + PATH_WL_FOLDER + '/' + filename + '"'
        DESTINATION_PATH = REMOTE_USER_NAME + '@' + REMOTE_SERVER_ADDRESS + ':"' + REMOTE_INPUT_FILE_PATH + remote_folder_name + '"'

        # scp command to upload the input file in the remote server
        scp_cmd = 'scp -F "' + PATH_SSH_CONFIG + '" ' + SOURCE_PATH + ' ' + DESTINATION_PATH
        # print(scp_cmd)
        os.system(scp_cmd)


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
        # print(ssh_cmd)
        os.system(ssh_cmd)

    remote_end = time.time()
    remote_time = remote_end - remote_start
    # 
    # run remote-always: end
    # 






    # 
    # run algo: start
    # 

    # de_start = time.time()


    # de_end = time.time()
    # de_time = de_end - de_start

    # 
    # run algo: end
    # 





    # print observations
    # print("SBC-only: ", sbc_time)
    print("Remote-always: ", remote_time)
    # print("Using implemented algorithm: ", de_time)




if __name__ == "__main__":
    # start background processes
    # start_daemon()


    open_ssh_tunnel()
    start_docker()


    # execute workloads
    for workload_number in range(1,2):
        get_filenames(workload_number)
        execute_workload(workload_number)



    # stop background processes
    stop_docker()
    close_ssh_tunnel()



    # write experiment data to csv file
    # with open('text.csv','a') as csv_file:
    #     file_writer = csv.writer(csv_file)
    #     file_writer.writerow(wl_sbc_all[0])
    #     file_writer.writerow(wl_sbc_all[1])
    #     #file_writer.writerow(wl_sbc_all[2])
    #     file_writer.writerow(total_time)

    # generate_test_summary()
