#!/usr/bin/env python

####################################
#                                  #
#           DESCRIPTION            #
#                                  #
####################################
# this script reads sightings from ornitho.de (.at etc. can be added too) and
# these sightings are matched against a lifelist from the same site
# the results (i.e. sightings which are not yet on your lifelist) are written into an html file
# the script can be found at goessinger.eu for more information send an email to paul (at) goessinger (dot) eu

##### WARNING: the script will load a lot of webpages, so be patient!!!!

# Todo
# login in eigene funktion

# import Python packages
import locale, requests, datetime, re, time, csv, urllib
from bs4 import BeautifulSoup
from lxml import etree
from configparser import ConfigParser
from importlib import reload
requests.packages.urllib3.disable_warnings()

# import functions
from div import *
from ebird import *
from ornitho import *
from otus import *

# setting utf-8 encoding
#reload(sys) 
#sys.setdefaultencoding('utf8')

# set german weekdays
loc= locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

####################################
#                                  #
#         CONFIG SECTION           #
#                                  #
####################################
# get configuration
config = ConfigParser()
config.read("/scripts/birding.ini")
path = config.get('SectionGeneral', 'path')
fileCSS  = config.get('SectionGeneral', 'fileCSS')
ornithodeuser = config.get('SectionOrnithode', 'user')
ornithodepass = config.get('SectionOrnithode', 'pass')
ebirduser = config.get('SectionEbird', 'user')
ebirdpass = config.get('SectionEbird', 'pass')

#ornitho.de
ornithodepayload = { "login":"1", "USERNAME":ornithodeuser, "REMEMBER":"ON", "PASSWORD":ornithodepass }
ornithodespecieslist = [ 137,136,1594,73,1371,1016,1017,1499,57,58,64,65,62,1006,67,59,74,78,79,80,83,75,105,84,97,107,108,99,96,98,93,89,87,102,100,90,91,116,120,124,135,132,130,1079,1081,127,128,139,1156,186,185,1127,192,188,184,181,187,1082,1563,1094,51,49,50,48,1104,6,4,1084,17,19,1128,10,12,11,13,14,1107,16,20,22,21,23,25,27,44,43,37,32,35,143,162,161,159,160,156,157,153,152,1011,155,164,1319,1020,149,176,175,170,1393,172,171,178,1155,195,194,1504,206,589,199,203,204,259,255,1102,1540,590,211,210,1037,1036,221,222,1408,1073,1074,239,237,1092,256,234,235,229,1130,251,1023,252,1291,1026,243,1027,244,1707,1025,245,246,247,1022,250,248,260,261,262,1605,265,266,264,263,304,299,300,301,1135,302,286,268,285,1070,283,580,591,277,269,280,278,1068,1162,1357,1416,1071,279,1069,1417,1116,289,297,1117,295,305,534,311,1121,1306,1613,1205,537,536,566,539,1330,1042,313,315,324,320,318,316,323,1018,1167,326,328,1009,331,330,1083,489,488,1065,587,1481,1482,1483,1486,1174,1172,1044,343,1435,345,350,352,416,1098,1100,451,448,1321,1099,452,1096,454,1356,453,1621,1077,418,420,427,424,425,430,432,1061,428,444,434,435,1468,441,442,440,1342,1344,1343,439,485,492,1001,1615,406,405,1178,409,1133,410,1618,413,1619,1620,543,443,403,1111,392,387,1078,390,1448,398,400,401,1456,402,1087,1440,1106,549,550,464,1007,465,466,1008,470,484,477,479,480,478,482,473,513,576,517,516,1706,506,1520,532,533,522,526,528,1624,530,529,1362,523,524,525,1088,1093 ]
ornithoatspecieslist = [ 2000, 1336, 137, 136, 55, 52, 1594, 53, 1502, 73, 70, 1371, 1016, 1017, 72, 1499, 71, 57, 1595, 58, 1598, 69, 63, 64, 66, 65, 62, 1006, 67, 59, 74, 77, 78, 79, 80, 83, 75, 110, 109, 105, 84, 97, 107, 108, 99, 96, 98, 93, 114, 89, 87, 102, 100, 90, 91, 116, 120, 124, 135, 132, 131, 130, 129, 133, 1079, 1081, 134, 1603, 127, 128, 126, 139, 140, 142, 141, 189, 1156, 186, 185, 1127, 192, 184, 183, 182, 181, 187, 1082, 1563, 1320, 45, 46, 1094, 51, 49, 50, 1593, 48, 1104, 9, 6, 7, 1506, 1, 2, 1591, 3, 4, 1145, 1084, 17, 19, 1128, 1528, 10, 12, 11, 13, 14, 1107, 16, 1214, 20, 22, 21, 23, 25, 27, 44, 1059, 588, 43, 36, 31, 32, 35, 41, 169, 143, 162, 161, 168, 159, 160, 156, 157, 1537, 1542, 153, 154, 152, 1197, 1011, 164, 147, 1319, 145, 146, 1020, 149, 176, 177, 175, 170, 1393, 172, 171, 178, 1155, 195, 194, 193, 1504, 206, 589, 196, 197, 200, 198, 199, 203, 204, 259, 209, 215, 216, 1102, 1540, 590, 211, 210, 1037, 1036, 221, 1408, 226, 1073, 1074, 1607, 240, 239, 237, 1092, 258, 257, 256, 234, 235, 229, 1130, 231, 1262, 251, 1023, 252, 1291, 1026, 1027, 1707, 1025, 245, 246, 247, 1022, 248, 260, 261, 262, 1605, 265, 266, 264, 267, 263, 304, 299, 300, 301, 1266, 1135, 302, 286, 268, 287, 285, 1070, 283, 580, 591, 277, 269, 270, 280, 276, 278, 272, 1609, 1159, 1068, 1162, 1357, 1416, 1071, 279, 1069, 1610, 1417, 1116, 291, 288, 1513, 290, 297, 1117, 298, 295, 294, 305, 534, 1121, 1306, 1613, 1205, 537, 569, 536, 566, 539, 1330, 1042, 313, 324, 320, 318, 319, 316, 317, 1018, 321, 1167, 325, 326, 328, 1009, 331, 1083, 333, 335, 341, 338, 339, 340, 489, 488, 1065, 587, 1481, 1482, 1483, 1486, 369, 366, 1174, 1172, 1044, 374, 375, 376, 343, 1435, 345, 348, 350, 353, 352, 1200, 379, 377, 1477, 416, 450, 449, 1098, 1100, 451, 445, 448, 1321, 1099, 452, 1096, 454, 1356, 453, 1621, 1246, 1077, 418, 427, 424, 423, 425, 1179, 430, 432, 1061, 428, 444, 436, 435, 1468, 437, 441, 442, 440, 1342, 1344, 1343, 439, 455, 456, 1254, 485, 383, 381, 382, 1639, 385, 492, 1001, 384, 1615, 406, 405, 415, 407, 1178, 574, 409, 1133, 410, 1618, 412, 414, 413, 1619, 1620, 543, 443, 457, 460, 459, 403, 1111, 386, 392, 387, 1078, 389, 390, 1448, 395, 1244, 398, 400, 401, 1456, 402, 1087, 462, 461, 1440, 1106, 496, 549, 550, 464, 1007, 465, 466, 1008, 467, 463, 468, 469, 470, 474, 484, 477, 479, 480, 478, 482, 473, 519, 498, 513, 511, 1496, 576, 512, 508, 517, 516, 515, 507, 503, 505, 1706, 504, 506, 1520, 532, 533, 522, 526, 528, 527, 1624, 530, 529, 1362, 523, 524, 525, 1088, 1093 ]

#ebird.org
ebirdpayload = { "username":ebirduser, "password":ebirdpass}
ebirdloginurl="https://secure.birds.cornell.edu/cassso/login"
ebirdlifelisturl = "http://ebird.org/ebird/MyEBird?cmd=list&time=life&fmt=csv&rtype=country&r=DE"
ebirdlistspecies = "http://ebird.org/ws1.1/data/obs/region/recent?maxResults=10000&locale=de_DE&fmt=xml&includeProvisional=true"
ebirdlistallsightings = "http://ebird.org/ws1.1/data/obs/region_spp/recent?maxResults=10000&locale=de_DE&fmt=xml&includeProvisional=true&" #larus%20delawarensis

# List or european countries
europe = ["AL", "AD", "AM", "AT", "AZ", "BY", "BE", "BA", "BG", "FR", "HR", "CY", "CZ", "DK", "EE", "FI", "GE", "GR", "HU", "IE", "IS", "IT", "KZ", "XK", "LV", "LI", "LT", "LU", "MK", "MT", "MD", "MC", "ME", "NL", "NO", "PL", "PT", "RO", "SM", "RS", "SK", "SI", "ES", "SE", "CH", "UA", "UK", "VA"]

####################################
#                                  #
#            FUNCTIONS             #
#                                  #
####################################

def main():
    ############ Germany from ebird, ornitho.de & otus
    targetsGermany = ebirdGetArea("7", "DE", "country", "DE", ebirdlistspecies, ebirdlistallsightings, ebirdpayload)#time in days, area, lifelist
    targetsGermany += ornithoGetSpecies("7", "de", ornithodepayload, ornithodespecieslist)
    targetsGermany += othusGetSightings(7) #time
    writeData(targetsGermany, "47.86", "11.28", "7", "germanyJS.js", "germany.html", path, fileCSS)

    ############ Austria from ebird & ornitho.at
    targetsAustria = ebirdGetArea("7", "AT", "country", "AT", ebirdlistspecies, ebirdlistallsightings, ebirdpayload)#time in days, area, lifelist
    targetsAustria = ornithoGetSpecies("7", "at", ornithodepayload, ornithoatspecieslist)
    writeData(targetsAustria, "47.86", "11.28", "7", "austriaJS.js", "austria.html", path, fileCSS)

    ############ Europe from ebird
    targetsEurope = []
    for country in europe:
        targetsEurope += ebirdGetArea("7", country, "country", "eur", ebirdlistspecies, ebirdlistallsightings, ebirdpayload)
        #time in days, area, lifelist BOSNIEN
    writeData(targetsEurope, "47.86", "11.28", "4", "europeJS.js", "europe.html", path, fileCSS)

    ############ Oman, Israel, Egypth from ebird
    targetsOman = ebirdGetArea("7", "OM", "country", "world", ebirdlistspecies, ebirdlistallsightings, ebirdpayload)#time in days, area, lifelist OMAN
    writeData(targetsOman, "20.83", "56.89", "7", "omanJS.js", "oman.html", path, fileCSS)
    targetsIsrael = ebirdGetArea("7", "IL", "country", "world", ebirdlistspecies, ebirdlistallsightings, ebirdpayload)#time in days, area, lifelist ISRAEL
    writeData(targetsIsrael, "31.76", "35.21", "7", "israelJS.js", "israel.html", path, fileCSS)
    targetsEgypt = ebirdGetArea("7", "EG", "country", "world", ebirdlistspecies, ebirdlistallsightings, ebirdpayload)#time in days, area, lifelist ISRAEL
    writeData(targetsEgypt, "30.97", "27.43", "7", "EgyptJS.js", "Egypt.html", path, fileCSS)

    ############ USA  from ebird
    targetsUSA = ebirdGetArea("7", "US-NV", "subnational1", "US", ebirdlistspecies, ebirdlistallsightings, ebirdpayload)#time in days, area, lifelist NEVADA
    targetsUSA += ebirdGetArea("7", "US-CA", "subnational1", "US", ebirdlistspecies, ebirdlistallsightings, ebirdpayload)#time in days, area, lifelist CALIFORNIA
    #targetsUSA += ebirdGetArea("7", "US-TX", "subnational1", "US", ebirdlistspecies, ebirdlistallsightings, ebirdpayload)#time in days, area, lifelist TEXAS
    writeData(targetsUSA, "36.18", "-115,33", "7", "usaJS.js", "usa.html", path, fileCSS)

if __name__ == "__main__":
    main()
