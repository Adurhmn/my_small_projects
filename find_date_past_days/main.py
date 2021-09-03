import sys
from helper_functions import HelperClass

class FindDatePastDays(HelperClass):
    def __init__(self, date, days_to_pass):
        self.date = date
        self.days_to_pass = days_to_pass
        self.day = int(date.split('-')[0])
        self.month = int(date.split('-')[1])
        self.year = int(date.split('-')[2])
        self.year_days = 365  # Non Leap

    def filterout_years(self):
        if self.days_to_pass >= self.year_days:
            # print("is_positive")
            total_years = self.days_to_pass // self.year_days
            leap_year_interruption = 0

            # Implementing principle for first year (checks if first year has any leap interruption; passes starting year) (starting year)1999>>>>>(middle years)>>>>>2010(last year)
            if self.is_leap(self.year) and self.month <= 2:
                    leap_year_interruption += 1
            self.forward_one_year()
            total_years -= 1

            # Implementing principles for middle years (checks if middle year has any leap interruption; passes one year per iteration) (this loop doesn't check if the final year is leap; it just gets to the final year; but it checks if years before final are leap)
            for ind in range(total_years):
                if self.is_leap(self.year):
                    leap_year_interruption += 1
                self.forward_one_year()

            # Implementing principles for last year (checks if final year has any leap interruption)
            if self.is_leap(self.year) and self.month >= 3:
                leap_year_interruption += 1

            self.days_to_pass -= leap_year_interruption # this resets the leap_year_interruption

            # print(self.day, self.month, self.year, f'\n{self.days_to_pass}, *{leap_year_interruption}', sep='-', end='\n\n')

        elif self.days_to_pass <= -(self.year_days): # if negative
            # print("is negative")
            total_years = abs(self.days_to_pass) // self.year_days
            leap_year_interruption = 0

            # Implementing principle for last year year (checks if last year has any leap interruption; passes last year)   (starting year)1999<<<<<<(middle years)<<<<<<2010(last year)
            if self.is_leap(self.year) and self.month >= 3:
                leap_year_interruption += 1
            self.rewind_one_year()
            total_years -= 1

            # Implementing principles for middle years (checks if middle year has any leap interruption; passes one year per iteration) (this loop doesn't check if the first(final) year is leap; it just gets to the first(final) year; but it checks if years before after are leap)
            for ind in range(total_years):
                if self.is_leap(self.year):
                    leap_year_interruption += 1
                self.rewind_one_year()

            # Implementing principles for first year (checks if first(final) year has any leap interruption)
            if self.is_leap(self.year) and self.month <= 2:
                leap_year_interruption += 1

            self.days_to_pass += leap_year_interruption # this resets the leap_year_interruption

            # print(self.day, self.month, self.year, f'\n{self.days_to_pass}, *{leap_year_interruption}', sep='-', end='\n\n')


    def calculate_date(self):
        # FILTER OUT YEARS----
        while True:
            if self.days_to_pass >= self.year_days or self.days_to_pass <= -(self.year_days):
                self.filterout_years()
                continue
            break

        if self.days_to_pass > 0: # if positive, increase date with days_to_pass
            # FILTER OUT MONTHS AND CALCULATE THE DATE----
            # the days_to_pass value is increased by the current day value since the algorithm considers that the first month starts from 0 and not the current day.
            self.days_to_pass += self.day

            sorted_months = self.sort_months(self.month)
            for m_k_ind, m_k in enumerate(sorted_months):

                month_days = self.get_noofdays_of(month=m_k, year=self.year)

                if self.days_to_pass - month_days > 0:
                    # if days_to_pass is greater than month_days, then answer date not in this month, so moving to next month without any changes in the date(no real-time changes) except if the month goes to next year.
                    self.days_to_pass -= month_days
                    # if next month starts from next year, then change year.
                    self.set_year_if_year_changes(month=m_k)

                elif self.days_to_pass - month_days < 0:
                    # if days_to_pass is lesser than the month_days, then current month is the answer month and days_to_pass is the answer day.
                    self.set_date(day=self.days_to_pass, month=m_k)
                    break

                else:
                    # if days_to_pass and month_days are same, first day of next month is the answer date.
                    self.set_date(day=1, month=months_key[m_k_ind + 1])
                    # if next month starts from next year, then change year.
                    self.set_year_if_year_changes(month=m_k)
                    break

            # print(self.day, self.month, self.year, f'\n{self.days_to_pass}', sep='-', end='\n\n')

        elif self.days_to_pass < 0: # if negative, decrease date with days_to_pass

            self.days_to_pass = abs(self.days_to_pass)
            # FILTER OUT MONTHS AND CALCULATE THE DATE----
            # the days_to_pass value is increased by the remaining days of the month since the algorithm considers that the first month starts from its last day and not the current day.
            start_month_days = self.get_noofdays_of(month=self.month, year=self.year)
            self.days_to_pass += start_month_days - self.day

            sorted_months = self.sort_months(self.month, "Rewind")
            for m_k_ind, m_k in enumerate(sorted_months):

                month_days = self.get_noofdays_of(month=m_k, year=self.year)

                if self.days_to_pass - month_days > 0:
                    # if days_to_pass is greater than month_days, then answer date not in this month, so moving to next month without any changes in the date(no real-time changes) except if the month goes to next year.
                    self.days_to_pass -= month_days
                    # if next month starts from next year, then change year.
                    self.set_year_if_year_changes(month=m_k, condition="Rewind")

                elif self.days_to_pass - month_days < 0:
                    # if days_to_pass is lesser than the month_days, then current month is the answer month and month_days - days_to_pass is the answer day.
                    self.set_date(day=month_days - self.days_to_pass, month=m_k)
                    break

                else:
                    # if days_to_pass and month_days are same, first day of next m_k is the answer date.
                    self.set_date(day=1, month=months_key[m_k_ind - 1])
                    # if next month starts from next year, then change year.
                    self.set_year_if_year_changes(month=m_k, condition="Rewind")
                    break

            # print(self.day, self.month, self.year, f'\n{self.days_to_pass}', sep='-', end='\n\n')
        return f"{self.day}-{self.month}-{self.year}"




a = FindDatePastDays('4-9-2021', -99)
date = a.calculate_date()
print(date)
