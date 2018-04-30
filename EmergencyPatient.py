



import csv
from datetime import *
from copy import deepcopy
allrows = []

def countperfifteen(listofkeys, totalvictimtimeslot):
    finalslotdicto = {}
    currenttimeslots = []
    hours = []
    minutes = []
    for firstelem in listofkeys:
        hours = []
        minutes = []
        print(firstelem)
        boole = True
        boolemins = True
        i = 0
        while boole:
            hours.append(firstelem[i])
            if firstelem[i] == ":":
                boole = False
            i += 1
        j = len(firstelem)-1
        while boolemins:
            print(j)
            minutes.append(firstelem[j])
            if firstelem[j] == ":":
                boolemins = False
            j -= 1
        print(hours)
        hours.pop()
        newhours = int(''.join(hours))
        print(newhours)
        print(hours)
        print(minutes)
        minutes.pop()
        minutes.reverse()
        print(minutes)
        newminutes = int(''.join(minutes))
        timenow = time(newhours, newminutes, 0)

        currenttimeslots.append(timenow)
    print(currenttimeslots)



    for slot in currenttimeslots:
        print(slot)
    a = datetime(year=2017, month=1, day=1, minute=0)
    for i in range(0,20*4):
        print("THIS IS THE ITERATION")
        print(i)
        listofslots = []
        b = a + timedelta(minutes=15.0)  # days, seconds, then other fields.
        print(a, b)
        # move 15 mins
        a = b
        groupedslots = []
        for indexer in range(0, 15):
            groupedslots.append(a + timedelta(minutes = float(indexer)))
        for gslot in groupedslots:
            # make them in hh mm ss format
            gslot = time(gslot.hour, gslot.minute, gslot.second)

        for slot in currenttimeslots:
            temptime = time(slot.hour, slot.minute, slot.second)
            for gslot in groupedslots:
                if temptime.hour == gslot.hour and temptime.minute == gslot.minute:
                    print("YAYAYAYAYAY")
                    print(temptime, gslot)
                    listofslots.append(temptime)
        # TODO Make the stuff the right object since now time objects vs not time objcts as kyes
        finalslotdicto[(a,b)] = [totalvictimtimeslot[slot] for slot in listofslots]
    print(finalslotdicto)
    for key in finalslotdicto:
        print("hey")
        for subkey in finalslotdicto[key]:
            print(subkey)





    print("#################################")
    for slot in groupedslots:
        print(slot)









    print(b.time())

    print(a)
    print(b)

def countvictimspertimeslot(nestedlist):
    sum = 0


            # injured killed injured killed injured killed
            # find the amount of people injured

    for j in range(0, len(nestedlist), 2):
        # this is where we count the victims: take all the injuries and sum them. TODO we can also see the type of accident, and from there decide the treatment time
        sum += int(nestedlist[j])
    return sum

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

# data, fatal list, data, fatal list, etc...
victimpertimeslotdicto = {}
# loop over the days (key)
timeslot = ""
totalvictimtimeslot = {}
for key in finaldaysdict:
#    countvictimspertimeslot(finaldaysdict[key])
    # loop over the accidents (nestedlist)
    for index in range(0, len(finaldaysdict[key])):
        if index%2 == 0:
            print("first list xD")
            print(finaldaysdict[key][index+1])
            print("second list xDD")
            print(finaldaysdict[key][index])
            print(countvictimspertimeslot(finaldaysdict[key][index+1]))
            timeslot = finaldaysdict[key][index][0][1]
            count = countvictimspertimeslot(finaldaysdict[key][index+1])
            print("Timeslot")
            print(timeslot)

            if timeslot not in totalvictimtimeslot:
                totalvictimtimeslot[timeslot] = count
            else:
                totalvictimtimeslot[timeslot] += count


            if timeslot not in victimpertimeslotdicto:
                victimpertimeslotdicto[timeslot] = []
                victimpertimeslotdicto[timeslot].append((countvictimspertimeslot(finaldaysdict[key][index+1]), finaldaysdict[key][index], finaldaysdict[key][index+1]))
            else:
                victimpertimeslotdicto[timeslot].append((countvictimspertimeslot(finaldaysdict[key][index+1]), finaldaysdict[key][index], finaldaysdict[key][index+1]))


# victimpertimeslotdicto gives every accident and its data, given a key of a timeslot
# totalvictimtimeslot gives the total amount of patients injured at a certain timeslot
sum = 0
for timeslot in totalvictimtimeslot:
    if totalvictimtimeslot[timeslot] > 12:
        print(timeslot)
print(victimpertimeslotdicto["14:20"])
print(totalvictimtimeslot["14:20"])
templist = list(totalvictimtimeslot.keys())
templist.sort()
print(templist)
countperfifteen(templist, totalvictimtimeslot)




# 0, 1, 2, 3, 6, 10, 11, 12, 13, 14, 15, 16, 17
