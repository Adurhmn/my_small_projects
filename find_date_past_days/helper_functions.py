class HelperClass():
    def validate_dates(self):
        '''Validates the values of from_date and to_date according to the principles of Gregorian calendar'''
        if not 12 >= self.month > 0:
            raise ValueError('A year months between 1 to 12. Please recheck \'month\' value')
        if not self.get_noofdays_of(self.month, self.year) > self.day > 0:
            raise ValueError('Date is wrong..! Please recheck')
        if self.year < 1583:
            raise ValueError('This program is based on Gregorian calself.endar which was invented on 1582. Enter dates after 1582..!')

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

    def forward_one_year(self):
        self.year += 1
        self.days_to_pass -= self.year_days

    def rewind_one_year(self):
        self.year -= 1
        self.days_to_pass += self.year_days

    def sort_months(self, month, order="Forward"):
        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        current_month_ind = months.index(month)
        if order == "Forward":
            sorted_months = months[current_month_ind: ] + months[ :current_month_ind]
        elif order == "Rewind":
            sorted_months = months[current_month_ind: : -1] + months[len(months)-1: current_month_ind: -1]
        return sorted_months

    def set_date(self, day=None, month=None, year=None):
        if day is not None:
            self.day = day
        if month is not None:
            self.month = month
        if year is not None:
            self.year = year

    def set_year_if_year_changes(self, month, condition="Forward"):
        '''Checks if next month is in same year or in next year
            If so, changes the year to next year
            >> This function must be used only if the month changes <<'''

        if condition == "Forward":
            months = self.sort_months(month, order="Forward")
            if months[1] == 1:
                print("year changed")
                self.set_date(year=self.year + 1)
        elif condition == "Rewind":
            months = self.sort_months(month, order="Rewind")
            if months[1] == 12:
                print("year changed")
                self.set_date(year=self.year - 1)
