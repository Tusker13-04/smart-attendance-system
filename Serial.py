import serial

import json
from datetime import datetime


timeThreshold = 600
arduino = serial.Serial(port="COM3", baudrate=9600)
filePath = r"data.json"


def checkTime(t1, t2):
    global timeThreshold
    t1 = datetime(int(t1[0]), int(t1[1]), int(t1[2]), int(t1[3]), int(t1[4]), int(t1[5]))
    print(t1.strftime("%Y:%m:%d:%H:%M:%S"))
    print(t2.strftime("%Y:%m:%d:%H:%M:%S"))
    diff = (t2 - t1).total_seconds()
    print(f"difference is {diff}")
    if diff <= timeThreshold:
        return True
    else:
        return False


def updateEntry(usn, uid):
    global filePath
    with open(filePath, "r") as fil:
        data = fil.read()
        print(data)
    data = json.loads(data)
    now = datetime.now()
    if usn in data.keys():
        currUser = data[usn]
    else:
        print(usn, "is not in the database")
        print("User Not Registered")
        return
    current_time = now.strftime("%Y:%m:%d:%H:%M:%S")
    currUser["uid"] = uid
    if currUser["inSchool"]:
        lastTimeEntry = currUser["entries"][len(currUser["entries"]) - 1]["start"].split(":")
        print(lastTimeEntry)
        if not checkTime(lastTimeEntry, now):
            currUser["entries"][len(currUser["entries"]) - 1]["end"] = current_time
            currUser["inSchool"] = False
            print(data)
        else:
            print("cool down need")
            return
    else:
        lastTimeEntry = currUser["entries"][len(currUser["entries"]) - 1]["end"].split(":")
        print(lastTimeEntry)
        if not checkTime(lastTimeEntry, now):
            print("cool down not needed")
            currUser["entries"].append({"start": current_time})
            currUser["inSchool"] = True
            print(data)
        else:
            print("cool down needed")
            return

    with open(filePath, "w") as fil1:
        data = json.dumps(data)
        fil1.write(data)


uid = ""
nameUsn = []


while True:
    line = str(arduino.readline())
    if "uid" in line.lower():
        uid = line.split(":")[1]
    if "name" in line.lower():

        nameUsn = line.split(":")[1].split(";")
        usn=nameUsn[1]
        usn = usn[0:len(usn)-5]
        print(usn,"<--usn")
        print(nameUsn,"<---nameUsn")
        updateEntry(usn, uid)
        uid = ""
        nameUsn = []

