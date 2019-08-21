# module for reading data from ebird
# comparing it to a csv life list
# an returning the sightings

import csv, requests, datetime, os.path
from ebird.api import get_observations

# read life list
def ebirdGetLifeList(region):
    ebirdLifeList = []
    filename = "./lifelists/ebird_" + region + "_life_list.csv"
    if not os.path.exists(filename):
        filename = "./lifelists/ebird_world_life_list.csv"
    with open(filename, "rt") as mylist:
       reader = csv.reader(mylist)
       next(reader, None)
       for row in reader:
          ebirdLifeList.append(row[1].split(" - ")[1].strip(" "))
    return(ebirdLifeList)

# get list of observations in the region
def ebirdGetAllObservations(region, time, ebirdkey, ebirdlocale):
    ebirdAllObservations = get_observations(ebirdkey, region, back=time, locale=ebirdlocale)
    return(ebirdAllObservations)

# compare ebirdLifeList and ebirdAllObservations and return the ones not on the ebirdLifeList
def ebirdCompareSpecies(ebirdLifeList, ebirdAllObservations):
    for j in ebirdLifeList:
        for i in ebirdAllObservations:
            sciName = i["sciName"]
            if (j == sciName) or ("(" in sciName) or (" x " in sciName) or ("." in sciName) or ("/" in sciName):
                ebirdAllObservations.remove(i)
    return(ebirdAllObservations)   

# get the data in the right format to put it on a google map
# original structure: {'lng': 8.2904298, 'locName': 'Mainz, Volkspark', 'howMany': 2, 'sciName': 'Psittacula krameri', 'obsValid': True, 'locationPrivate': True, 'obsDt': '2018-03-17 08:35', 'obsReviewed': False, 'comName': 'Rose-ringed Parakeet', 'lat': 49.9877824, 'locID': 'L6362779', 'locId': 'L6362779'}
# target structure: [number, name, sciname, source, url, latitude, longitude, location, date, area]
def ebirdCleanData(ebirdTargets, region):
    ebirdCleanTargets = []
    for species in ebirdTargets:
        try: number = species["howMany"]
        except: number = "x"
        name = species["comName"].replace("'","`") #some names include ' that will break the java script later on
        sciname = species["sciName"]
        source = "<a target=\"_blank\" href=ebird.org>ebird.org</a>"
        url = "ebird.org"
        latitude = species["lat"]
        longitude = species["lng"]
        location = species["locName"]
        try: date = datetime.datetime.strptime(species["obsDt"], "%Y-%m-%d %H:%M")
        except: date = datetime.datetime.strptime(species["obsDt"], "%Y-%m-%d")
        area = region
        ebirdCleanTargets.append([number, name, sciname, source, url, latitude, longitude, location, date, area])
    return(ebirdCleanTargets)

def ebirdGetArea(region, time, ebirdkey, ebirdlocale):
    ebirdLifeList = ebirdGetLifeList(region)
    ebirdAllObservations = ebirdGetAllObservations(region, time, ebirdkey, ebirdlocale)
    ebirdTargets = ebirdCompareSpecies(ebirdLifeList, ebirdAllObservations)
    ebirdCleanTargets = ebirdCleanData(ebirdTargets, region)
    return(ebirdCleanTargets)
