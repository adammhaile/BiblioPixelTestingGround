import time, sys
import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

from bibliopixel.led import *
import bibliopixel.colors as colors

_useVis = len(sys.argv) > 1
drivers = []
gen = MultiMapBuilder()

if _useVis:
	from bibliopixel.drivers.visualizer import DriverVisualizer
	drivers = [DriverVisualizer(num=0, width=25, height=50, pixelSize=10, stayTop=True)]
	gen.addRow(mapGen(25, 50, serpentine=False))
else:
	from bibliopixel.drivers.serial_driver import *
	drivers.append(DriverSerial(LEDTYPE.NEOPIXEL, 25*25, c_order=ChannelOrder.RGB, deviceID=0))
	drivers.append(DriverSerial(LEDTYPE.NEOPIXEL, 25*25, c_order=ChannelOrder.RGB, deviceID=1))
	gen.addRow(mapGen(25, 25, rotation = MatrixRotation.ROTATE_90, vert_flip = True))
	gen.addRow(mapGen(25, 25, rotation = MatrixRotation.ROTATE_90, vert_flip = False))

#load the LEDStrip class
from bibliopixel.led import *
led = LEDMatrix(drivers, width=25, height=50, coordMap = gen.map, threadedUpdate=False)
if not _useVis:
	led.setMasterBrightness(128)
