class find_days_between_dates():
    def __init__(self, from_date, to_date):
        self.start_day = int(from_date.split('-')[0])
        self.start_month = int(from_date.split('-')[1])
        self.start_year = int(from_date.split('-')[2])
        self.end_day = int(to_date.split('-')[0])
        self.end_month = int(to_date.split('-')[1])
        self.end_year = int(to_date.split('-')[2])
        self.leap_year_days = 366
        self.nonleap_year_days = 365
        self.validate_dates()

    def validate_dates(self):
        '''Validates the values of from_date and to_date according to the principles of Gregorian calendar'''
        if self.start_month > 12 or self.end_month > 12:
            raise ValueError('A year has only 12 months, please recheck \'month\' value')
        if self.start_day > self.get_noofdays_of(self.start_month, self.start_year) or self.end_day > self.get_noofdays_of(self.end_month, self.end_year):
            raise ValueError('Date is wrong..! Please recheck')

        if self.start_year < 1583:
            raise ValueError('This program is based on Gregorian calself.endar which was invented on 1582. Enter dates after 1582..!')

        if self.start_year > self.end_year:
            raise ValueError('start date cannot be higher than end date..!') # if start year is greater than end year
        elif self.start_year == self.end_year:
            if self.start_month > self.end_month:
                raise ValueError('start date cannot be higher than end date..!') # if start month is greater than end month during same year
            elif self.start_month == self.end_month:
                if self.start_day > self.end_day:
                    raise ValueError('start date cannot be higher than end date..!') # if start day is greater than end day during same year and month


    def is_leap(self, year):
        '''Finds if a year is a leap year'''
        if year > 1582:
            if year%4 == 0:
                if year%100 == 0:
                    if year%400 == 0:
                        return True
                    return False
                return True
            return False
        else:
            raise ValueError('This program is based on Gregorian calendar so the start year must be after 1582...')

    def get_noofdays_of(self, month, year):
        '''Returns no.of.days present in the given month&year'''
        days_map = {
        1: 31, #january
        2: None, #february
        3: 31, #march
        4: 30, #april
        5: 31, #may
        6: 30, #june
        7: 31, #july
        8: 31, #august
        9: 30, #september
        10: 31, #october
        11: 30, #november
        12: 31, #december
        }

        if self.is_leap(year):
            days_map[2] = 29
        else:
            days_map[2] = 28
        return days_map[month]

    def remaining_days(self, day, month, year, count_direction='forward'):
        '''Finds no.of.days present between the given date(d/m/y) and
            the end(start if count_direction == 'backward') of the year'''

        days = 0
        if count_direction == 'forward': # calculates remaining days from given date to the END OF THE YEAR >---->|
            for current_month in range(month, 12+1):
                current_month_days = self.get_noofdays_of(current_month, year)
                if current_month == month:
                    days += (current_month_days - (day - 1))  # reduction of is to include the starting day also!
                else:
                    days += current_month_days

        elif count_direction == 'backward': # calculates the passed days from the given date to the START OF THE YEAR |<----<
            for current_month in range(month, 1-1, -1):
                current_month_days = self.get_noofdays_of(current_month, year)
                if current_month == month:
                    days += day
                else:
                    days += current_month_days

        return days

    def calculate_noofdays(self):
        '''Finds the days present in between the given dates. Includes both start and end dates also'''

        nonleap_year_days = 365
        leap_year_days = 366
        total_days = 0
        if self.start_year == self.end_year:
            total_days = (self.remaining_days(self.start_day, self.start_month, self.start_year, count_direction='forward') - self.remaining_days(self.end_day, self.end_month, self.end_year, count_direction='forward')) + 1
        else:
            for year in range(self.start_year, self.end_year+1):
                if year == self.start_year:
                    total_days += self.remaining_days(self.start_day, self.start_month, self.start_year, count_direction='forward')
                elif year == self.end_year:
                    total_days +=self. remaining_days(self.end_day, self.end_month, self.end_year, count_direction='backward')
                else:
                    if self.is_leap(year):
                        total_days += leap_year_days
                    else:
                        total_days += nonleap_year_days
        return total_days

day_calc = find_days_between_dates('28-5-2021', '3-9-2021')
no_of_days = day_calc.calculate_noofdays()
print(no_of_days)
