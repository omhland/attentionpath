import pickle
import datetime as dt
import numpy as np
import os
import timing_manager as tm


class command_scheduler:
    def __init__(self):
        #Attempt to load existing commands
        self.cmds_memory_file = absolute_path("python_data/command_scheduler")
        try:
            self.commands = self.load_commands()
        except:
            #Run scripts to intialize the standard commands 
            dirname = os.path.dirname(__file__)
            prc_file = os.path.join(dirname, "python_data/procedures.py")
            com_file = os.path.join(dirname, "python_data/commands.py")

            exec(open(prc_file).read())
            exec(open(com_file).read())
            self.commands = commands
            print("exception")

        pause = 1

    def update_and_execute(self):
        executables = []
        command_mask = np.zeros(len(self.commands))
        #Loop through commands and determine if they should be executed
        for (i, command) in enumerate(self.commands):
            if command.decision():
                command_mask[i] = 1
                executables.append(command.strings)
        self.save_classes()

        #Save the updated classes to memory

        workspace_string = self.workspace_string(command_mask)
        #Put the new string in a list and append
        executables.append([workspace_string])
        return executables


    ## Functions for loading and storing
    def load_commands(self):
        # Load commands from prior update
        with open(self.cmds_memory_file, 'rb') as file:
            commands = commands_dict = pickle.load(file)
        return commands

    def save_classes(self):
    # Save commands after update
        with open(self.cmds_memory_file, 'wb') as file:
            pickle.dump(self.commands, file)

    ## Functions for debugging
    def debug_function(self):
        #Usefull studying values during the execution
        self.names = [com.ws_name for com in self.commands]
        self.timings = [com.timing_manager for com in self.commands]
        self.periods = [ti.period_length for ti in self.timings]
        self.boots = [ti.last_boot for ti in self.timings]
        self.num_boots = [ti.num_boots_today for ti in self.timings]
        print(self.names)
        print(self.num_boots)


    ## Create workspace string
    def workspace_string(self, mask):
        #Find workspace to focus on
        ws_num, ws_name = self.choose_workspace_focus(mask)
        #assmbeling i3-msg
        i3_string = "i3-msg 'workspace " + ws_num.__str__() + ":" + ws_name + "'"
        return i3_string

    ## Function for handeling workspaces
    def choose_workspace_focus(self, mask):
        #Determine witch workspace to focus on (in case of conflict)
        #TODO: The algorithm assumes that no workspaces have number conflicts

        #Load workspace data into lists
        workspaces_numbers = [com.ws_num for com in self.commands]
        workspaces_focus = [com.ws_focus for com in self.commands]
        wss_name = [com.ws_name for com in self.commands]
        #Make numpy arrays
        wss_num = np.array(workspaces_numbers, dtype=int)
        wss_focus = np.array(workspaces_focus, dtype=int)
        #Mask out values 
        masked =  wss_num*wss_focus*mask
        #Find focus cadidate with the highest score
        if np.any(masked):
            arg = masked.argmax()
            ws_num = wss_num[arg]
            ws_name = wss_name[arg]
        else:
            #Choose the 'unfocused' workspace with the highest ws number
            arg = (wss_num*mask).argmax()
            ws_num = wss_num[arg]
            ws_name = wss_name[arg]

        return ws_num, ws_name

    ### Editor commands 
    def editor(self):
        print("Welcome to the command editor. Please choose one of the following options.")
        options = [command.ws_name for command in self.commands]
        options.append("Add new command")

        for (i, option) in enumerate(options):
            print(i.__str__() + ": " + option)

        usr_input = int(input("Insert number (1-" + i.__str__() + "): "))

        if usr_input == i:
            self.add_new_command()
        elif (usr_input >= 1) & (usr_input < i):
            self.edit_command(usr_input)
        else:
            print("invalid input")


    def add_new_command(self):
            print("\nCreating new command \n")
            #self.add_command()

            new_command = self.take_user_input()

            save = input("Would you like to save the new command? [y/n]")
            if save.casefold() == 'y'.casefold():
                self.commands.append(new_command)
                self.save_classes()

            # Input command procedures...


    def edit_command(self, command_num):
        print('\nEditing command\n')
        print('0: Edit command \n1: Activate/deactivate command NOTE: Note made yet\n2. Delete command')
        usr_input = int(input('Enter action (0-2): '))
        #Edit command
        if usr_input == 0:
            print("These are the existing commands")
            varnames = command_class.__init__.__code__.co_varnames
            #Remove 'self' from list
            variables = varnames[1:]
            print(command_num)
            self.print_existing(variables, slice(command_num, command_num+1))

            edited_command = self.take_user_input()

            save = input("Would you like to save the new command? [y/n]")
            if save.casefold() == 'y'.casefold():
                self.commands[command_num] = edited_command
                self.save_classes()

        #Activate command
        elif usr_input == 1:
            activate = 1
        #Delete command
        elif usr_input == 2:
            delete = input('Are you sure you want to delete? [y/n]')
            if delete.casefold() == 'y'.casefold():
                self.commands.pop(command_num)
                self.save_classes()



    def take_user_input(self):
        #Variables that needs to be defined by the user
        varnames = command_class.__init__.__code__.co_varnames
        #Remove 'self' from list
        variables = varnames[1:]
        #Number of existing commands
        num_commands = len(self.commands)

        #Determine if the users wants to look at other classes for inspiration
        show_comp = True if 'y'.casefold() == input("Would you like to see properties of existing commands? [y/n] ") else False
        if show_comp :
            num_commands = len(self.commands)
            usr_input = int(input("To see all commands, type 0\nTo see a specific command, type its number (1-" + str(num_commands) + ")\n"))
            #Slice used to accsess one or all the commands
            var_slice = slice(0,-1) if usr_input == 0 else slice(usr_input-1, usr_input)

        #Determine if the user wants explonations of the variables
        show_explonation = True if input("Would you like to see the the property explonations when choosing? yes, no [y/n] ").casefold()=='y'.casefold() else False

        #List to store user input
        print(variables)
        input_vars = len(variables) * [None]
        #Loop through variables
        for (j,var) in enumerate(variables):
            if show_explonation:
                print(var + ': ' + property_explonations[var])
            if show_comp:
                self.print_existing([var], var_slice)
            type = property_type[var]
            if type == 'list':
                property_list = []

                while True:
                    property_list.append(input(var + "="))
                    if (input("Add another element?[y/n]")=='n'.casefold()):
                        break
                input_vars[j] = property_list
            elif type=='int':
                input_vars[j] = int(input(var + "="))
            elif type=='string':
                input_vars[j] = input(var + "=")
        print(input_vars)
        return command_class(*input_vars)


    def print_existing(self, vars, index=slice(0,-1)):
        #a = str(exec("command.%s" % (var))
        commands = self.commands[index]
        print(commands)
        for (i, command) in enumerate(commands, start=1):
            for var in vars:
                command_var = (command.__dict__[var])
                #print(command_var)

                if isinstance(command_var, list):
                    print(i.__str__() + ": " + command.ws_name + "." + var + "=" )
                    for item in command_var:
                        print(" " + str(item))
                else:
                    print(i.__str__() + ": " + command.ws_name + "." + var + "=" + str(command_var))


    def write_commands_to_file(self, directory):
        commands = self.load_commands()
        # read a list of lines into data
        cmnd_str = ["### \n#Commands overview " + dt.datetime.today().ctime() + " \n### \n",]
        tmg_str = ["### \n#Command timing overview \n### \n",]
        for (i, command) in enumerate(self.commands):
            command_data, timing_data = command.return_information_strings()
            new_cmnd_str, new_tmg_str = self.write_command_info(i, command_data, timing_data)
            cmnd_str = cmnd_str + new_cmnd_str
            tmg_str = tmg_str + new_tmg_str

        text_directory = directory + "/info_text_files/"
        filepath = text_directory + "commands.txt"
        with open(filepath, 'w') as file:
            file.writelines(cmnd_str)
            file.close()

        filepath = text_directory + "timing.txt"
        with open(filepath, 'w') as file:
            file.writelines(tmg_str)
            file.close()

        filepath = text_directory + "test.txt"
        str = 'Executed at ' + dt.datetime.now().ctime() + '\n'
        with open(filepath, 'a') as file:
            file.writelines(str)
            file.close()

    def write_command_info(self, command_num, command_data, timing_data):

            #Loop through procedures
            procedures = command_data.pop("command_procedures")
            command_data_str = ["\n \n####Command " + command_num.__str__() + ": " + command_data["ws_name"] + " \n",]
            command_data_str.append("#Command data\n")
            command_data_str.append("command_procedures=[ \n")
            current_line = 1
            for (i, procedure) in enumerate(procedures, start=current_line):
                command_data_str.append("   " + procedure + ",\n")
            command_data_str.append("]\n")
            current_line = i+1

            #Loop over command data
            keys = command_data.keys()
            values = command_data.values()
            for i, (key, value) in enumerate(zip(keys, values), start=current_line):
                command_data_str.append(key + "=" + value + "\n")

            timing_data_str = ["\n \n####Command " + command_num.__str__() + ": " + command_data["ws_name"] + " \n",]

            #Loop over timing data 
            keys = timing_data.keys()
            values = timing_data.values()
            timing_data_str.append("#Timing_data\n")
            for i, (key, value) in enumerate(zip(keys, values), start=current_line):
                timing_data_str.append(key + "=" + value + "\n")

            return command_data_str, timing_data_str



global property_explonations
property_explonations = {
    "command_procedures": 'Type: List of strings. These are the commands that are executed by i3',
    "ws_name": 'Type: String. The name of the workspace',
    "ws_num": 'Type: Int. The workspace number',
    "ws_focus": 'Type: Int (0 or 1) (Default=False). Should the workspace be focused when launched',
    "period_length": 'Type: Int>0. Frequency (in terms of days) that the command should launch',
    "timing_string": 'Type: String. Timing information of the string', #TODO: FIx
    "start": 'Type: Int>0. In how many days from now should this command start executing. Note: buggy'
}
global property_type
property_type = {
    "command_procedures": 'list',
    "ws_name": 'string',
    "ws_num": 'int',
    "ws_focus": 'int',
    "period_length": 'int',
    "timing_string": 'string',
    "start": 'int'
}
class command_class:
    # This is a skeleton class for different command_class
    def __init__(self, command_procedures, ws_name, ws_num, period_length, timing_string, start=0, ws_focus=False):

        self.command_procedures = command_procedures; self.ws_name = ws_name; self.ws_num = ws_num; self.ws_focus = ws_focus
        #Store timing decisions in timing class (for creation purposes)
        self.period_length = period_length; self.timing_string = timing_string; self.start = start

        #Store timing decisions in timing class
        self.timing_manager = tm.timing_manager(period_length, timing_string, dt.timedelta(start))

        self.strings = self.i3_string_assembly()


    def decision(self):
        #Decide if the command execute
        #This will be more complex if todoist is integrated properly
        return self.timing_manager.should_execute()

    def i3_string_assembly(self):
        #Assemble i3 executable strings
        i3 = "i3-msg '"
        ws = "workspace " + self.ws_num.__str__() + ":" + self.ws_name + "; "
        return [i3 + ws + 'exec ' + procedure + "'" for procedure in self.command_procedures]

    def return_information_strings(self):
        ws_num_string = self.ws_num.__str__()
        ws_focus_string = self.ws_focus.__str__()
        last_boot_str = self.timing_manager.last_boot.__str__()
        period_length_str = self.timing_manager.period_length.__str__()
        next_launch_str = self.timing_manager.next_launch.ctime()
        timing_str = self.timing_manager.timing_string
        num_boots_today_str = self.timing_manager.num_boots_today.__str__()

        command_data = {
            "ws_num" : ws_num_string,
            "ws_focus" : ws_focus_string,
            "command_procedures" : self.command_procedures,
            "ws_name" : self.ws_name
        }
        #Timing data
        timing_data = {
            "period_length": period_length_str,
            "timing": timing_str,
            "last_boot": last_boot_str,
            "num_boots_today" : num_boots_today_str,
            "next_launch": next_launch_str
        }
        return command_data, timing_data


#TODO: Adding new commands
def new_command():
    print("Choose between the following procedures:")
    #Require input
    print("Choose between the following procedures:")
    #Require input
    #ETC


def absolute_path(filename):
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, 'python_data/command_scheduler')


def reset_day(shift=1):
    cmds_memory_file = absolute_path("python_data/command_scheduler")
    with open(cmds_memory_file, 'rb') as file:
        commands = commands_dict = pickle.load(file)
    for command in commands:
        command.timing_manager.num_boots_today = 0
        last_boot = (dt.date.today() - dt.timedelta(shift))
        command.timing_manager.last_boot = last_boot
        period = command.timing_manager.period_length
        command.timing_manager.next_launch = (last_boot + dt.timedelta(period))
    with open(cmds_memory_file, 'wb') as file:
        pickle.dump(commands, file)

def reset():
    cmds_memory_file = absolute_path("python_data/command_scheduler")
    with open(cmds_memory_file, 'rb') as file:
        commands = commands_dict = pickle.load(file)
    for command in commands:
        command.timing_manager.num_boots_today = 0
    with open(cmds_memory_file, 'wb') as file:
        pickle.dump(commands, file)
#Fix
#commands_file = 'python_data/commands'





