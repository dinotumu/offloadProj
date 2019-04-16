#!/usr/bin/python3

# imports
import speedtest
import time
import csv
import os

# Path to the files required by the program: Under the asssumption that PWD is offloadProj
PWD = os.getcwd()
PWD = PWD + '/sbc'
# PATH_TO_MAXBWMON_CSV_FILE = PWD + '/data/max_bw_mon.csv'
PATH_TO_MAXBWMON_FILE = PWD + '/data/max_bw_mon_now.csv'

while True:
    start = time.time()

    # source = "192.168.1.100"
    # test = speedtest.Speedtest(source_address=source)
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    result = test.results.dict()

    # print(result['download'], result['upload'])

    rx = result['download']/8
    tx = result['upload']/8
    timestamp = time.time()
    row = [timestamp, rx, tx]

    # write to the file(s)
    # write to csv file
    # with open(PATH_TO_MAXBWMON_CSV_FILE,'a') as csv_file:
    #     file_writer = csv.writer(csv_file)
    #     file_writer.writerow(row)

    # write to max_bw_mon_now
    with open(PATH_TO_MAXBWMON_FILE, 'w') as maxbwmon:
        file_writer = csv.writer(maxbwmon)
        file_writer.writerow(row)
    
    print("cpu_bw_mon updated")

    end = time.time()
    # exec_time = end - start
    # print(exec_time)
    # time.sleep(1 - exec_time)
    time.sleep(120 - end + start)

# End of while loop