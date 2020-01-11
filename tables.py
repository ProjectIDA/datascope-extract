#!/usr/bin/env python3

# system imports
import sys
import os

# local imports
from extract import extractTable

# other imports
from fabulous.color import red, bold

################################################################################
def main():
    site = Site()
    site.extract()
    chan = Chan()
    chan.extract()
    abbrev = Abbrev()
    abbrev.extract()
    seedloc = Seedloc()
    seedloc.extract()
    stage = Stage()
    stage.extract()
    units = Units()
    units.extract()

################################################################################

class Table:

    # Initializer / Instance Attributes
    def __init__(self):
        pass

    # Extract method
    def extract(self):
        self.outfileName = self.tableName + ".json"
        extractTable(self.tableName, self.outfileName, self.fieldList, self.ranges)

class Site(Table):

    # Initializer / Instance Attributes
    def __init__(self):
        self.tableName = "IDA.site"
        self.fieldList = ["code", "begt", "endt", "lat", "lon", "elev", "staname", "lddate"]
        self.ranges = ((0,6), (7,17), (25,17), (43,9), (53,9), (63,9), (73,50), (125,17))

class Chan(Table):

    # Initializer / Instance Attributes
    def __init__(self):
        self.tableName = "IDA.chan"
        self.fieldList = ["sta", "chn", "loc", "begt", "endt", "edepth", "hang", "vang", "flag", "instype", "nomfreq"]
        self.ranges = ((0,6), (7,8), (16,2), (19,17), (37,17), (55,9), (65,6), (72,6), (79,2), (82,6), (89,16))

class Abbrev(Table):

    # Initializer / Instance Attributes
    def __init__(self):
        self.tableName = "IDA.abbrev"
        self.fieldList = ["item", "desc"]
        self.ranges = ((0,6), (7,50))

class Seedloc(Table):

    # Initializer / Instance Attributes
    def __init__(self):
        self.tableName = "IDA.seedloc"
        self.fieldList = ["sta", "chn", "begt", "endt", "seedchn", "loc", "lddate"]
        self.ranges = ((0,6), (7,8), (16,17), (34,17), (52,6), (59,2), (62,17))

class Stage(Table):

    # Initializer / Instance Attributes
    def __init__(self):
        self.tableName = "IDA.stage"
        self.fieldList = ["sta", "chn", "loc", "begt", "endt", "stageid", "ssident", "gnom", "gcalib", "iunits", "ounits", "izero", "decifac", "srate", "leadfac", "dir", "dfile", "lddate"]
        self.ranges = ((0,6), (7,8), (16,2), (19,17), (37,17), (55,8), (64,16), (81,11), (93,10), (104,16), (121,16), (138,8), (147,8), (156,11), (168,11), (180,64), (245,32), (278,17))

class Units(Table):

    # Initializer / Instance Attributes
    def __init__(self):
        self.tableName = "IDA.units"
        self.fieldList = ["uniot", "desc"]
        self.ranges = ((0,16), (17,50))


################################################################################
if __name__ == '__main__':
    main()
