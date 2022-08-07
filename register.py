import json


with open(r"data.json", "r") as f:
    content = json.loads(f.read())

name = input("Name: ")
usn = input("Usn: ")
uid = input("Uid: ")

content[usn] = {"name": name, "uid": uid, "entries": [], "inSchool": False}

newContent = json.dumps(content)

with open(r"data.json", "w") as f:
    f.write(newContent)
