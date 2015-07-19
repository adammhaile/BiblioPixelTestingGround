from kilo import *

from bibliopixel.animation import MatrixCalibrationTest
from matrix_animations import Bloom
anim = MatrixCalibrationTest(led)
anim = Bloom(led)
try:
    anim.run(amt=6, fps=60)
except KeyboardInterrupt:
    led.all_off()
    led.update()
