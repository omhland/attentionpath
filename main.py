import system_classes
import os
import datetime


dirname = os.path.dirname(__file__)

#TODO: remove
#path = os.path.join(dirname, 'python_data/command_scheduler')
#os.remove(path)


scheduler = system_classes.command_scheduler()

executables_list = scheduler.update_and_execute()

command_file = os.path.join(dirname, "bash_commands.txt")
file = open(command_file, "w")
now = datetime.datetime.now()
file.write("#The last execution of this script was " + now.ctime() + "\n")
for (i, executables) in enumerate(executables_list):
    comment = "#i3 command nr: " + (i+1).__str__()
    file.write(comment + "\n")
    for executable in executables:
        file.write(executable + "\n")

    file.write("sleep 0.9 \n \n")

file.close()
#a = 'i3-msg \'exec "google-chrome-stable --new-window https://wikipedia.com"\''
#file.write(a + "\n")
