# module for reading data from ebird
# comparing it to a csv life list
# an returning the sightings

import csv, requests, datetime, os.path
from ebird.api import region_observations, region_species

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

# get list of observed species in the region
def ebirdGetAllSpecies(region, time):
    ebirdAllSpecies = region_observations(region, back=time, provisional=True)
    return(ebirdAllSpecies)

# compare ebirdLifeList and eBirdAllSpecies and return the ones not on the ebirdLifeList
def ebirdCompareSpecies(ebirdLifeList, ebirdAllSpecies):
    for j in ebirdLifeList:
        for i in ebirdAllSpecies:
            sciName = i["sciName"]
            if (j == sciName) or ("(" in sciName) or (" x " in sciName) or ("." in sciName) or ("/" in sciName) or ("Sylvia melanocephala" in sciName) or ("Monticola solitarius" in sciName) or ("Alectoris rufa" in sciName):
                ebirdAllSpecies.remove(i)
    return(ebirdAllSpecies)   

# get all sightings of the last "time" days in "region" that are not on the lifelist
def ebirdGetSightings(ebirdRelevantSpecies, region, time):
    ebirdTargets = []
    for species in ebirdRelevantSpecies:
        sciName = species["sciName"]
        answer = region_species(sciName, region)
        for line in answer:
            ebirdTargets.append(line)
    return(ebirdTargets)

# get the data in the right format to put it on a google map
# original structure: {'lng': 8.2904298, 'locName': 'Mainz, Volkspark', 'howMany': 2, 'sciName': 'Psittacula krameri', 'obsValid': True, 'locationPrivate': True, 'obsDt': '2018-03-17 08:35', 'obsReviewed': False, 'comName': 'Rose-ringed Parakeet', 'lat': 49.9877824, 'locID': 'L6362779', 'locId': 'L6362779'}
# target structure: [number, name, sciname, source, url, latitude, longitude, location, date, area]
def ebirdCleanData(ebirdTargets, region):
    ebirdCleanTargets = []
    for species in ebirdTargets:
        try: number = species["howMany"]
        except: number = "x"
        name = species["comName"]
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

def ebirdGetArea(region, time):
    ebirdLifeList = ebirdGetLifeList(region)
    ebirdAllSpecies = ebirdGetAllSpecies(region, time)
    ebirdRelevantSpecies = ebirdCompareSpecies(ebirdLifeList, ebirdAllSpecies)
    ebirdTargets = ebirdGetSightings(ebirdRelevantSpecies, region, time)
    ebirdCleanTargets = ebirdCleanData(ebirdTargets, region)
    return(ebirdCleanTargets)
