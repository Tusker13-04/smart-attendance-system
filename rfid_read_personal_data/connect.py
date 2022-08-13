import ntptime
import time
#if needed, overwrite default time server 
ntptime.host = "1.in.pool.ntp.org"
ssid="ssid"
key="key"
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

def do_sync():
    try:
        print("Local time before synchronization: %s" %str(time.localtime())) #make sure to have internet connection 
        ntptime.settime()
        print("Local time after synchronization: %s" %str(time.localtime()))
    except:
        do_connect()