#!/usr/bin/env python

####################################
#                                  #
#           DESCRIPTION            #
#                                  #
####################################
# these functions handle file wirting etc.

import time

####################################
#                                  #
#            FUNCTIONS             #
#                                  #
####################################

def writeData(targets, maplat, maplng, zoomset, filenameJS, filenameHTML, path, fileCSS, googleAPI):
    #check if there are any sightings
    if targets: 
        #draw map
        contentmap = buildMap(targets, maplat, maplng, zoomset)
        writeFile(contentmap ,path + filenameJS)
        # write HTML file
        contenthtml = buildHTMLpage(targets, fileCSS, filenameJS, googleAPI)
        writeFile(contenthtml, path + filenameHTML)

def writeFile(content, filename):
    file = open(filename, "w")
    file.write(content)
    file.close()

def buildMap(targets, maplat, maplng, zoomset):
    i = 0
    birdVar = "var centerloc = {lat: " + maplat + ", lng: "+ maplng + "};\n var zoomset = " + str(zoomset) + "\n\n"
    birdVar += "var locations = ["
    for sight in targets:
        i += 1
        birdVar += "[\'" + str(sight[1]) +" (" + str(sight[0]) + ") " + "| " + "\'," + str(sight[5]) + "," + str(sight[6]) + "," + str(i) + "],\n"
    birdVar += "];"
    return birdVar

def buildHTMLpage(targetlist, fileCSS ,fileJS, googleAPI):
    sortedlist = []
    source = "<html><head>\n"
    source += "<title>Automatic generated sightings page</title>\n"
    source += "<link rel=\"stylesheet\" href=\"" + fileCSS + "\">\n"
    source += "<link rel=\"shortcut icon\" type=\"image/png\" href=\"./img/favicon.ico\">\n"
    source += "<meta charset=\"utf-8\">"
    source += "</head>\n"
    source += "<script src=\"sorttable.js\"></script>\n"
    source += "<script src=\"markerclusterer.js\" type=\"text/javascript\"></script>\n"
    source += "<script src=\"https://maps.googleapis.com/maps/api/js?v=3.exp&key=" + googleAPI + "\" type=\"text/javascript\"></script>\n"
    source += "<div class=\"date\">File generated: " + time.strftime("%Y/%m/%d @ %H:%M:%S") + "</div>\n"
    source += "<body id=birding><div id=header>All relevant sightings in your area:</div>\n"
    source += "<table class=\"sortable\">\n"
    sortedlist = [item[1] for item in targetlist]
    for name in set(sortedlist):
        source += "<tr> <td>"
        source += str(name)
        source += "</td> </tr>\n"
    source += "</table>\n"
    source += "<div id=\"map\"></div>\n"
    source += "<script src=\"" + fileJS + "\"></script> <script src=\"birdMap.js\"></script>\n"
    source += "<table class=\"sortable\">\n"
    source += "<tr><th>Datum</th><th>Land</th><th>Anzahl</th><th>Name</th><th>Wiss. Name</th><th>Ort</th><th>Quelle</th></tr>\n"
    for line in targetlist:
        try: target = [line[8], line[9], line[0], line[1], line[2], line[7], line[3]]  # date, land, number, commonname, sciencename, source, locationname,
        except: print(line)
        source += "<tr>"
        for column in target:
            source += "<td>"
            source += str(column)
            source += "</td>"
        source += "</tr>\n"
    source += "</table>\n"
    source += "<div class=\"footer\">Script can be found at <a href=\"http://goessinger.eu/\">goessinger.eu</a></div>\n"
    source += "</body></html>"
    return source

