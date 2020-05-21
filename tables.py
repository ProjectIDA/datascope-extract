#!/usr/bin/env python3

# system imports
import sys
import os
import json

# other imports
# from fabulous.color import red, bold

################################################################################
def main():
    # the order of procesing in important
    # as some tables adepened on others.

    instype = Instype()
    instypeRecs = instype.extract()
    instype.saveJSON('output/initial_instype_data.json')

    network = Network()
    networkRecs = network.extract()
    network.saveJSON('output/initial_network_data.json')

    site = Site(networkRecs)
    siteRecs = site.extract()
    site.saveJSON('output/initial_station_data.json')

    chan = Chan(instypeRecs, siteRecs)
    chanRecs = chan.extract()
    chan.saveJSON('output/initial_chan_data.json')

    stage = Stage(chanRecs)
    stage.extract()
    stage.saveJSON('output/initial_stage_data.json')

    seedloc = Seedloc()
    seedloc.extract()
    seedloc.saveJSON('output/initial_seedloc_data.json')

    units = Units()
    units.extract()
    units.saveJSON('output/initial_units_data.json')

################################################################################

class Table:

    # Initializer / Instance Attributes
    def __init__(self):
        self.tableName = None   # str: name of source datascope table
        self.fieldList = []     # [str]: table field names for output
        self.ranges = []        # tuple of tuple pairs that contain the 
                                #   start column and length for each field
                                #   in source table
        self.djangoModel = None # model name for django loaddata function
        self.dataList = [  ]    # [dict]: list of dicts each of which represents
                                #   a single row in the source table

    def readTable(self, firstRecNdx=None, lastRecNdx=None):
        """ Read the source table and encode each record
            as a python Dict.

            Parameters:
                firstRecNdx (None, int):
                    If specified, start encoding with the firstRecNdx'th record.
                    Record indexing is 0-based.

                lastRecNdx (None, int):
                    If specified, end encoding with the lastRecNdx'th record.
                    Record indexing is 0-based.

            Returns:
                [dict]: list of encoded records
        """

        dbDir = os.environ.get('IDA_DATASCOPEDB_DIR')
        dbSite = dbDir + '/' +  self.tableName

        try:
            table_fp = open(dbSite, 'r')
        except FileNotFoundError:
            print("File does not exist: {}".format(dbSite))
            raise SystemExit
        except IOError:
            print ("Could not read from: {}".format(dbSite))
            raise SystemExit
            
        rowList = []
        rowDict = {}
        columnDict = {}
        idx = 1
        for recNdx, line in enumerate(table_fp):
            # skip if not within the reange, if specified
            if ((firstRecNdx is not None) and recNdx < firstRecNdx) or \
                ((lastRecNdx is not None) and recNdx > lastRecNdx):
                continue

            columnList = []
            for rng in self.ranges:
                val_str = line[rng[0]:rng[0]+rng[1]].strip()
                if val_str == '-':
                    val_str = ""  # blank out datascope 'null' values
                columnList.append(val_str)
                columnDict = dict(zip(self.fieldList, columnList))

            rowDict = { "model" : self.djangoModel, "pk" : idx, "fields" : columnDict }
            idx += 1
            rowList.append(rowDict)
        
        table_fp.close()

        return rowList

    # Extract method
    def extract(self):
        self.dataList = self.readTable()
        return self.dataList

    # def jsonFilename(self):
    #     return self.tableName + ".json"

    def saveJSON(self, oFilename):

        if not self.dataList:
            print("Error: Can't write JSON before extracting data.")
            return

        try:
            json_fp = open(oFilename, 'w')
        except FileNotFoundError:
            print("File does not exist: {}".format(oFilename))
            raise SystemExit
        except IOError:
            print ("Could not read from: {}".format(oFilename))
            raise SystemExit

        json_string = json.dumps(self.dataList, indent=3)

        json_fp.write(json_string)
        json_fp.close()


class Network(Table):

    """ Just way to generate afixture for the network table
        with a single record. Some fields that were not 
        maintained in the datascope DB are hardcoded here.
    """

    # Initializer / Instance Attributes
    def __init__(self):
        self.djangoModel = 'stations.network'
        self.tableName = "IDA.abbrev"
        self.fieldList = ["code", "description"]
        self.ranges = ((0,6), (7,50))

    def jsonFilename(self):
        return "IDA.network.json"

    def extract(self):
        self.dataList = self.readTable(lastRecNdx=0)

        for net in self.dataList:
            net['fields']['start_date'] = 504925200.0
            net['fields']['end_date'] = 9999999999.0

        return self.dataList


class Site(Table):

    # Initializer / Instance Attributes
    def __init__(self, netRecs):
        self.djangoModel = 'stations.station'
        self.tableName = "IDA.site"
        self.fieldList = ["code", "start_date", "end_date", "latitude", "longitude", "elevation", "site"]
        self.ranges = ((0,6), (7,17), (25,17), (43,9), (53,9), (63,9), (73,50), (125,17))

    def extract(self):
        self.dataList = self.readTable()

        # need to pull in data from  site and abbrev lists
        for _, siteRec in enumerate(self.dataList):

            # populate network_id to 1 (for only network in DB at this time)
            siteRec['fields']['network_id'] = 1

        return self.dataList


class Chan(Table):

    # Initializer / Instance Attributes
    def __init__(self, abbrevs, sites):
        self.djangoModel = 'stations.channelepoch'
        self.tableName = "IDA.chan"
        self.fieldList = ["station", "code", "location_code", "start_date", "end_date", "depth", "azimuth", "dip", "types", "sensor", "nomfreq", "elevation"]
        self.ranges = ((0,6), (7,8), (16,2), (19,17), (37,17), (55,9), (65,6), (72,6), (79,2), (82,6), (89,16))
        self.abbrevList = abbrevs
        self.siteList = sites

    # Extract method for Channel that pulls in some fields from parent Site/Station record

    def extract(self):
        self.dataList = self.readTable()

        # need to pull in data from  site and abbrev lists
        for _, chanRec in enumerate(self.dataList):

            # pull down data from parent site record
            if not self.getSiteListInfo(chanRec):
                print(f'Station not found for chan rec {chanRec}. This is very bad.')
                return None

            # swap in instype_id fk from abbrev list
            if not self.getAbbrevInfo(chanRec):
                print(f'Instype not found in IDA.abbrev for chan rec {chanRec}. This is very bad.')
                return None

        return self.dataList

    def getSiteListInfo(self, chanRec):
        """ looks up record in siteList for chanRec bu station 'code'.
            Retrieves elevation, latitude and longitude from site record
            and initializes chan level fields. """

        code = chanRec['fields']['station']
        startdt = float(chanRec['fields']['start_date'])
        enddt = float(chanRec['fields']['end_date'])

        sta = next((sta for sta in self.siteList 
            if (sta['fields']['code'] == code) and 
                ((startdt+1.0) > float(sta['fields']['start_date'])) and
                ((enddt-1.0) < float(sta['fields']['end_date']))), None)
        if sta:
            chanRec['fields']['station'] = sta["pk"]
            chanRec['fields']['elevation'] = sta['fields']['elevation']
            chanRec['fields']['longitude'] = sta['fields']['longitude']
            chanRec['fields']['latitude'] = sta['fields']['latitude']
        else:
            return False

        return True

    def getAbbrevInfo(self, chanRec):
        """ looks up record in abbrevList to obtain the FK. This FK will
            be used to retrieve 'sensor' description text instead of the 
            abbreviation that used to be stored in the datascope INSTYPE 
            field. """

        instype = chanRec['fields']['sensor']

        abv = next((abv for abv in self.abbrevList 
            if (abv['fields']['abbrev'] == instype)), None)
        if abv:
            chanRec['fields']['instype_id'] = abv["pk"]
        else:
            return False

        return True


class Instype(Table):

    # Initializer / Instance Attributes
    def __init__(self):
        self.djangoModel = 'stations.instype'
        self.tableName = "IDA.abbrev"
        self.fieldList = ["abbrev", "description"]
        self.ranges = ((0,6), (7,50))

    def jsonFilename(self):
        return 'IDA.instype.json'

    def extract(self):
        self.dataList = self.readTable(firstRecNdx=1)
        return self.dataList


class Seedloc(Table):

    # Initializer / Instance Attributes
    def __init__(self):
        self.djangoModel = 'stations.seedloc'
        self.tableName = "IDA.seedloc"
        self.fieldList = ["sta", "chn", "start_date", "endt", "seedchn", "loc", "lddate"]
        self.ranges = ((0,6), (7,8), (16,17), (34,17), (52,6), (59,2), (62,17))

class Stage(Table):

    # Initializer / Instance Attributes
    def __init__(self, chanList):
        self.djangoModel = 'stations.stage'
        self.tableName = "IDA.stage"
        self.fieldList = ["stacode", "chncode", "location", "start_date", "end_date", "stageid", "ssident", "gnom", "gcalib", "input_units", "output_units", "decimation_factor", "decimation_input_sample_rate", "dir", "dfile"]
        self.ranges = ((0,6), (7,8), (16,2), (19,17), (37,17), (55,8), (64,16), (81,11), (93,10), (104,16), (121,16), (147,8), (156,11), (180,64), (245,32))

    ######
    # NOTE: stage_gain = gnom * gcalib
    # NOTE: inoput nad output units will need to be converted using units table.
    ######

class Units(Table):

    # Initializer / Instance Attributes
    def __init__(self):
        self.djangoModel = 'stations.unit'
        self.tableName = "IDA.units"
        self.fieldList = ["unit", "desc"]
        self.ranges = ((0,16), (17,50))


################################################################################
if __name__ == '__main__':
    main()
