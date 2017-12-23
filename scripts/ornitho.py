####################################
#                                  #
#           DESCRIPTION            #
#                                  #
####################################
# this functions reads sightings from ornitho.de (.at etc. can be added too)
# these sightings are matched against a lifelist from ornitho.de
# the results (i.e. sightings which are not yet on your lifelist) are written into an html file
# the script can be found at goessinger.eu for more information send an email to paul (at) goessinger (dot) eu

#from lxml import etree
import requests, datetime, re, time
from bs4 import BeautifulSoup

####################################
#                                  #
#            FUNCTIONS             #
#                                  #
####################################

# stolen from github, rewrite maybe
# converts location from or to google maps
def dms2dec(dms_str):
    dms_str = re.sub(r'\s', '', dms_str)
    if re.match('[swSW]', dms_str):
        sign = -1
    else:
        sign = 1
    (degree, minute, second, frac_seconds, junk) = re.split('\D+', dms_str, maxsplit=4)
    return sign * (int(degree) + float(minute) / 60 + float(second) / 3600 + float(frac_seconds) / 36000)

# ornitho does not offer any API and the results are spread over several pages
# the first function will get the data from each page
def OrnithoGetPage(s, dataurl):
    htmlsource = s.get(dataurl)
    return htmlsource

# the function OrnithoGetSightings is used to read all sightings from http://ornitho.de/    
def OrnithoGetSightings(ornithopayload, ornithologin, ornithodataurl, pagenumber, ornithoSpecies, area):
    currentpage = pagenumber
    s = requests.Session()
    response = s.post(ornithologin, data=ornithopayload)
    dataurl = ornithodataurl + str(currentpage)
    soup = BeautifulSoup(OrnithoGetPage(s, dataurl).text, "lxml")
    all = soup.find_all("div")
    for item in all:
        divclass = str(item.get("class"))
        if "listSubmenu" in divclass:
            location = item.text
        if "listTop" in divclass:
            date = datetime.datetime.strptime(item.text, "%A, %d. %B %Y")
        if "listObservation" in divclass:
            content = item.find_all("span")
            for i in content:
                    urls = i.find_all("a")
                    for url in urls:
                        try:
                            if (url.next_element.get("alt") == "Beobachtung anzeigen"):
                                href = url.get("href")
                                source = "<a target=\"_blank\" href=\"" + href + "\">ornitho.de</a>"
                                ornithoSpecies.append([number, name, sciname, source, href, "pointnorth", "pointeast", location, date, area])
                        except:
                            continue
                    if "bodynocolor" in str(i.get("class")): 
                        if str(i.text[0]).istitle(): #if element is a birdname
                            name = str(i.text).split("(")[0].strip(" ") # we need to split since name & sciname are in one textfield
                            sciname = str(i.text).split("(")[1].strip(")") # remove the tailing "("
                            #find url
                        else: # runs first!
                            number = i.text.decode('unicode_escape').encode('ascii','ignore')
    #see if there are pages left to look at
    soup = BeautifulSoup(OrnithoGetPage(s, dataurl).text, "lxml")
    pagedata = soup.find_all("div", { "class" : "mpButton" } )
    pagelist = []
    for j in pagedata:
        try:    # not all entries are actuall numbers
            pagelist.append(int(j.text))
        except:
            continue
    pagelist = sorted(set(pagelist))
    try:
        if pagelist[-1] > currentpage: 
            currentpage += 1
            ornithoSpecies.append(OrnithoGetSightings(ornithopayload, ornithologin, ornithodataurl, currentpage, ornithoSpecies, area))
    except:
        pass
    return ornithoSpecies

# the function reads the location for each relevant sighting
def OrnithoGetLocations(ornithopayload, ornithologin, ornithorelevantSpecies):
    targets = []
    s = requests.Session()
    response = s.post(ornithologin, data=ornithopayload)
    for sighting in ornithorelevantSpecies:
        url = sighting[4]
        soup = BeautifulSoup(OrnithoGetPage(s, url).text, "lxml")
        # itterate through all div elements
        all = soup.find_all("div")
        for item in all:
            divclass = str(item.get("class"))
            if "box" in divclass:
                href = item.find_all("a")
                locurl = href[1].get("href")
                break
        # read location url to find data
        v = requests.Session()
        soup2 = BeautifulSoup(OrnithoGetPage(s, locurl).text, "lxml")
        all2 = soup2.find_all("table")
        for item in all2:
            tablewidth = str(item.get("width"))
            if "100%" in tablewidth:
                tables = item.find_all("table")
                for table in tables:
                    tablewidth = str(table.get("width"))
                    if "780" in tablewidth:
                        tables2 = table.find_all("table")
                        for table2 in tables2:
                            tablewidth = str(table2.get("width"))
                            if "98" in tablewidth:
                                m = re.findall("[0-9][0-9]*\xc2\xb0[0-9][0-9]*'[0-9][0-9]*.[0-9][0-9]''\s[E,N]", str(table2.text))
                                sighting[5] = dms2dec(m[1])
                                sighting[6] = dms2dec(m[0])
                                targets.append(sighting)
                break
    return targets

def ornithoGetSpecies(time, area, ornithopayload, ornithospecieslist):
    ornithologin = "http://www.ornitho." + area + "/index.php"
    ornithoSpecies = []
    targets = []
    for speciesid in ornithospecieslist:
        ornithodataurl = "http://www.ornitho." + area + "/index.php?m_id=94&sp_DChoice=offset&sp_DOffset=" + time + "&sp_S=" + str(speciesid) + "&submit=Abfrage+starten&mp_item_per_page=60&sp_SChoice=species&mp_current_page="
        ornithoSpecies = OrnithoGetSightings(ornithopayload, ornithologin, ornithodataurl, 1, ornithoSpecies, area)
    targets = OrnithoGetLocations(ornithopayload, ornithologin, ornithoSpecies)
    return targets

