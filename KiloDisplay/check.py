from kilo import *

from bibliopixel.animation import MatrixCalibrationTest
from matrix_animations import Bloom

from pad import pad
from Snake import Snake
from Tetris import Tetris

import bibliopixel.log as log
log.setLogLevel(log.INFO)

anim = Snake(led, pad)
try:
    anim.run(fps=30)
except KeyboardInterrupt:
    led.all_off()
    led.update()
