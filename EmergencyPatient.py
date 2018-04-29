



import csv
from copy import deepcopy
allrows = []

def checkbyday(listofdata):
    # listofdata is the original copy, datalist is the deep copy
    datalist = deepcopy(listofdata)

    firstday = datalist[0][0]
    # first check if there are no days missing:
    # 0, 1, 2, 3, 6, 10, 11, 12, 13, 14, 15, 16, 17
    # keep the above indices
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
        if elem[0] == firstday:

            elemlist.append([elem[i] for i in tokeep])
            elemlist.append([elem[j] for j in fatalities])
            othertempdicto["data"] = [elem[i] for i in tokeep]
            tempdicto["fatalities"] = [elem[j] for j in fatalities]

            otherelemlist.append(othertempdicto)
            otherelemlist.append(tempdicto)

        daysdict[elem[0]] = elemlist
        daysdict2[elem[0]]= otherelemlist
    print(daysdict2)
    #for entry in datalist:


    print("###########")
    print(daysdict)









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
