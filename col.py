from bibliopixel.drivers.serial_driver import *
from bibliopixel import *

driver = DriverSerial(type=LEDTYPE.NEOPIXEL, num=25*25, c_order=ChannelOrder.GRB)
led = LEDMatrix(driver, width=25, height=25, serpentine=True, threadedUpdate=True, masterBrightness=64)

from BiblioPixelAnimations.matrix.bloom import Bloom
import time

anim = Bloom(led, dir=True)

try:
    anim.run(fps=30, amt=6)
except:
    led.all_off()
    led.update()
    time.sleep(1)
