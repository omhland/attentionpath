import os


def i3_workspace_string(workspace):
    ws = "workspace " + workspace.number.__str__() + ":" + workspace.title
    return ws

def i3_set_focus():
    workspace_string = i3_workspace_string(workspace)
    return "#Set fouces " + os.linesep + "sleep 0.5" + os.linesep + i3_msg_creator([workspace_string])

def i3_msg_creator(commands):
    i3_msg = "i3-msg '"
    for command in commands:
        i3_msg = i3_msg + command + '; '
    return i3_msg + "'"


def get_workspace_i3_commands(title, number, commands, layout = None, layout_file_location=None):
    workspace_string = "workspace " + number.__str__() + ":" + title

    # Assemble list string commands 
    command_strings = [i3_msg_creator([workspace_string, "exec " + command]) for command in commands]

    # Add a comment amound the strings
    comment = "#Assembling workspace named " + title

    if layout:
        layout_string = i3_msg_creator([workspace_string, "append_layout " + layout])
        command_strings.insert(0, layout_string)


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
