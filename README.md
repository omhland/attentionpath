# attentionpath

## Installation

`attentionpath` is light and simple – it only requires that you have *bash*, *python3* and *i3* installed. Happily, the installation is also straightforward. Follow these 2 steps:

1. Clone the repo
```
cd ~/.config/
git clone https://github.com/omhland/attentionpath
```
2. Configuring i3

Place the fowllowing snippet into your i3 `config` file. 
```
exec_always ~/.config/attentionPath/i3_launch_manager.sh
```
You'll typically find this in `.config/i3/config`.


# Setup

## How to write your configuration file
The `config` file defines a set of workspaces and a focus priority queue. The following section will show you how to configure attentionpath.

The snippet below illustrates the syntax:
```
"A comment

"Set focus priority
= workspace_number_X, focused_ws_Y, ...
{
: layout_name
# Workspace_1
+ workspace_number
@ day:weekday, day:another_weekday, date:DD.MM
-command_1
-command_2
}

{
# New_workspace
...
}

```
The program starts from the top and works downwards.
- Workspaces are defined within curly brackets `{}`.
- Properties (`#, @, -`) are added to the initialized workspace.  

The properties possible properties are:
1. Name, marked by `#`. 
1. Timing, marked by `@`.
1. Number, marked by `+`.
1. Commands, marked by `-`.


### Adding a workspace title
The string that follows `#` will be used as the workspace's name. For example, the snippet.
```
# Productivity
```
will yield a workspace called *productivity*.


### Commands
The workspace will be populated by the programs you choose to run within it. The programs are specified by `-`. E.g.
```
-google-chrome --args --new-window google.com
```
Running a command in your terminal is a good way to assess if the command will work. Check out the following [section](#Execution time) to see more examples.

### Setting the workspace number
Each workspace has an associated number. Set this by using `+ x`, where x is some integer.

### Focused workspace
Only one workspace can be focused at launch. This will either be 
- The last workspace in the list
- Some specified workspace.
Use `=` to determine which workspace to focus on. Use a comma-separated list to make a prioritization order. E.g.
```
= 5, 4, 3
```
With this scheme, workspace five will always be focused when it launches. Workspace 3 will only launch if neither workspace 5 nor 4 launches.

### Execution time
`@` determines the execution times. An execution time must correspond to a weekday. The options are `monday, thusday, wednesday, thursday, friday, saturday`. The execution times are specified using a comma separated list, e.g.
```
@ monday, wednesday, saturday
```

# Command Examples

**Opening files with libreoffice**
`-libreoffice Documents/fincances/budget.xlsx`

**Open chrome**
`-google-chrome-stable --args --new-window https://todoist.com/app/project/2269572090`

**Open chrome with multiple tabs**
`-google-chrome-stable --args --new-window google.com github.com stackoverflow.com`

**Opening a file with Vim**
'-gnome-terminal -x vim ~/Documents/msg/daily.text`

**Using flatpack**
`-flatpak run com.toggl.TogglDesktop`


# Implementation

The implementation is a combination of Python and Bash.

This is a prototype rather than a complete project.

## Python 
The config file is read and processed by the `input_reader` class. The `input_reader.read_config` is the only function that should be used when using this class.

#### `input_reader.read_config`
**Input:** `config_file_location`
**Output:** `workspaces`, `focus`

- `workspaces` is a list that contains all the requested *workspaces*. Each workspace is of the type `workspace`.  
- `focus` is a list of ints. This list will be used to determine which workspace to focus.

#### The `workspace` class
The `workspace class` contains all the properties that define a workspace. The properties are as follows:
- title
- number
- commands
- timing





















>>>>>>> b17bfec (Attentionpath made (somewhat) presentable)
