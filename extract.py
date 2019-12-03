#!/usr/bin/env python3

# system imports
import sys
import os

# local imports

# other imports
from fabulous.color import red, bold

################################################################################
def main():
    getStationList()

################################################################################
def getStationList():
 
    dbDir = os.environ.get('IDA_DATASCOPEDB_DIR')
    dbSite = dbDir + '/' + "IDA.site"
    jsonOut = "IDAsite.json"
    testOut = "IDAsite.out"

    try:
        site_fp = open(dbSite, 'r')
    except FileNotFoundError:
        print("File does not exist: {}".format(dbSite))
        raise SystemExit
    except IOError:
        print ("Could not read from: {}".format(dbSite))
        raise SystemExit
        
    try:
        json_fp = open(jsonOut, 'w')
    except FileNotFoundError:
        print("File does not exist: {}".format(jsonOut))
        raise SystemExit
    except IOError:
        print ("Could not read from: {}".format(jsonOut))
        raise SystemExit

    try:
        test_fp = open(testOut, 'w')
    except FileNotFoundError:
        print("File does not exist: {}".format(test.out))
        raise SystemExit
    except IOError:
        print ("Could not read from: {}".format(test.out))
        raise SystemExit

    siteList = []

    FIELDLIST = ["code", "begt", "endt", "lat", "lon", "elev", "staname", "lddate"]
    RANGES = ((0, 6), (6, 18), (24, 18), (42,10), (52,10), (62,10), (72,50), (122,19))

    rowDict = {}
    columnDict = {}
    idx = 1
    for line in site_fp:
        columnList = []
        for rng in RANGES:
            columnList.append(line[rng[0]:rng[0]+rng[1]].strip())
            columnDict = dict(zip(FIELDLIST, columnList))

        print(columnDict)
        rowDict.update({"pk" : idx, {"model" : "stations.station", {"fields" : columnDict}}})
        idx += 1

    print(rowDict)

    site_fp.close()
    json_fp.close()
    test_fp.close()

################################################################################
if __name__ == '__main__':
    main()
