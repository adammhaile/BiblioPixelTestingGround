#Load driver for your hardware, visualizer just for example
from bibliopixel import *
from bibliopixel.animation import *
from bibliopixel.drivers.visualizer import DriverVisualizer
from bibliopixel.drivers.serial_driver import *


import bibliopixel.log as log
log.setLogLevel(log.DEBUG)

from bibliopixel.led import *

from BiblioPixelAnimations.matrix import opencv_video

#driver = DriverSerial(LEDTYPE.LPD8806, num = 32*32, dev="COM7")
driver = DriverVisualizer(width=25, height=50, pixelSize=10, stayTop=True)
led = LEDMatrix(driver, serpentine = isinstance(driver, DriverVisualizer), threadedUpdate=True)
led.setMasterBrightness(255)
try:
    anim = opencv_video.OpenCVVideo(led, videoSource = "getlucky.avi", mirror = True, offset = 0.0, crop=True, useVidFPS=True)
    anim.run()#fps=10)#fps = 30)
except KeyboardInterrupt:
    led.all_off()
    led.update()
    time.sleep(0.1)

