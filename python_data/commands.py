#Command specifications
global commands
commands = [
    command_class([start_up, calendar], "Plan_the_day", 10, period_length=1, timing_string="first", ws_focus=True),
    command_class([freedom, message_bundle], "Freedom_and_messages", 9, period_length=1, timing_string="first"),
    command_class([toggl, deep_work, freedom], "Work", 1, period_length=1, timing_string="every"),
    command_class([toggl_web, end_of_day], "End_of_day", 0, period_length=1, timing_string="every"),
    command_class([toggl_web, todoist_review], "Review", 15, period_length=7, timing_string="first", ws_focus=True),
    command_class([network_book, vim_advanced], "Course_of_the_day", 11, period_length=1, timing_string="first", ws_focus=True),
]
