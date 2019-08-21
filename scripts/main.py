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

# import python modules
import locale
from datetime import datetime
from configparser import ConfigParser

# import functions
from div import *
from ebird_functions import *
#from ornitho import *
#from otus import *

# setting utf-8 encoding
#reload(sys) 
#sys.setdefaultencoding('utf8')

# set german weekdays
#loc = locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

####################################
#                                  #
#         CONFIG SECTION           #
#                                  #
####################################
# get configuration
config = ConfigParser()
config.read("./birding.ini")
path = config.get('SectionGeneral', 'path')
fileCSS  = config.get('SectionGeneral', 'fileCSS')
googleAPI = config.get('SectionGeneral', 'googleAPI')
ornithodeuser = config.get('SectionOrnithode', 'user')
ornithodepass = config.get('SectionOrnithode', 'pass')
ornithodelist = config.get('SectionOrnithode', 'list')
ebirduser = config.get('SectionEbird', 'user')
ebirdpass = config.get('SectionEbird', 'pass')
ebirdkey = config.get('SectionEbird', 'key')
ebirdlocale = config.get('SectionEbird', 'locale')

#ornitho.de
ornithodepayload = { "login":"1", "USERNAME":ornithodeuser, "REMEMBER":"ON", "PASSWORD":ornithodepass }
ornithoatspecieslist = [ 2000, 1336, 137, 136, 55, 52, 1594, 53, 1502, 73, 70, 1371, 1016, 1017, 72, 1499, 71, 57, 1595, 58, 1598, 69, 63, 64, 66, 65, 62, 1006, 67, 59, 74, 77, 78, 79, 80, 83, 75, 110, 109, 105, 84, 97, 107, 108, 99, 96, 98, 93, 114, 89, 87, 102, 100, 90, 91, 116, 120, 124, 135, 132, 131, 130, 129, 133, 1079, 1081, 134, 1603, 127, 128, 126, 139, 140, 142, 141, 189, 1156, 186, 185, 1127, 192, 184, 183, 182, 181, 187, 1082, 1563, 1320, 45, 46, 1094, 51, 49, 50, 1593, 48, 1104, 9, 6, 7, 1506, 1, 2, 1591, 3, 4, 1145, 1084, 17, 19, 1128, 1528, 10, 12, 11, 13, 14, 1107, 16, 1214, 20, 22, 21, 23, 25, 27, 44, 1059, 588, 43, 36, 31, 32, 35, 41, 169, 143, 162, 161, 168, 159, 160, 156, 157, 1537, 1542, 153, 154, 152, 1197, 1011, 164, 147, 1319, 145, 146, 1020, 149, 176, 177, 175, 170, 1393, 172, 171, 178, 1155, 195, 194, 193, 1504, 206, 589, 196, 197, 200, 198, 199, 203, 204, 259, 209, 215, 216, 1102, 1540, 590, 211, 210, 1037, 1036, 221, 1408, 226, 1073, 1074, 1607, 240, 239, 237, 1092, 258, 257, 256, 234, 235, 229, 1130, 231, 1262, 251, 1023, 252, 1291, 1026, 1027, 1707, 1025, 245, 246, 247, 1022, 248, 260, 261, 262, 1605, 265, 266, 264, 267, 263, 304, 299, 300, 301, 1266, 1135, 302, 268, 287, 285, 1070, 283, 580, 591, 277, 269, 270, 280, 276, 278, 272, 1609, 1159, 1068, 1162, 1357, 1416, 1071, 1069, 1610, 1417, 1116, 291, 288, 1513, 290, 297, 1117, 298, 295, 294, 305, 534, 1121, 1306, 1613, 1205, 537, 569, 536, 566, 539, 1330, 1042, 313, 324, 320, 318, 319, 316, 317, 1018, 321, 1167, 325, 326, 328, 1009, 331, 1083, 333, 335, 341, 338, 339, 340, 489, 488, 1065, 587, 1481, 1482, 1483, 1486, 369, 366, 1174, 1172, 1044, 374, 375, 376, 343, 1435, 345, 348, 350, 353, 352, 1200, 379, 377, 1477, 416, 450, 449, 1098, 1100, 451, 445, 448, 1321, 1099, 452, 1096, 454, 1356, 453, 1621, 1246, 1077, 418, 427, 424, 423, 425, 1179, 430, 432, 1061, 428, 444, 436, 435, 1468, 437, 441, 442, 440, 1342, 1344, 1343, 439, 455, 456, 1254, 485, 383, 381, 382, 1639, 385, 492, 1001, 384, 1615, 406, 405, 415, 407, 1178, 574, 409, 1133, 410, 1618, 412, 414, 413, 1619, 1620, 543, 443, 457, 460, 459, 403, 1111, 386, 392, 387, 1078, 389, 390, 1448, 395, 1244, 398, 400, 401, 1456, 402, 1087, 462, 461, 1440, 1106, 496, 549, 550, 464, 1007, 465, 466, 1008, 467, 463, 468, 469, 470, 474, 484, 477, 479, 480, 478, 482, 473, 519, 498, 513, 511, 1496, 576, 512, 508, 517, 516, 515, 507, 503, 505, 1706, 504, 506, 1520, 532, 533, 522, 526, 528, 527, 1624, 530, 529, 1362, 523, 524, 525, 1088, 1093 ]

# List or european countries
europe = ["AL", "AD", "AM", "AT", "AZ", "BY", "BE", "BA", "BG", "FR", "HR", "CY", "CZ", "DK", "EE", "FI", "GE", "GR", "HU", "IE", "IS", "IT", "KZ", "XK", "LV", "LI", "LT", "LU", "MK", "MT", "MD", "MC", "ME", "NL", "NO", "PL", "PT", "RO", "SM", "RS", "SK", "SI", "ES", "SE", "CH", "UA", "UK", "VA"]

####################################
#                                  #
#            FUNCTIONS             #
#                                  #
####################################

def main():
    print("=======================================================")
    print("script startet @ " + str(datetime.datetime.now()))
    ############ Germany from ebird, ornitho.de & otus
    targetsGermany = ebirdGetArea("DE", "7", ebirdkey, ebirdlocale) 
    #targetsGermany += ornithoGetSpecies("7", "de", ornithodepayload, ornithodelist)
    #targetsGermany += othusGetSightings(7) #time
    writeData(targetsGermany, "47.86", "11.28", "7", "germanyJS.js", "germany.html", path, fileCSS, googleAPI)
    print("finished Germany @ " + str(datetime.datetime.now()))

    ############ Austria from ebird & ornitho.at
    #targetsAustria = ebirdGetArea("AT", "7")
    #targetsAustria = ornithoGetSpecies("7", "at", ornithodepayload, ornithoatspecieslist)
    #writeData(targetsAustria, "47.86", "11.28", "7", "austriaJS.js", "austria.html", path, fileCSS, googleAPI)
    #print("finished austria @ " + str(datetime.datetime.now()))

    ############ Europe from ebird
    targetsEurope = []
    for country in europe:
        targetsEurope += ebirdGetArea(country, "7", ebirdkey, ebirdlocale)
    writeData(targetsEurope, "47.86", "11.28", "4", "europeJS.js", "europe.html", path, fileCSS, googleAPI)
    print("finished Europe @ " + str(datetime.datetime.now()))

    ############ Southafrika, Lesotho, Swasiland
    targetsSA = ebirdGetArea("ZA", "7", ebirdkey, ebirdlocale)
    targetsSA += ebirdGetArea("LS", "7", ebirdkey, ebirdlocale)
    targetsSA += ebirdGetArea("SZ", "7", ebirdkey, ebirdlocale)
    writeData(targetsSA, "-30.50", "20.43", "4", "SAJS.js", "SA.html", path, fileCSS, googleAPI)
    print("finished southern Africa @ " + str(datetime.datetime.now()))

    ############ Oman, Israel, Egypth from ebird
    #targetsOman = ebirdGetArea("OM", "7")
    #writeData(targetsOman, "20.83", "56.89", "7", "omanJS.js", "oman.html", path, fileCSS, googleAPI)
    #targetsIsrael = ebirdGetArea("IL", "7")
    #writeData(targetsIsrael, "31.76", "35.21", "7", "israelJS.js", "israel.html", path, fileCSS, googleAPI)
    #targetsEgypt = ebirdGetArea("EG", "7")
    #writeData(targetsEgypt, "30.97", "27.43", "7", "EgyptJS.js", "Egypt.html", path, fileCSS, googleAPI)

    ############ USA from ebird
    #targetsUSAwest = ebirdGetArea("US-NV", "7")
    #targetsUSAwest += ebirdGetArea("US-CA", "7")
    #targetsUSAwest += ebirdGetArea("US-TX", "7")
    #writeData(targetsUSAwest, "36.18", "-115.33", "7", "USAwest.js", "USAwest.html", path, fileCSS, googleAPI)
    #targetsUSAeast = ebirdGetArea("US-NJ", "7")
    #targetsUSAeast += ebirdGetArea("US-NY", "7")
    #writeData(targetsUSAeast, "36.18", "-115.33", "7", "USAeast.js", "USAeast.html", path, fileCSS, googleAPI)

    ############ Thailand from ebird
    targetThailand = ebirdGetArea("TH", "7", ebirdkey, ebirdlocale)
    writeData(targetThailand, "36.18", "-115.33", "7", "Thailand.js", "Thailand.html", path, fileCSS, googleAPI)
    print("finished Thailand @ " + str(datetime.datetime.now()))

    ############ create menue
    writeMenu(path)
    print("script finished @ " + str(datetime.datetime.now()))
    print("=======================================================")

if __name__ == "__main__":
    main()
