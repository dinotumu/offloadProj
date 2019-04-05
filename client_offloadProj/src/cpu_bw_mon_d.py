#!/usr/bin/python3

# imports
import time
import csv
import os

# constant for exponential moving average
ALPHA = 0.80

# Path to the files required by the program: Under the asssumption that PWD is offloadProj
PWD = os.getcwd()
PWD = PWD + '/client_offloadProj'
PATH_TO_FILE = PWD + '/data/input_files'
PATH_OCR_OUTPUT = PWD + '/data/output/'
PATH_TO_FILE_DIR = PWD + '/data/input/'
PATH_TO_CPUBWMON_CSV_FILE = PWD + '/data/cpu_bw_mon.csv'
PATH_TO_CPUBWMON_FILE = PWD + '/data/cpu_bw_mon.txt'

# initiate variables
last_idle = last_total = 0
start_cpu = 0 
start_bw = 0 


while True:

    start = time.time()

    # calculation of cpu utilization
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    cpu_utilization = 100.0 * (1.0 - idle_delta / total_delta)
        
    # calculation of average cpu utilization using ema
    if start_cpu==0 :
        cpu_ema = cpu_utilization
        start_cpu = 1

    current_cpu_util = cpu_utilization
    cpu_ema = ((current_cpu_util - cpu_ema) * ALPHA) + cpu_ema
    average_cpu_utilization = cpu_ema

    # calculation of bandwidth utilization
    with open('/proc/net/dev') as f:
        pass
    
    bw_utilization = 0
    
    
    # calculation of average bandwidth utilization using ema
    if start_bw==0 :
        bw_ema = bw_utilization
        start_bw = 1

    current_bw_util = bw_utilization
    bw_ema = ((current_bw_util - bw_ema) * ALPHA) + bw_ema
    average_bw_utilization = bw_ema
    
    
    
    timestamp = time.time()
    row = [timestamp, cpu_utilization, average_cpu_utilization, bw_utilization, average_bw_utilization]
    # write to the file(s)
    # write to csv file
    with open(PATH_TO_CPUBWMON_CSV_FILE,'a') as csv_file:
        file_writer = csv.writer(csv_file)
        file_writer.writerow(row)

    # write to avg_cpu_bw_now
    with open(PATH_TO_CPUBWMON_FILE, 'w') as cpubwmon:
        cpubwmon.write(row)
    

    end = time.time()
    exec_time = end - start
    time.sleep(1 - exec_time)