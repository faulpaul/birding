####################################
#                                  #
#           DESCRIPTION            #
#                                  #
####################################
# this functions reads sightings from otus-bayern.de
# the results are later written into an html file
# the script can be found at goessinger.eu for more information send an email to paul (at) goessinger (dot) eu

#from lxml import etree
import urllib
from datetime import datetime, timedelta

####################################
#                                  #
#            FUNCTIONS             #
#                                  #
####################################
def otusCleanLine(line):
    return(line.split("=")[1].replace("'", "").replace("\n", "").replace(";", "").strip())

def othusGetSightings(time):
    url = "http://www.otus-bayern.de/beobachtungen/aktuelle_beobachtungen.php"
    targets = [] #[number, name, sciname, source, href, lat, lng, location, date]
    number = ""
    sciname = ""
    source = "otus-bayern.de"
    href = "http://www.otus-bayern.de/beobachtungen/aktuelle_beobachtungen.php"
    i = 0
    mindate = datetime.today() - timedelta(days=time)
    req = urllib.request.urlopen(url)
    content = req.readlines()
    for line in content:
        line = line.decode('utf-8')
        if str("Beob[" + str(i) + "]['Titel']") in line:
            name = otusCleanLine(line)
        #if "Beob[0]['id']" in line:
        #    print(line)
        if str("Beob[" + str(i) + "]['Datum']") in line:
            date = datetime.strptime(otusCleanLine(line), '%d.%m.%Y') 
        if str("Beob[" + str(i) + "]['Ort']") in line:
            location = line.split("=")[1]
        #if "Beob[0]['Beobachter']" in line:
        #    print(line)
        if str("Beob[" + str(i) + "]['lat']") in line:
            lat = otusCleanLine(line)
        if str("Beob[" + str(i) + "]['lng']") in line:
            lng = otusCleanLine(line)
            targets.append([number, name, sciname, source, href, lat, lng, location, date, "DE"])
            if mindate <= date:
                i += 1
            else:
                return(targets)
