## Test script for testing if the various functions in config_reader.py works
import timing_intervals as ti
import datetime as dt

test_constructor = False
test_is_in_interval = True

if __name__ == "__main__":
    print("Testing constructor")
    # Test that should work well
    if test_constructor:
        days_test1 = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        days_test2 = days_test1[0:3]
        days_test3 = days_test1[3:6]

        days_test4 = [0, 1, 2, 3, 4, 5, 6]
        days_test5 = days_test4[0:3]

        hour_start_test1 = 0; hour_start_test2 = 10; hour_start_test3 = 22
        hour_end_test1 = 1; hour_end_test2 = 15; hour_end_test3 = 23

        minute_start_test1 = 0; minute_start_test2 = 30; minute_start_test3 = 58
        minute_end_test1 = 1; minute_end_test2 = 40; minute_end_test3 = 59

        ti.timing_intervals(days_test1, hour_start_test1, hour_end_test1, minute_start_test1, minute_end_test1)
        print("Test 1 passed \n\n")
        ti.timing_intervals(days_test2, hour_start_test2, hour_end_test2, minute_start_test2, minute_end_test2)
        print("Test 2 passed \n\n")
        ti.timing_intervals(days_test3, hour_start_test3, hour_end_test3, minute_start_test3, minute_end_test3)
        print("Test 3 passed \n\n")

        ti.timing_intervals(days_test4, hour_start_test1, hour_end_test1, minute_start_test1, minute_end_test1)
        print("Test 4 passed")
        ti.timing_intervals(days_test5, hour_start_test2, hour_end_test2, minute_start_test2, minute_end_test2)
        print("Test 5 passed \n\n")

        ti.timing_intervals(days_test1)
        print("Test 6 passed \n\n")
        ti.timing_intervals(days_test4)
        print("Test 7 passed \n\n")

    # Test if the function is_in_interval works
    if test_is_in_interval:

        # Test with a class that only return true on the current day
        today = dt.datetime.now().weekday()
        timing_class_only_today = ti.timing_intervals([today])

        # Test for days in the week
        for day in range(7):
            if day == today:
                # Test for today (should be true)
                if timing_class_only_today.is_in_interval():
                    print("Timing class correctly returned true when testing \
                        is_in_interval for the current day")
                else:
                    raise Exception(f'Timing class incorrectly returned false when testing'
                                    f'is_in_interval for the current day')

            elif day is not today:
                if timing_class_only_today.is_in_interval(day=day):
                    raise Exception('Timing class incorrectly returned true'
                            'when testing is_in_interval for the current day')
        print('Timing class correctly returned false when testing '
                'is_in_interval for all days except the current day')

        # Test a class that is only specify the the current hour
        current_time = dt.datetime.now()
        current_hour = current_time.hour
        next_hour = (current_hour + 1) % 24
        all_weekdays = [i for i in range(7)]
        timing_class_only_current_hour = ti.timing_intervals(all_weekdays,
                                start_hour=current_hour, end_hour=current_hour)

        # Test for the current time (should be true)
        all_hours = [i for i in range(24)]
        for hour in all_hours:
            if hour == current_hour:
                if timing_class_only_current_hour.is_in_interval():
                    print('Timing class correctly returned true when testing'
                        'is_in_interval for the current hour')
                else:
                    raise Exception('Timing class incorrectly returned false when testing'
                        'is_in_interval for the current hour')

            else:
                if timing_class_only_current_hour.is_in_interval(
                    time=dt.time(hour=hour, minute=0)):
                    raise Exception("Timing class incorrectly returned true when testing" +
                            " is_in_interval for a the hour %s" % hour)
        print("Timing class correctly returned false when testing for all" +
              "other hours than the current hour")
