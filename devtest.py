import sys

dev = "COM5"

if len(sys.argv) > 1:
	dev = sys.argv[1]

from bibliopixel.drivers.serial_driver import *

print "DeviceID: {}".format(DriverSerial.getDeviceID(dev))
print "DeviceVer: {}".format(DriverSerial.getDeviceVer(dev))

