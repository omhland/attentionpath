# FIXME BUGS
# 1. Focus support has not been implemented


import datetime as dt
import os
from math import isnan, nan

from IPython import embed as e

import i3_interface as i3

from workspace_class import workspace as w_fix


def extract_time_string(input):
    """
    Extracts the time string from the input string.

        Parameters:
            input: a string in the form of "weekday_name_1, weekday_name_2 & HH:MM,HH:MM"

        Output:
            weekdays: a list of weekdays
            start_hour: an int that represents the start hour
            start_minute: an int that represents the start minute
            end_hour: an int that represents the end hour
            end_minute: an int that represents the end minute
    """
    assert (num_dividers:=input.count("&")) in [0, 1], "Error: The symbol & is not used correctly"
    has_time = bool(num_dividers)

    if has_time:
        weekdays_raw_string, time_raw = input.split('&')
        start_time, end_time = time_raw.split('-')

        start_hour, start_minute = start_time.split(':')
        end_hour, end_minute = end_time.split(':')

        # Convert the strings to ints
        start_hour = int(start_hour)
        start_minute = int(start_minute)
        end_hour = int(end_hour)
        end_minute = int(end_minute)

    else:
        weekdays_raw_string = input
        start_hour, start_minute = None, None
        end_hour, end_minute = None, None

    weekdays_raw = weekdays_raw_string.split(',')
    weekdays = [weekday_raw.strip().lower() for weekday_raw in weekdays_raw]

    return weekdays, start_hour, start_minute, end_hour, end_minute



class InputReader:
    """
    The InputReader class is used to read the input from the user.

    The class as will call the workspace class each time it finds a new
    workspace in the config file. The workspace will then be populated with new
    properties as they are found.
    """

    def __init__(self, layout_path="../layouts"):
        """ This function initializes the reading class.
            Parameters:
                layout_path: the path to the layouts
        """
        self.layout_path = layout_path
        self.workspaces = []
        self.num_workspaces = 0
        self.focus = float("nan")
        self.commands = ["{", "#", "-", "+", "@", "=", "}", ":", "_"]
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
        """ Assesses the incomming command either
        - creates a new workspace
        - assigns the command to a new
        input: a command in the form of a string
        """
        if command == '=':
            assert not w_fix.has_focus_que(), "Error: The focus queue is defined multiple times in the config."

            focus_que_raw = input.split(',')
            focus_que = [int(ws_num) for ws_num in focus_que_raw]
            w_fix.set_focus_que(focus_que)

        if command == '}':
            # Be aware of the potential for copy mistakes
            self.workspaces.append(self.current_ws)
        elif command == '{':
            self.current_ws = workspace()
            self.current_ws_fix = w_fix()
        elif command == '#':
            self.current_ws.add_title(input)
            self.current_ws_fix.set_attribute("title", input)
        elif command == ':':
            input = os.path.join(self.layout_path, input)
            self.current_ws.add_layout(input)
            self.current_ws_fix.set_attribute("layout", input)
        elif command == '@':
            extract_time_string(input)
            weekdays_raw = input.split(',')
            weekdays_input = [weekday_raw.strip().lower() for weekday_raw in weekdays_raw]



            # FIXME this should be removed
            #  self.current_ws.add_timing([self.weekdays.index(weekday) for weekday in weekdays_input])



            #  self.current_ws_fix.set_timing([self.weekdays.index(weekday) for weekday in weekdays_input])

            weekdays, start_hour, start_minute, end_hour, end_minute = extract_time_string(input)
            self.current_ws_fix.set_timing(weekdays, start_hour, start_minute, end_hour, end_minute)



        elif command == '-':
            self.current_ws.add_command(input)
            self.current_ws_fix.set_attribute("commands", input)
        elif command == '+':
            self.current_ws.add_number(int(input))
            self.current_ws_fix.set_attribute("number", input)
        elif command == '=':
            # Convert from written list to a list of ints
            focus_str = list(input.split(","))
            self.focus = [int(item) for item in focus_str]





class workspace:
    """ A workspace maps to workspaces in i3. Each workspace can have a title,
    a number, a list of commands, a layout. The workspace will also contain
    information about when the workspace should be launched.
    """
    attributes = {
            "title": "",
            "number": 1,
            "commands": [],
            "layout": None,
            "timing": [],
            }
    def __init__(self):
        #Setting some default values
        self.title = "No name"
        self.number = 1
        #Initializing empty command list
        self.commands = []
        self.layout = None

    def add_title(self, input):
        self.title = input
        self.attributes["title"] = input

    def add_timing(self, input):
        self.timing = input
        self.attributes["timing"] = input

    def add_command(self, input):
        self.commands.append(input)
        self.attributes["commands"] = input

    def add_number(self, input):
        self.number = input
        self.attributes["number"] = input

    def add_layout(self, input):
        self.layout = input
        self.attributes["layout"] = input


# Fetch directory name
dirname = os.path.dirname(os.path.realpath(__file__))
output_path = os.path.join(dirname, "bash_output")
parent = os.path.join(dirname, os.pardir)

# Fetch location of important files
config_file = os.path.join(parent, "config")
layout_file_location = os.path.join(parent, "layouts")


# Initialize and run reader
reader = InputReader(layout_file_location)
#FIXME workspaces does not need to be printed like this
workspaces, focus = reader.read_config(config_file)

# TODO current focus can be a class member of the workspace class
current_focus =  {"que_number":nan}


workspaces_to_launch, workspace_focus_id = w_fix.get_launchable_workspaces()

command_strings = []
for workspace in workspaces_to_launch:
    if workspace.should_launch():
        attr = workspace.get_attributes()
        title = attr['title']
        number = attr['number']
        commands = attr['commands']
        layout = attr['layout']
        command_strings.append(i3.get_workspace_i3_commands(title, number,
                                                            commands, layout,
                                                            layout_file_location))

# Find file for bash commands
command_file = os.path.join(output_path, "JUNE2022_test.txt")
with open(command_file, "w") as output_file:
    output_file.write(f'#This script was updated '
                      f'{dt.datetime.now().ctime()} \n\n')

    for command_string in command_strings:
        for string in command_string:
            output_file.write(string)

    #  if workspace_focus_id:
        #  focus_command_str = i3.i3_set_focus()
        #  output_file.write(focus_command_str)
