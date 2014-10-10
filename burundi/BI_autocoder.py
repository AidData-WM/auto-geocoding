# -*- coding: utf-8 -*-

import urllib
import xml.etree.ElementTree as ET
import csv

dict = {}

def removeDuplicates(values):
    ''' returns given list with removed duplicates '''
    output = []
    seen = set()
    valueID = [x[1] for x in values]
    i = 0
    for id in valueID:
        if id not in seen:
            output.append(values[i])
            seen.add(id)
        i += 1
    return output

def extractFromXML(url):
    ''' returns information from geonames API XML doc at given URL '''
    matches = []
    i = 0
    tree = ET.parse(urllib.urlopen(url))
    for elem in tree.iter(tag='name'):
        matches.append([elem.text])
    for elem in tree.iter(tag='geonameId'):
        matches[i].extend([int(elem.text)])
        i+=1
    return matches
        
def getLocData(numLocs, name, featureCode):
    ''' returns geonames matches for given location  '''
    url = "http://api.geonames.org/search?name_equals=" + name + "&country=BI" + "&featureCode=" + featureCode + "&username=dnicholson"
    matches = extractFromXML(url)
    if len(matches) < numLocs:
        url = "http://api.geonames.org/search?q=" + name + "&fuzzy=0.8" + "&country=BI" + "&featureCode=" + featureCode + "&username=dnicholson"
        fuzzyMatches = extractFromXML(url)
        if (len(matches) == 0) and (len(fuzzyMatches) == 0):
            return None
        else:
            return removeDuplicates(matches + fuzzyMatches)
    else:
        return removeDuplicates(matches)

def geonamesLocMatches(cell, featureCode):
    ''' returns list of geonames location matches for locations in given csv cell '''
    cellMatches = []
    if cell != "":
        cell = cell.split("; ")
        cell = [x.strip().lower() for x in cell]
        if "non spécifié" in cell:
            cell.remove("non spécifié")
        numLocs = len(cell)
        if numLocs > 0:
            for loc in cell:
                if loc in dict:
                    cellMatches.extend(dict[loc])
                else:
                    geonamesData = getLocData(numLocs, loc, featureCode)
                    if geonamesData is not None:
                        dict[loc] = geonamesData
                        cellMatches.extend(dict[loc])
    return cellMatches
        
def run():
    ''' reads csv file and calls functions to find geonames matches for locations within this file, writes original csv and found geonames matches to new csv '''
    f_read = open('burundiDAD.csv', 'r')
    f_write = open('burundiDAD_autocoded2.csv', 'w')
    reader = csv.reader(f_read)
    writer = csv.writer(f_write)
    
    rownum = 0
    for row in reader:
        if rownum == 0:
            writer.writerow(row + ["ADM2 Geonames Matches", "ADM1 Geonames Matches"])
        else:
            ADM1 = row[17].strip()
            row_ADM1 = geonamesLocMatches(ADM1, 'ADM1')
            if len(row_ADM1) == 0:
                row_ADM1 = ""
            ADM2 = row[18].strip()
            row_ADM2 = geonamesLocMatches(ADM2, 'ADM2')
            if len(row_ADM2) == 0:
                row_ADM2 = ""
            row.append(row_ADM2)
            row.append(row_ADM1)
            writer.writerow(row)
        rownum += 1
    print "finished writing csv"

if __name__ == "__main__":
    run()
