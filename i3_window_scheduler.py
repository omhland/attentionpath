#!/usr/bin/python3
### BEGIN INIT INFO
# Provides:          i3_window_scheduler.py
# Required-Start:    $all
# Required-Stop:     $remote_fs $syslog
# Default-Start:     3
# Default-Stop:            
# Short-Description: Start daemon at boot time
# Description:       Enables i3 window launcher 
### END INIT INFO


import os
import datetime
import sys

#dirname = os.path.dirname(__file__)
dirname = "/home/ole/config_files/i3_manager"
print(sys.path)
sys.path.insert(0, dirname)
print(sys.path)

import system_classes
#TODO: remove
#path = os.path.join(dirname, 'python_data/command_scheduler')
#os.remove(path)



scheduler = system_classes.command_scheduler()
scheduler.write_commands_to_file(dirname+'/last_boot')
executables_list = scheduler.update_and_execute()

command_file = os.path.join(dirname, "bash_commands.txt")
file = open(command_file, "w")
now = datetime.datetime.now()
file.write("#The last update of this script was " + now.ctime() + "\n")
for (i, executables) in enumerate(executables_list):
    comment = "#i3 command nr: " + (i+1).__str__()
    file.write(comment + "\n")
    for executable in executables:
        file.write(executable + "\n")

    file.write("sleep 0.9 \n \n")
file.close()
scheduler.write_commands_to_file(dirname)


#a = 'i3-msg \'exec "google-chrome-stable --new-window https://wikipedia.com"\''
#file.write(a + "\n")
