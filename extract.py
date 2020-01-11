#!/usr/bin/env python3

# system imports
import sys
import os
import json

# local imports

# other imports
from fabulous.color import red, bold

################################################################################
def main():

    fieldList = ["code", "begt", "endt", "lat", "lon", "elev", "staname", "lddate"]
    #ranges = ((0,6), (6,18), (24,18), (42,10), (52,10), (62,10), (72,50), (122,19))
    ranges = ((0,6), (7,17), (25,17), (43,9), (53,9), (63,9), (73,50), (124,17))
    tableName = "IDA.site"
    outfileName = tableName + ".json"

    extractTable(tableName, outfileName, fieldList, ranges)

################################################################################
def extractTable(table, ofName, fields, ranges):
 
    dbDir = os.environ.get('IDA_DATASCOPEDB_DIR')
    dbSite = dbDir + '/' + table
    jsonOut = ofName

    try:
        table_fp = open(dbSite, 'r')
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

    rowList = []
    rowDict = {}
    columnDict = {}
    idx = 1
    for line in table_fp:
        columnList = []
        for rng in ranges:
            columnList.append(line[rng[0]:rng[0]+rng[1]].strip())
            columnDict = dict(zip(fields, columnList))

        rowDict = { "model" : "stations.station", "pk" : idx, "fields" : columnDict }
        idx += 1
        rowList.append(rowDict)
    
    json_string = json.dumps(rowList)
    json_fp.write(json_string)

    table_fp.close()
    json_fp.close()

################################################################################
if __name__ == '__main__':
    main()
