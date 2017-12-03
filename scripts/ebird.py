####################################
#                                  #
#           DESCRIPTION            #
#                                  #
####################################
# this is a list of functions to read sightings from ebird.org
# these sightings are matched against a lifelist from ebird.org
# the results (i.e. sightings which are not yet on your lifelist) are written into an html file
# the script can be found at goessinger.eu for more information send an email to paul (at) goessinger (dot) eu
# all configuration is done in the main.py
import csv, urllib, datetime, time, requests
from lxml import etree

def ebirdGetLifelist(lifelist, ebirdpayload):
    ebirdLifelist = []
    #login
    #ebirdloginurl="https://secure.birds.cornell.edu/cassso/login"
    #ebirdlifelisturl="http://ebird.org/ebird/MyEBird?cmd=list&time=life&fmt=csv&rtype=country&r=" + lifelist
    #with requests.Session() as s:
    #    s.post(ebirdloginurl, data=ebirdpayload)
    #    download = s.get(ebirdlifelisturl)
#    decoded_content = download.content.decode('utf-8')
#    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    filename = "./lifelists/ebird_" + lifelist + "_life_list.csv"
    with open(filename, "rt") as mylist:
        reader = csv.reader(mylist)
        next(reader, None)
        for row in reader:
            ebirdLifelist.append(row[1].split(" - ")[1].strip(" "))
    return(ebirdLifelist)

def ebirdGetAllSpecies(ebirdlistspecies, region, area, time):
    #get a list off all species seen in the last X days
    ebirdSpecies = []
    # open connection
    ebirdlistspecies = ebirdlistspecies + "&back=" + time + "&rtype=" + region + "&r=" + area
    xmlsource = urllib.request.urlopen(ebirdlistspecies)
    context = etree.iterparse(xmlsource)
    for action, elem in context:
            if elem.tag == "sci-name":
                sciname = elem.text
            if elem.tag == "sighting":
                ebirdSpecies.append(sciname)
            if elem.getparent() is None: break #fix for bug 1185701
    xmlsource.close()
    return ebirdSpecies

def ebirdCompareSpecies(ebirdLifelist, ebirdSpecies):
    # compare seen species to lifelist
    # return the ones not yet on lifelist
    ebirdRelevantSpecies = []
    for j in ebirdLifelist:
        for i in ebirdSpecies:
            if (j == i) or ("(" in i) or (" x " in i) or ("Sylvia melanocephala" in i) or ("Monticola solitarius" in i) or ("Alectoris rufa" in i):
                 ebirdSpecies.remove(i)
    #return(ebirdRelevantSpecies)
    return(ebirdSpecies)        

def ebirdGetSightings(ebirdRelevantSpecies, ebirdlistallsightings, region, area, time):
    # get list of sightings for all relevant species
    ebirdTargets = []
    for species in ebirdRelevantSpecies:
        if ("," in species) or ("/" in species) or ("." in species):
            continue 
        url = ebirdlistallsightings + "&back=" + time + "&rtype=" + region + "&r=" + area +"&sci=" + species.replace(" ", "%20") #Leerzeichen zu %20 
        xmlsource = urllib.request.urlopen(url)
        context = etree.iterparse(xmlsource)
        for action, elem in context:
            if elem.tag == "loc-name":
                location = elem.text.rstrip()
			if elem.tag == "location-private":
			    location = "private"
            if elem.tag == "how-many":
                number = elem.text
            if elem.tag == "com-name":
                name = elem.text.replace("'", " ")
            if elem.tag == "sci-name":
                sciname = elem.text
            if elem.tag == "obs-dt":
                try: date = datetime.datetime.strptime(elem.text, "%Y-%m-%d %H:%M")
                except: date = datetime.datetime.strptime(elem.text, "%Y-%m-%d")
            if elem.tag == "lat":
               latitude = elem.text
            if elem.tag == "lng":
               longitude = elem.text
            if elem.tag == "sighting":
                source = "<a target=\"_blank\" href=\"" + url + "\">ebird.org</a>"
                try: ebirdTargets.append([number, name, sciname, source, url, latitude, longitude, location, date, area])
                except:
				    number = "x"
                    ebirdTargets.append([number, name, sciname, source, url, latitude, longitude, location, date, area])
            if elem.getparent() is None: break #fix for bug 1185701
    #xmlsource.close()
    return ebirdTargets

def ebirdGetArea(time, area, region, lifelist, ebirdlistspecies, ebirdlistallsightings, ebirdpayload):
    ebirdlifeList = []
    ebirdSpecies = []
    ebirdRelevantSpecies = []
    targets = []
    # get lifelist
    ebirdLifelist = ebirdGetLifelist(lifelist, ebirdpayload)
    # get all sighted species in the last X days
    ebirdSpecies = ebirdGetAllSpecies(ebirdlistspecies, region, area, time)
    # return all species sighted that are not in the lifelist
    ebirdRelevantSpecies = ebirdCompareSpecies(ebirdLifelist, ebirdSpecies)
    # search all sightings of the target species in the last 7 days
    targets = ebirdGetSightings(ebirdRelevantSpecies, ebirdlistallsightings,region, area, time)
    return targets
