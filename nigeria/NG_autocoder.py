#
# NG_autocoder.py
#
# Extracts locations from csv and finds their Geonames matches for Nigeria DAD.
#

import urllib
import xml.etree.ElementTree as ET
import csv

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
    for elem in tree.iter(tag='toponymName'):
        matches.append([elem.text])
    for elem in tree.iter(tag='geonameId'):
        matches[i].extend([elem.text])
        i+=1
    return matches
        
def getLocData(numLocs, name, featureCode):
    ''' returns geonames matches for given location  '''
    url = "http://api.geonames.org/search?name_equals=" + name + "&country=NG" + "&featureCode=" + featureCode + "&username=dnicholson"
    matches = extractFromXML(url)
    if len(matches) < numLocs:
        url = "http://api.geonames.org/search?q=" + name + "&fuzzy=0.8" + "&country=NG" + "&featureCode=" + featureCode + "&username=dnicholson"
        fuzzyMatches = extractFromXML(url)
        if (len(matches) == 0) and (len(fuzzyMatches) == 0):
            return None
        else:
            return removeDuplicates(matches + fuzzyMatches)
    else:
        return removeDuplicates(matches)

def geonamesLocMatches(cell, featureCode):
    ''' returns list of geonames location matches for locations in given csv cell '''
    row = []
    if cell != "":
        cell = cell.split("; ")
        if "Unallocated" in cell:
            cell.remove("Unallocated")
        if "Unspecified" in cell:
            cell.remove("Unspecified")
        numLocs = len(cell)
        if numLocs > 0:
            for loc in cell:
                geonamesData = getLocData(numLocs, loc, featureCode)
                if geonamesData is not None:
                    row.extend(geonamesData)
    return row
        
def run():
    ''' reads csv file and calls functions to find geonames matches for locations within this file, writes original csv and found geonames matches to new csv '''
    f_read = open('nigeriaDAD.csv', 'r')
    f_write = open('nigeriaDAD_autocoded.csv', 'w')
    reader = csv.reader(f_read)
    writer = csv.writer(f_write)
    
    rownum = 0
    for row in reader:
        if rownum == 0:
            writer.writerow(row + ["LGA Geonames Matches", "State GeoNames Matches", "Country GeoNames Match"])
        else:
            state = row[11].strip()
            row_state = geonamesLocMatches(state, 'ADM1')
            if len(row_state) == 0:
                row_state = ""
            lga = row[12].strip()
            row_lga = geonamesLocMatches(lga, 'ADM2')
            if len(row_lga) == 0:
                row_lga = ""
            country = getLocData(1, 'Nigeria', 'PCLI')
            row.append(row_lga)
            row.append(row_state)
            row.append(country)
            writer.writerow(row)
        rownum += 1
    print 'finished writing to csv'


if __name__ == "__main__":
    run()
