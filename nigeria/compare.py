#
# compare.py
#
# Compares project locations coded by Autocoder and correct locations from Toolkit.
#

import csv

def outputCSV(matching, auto, compare):
    ''' write comparison data to csv '''
    with open('compare.csv', 'w') as f:
        writer = csv.writer(f)
        # incorrect indicates not ni 
        writer.writerow(['Project ID', 'Toolkit Locations Found by Autocoder', 'All Toolkit Locations', 'All Autocoder Locations', 'Percentage Correct of Locations Found by Autocoder', 'Percentage Incorrect of Locations Found by Autocoder'])
        for row in matching:
            numCFound = len([x for x in auto[row[0]] if x in compare[row[0]]])
            numIFound = len([x for x in auto[row[0]] if x not in compare[row[0]]])
            numTotal = len(auto[row[0]])
            pCFound = 100 * float(numCFound)/float(numTotal)
            pIFound = 100 * float(numIFound)/float(numTotal)
            writer.writerow([row[0], compare[row[0]], row[1], auto[row[0]], "%.2f" % pCFound, "%.2f" % pIFound])
    
def compareLocs(matching):
    ''' build dictionary with project ID as key and matching locations from autocoder and toolkit as value '''
    compare = {}
    auto = {}
    for row in matching:
        # search for autocoder location matches in toolkit in order of precision
        # if autocoder found ADM2 locations, look for ADM2 matches in toolkit
        if len(row[2][0]) != 0:
            compare[row[0]] = sorted(list(set(row[2][0]).intersection(row[1])))
            auto[row[0]] = row[2][0]
        # if autocoder found ADM1 locations and no ADM2 locations or ADM2 location matches, look for ADM1 matches in toolkit
        if (row[0] not in compare.keys()) and (len(row[2][1]) != 0):
            compare[row[0]] = sorted(list(set(row[2][1]).intersection(row[1])))
            auto[row[0]] = row[2][1]
        elif (row[0] in compare.keys()) and (len(compare[row[0]]) == 0):
            compare[row[0]] = sorted(list(set(row[2][1]).intersection(row[1])))
            auto[row[0]] = row[2][1]
        # if autocoder found no ADM1 or ADM2 locations or no ADM1 or ADM2 location matches, look for country matches in toolkit
        if (row[0] not in compare.keys()) or (len(compare[row[0]]) == 0):
            compare[row[0]] = sorted(list(set(row[2][2]).intersection(row[1])))
            auto[row[0]] = row[2][2]
    outputCSV(matching, auto, compare)

def strip(loclist):
    ''' convert list of location codes into ordered list of integers '''
    output = []
    for x in loclist:
        if x != "":
            output.append(int(x))
    return sorted(output)
            
def findMatchingProjs(tk, auto):
    ''' build list of project ID, toolkit location codes, and autocoder location codes '''
    tk.sort()
    auto.sort()
    matching = []
    for rowTK in tk:
        for rowA in auto:
            if rowTK[0] == rowA[0]:
                matching.append([rowTK[0], strip(rowTK[12].split(",")), [strip(rowA[20].split(",")), strip(rowA[22].split(",")), strip(rowA[23].split(","))]])
                break
    compareLocs(matching)

def readCSV():
    ''' read project data from toolkit and autocoder csvs '''
    with open('nigeria_toolkit.csv', 'r') as f:
        reader = csv.reader(f)
        tk = []
        id_tk = []
        rownum = 0
        for row in reader:
            if rownum != 0:
                tk.append(row)
                id_tk.append(row[0].strip())
            rownum += 1

    with open('nigeria_autocode.csv', 'r') as f:
        reader = csv.reader(f)
        auto = []
        id_auto = []
        rownum = 0
        for row in reader:
            if rownum != 0:
                auto.append(row)
                id_auto.append(row[0].strip())
            rownum += 1
    findMatchingProjs(tk, auto)

            
if __name__ == "__main__":
    readCSV()
            
