"""
Project for Week 4 of "Python Programming Essentials".
Collection of functions to process dates.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import datetime


# import calendar
def month_day(month, feb):
    if month in (1, 3, 5, 7, 8, 10, 12):
        day = 31
    # return 31
    elif month == 2:
        day = feb
    # return 29
    else:
        day = 30
    #   return 30
    return day


def days_in_month(year, month):
    """
    Inputs:
      year  - an integer between datetime.MINYEAR and datetime.MAXYEAR
              representing the year
      month - an integer between 1 and 12 representing the month

    Returns:
      The number of days in the input month.
    """
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                day = month_day(month, 29)
            else:
                day = month_day(month, 28)
        else:
            day = month_day(month, 29)
    else:
        day = month_day(month, 28)
    return day


def is_valid_date(year, month, day):
    """
    Inputs:
      year  - an integer representing the year
      month - an integer representing the month
      day   - an integer representing the day

    Returns:
      True if year-month-day is a valid date and
      False otherwise
    """
    if datetime.MINYEAR <= year <= datetime.MAXYEAR:
        if 1 <= month <= 12:
            if 0 < day <= days_in_month(year, month):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def days_between(year1, month1, day1, year2, month2, day2):
    """
    Inputs:
      year1  - an integer representing the year of the first date
      month1 - an integer representing the month of the first date
      day1   - an integer representing the day of the first date
      year2  - an integer representing the year of the second date
      month2 - an integer representing the month of the second date
      day2   - an integer representing the day of the second date

    Returns:
      The number of days from the first date to the second date.
      Returns 0 if either date is invalid or the second date is
      before the first date.
    """
    if is_valid_date(year1, month1, day1) & is_valid_date(year2, month2, day2):
        diff_day = datetime.date(year2, month2, day2) - datetime.date(year1, month1, day1)
        if diff_day.days < 0:
            return 0
        else:
            return int(diff_day.days)
    else:
        return 0


def age_in_days(year, month, day):
    """
    Inputs:
      year  - an integer representing the birthday year
      month - an integer representing the birthday month
      day   - an integer representing the birthday day

    Returns:
      The age of a person with the input birthday as of today.
      Returns 0 if the input date is invalid or if the input
      date is in the future.
    """
    if is_valid_date(year, month, day):
        today = datetime.date.today()
        days = days_between(year, month, day, today.year, today.month, today.day)
        if days > 0:
            return days
        else:
            return 0
    else:
        return 0
# print(days_between(2014,5,6,2014,5,5))
