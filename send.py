from bibliopixel.drivers.network import DriverNetwork
from bibliopixel.led import LEDMatrix
from matrix_animations import *
from bibliopixel import *
log.setLogLevel(log.DEBUG)

#must init with same number of pixels as receiver
w = 32	
h = 32
driver = DriverNetwork(w*h, port=1618)
led = LEDMatrix(driver, width=w, height=h, vert_flip=False, serpentine=False, threadedUpdate=False)

from bibliopixel.animation import MatrixCalibrationTest
anim = MatrixCalibrationTest(led)
try:
	anim = Bloom(led, dir=True)
	anim.run(amt=6)#, fps = 60)
except KeyboardInterrupt:
	led.all_off()
	led.update()