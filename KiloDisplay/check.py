from kilo import *

from bibliopixel.animation import MatrixCalibrationTest
from matrix_animations import Bloom

from GameTest import GameTest
from GamePadEmu import GamePadEmu
# from Snake import Snake
from Tetris import Tetris

import bibliopixel.log as log
log.setLogLevel(log.INFO)

pad = GamePadEmu()
anim = Tetris(led, pad)
try:
    anim.run(fps=30)
except KeyboardInterrupt:
    led.all_off()
    led.update()
