from kilo import *

from bibliopixel.animation import MatrixCalibrationTest
from matrix_animations import Bloom

from pad import pad
from Snake import Snake
from Tetris import Tetris

import bibliopixel.log as log
log.setLogLevel(log.INFO)

choice = "snake"
if len(sys.argv) > 1:
    choice = sys.argv[1]

choices = {
    "snake":Snake(led, pad),
    "tetris":Tetris(led, pad)
}
anim = choices[choice]
try:
    anim.run(fps=30)
except KeyboardInterrupt:
    led.all_off()
    led.update()
    time.sleep(0.5)
    led.all_off()
    led.update()
    time.sleep(0.5)
