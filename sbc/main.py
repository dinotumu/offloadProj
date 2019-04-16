#!/usr/bin/python3

import os



# define variables
PWD = os.getcwd() 
SBC_PWD = PWD + '/sbc'


PATH_TO_CPUBWMON_FILE = PWD + '/data/cpu_bw_mon_now.csv'







# start daemons on sbc


cpu_bw_daemon = "/usr/bin/python3 " + PWD + "/sbc/src/cpu_bw_mon_d.py &"

max_bw_daemon = "/usr/bin/python3 " + PWD + "/sbc/src/max_bw_mon_d.py &"


# print(PWD, SBC_PWD, cpu_bw_daemon, max_bw_daemon)




# start docker script on remote server

# ssh to remote server
# execute start docker script



# run sbc-only with workload i

# run remote-always with workload i

# run algorithm with workload i 



# stop docker script on remote server

# ssh to remote server
# execute start docker script




