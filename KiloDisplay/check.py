from kilo import *

from bibliopixel.animation import MatrixCalibrationTest
from matrix_animations import Bloom

from GameTest import GameTest
from GamePadEmu import GamePadEmu
from Snake import Snake

pad = GamePadEmu()
anim = Snake(led, pad)
try:
    anim.run(fps=30)
except KeyboardInterrupt:
    led.all_off()
    led.update()
