from kilo import *

from bibliopixel.animation import MatrixCalibrationTest
from matrix_animations import Bloom

from pad import pad
# from Snake import Snake
from Tetris import Tetris

import bibliopixel.log as log
log.setLogLevel(log.INFO)

data = {
    "A": (255,0,0),
    "B": (0,255,0),
    "X": (0,0,255),
    "Y": (128,0,64),
    "RED":(255,0,0)
}
pad.setLights(data)
anim = Tetris(led, pad)
try:
    anim.run(fps=30)
except KeyboardInterrupt:
    led.all_off()
    led.update()
