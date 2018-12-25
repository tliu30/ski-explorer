"""
A list of cities, to be used as locations to / from which
to travel.
"""

from enum import Enum


class Cities(Enum):
    BOSTON = 1
    NYC = 2
    NYC_AIR = 3   # e.g., NYC Airports (for rental info)
    DENVER = 4
    RENO = 5  # for Lake Tahoe
    HAYDEN = 6  # colorado; near beaver creek
    SLC = 7  # Salt Lake City
    BOISE = 8  # boise
