import main
import network
import urequests
from os import uname


def do_read():

	if uname()[0] == 'WiPy':
		rdr = main.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
	elif uname()[0] == 'esp8266':
		rdr = main.MFRC522(0, 2, 4, 5, 14)
	else:
		raise RuntimeError("Unsupported platform")

	print("")
	print("Place card before reader to read from address 0x08")
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
						nameusn=[]
						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							print("Address 8 data: %s" % rdr.read(8))
							for decimal in rdr.read(8):
								nameusn.append(str(chr(decimal)))
							print(("".join(nameusn)).replace('\n',''))
							response = urequests.get(f"https://webhook.site/aa19f85a-4e8f-4be7-bbea-04a4b4b66bed?tag={nameusn}")
							print(response.code)
							rdr.stop_crypto1()
						else:
							print("Authentication error")
					else:
						print("Failed to select tag")

	except KeyboardInterrupt:
		print("Bye")

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ssid', 'key')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

do_read()