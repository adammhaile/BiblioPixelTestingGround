from kilo import led
from GamePadEmu import GamePadEmu
from Snake import Snake

if __name__ == "__main__":
    import time
    with GamePadEmu() as pad:
        anim = Snake(led, pad)
        try:
            anim.run(fps=30)
        except KeyboardInterrupt:
            led.all_off()
            led.update()
            time.sleep(1)
