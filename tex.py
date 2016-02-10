from bibliopixel import *
import bibliopixel.colors as colors
from bibliopixel.drivers.visualizer import DriverVisualizer
import bibliopixel.log as log
log.setLogLevel(log.DEBUG)
import time

from BiblioPixelAnimations.matrix.TallClock import TallClock
from BiblioPixelAnimations.matrix.ImageShow import ImageShow

driver = DriverVisualizer(width=25, height=50, pixelSize=10)
led = LEDMatrix(driver, serpentine=False, threadedUpdate=True)

anim = ImageShow(led, "G:/Testing/bttf.png", offset=(0,0))
anim.run(fps=10)
# anim = TallClock(led)
# anim.run(fps=30)

# anim = ImageDissolve(led, ["G:/Testing/anims/1.bmp", "G:/Testing/anims/2.bmp", "G:/Testing/anims/3.bmp", "G:/Testing/anims/4.bmp"], pixelRate=20)
# anim.run(fps=30, untilComplete=True)
