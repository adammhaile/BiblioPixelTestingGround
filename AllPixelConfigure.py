import sys
from bibliopixel import *
from bibliopixel.drivers.serial_driver import *

types = [
		[LEDTYPE.GENERIC, "GENERIC"],
		[LEDTYPE.LPD8806, "LPD8806"],
		[LEDTYPE.WS2801 , "WS2801 "],
		[LEDTYPE.NEOPIXEL, "WS2812/NEOPIXEL"],
		[LEDTYPE.APA104 , "APA104"],
		[LEDTYPE.WS2811_400, "WS2811_400"],
		[LEDTYPE.TM1809 , "TM1809/TM1804"],
		[LEDTYPE.TM1803 , "TM1803 "],
		[LEDTYPE.UCS1903, "UCS1903"],
		[LEDTYPE.SM16716, "SM16716"],
		[LEDTYPE.APA102 , "APA102/DOTSTAR"],
		[LEDTYPE.LPD1886, "LPD1886"],
		[LEDTYPE.P9813, "P9813"]
	]

def O(msg):
	print "\n" + msg

def I(msg):
	return raw_input("\n" + msg)

def get_int(msg, invalid = -1):
	v = I(msg)
	try:
		return int(v)
	except:
		return invalid

def showSelectList(msg, values):
	print "\n" + msg
	shift = len(str(len(values)))
	count = 0
	for v in values:
		print "{}: {}".format(str(count).rjust(shift), v)
		count += 1
	return get_int("Choice: ")

try:
	print "Press Ctrl+C anytime to quit."

	O("Scanning for devices...")

	DriverSerial.foundDevices = []
	devs = DriverSerial.findSerialDevices()

	d = ""
	if len(devs) == 0:
		I("No devices found! Please connect one and press any key...")
		raise ValueError()
	elif len(devs) > 1:
		d = showSelectList("Select device:", devs)
		if d < 0 or d >= len(devs): 
			O("Invalid choice!")
			raise ValueError()
		d = devs[d]
	else:
		d = devs[0]

	t = showSelectList("Choose LED Type", [v[1] for v in types])
	if t < 0 or t >= len(types):
		O("Invalid choice!")
		raise ValueError()
	t = types[t]

	num = get_int("Number of LEDs: ", invalid=0)
	if num <= 0:
		O("Invalid choice!")
		raise ValueError()

	spi = 2
	useSPI = t[0] in SPIChipsets
	if useSPI:
		spi = get_int("SPI Speed (1-24): ", invalid=0)
		if spi <= 0:
			O("Invalid choice!")
			raise ValueError()

	details = "Device: {}\nLED Type: {}\nNum LEDs: {}".format(d, t[1], num)
	if useSPI:
		details += "\nSPI Speed: {}".format(spi)

	O(details + "\n")

	driver = None
	try:
		driver = DriverSerial(t[0], num, dev=d, SPISpeed=spi, restart_timeout=6)
		O("Configure complete!")
	except BiblioSerialError, e:
		O("Error configuring device!")

	

except KeyboardInterrupt:
	sys.exit(128 + signal.SIGINT)
except ValueError, e:
	pass


