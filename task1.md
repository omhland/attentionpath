# Configuration reader 

Your script is responsible for:

1. Reading a `.json` script

The json file needs to defined multiple workspaces. Each worspace can have the
following members
```
{
"title":
"number":  
"commands":
"layout":
"timing":
    {
    "weekdays"
    "start_hour"
    "end_hour"
    "start_minute"
    "end_minute"
    }
}
```
2. Create a list of `workspaces`

The script needs to use the `workspace` class – which is defined in `workspace_class.py`.

You can set "title", "number", "layout" and "commands" using the constructor of
the workspace class (`__init__()` – or set them using the `set_attribute(key,
value)`.

Timing must be set independantly using the `set_timing` method. 
