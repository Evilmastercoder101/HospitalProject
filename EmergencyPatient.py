



import csv
from datetime import *
from copy import deepcopy
allrows = []

def samedate(date, datetuple):
    currentmonth = int(''.join([date[i] for i in range(0, 2)]))
    currentday = int(''.join([date[i] for i in range(3, 5)]))
    currentyear = int(''.join([date[i] for i in range(6, len(date))]))

    tupleday = datetuple[2]
    tuplemonth = datetuple[1]
    tupleyear = datetuple[0]


    if tupleday == currentday and tuplemonth == currentmonth and tupleyear == currentyear:
        return True
    else:
        return False


def checkbyday(listofdata):
    # listofdata is the original copy, datalist is the deep copy
    datalist = deepcopy(listofdata)

    # get the first date in the list






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
    yesterdaydate = date(2011, 12, 11)
    # slaat nergens op xD
    for elem in datalist:

        today = elem[0]

        currentmonth = int(''.join([today[i] for i in range(0, 2)]))
        currentday = int(''.join([today[i] for i in range(3, 5)]))
        currentyear = int(''.join([today[i] for i in range(6, len(today))]))

        # make tomorrow:
        timer = timedelta(days=1)
        todaydate = date(currentyear, currentmonth, currentday)
        tomorrow = todaydate + timer

        # empty the elemlist var when going to the next day
        print(elem[0], todaydate)
        if not samedate(elem[0], yesterdaydate.timetuple()):
            elemlist = []




        if samedate(elem[0], todaydate.timetuple()):
            print("today is: ")
            print(today)
            elemlist.append([[elem[i] for i in tokeep]])
            elemlist.append([elem[j] for j in fatalities])
            daysdict[todaydate] = elemlist


        else:
            print("something is wrong!")
            break
        yesterdaydate = deepcopy(todaydate)
    return daysdict







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


# date, time, borough, zip, lat, long, latlongloc, onstreet, cross street, offstreet, injured, killed, injured, killed, injured, killed, injured, killed, factor, factor, factor
finaldaysdict = checkbyday(allrows)
for key in finaldaysdict:
    print(key, finaldaysdict[key])


# 0, 1, 2, 3, 6, 10, 11, 12, 13, 14, 15, 16, 17
