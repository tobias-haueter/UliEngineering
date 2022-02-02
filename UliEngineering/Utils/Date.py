#!/usr/bin/env python3
from collections import namedtuple
from calendar import monthrange

__all__ = ["Date", "all_dates_in_year", "number_of_days_in_month"]

Date = namedtuple("Date", ["year", "month", "day"])

def number_of_days_in_month(year=2019, month=1):
    """
    Returns the number of days in a month, e.g. 31 in January (month=1).
    Takes into account leap days.
    """
    return monthrange(year, month)[1]

def all_dates_in_year(year=2019):
    """
    Iterates all dates in a specific year, taking into account leap days.
    Yields Date() objects.
    """
    for month in range(1, 13): # Month is always 1..12
        for day in range(1, number_of_days_in_month(year, month) + 1):
            yield Date(year, month, day)
