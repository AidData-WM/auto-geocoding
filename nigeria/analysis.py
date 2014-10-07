#
# analysis.py
#
# Produces statistics on accuracy of Autocoder compared to Toolkit.
#

import csv
import numpy

def getStats():
    f = open('NG_compare.csv', 'r')
    reader = csv.reader(f)
    correct = []
    incorrect = []
    allFound = 0
    incorrectFound = 0
    noneFound = 0
    total = 0
    rownum = 0
    for row in reader:
        if rownum != 0:
            correct.append(float(row[4]))
            incorrect.append(float(row[5]))
            if row[4] == '100.00':
                allFound += 1
            if row[5] == '100.00':
                noneFound += 1
            if row[5] != '0.00':
                incorrectFound += 1
            total += 1
        rownum += 1
    correctAvg = numpy.mean(correct)
    incorrectAvg = numpy.mean(incorrect)
    pAllFound = 100 * float(allFound)/float(total)
    pNoneFound = 100 * float(noneFound)/float(total)
    pIncorrectFound = 100 * float(incorrectFound)/float(total)
    outputStats(correctAvg, incorrectAvg, pAllFound, pNoneFound, pIncorrectFound)

def outputStats(correctAvg, incorrectAvg, pAllFound, pNoneFound, pIncorrectFound):
    fw = open('NG_analysis.csv', 'w')
    writer = csv.writer(fw)
    writer.writerow(['Description', 'Percentage'])
    writer.writerow(['Average percentage of correct locations per project found by autogeocoder', "%.2f" % correctAvg])
    writer.writerow(['Average percentage of incorrect locations per project found by autogeocoder', "%.2f" % incorrectAvg])
    writer.writerow(['Projects with all correct locations found by autogeocoder out of total projects', "%.2f" % pAllFound])
    writer.writerow(['Projects with no correct locations found by autogeocoder out of total projects', "%.2f" % pNoneFound])
    writer.writerow(['Projects with some incorrect locations found by autogeocoder out of total projects', "%.2f" % pIncorrectFound])


if __name__ == "__main__":
    getStats()
    
