#!/usr/bin/env python3

# system imports
import sys
import os

# local imports

# other imports
from fabulous.color import red, bold

################################################################################
def main():
    ranges = ((0, 6), (6, 18), (24, 18), (42,10), (52,10), (62,10), (72,50), (122,19))
    station = Table("station", ranges)

################################################################################

class Table:

    # Initializer / Instance Attributes
    def __init__(self, name, ranges):
        self.name = name
        self.range = ranges

################################################################################
if __name__ == '__main__':
    main()
