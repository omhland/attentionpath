import datetime as dt
from math import isnan, nan
import os

class input_reader:
    def __init__(self):
        self.workspaces = []
        self.num_workspaces = 0
        self.focus = float("nan")
        self.commands = ["{", "#", "-", "+", "@", "=", "}", ":"]
        self.weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        # Default timing – the command will not activiate
        self.timing = -1

    def read_config(self, input_file):
        """Reads the config file line by line and sends them to the command 
        `handler` if the line contains a command.

        input_file: name of the config file
        """
        # Import config file and read lines
        config_file = open(input_file)
        lines = config_file.readlines()

        # Loop through lines
        for line in lines:
            # Extract information from the line 
            command = line[0]
            input = line[1:].strip()

            if self.is_command(command):
                #Handle new command
                self.handler(command, input)

        return self.workspaces, self.focus


    def is_command(self, command):
        if command in self.commands:
            return True
        else:
            return False

    def handler(self, command, input):
        if command == '}':
            # Be aware of the potential for copy mistakes
            self.workspaces.append(self.current_ws)
        elif command == '{':
            self.current_ws = workspace()
        elif command == '#':
            self.current_ws.add_title(input)
        elif command == ':':
            self.current_ws.add_layout(input)
        elif command == '@':
            weekdays_raw = input.split(',')
            weekdays_input = [weekday_raw.strip().lower() for weekday_raw in weekdays_raw]
            self.current_ws.add_timing([self.weekdays.index(weekday) for weekday in weekdays_input])

        elif command == '-':
            self.current_ws.add_command(input)
        elif command == '+':
            self.current_ws.add_number(int(input))
        elif command == '=':
            # Convert from written list to a list of ints
            focus_str = list(input.split(","))
            self.focus = [int(item) for item in focus_str]

class workspace:
    def __init__(self):
        #Setting some default values
        self.title = "No name"
        self.number = 1
        #Initializing empty command list
        self.commands = []
        self.layout = None

    def add_title(self, input):
        self.title = input

    def add_timing(self, input):
        self.timing = input

    def add_command(self, input):
        self.commands.append(input)

    def add_number(self, input):
        self.number = input

    def add_layout(self, input):
        self.layout = input

def i3_workspace_string(workspace):
    ws = "workspace " + workspace.number.__str__() + ":" + workspace.title
    return ws

def i3_set_focus(workspace):
    workspace_string = i3_workspace_string(workspace)
    return "#Set fouces " + os.linesep + "sleep 0.5" + os.linesep + i3_msg_creator([workspace_string])

def i3_msg_creator(commands):
    i3_msg = "i3-msg '"
    for command in commands:
        i3_msg = i3_msg + command + '; '
    return i3_msg + "'"

def i3_string_assembly(workspace, layout_file_location):
    #Assemble i3 executable strings
    workspace_string = i3_workspace_string(workspace)

    #Assemble list string commands 
    command_strings = [i3_msg_creator([workspace_string, "exec " + command]) for command in workspace.commands]


    if workspace.layout != None:
        layout_file_name = workspace.layout + ".json"
        layout_string = i3_msg_creator([workspace_string, "append_layout " + os.path.join(layout_file_location, layout_file_name)])
        command_strings.insert(0, layout_string)


    # Add a comment amound the strings
    comment = "#Assembling workspace named " + workspace.title

    # Add a sleep timer – this is required because i3 require some extra time for waiting between window lanuchers.
    # Future – add in extra sleep timing based on amount or windows, or similar. 
    i3_sleep_time = 1.2
    i3_sleep_string = "sleep " + i3_sleep_time.__str__()

    #Include comment and timer
    command_strings.insert(0, comment)
    command_strings.append(i3_sleep_string)
    # Inserting line endings
    command_strings = [string + os.linesep for string in command_strings]
    command_strings.insert(0, os.linesep)
    return command_strings



#Fetch directory name
dirname = os.path.dirname(os.path.realpath(__file__))

#Fetch location of important files
config_file = os.path.join(dirname, "config")
layout_file_location = os.path.join(dirname, "layouts")


#Initialize and run reader
reader = input_reader()
workspaces, focus = reader.read_config(config_file)
current_focus =  {"que_number":nan}

#Find file for bash commands 
command_file = "test.txt"
command_file = os.path.join(dirname, command_file)
#file = open(command_file, "w")
file = open(command_file, "w")
file.write("#The last update of this script was " + dt.datetime.now().ctime() + "\n")

#Find the current day
current_weekday = dt.date.today().weekday()

#Loop through workspaces 
for workspace in workspaces:
    #Asses if the workspace should be executed today
    if (current_weekday in workspace.timing):
        command_strings = i3_string_assembly(workspace, layout_file_location)
        for command_string in command_strings:
                file.write(command_string)

        #Asses is in the focus que
        if workspace.number in focus:
            que_number = focus.index(workspace.number)
            #Asses if the workspace is first in the focus que
            if isnan(current_focus['que_number']) | (que_number < current_focus['que_number']):
               current_focus = {"workspace":workspace, "que_number":que_number}

#Write focus command
if  not isnan(current_focus['que_number']):
    file.write(i3_set_focus(current_focus["workspace"]))

file.close()

