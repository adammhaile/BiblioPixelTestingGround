import time
from bibliopixel import *
from bibliopixel.drivers.visualizer import DriverVisualizer

driver = DriverVisualizer(width=25, height=50, pixelSize=15)
led = LEDMatrix(driver, width=0, height=0, serpentine=False, threadedUpdate=False)

from BiblioPixelAnimations.matrix.bloom import Bloom
from BiblioPixelAnimations.matrix.GameOfLife import GameOfLife
from BiblioPixelAnimations.matrix.MatrixRain import MatrixRain

from bibliopixel.animation import AnimationQueue
anim = AnimationQueue(led)

try:
    anim.addAnim(anim=Bloom(led), amt=6, fps=None, max_steps=30)
    anim.addAnim(anim=GameOfLife(led), fps=30, untilComplete=True)
    anim.addAnim(anim=MatrixRain(led), fps=30, max_steps=30*5)
    anim.run(untilComplete=False, threaded=True, fps=15)
    while not anim.stopped():
        print "Running..."
        time.sleep(1)
except:
    anim.stopThread(wait=True)
finally:
    led.all_off()
    led.update()
    print "Done!"
