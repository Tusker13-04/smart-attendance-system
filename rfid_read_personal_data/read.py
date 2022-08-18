import main
import network
import urequests
from os import uname
import connect
import dht
from machine import Pin

def do_read():
	connect.do_sync()

	rdr = main.MFRC522(0, 2, 4, 5, 14)


	print("")
	print("Place card before reader to read from address 0x08")
	print("")
	#timeT = 0
	#https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/04/dht_esp8266_bb.png?w=572&quality=100&strip=all&ssl=1 for pin config
	#sensor=dht.DHT11(Pin(13	))
	try:
		while True:

			(stat, tag_type) = rdr.request(rdr.REQIDL)
			#While im aware this is not good practice im still going to go ahead and do it cause im to lazy to implement it better
			'''if timeT >= 10000:
				do_sync()
				timeT=0
			else:
				timeT+=1'''

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
					print("New card detected")
					print("  - tag type: 0x%02x" % tag_type)
					print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print("")

					if rdr.select_tag(raw_uid) == rdr.OK:

						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
						nameusn=[]
						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							print("Address 8 data: %s" % rdr.read(8))
							for decimal in rdr.read(8):
								nameusn.append(str(chr(decimal)))
							print(("".join(nameusn)).replace('\n',''))
							nameUSN=("".join(nameusn)).replace('\n','')
							#sensor.measure()
							#temp=sensor.temperature()
							payload={'data':nameUSN}
							response = urequests.get(f"https://SmartAttendanceSystem-Server.prateekm2.repl.co",params=payload)
							print(response)
							rdr.stop_crypto1()
						else:
							print("Authentication error")
					else:
						print("Failed to select tag")

	except KeyboardInterrupt:
		print("Bye")


connect.do_connect()
do_read()