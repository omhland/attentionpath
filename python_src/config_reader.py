"""
input _ time hour, minute

create _

TODO Bug: The begining of the test.txt is broken. One comment is lost and the
begining of the first command is cut

"""

# FIXME BUG the command_strings are come in double pairs. This dosen't make any
#  sense
import datetime as dt
import os
from math import isnan, nan

from IPython import embed as e

import i3_interface as i3

from workspace_class import workspace as w_fix


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
            weekdays_raw = input.split(',')
            weekdays_input = [weekday_raw.strip().lower() for weekday_raw in weekdays_raw]
            self.current_ws.add_timing([self.weekdays.index(weekday) for weekday in weekdays_input])
            self.current_ws_fix.set_timing([self.weekdays.index(weekday) for weekday in weekdays_input])

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
workspaces, focus = reader.read_config(config_file)
current_focus =  {"que_number":nan}

command_strings = []
for workspace in w_fix.get_workspaces():
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

e()
#  TODO test from here
#  Simple test: Compare the text output from the new and the old versions
#  with open(command_file, "a") as output_file:

# TODO fix foucs stuff


#TODO most of the text bellow can and should be removed

# Find the current day TODO remove
current_weekday = dt.date.today().weekday()

# Find current time TODO remove
current_time = dt.datetime.now().time()





# Loop through workspaces
for workspace in workspaces:
    # Asses if the workspace should be executed today
    if (current_weekday in workspace.timing):
        command_strings_2 = i3.get_workspace_i3_commands(workspace.title, workspace.number,
                                                         workspace.commands, workspace.layout,
                                                         layout_file_location)
        with open(command_file, "a") as output_file:
            for command_string in command_strings_2:
                output_file.write(command_string)

        # Asses is in the focus que
        if workspace.number in focus:
            que_number = focus.index(workspace.number)
            #Asses if the workspace is first in the focus que
            if isnan(current_focus['que_number']) | (que_number < current_focus['que_number']):
               current_focus = {"workspace":workspace, "que_number":que_number}

if current_focus.get('que_number') is not None:
    with open(command_file, "a") as output_file:
        focus_command_str = i3.i3_set_focus(current_focus["workspace"])
        output_file.write(focus_command_str)



