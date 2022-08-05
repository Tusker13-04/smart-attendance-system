import serial
import threading
import json
from datetime import datetime
import time

timeThreshold = 600
arduino = serial.Serial(port="COM3", baudrate=9600)
timeouts = {}


def update():
    while 1:
        for i in timeouts.keys():
            if timeouts[i]["tick"] >= timeThreshold:
                timeouts[i]["updateAble"] = True
                timeouts[i]["tick"] = 0
            else:
                timeouts[i]["tick"] += 1
        time.sleep(1)


def updateEntry(fil, usn, uid):
    data = fil.read()
    data = json.loads(data)
    now = datetime.now()
    currUser = data[usn]
    current_time = now.strftime("%d:%m%y:%H:%M:%S")
    currUser["uid"] = uid
    if bool(currUser["inSchool"]):
        currUser["entries"][len(currUser["entries"]) - 1]["end"] = current_time
        currUser["inSchool"] = "0"
    else:
        currUser["entries"].append({"start": current_time})
        currUser["inSchool"] = "1"
    data = json.dumps(data)
    fil.write(data)

ticker = threading.Thread(target=update)
ticker.start()
uid = ""
nameUsn = []
with open("data.json") as file:
    while True:
        line = str(arduino.readline())
        
        
        if "uid" in line.lower():
            uid = line.split(":")[1]
        if "name" in line.lower():
            nameUsn = line.split(":")[1].split(";")
            if nameUsn[1] in timeouts.keys():
                if timeouts[nameUsn[1]]["updateAble"]:
                    updateEntry(file, nameUsn[1], uid)
                else:
                    print(f"cooldown not yet finished for {nameUsn[0]}")
            else:
                print("no user with this usn....")


            uid = ""
            name = []





