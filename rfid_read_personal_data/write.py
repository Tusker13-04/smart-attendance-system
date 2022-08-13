import main
from os import uname
import connect

def do_write():

	if uname()[0] == 'WiPy':
		rdr = main.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
	elif uname()[0] == 'esp8266':
		rdr = main.MFRC522(0, 2, 4, 5, 14)
	else:
		raise RuntimeError("Unsupported platform")

	print("")
	print("Place card before reader to write address 0x08")
	print("")
    

	try:
		while True:

			(stat, tag_type) = rdr.request(rdr.REQIDL)

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
					print("New card detected")
					print("  - tag type: 0x%02x" % tag_type)
					print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print("")

					if rdr.select_tag(raw_uid) == rdr.OK:

						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
						#TODO: Add a few checks for name and usn. ie: to check if they have a semicolon or if USN is of specific format
						name=input("Enter Name: ")
						usn = input("Enter USN: ")
						nameusn = name + ';' + usn
						if(len(nameusn)<16):
							nameusn=nameusn+'\n'*(16-len(nameusn))
						elif len(nameusn>16):
							#Cutting it short to only LAST 16 charecters so parts of name will be cutoff but USN remains intact
							nameusn=nameusn[16:]
						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							stat = rdr.write(8, bytes(nameusn,'utf-8'))
							nameUSN=nameusn+';'+str(raw_uid[0])+' ' +str(raw_uid[1])+' ' + str(raw_uid[2]) + ' ' + str(raw_uid[3])
							response = urequests.get(f"https://SmartAttendanceSystem-Server.prateekm2.repl.co?data={nameUSN}")
							rdr.stop_crypto1()
							if stat == rdr.OK:
								print("Data written to card")
							else:
								print("Failed to write data to card")
						else:
							print("Authentication error")
					else:
						print("Failed to select tag")

	except KeyboardInterrupt:
		print("Bye")
connect.do_connect()
do_write()