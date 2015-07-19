#Load driver for your hardware, visualizer just for example
# from bibliopixel.drivers.visualizer import DriverVisualizer
# driver = DriverVisualizer(num = 10)

from bibliopixel.drivers.serial_driver import *
driver = DriverSerial(LEDTYPE.GENERIC, 32*32, hardwareID = "16C0:0483", dev="")

import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

import bibliopixel.colors as colors

#load the LEDStrip class
from bibliopixel.led import *
led = LEDMatrix(driver, serpentine = False, threadedUpdate=True)

#load channel test animation
from bibliopixel.animation import MatrixCalibrationTest
anim = MatrixCalibrationTest(led)

try:
	anim.run()
finally:
	led.all_off()
	led.update()

time.sleep(0.1)