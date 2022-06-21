import datetime as dt
class timing_intervals:
    """ A class to handle the timing intervals for a workspace.
    attributes:
    interval_days: a list of ints representing the days of the week
    interval_times: a tuple of to datetime objects representing
    the start and end times
    """
    interval_days = []
    def __init__(self, weekdays, start_hour=None, end_hour=None, start_minute=None, end_minute=None):
        """ Initializes the timing intervals and takes care of the internal
        representations of the time.
        input:
        weekdays- list of weekdays to activate the command. Either a list of
        strings or a list of ints (0-6)
        start_hour: the hour to start the command (defaults to 0)
        end_hour: the hour to end the command (defaults to 23)
        start_minute: the minute to start the command (defaults to 0)
        end_minute: the minute to end the command (defaults to 59)
        """
        HOUR_UPPER_BOUND = 23
        HOUR_LOWER_BOUND = 0
        MINUTE_UPPER_BOUND = 59
        MINUTE_LOWER_BOUND = 0

        # Check if the input is valid
        if not isinstance(weekdays, list):
            raise ValueError("weekdays must be a list")
        elif any(not isinstance(day, (str, int)) for day in weekdays):
            raise ValueError("members of weekdays must be strings or ints (representing weekdays)")
        elif isinstance(weekdays[0], int):
            USE_INTS = True
            # Double check that only ints are used
            for day in weekdays[1:]:
                if not isinstance(day, int):
                    raise ValueError("weekdays must be a list of only ints\
                                     or only strings")
        elif isinstance(weekdays[0], str):
            USE_INTS = False
            # Double check that only strings are used
            for day in weekdays[1:]:
                if not isinstance(day, str):
                    raise ValueError("weekdays must be a list of only ints\
                                     or only strings")
        elif not isinstance(start_hour, int) and start_hour != None:
            raise ValueError("start_hour must be an int")
        elif not isinstance(end_hour, int) and end_hour != None:
            raise ValueError("end_hour must be an int")
        elif not isinstance(start_minute, int) and start_minute != None:
            raise ValueError("start_minute must be an int")
        elif not isinstance(end_minute, int) and end_minute != None:
            raise ValueError("end_minute must be an int")
        elif start_hour != None and start_hour > HOUR_UPPER_BOUND:
            raise ValueError("start_hour must be between 0 and 23")
        elif start_hour != None and start_hour < HOUR_LOWER_BOUND:
            raise ValueError("start_hour must be between 0 and 23")
        elif end_hour != None and end_hour > HOUR_UPPER_BOUND:
            raise ValueError("end_hour must be between 0 and 23")
        elif end_hour != None and end_hour < HOUR_LOWER_BOUND:
            raise ValueError("end_hour must be between 0 and 23")
        elif start_minute != None and start_minute > MINUTE_UPPER_BOUND:
            raise ValueError("start_minute must be between 0 and 59")
        elif start_minute != None and start_minute < MINUTE_LOWER_BOUND:
            raise ValueError("start_minute must be between 0 and 59")
        elif end_minute != None and end_minute > MINUTE_UPPER_BOUND:
            raise ValueError("end_minute must be between 0 and 59")
        elif end_minute != None and end_minute < MINUTE_LOWER_BOUND:
            raise ValueError("end_minute must be between 0 and 59")

        if start_hour == None:
            start_hour = HOUR_LOWER_BOUND
        if end_hour == None:
            end_hour = HOUR_UPPER_BOUND
        if start_minute == None:
            start_minute = MINUTE_LOWER_BOUND
        if end_minute == None:
            end_minute = MINUTE_UPPER_BOUND

        if start_hour > end_hour:
            raise ValueError("Upper values must be greater than lower values,\
                            and minutes must be within 0 to 59.")
        if start_minute > end_minute:
            raise ValueError("Upper values must be greater than lower values,\
                             and hours must be within 0 to 23.")

        self.time_interval= (dt.time(start_hour, start_minute),\
                             dt.time(end_hour, end_minute))

        if USE_INTS == True:
            self.set_interval_days_int(weekdays)
        elif USE_INTS == False:
            self.set_interval_days_str(weekdays)
        # This should always be true
        assert self.interval_days != [], "No days were specified"

    def set_interval_days_int(self, days):
        """ Sets the days of the week that the interval is active.
        Input: days -> a list of ints representing the days of the week
        Output: None
        """
        for day in days:
            if day not in range(0,7):
                raise ValueError("weekdays must be a list of ints representing weekdays")
            elif not isinstance(day, int):
                raise ValueError("weekdays must be a list of ints representing weekdays")
        self.interval_days = days

    def set_interval_days_str(self, days):
        """ Sets the days of the week that the interval is active.
        Input: days -> a list of strings representing the days of the week
        Output: None
        """
        WEEK = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in days:
            if day not in WEEK:
                raise ValueError("weekdays must be a list of strings\
                                 representing weekdays")
        self.interval_days = [WEEK.index(day) for day in days]

    def is_in_interval(self, time = None, day = None):
        """ Checks if the current time is within the interval. Will use the
        current time and current day if none is specified.
        Input (Optional):
        time -> a datetime.time object representing the current time
        day -> an int representing the current day of the week
        Output: :bool
        """
        if time is None:
            time = dt.datetime.now().time()
        else:
            if not isinstance(time, dt.time):
                raise ValueError("time must be a datetime.time\
                                 object")
        in_time_interval = self.time_interval[0] <= time <=\
            self.time_interval[1]

        if day is None:
            day = dt.date.today().weekday()
        else:
            if not isinstance(day, int):
                raise ValueError("day must be an int representing\
                                 a weekday")
            elif day not in range(0,7):
                raise ValueError("day must be an int representing\
                                 a weekday")
        on_correct_day = day in self.interval_days

        assert day in range(0,7), "Weekday is not in range"
        assert isinstance(in_time_interval, bool)
        assert isinstance(on_correct_day, bool)

        return on_correct_day and in_time_interval
