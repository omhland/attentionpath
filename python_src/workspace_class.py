# Workspace class
import timing_intervals
import os
from typing import TypedDict
from IPython import embed as e

class workspace_dict(TypedDict):
    title: str
    number: int
    commands: list
    layout: str

class workspace:
    """ A workspace maps to workspaces in i3. Each workspace can have a title,
    a number, a list of commands, a layout. The workspace will also contain
    information about when the workspace should be launched.
    """
    legal_commands =  ["layout", "number", "commands", "title", "timing"]

    __workspaces = []

    #TODO instances = [] -> init: self.append()
    #  https://stackoverflow.com/questions/12101958/how-to-keep-track-of-class-instances


    def __init__(self, keys=None, values=None):
        """ Initializes the workspace with the given keys and values.
        keys-> list of strings that represent the keys.
        values-> list of strings that represent the values.
        Both lists must be of the same length
        """
        self.timing = None
        self.attr = workspace_dict(title=None, number=None, commands=[], layout=None)

        self.__workspaces.append(self)

        if keys and values:
            assert len(keys) == len(values), "keys and values must be of same length"
            assert isinstance(keys, list), "keys must be a list"
            assert isinstance(values, list), "values must be a list"
            assert len(keys) == len(values)

            for key, value in zip(keys, values):
                self.set_attribute(key, value)



        # TODO add function lambdas for assesing if a workspace should launch

    def __add_title(self, title):
        """ Adds a title to the workspace.
        title-> string
        """
        if self.attr["title"] != None:
            raise ValueError(f"title already set to {self.attr['title']}")

        if isinstance(title, str):
            self.attr["title"] =  title
        else:
            raise ValueError("title must be a string")

    def __add_timing(self, input):
        self.timing = input

    def __add_command(self, command):
        """ Adds a command to the workspace.
        command-> string or list of strings
        """
        if isinstance(command, str):
            self.attr["commands"].append(command)
        elif isinstance(command, list):
            for c in command:
                assert c
                if isinstance(c, str) == False:
                    raise ValueError("command must be a string")
        else:
            raise ValueError("command must be a string or a list")

        self.attr["commands"].append(command)

    def __add_number(self, number):
        """ Adds a number to the workspace.
        number->  a string that represents the number of the workspace. The
        string must be numeric and without decimals. E.g. "1" or "2"
        """

        if self.attr["number"] != None:
            raise ValueError("number already set")

        if number.isnumeric():
            number = int(number)
            if int(number) != float(number):
                raise ValueError("number must be an integer")
            self.attr["number"] =  number
        else:
            raise ValueError("number must be numeric")

    def __add_layout(self, file_name):
        """ Adds a layout to the workspace.
        """
        if self.attr["layout"] != None:
            raise ValueError("layout already set")

        if isinstance(file_name, str) == False:
            raise ValueError("layout must be a string")
        # Check if file exists
        if os.path.isfile(file_name) == False:
            error_msg = f"The layout file called {file_name} does not exist"

            raise ValueError(error_msg)

        self.attr["layout"] =  file_name


    def __add_timing_interval(self, timing):
        """Adds a timing_intervals object to the class.
        timing-> timing_intervals object
        """
        if self.timing:
            raise ValueError("timing already set")
        if isinstance(timing, timing_intervals.timing_intervals):
            self.timing = timing
        else:
            raise ValueError('The timing input must be of type '
                             'timing_intervals')

    # Public functions

    def set_attribute(self, key, value):
        """ Assigns the value to the attribute given by key
        """
        assert isinstance(key, str)
        assert value
        if key == 'layout':
            self.__add_layout(value)
        elif key == 'number':
            self.__add_number(value)
        elif key == 'commands':
            self.__add_command(value)
        elif key == 'title':
            self.__add_title(value)
        else:
            error_msg = f"Illegal key input '{key}'. The key must be one of the following: {self.legal_commands}"
            raise ValueError(error_msg)
    def set_timing(self, weekdays, start_hour=None, end_hour=None,
                   start_minute=None, end_minute=None):
        """ Sets the timing of the workspace.
        weekdays-> list of strings that represent the weekdays.
        start_hour-> int that represents the start hour. (Optional)
        end_hour-> int that represents the end hour. (Optional)
        start_minute-> int that represents the start minute. (Optional)
        end_minute-> int that represents the end minute. (Optional)
        """

        if self.timing:
            raise ValueError("timing already set")

        self.timing = timing_intervals.timing_intervals( weekdays, start_hour,
                                            end_hour, start_minute, end_minute)



    def should_launch(self):
        """Returns true if the workspace should launch.
        Asses if timing is defined, if not-> Assume that the workspace
        is correctly timed
        """
        #TODO
        # Loop over function lambdas to asses if they should launch or not

        if self.timing:
            return self.timing.is_in_interval()
        else:
            print(self.attributes['title'])
            return True

    def get_attributes(self):
        """ Returns a dictionary of the workspace attributes.
        The dictionary will always return all attributs, but
        undefined attributes defaults to None
        """
        return self.attr

    @classmethod
    def get_workspaces(cls):
        return cls.__workspaces





