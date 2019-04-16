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
PATH_TO_CPUBWMON_FILE = PWD + '/data/cpu_bw_mon_now.csv'

# initiate variables
# for cpu
last_idle = last_total = 0
# for bw
last_tx = last_rx = rx_delta = tx_delta = 0
# for avg cpu
start_cpu = 0
# for avg bw 
start_tx = start_rx = 0 

while True:
    start = time.time()

    # calculation of cpu utilization
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    cpu_utilization = 100.0 * (1.0 - idle_delta / total_delta)

    # calculation of bandwidth utilization
    with open('/proc/net/dev') as f:
        fields_bw = [int(column) for column in f.readlines()[2].strip().split()[1:]]
    now_rx, now_tx = fields_bw[0], fields_bw[8]
    if last_rx & last_tx:
        rx_delta, tx_delta = now_rx - last_rx, now_tx - last_tx
    last_rx, last_tx = now_rx, now_tx
    
    # calculation of average cpu utilization using ema
    if start_cpu==0 :
        cpu_ema = cpu_utilization
        start_cpu = 1
    current_cpu_util = cpu_utilization
    cpu_ema = ((current_cpu_util - cpu_ema) * ALPHA) + cpu_ema
    # average_cpu_utilization = cpu_ema
    
    # calculation of average bandwidth utilization (transmitted) using ema
    if start_tx==0 :
        tx_ema = tx_delta
        start_tx = 1

    # current_tx_util = tx_delta
    tx_ema = ((tx_delta - tx_ema) * ALPHA) + tx_ema
    # average_tx_utilization = tx_ema
    
    # calculation of average bandwidth utilization (received) using ema
    if start_rx==0 :
        rx_ema = tx_delta
        start_rx = 1

    # current_rx_util = rx_delta
    rx_ema = ((rx_delta - rx_ema) * ALPHA) + rx_ema
    # average_rx_utilization = rx_ema
    
    timestamp = time.time()
    # row = [timestamp, cpu_utilization, average_cpu_utilization, rx_delta, average_rx_utilization, tx_delta, average_tx_utilization]
    row = [timestamp, cpu_utilization, cpu_ema, rx_delta, rx_ema, tx_delta, tx_ema]

    
    # write to the file(s)
    # write to csv file
    with open(PATH_TO_CPUBWMON_CSV_FILE,'a') as csv_file:
        file_writer = csv.writer(csv_file)
        file_writer.writerow(row)

    # write to avg_cpu_bw_now
    with open(PATH_TO_CPUBWMON_FILE, 'w') as cpubwmon:
        file_writer = csv.writer(cpubwmon)
        file_writer.writerow(row)
    

    end = time.time()
    # exec_time = end - start
    # print(exec_time)
    # time.sleep(1 - exec_time)
    time.sleep(1 - end + start)