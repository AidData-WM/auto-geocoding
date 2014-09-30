#
# NG_compare.py
#
# Compares project locations coded by Autocoder and Toolki for Nigeria DAD. 
#

import csv

def outputCSV(matching, auto, compare):
    ''' write comparison data to csv '''
    with open('compare.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Project ID', 'Toolkit Locations Found by Autocoder', 'All Toolkit Locations', 'All Autocoder Locations', 'Percentage of Toolkit Locations Found by Autocoder', 'All Locations Found?'])
        for row in matching:
            allFound = (compare[row[0]] == row[1])
            numFound = len(compare[row[0]])
            numTotal = len(row[1])
            pFound = 100 * float(numFound)/float(numTotal)
            writer.writerow([row[0], compare[row[0]], row[1], auto[row[0]], "%.2f" % pFound, allFound])
    
def compareLocs(matching):
    ''' build dictionary with project ID as key and matching locations from autocoder and toolkit as value '''
    compare = {}
    auto = {}
    for row in matching:
        if len(row[2][0]) != 0:
            compare[row[0]] = sorted(list(set(row[2][0]).intersection(row[1])))
            auto[row[0]] = row[2][0]
        elif len(row[2][1]) != 0:
            compare[row[0]] = sorted(list(set(row[2][1]).intersection(row[1])))
            auto[row[0]] = row[2][1]
            
        if (row[0] in compare.keys()) and (len(compare[row[0]]) == 0):
            compare[row[0]] = sorted(list(set(row[2][0]+row[2][1]).intersection(row[1])))
            auto[row[0]] = sorted(row[2][0] + row[2][1])
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
            
