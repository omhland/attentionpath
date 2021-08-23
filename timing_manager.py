import datetime as dt
class timing_manager:

    #Not neccesary now but will be nice in the future
    #TODO This only works if the system just booted
    def __init__(self, period_length, timing_string, start_delta): #, num_executions):
        self.time_dict = {
            "first": 1,
            "every": 2
        }
        self.timing_string = timing_string

        #num_executions = is_string or datetime...    int or 'always' string 
        self.period_length = period_length
        self.timing = self.time_dict[timing_string]

        #Store timing data: A bit hacky -> last boot will be set to the past 
        self.next_launch = dt.date.today()+start_delta
        self.last_boot = self.next_launch- dt.timedelta(period_length);
        self.num_boots_today = 0;

    def should_execute(self):

        #Set default value
        execute = False


        #Evaluate apps that should only launch at the first boot of the day
        #Determine if if the command should launch of this day
        current_day = dt.date.today()

        if current_day != self.last_boot:
            self.num_boots_today = 0

        if self.next_launch <= current_day:
            #Execute that should launch at every boot
            execute = True
            if self.timing == self.time_dict["every"]:
                self.next_launch = current_day

            if (self.timing == self.time_dict["first"]):
                #Evalute if the command has already been launched
                self.next_launch = current_day + dt.timedelta(self.period_length)

        #Save execution values 
        if execute:
            self.last_boot = dt.date.today()
            self.num_boots_today = self.num_boots_today + 1

        return execute
