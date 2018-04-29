



import csv
from datetime import *
from copy import deepcopy
allrows = []




def checkbyday(listofdata):
    # listofdata is the original copy, datalist is the deep copy
    datalist = deepcopy(listofdata)

    # get the first date in the list
    today = datalist[0][0]

    currentday = int(''.join([today[i] for i in range(0, 2)]))
    currentmonth = int(''.join([today[i] for i in range(3, 5)]))
    currentyear = int(''.join([today[i] for i in range(6, len(today))]))

    print(currentday)
    print(currentmonth)
    print(currentyear)

    # make tomorrow:
    timer = timedelta(days = 1)
    todaydate = date(currentyear,currentmonth,currentday)
    tomorrow = todaydate + timer
    tomorrowtuple = tomorrow.timetuple()

    print("TOMORROWTUPLE##############")
    print(tomorrowtuple[0])
    print(tomorrowtuple[1])
    print(tomorrowtuple[2])





    # first check if there are no days missing:

    # 0, 1, 2, 3, 6, 10, 11, 12, 13, 14, 15, 16, 17
    # keep the indices below

    tokeep = [0, 1, 2, 3, 6]
    # date, time, borough, zip, loc

    fatalities = [10, 11, 12, 13, 14, 15, 16, 17]
    # injured, killed, injured, killed, injured, killed, injured, killed,

    elemlist = []
    daysdict = {}
    daysdoubledict = {}
    tempdicto = {}
    othertempdicto = {}
    otherelemlist = []
    daysdict2 = {}
    for elem in datalist:
        tempdicto["data"] = None
        tempdicto["fatalities"] = None
        if elem[0] == today:
            elemlist.append([[elem[i] for i in tokeep]])
            elemlist.append([elem[j] for j in fatalities])
            daysdict[elem[0]] = elemlist
        elif elem[0] == tomorrow:
            print("hey")
    for key in daysdict:
        print(key)
        print("key")
    print(daysdict["04/03/2018"])







with open('NYPD_Motor_Vehicle_Collisions.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[2] == "QUEENS":
            allrows.append(row)

x = 0
y = 0
# location of the hospital:
# There are 62 hospitals in new york


hospitalxy = (x,y)
for row in allrows:
    print(row)
    print("\n")
# date, time, borough, zip, lat, long, latlongloc, onstreet, cross street, offstreet, injured, killed, injured, killed, injured, killed, injured, killed, factor, factor, factor
print(checkbyday(allrows))

# 0, 1, 2, 3, 6, 10, 11, 12, 13, 14, 15, 16, 17
