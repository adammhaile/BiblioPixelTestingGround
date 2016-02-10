try:
    import serial
    import serial.tools.list_ports
except ImportError as e:
    error = "Please install pyserial 2.7+! pip install pyserial"
    raise ImportError(error)

from distutils.version import LooseVersion

if LooseVersion(serial.VERSION) < LooseVersion('2.7'):
    error = "pyserial v{} found, please upgrade to v2.7+! pip install pyserial --upgrade".format(
        serial.VERSION)
    log.logger.error(error)
    raise ImportError(error)

import logging
log = logging.getLogger()


class CMDTYPE:
    INIT = 0
    GET = 42


class RETURN_CODES:
    SUCCESS = 255
    ERROR = 0
    ERROR_SIZE = 1
    ERROR_UNSUPPORTED = 2
    ERROR_BAD_CMD = 4


class SerialError(Exception):
    pass


class MSGEQ7(object):
    foundDevices = []

    def __init__(self, lower_threshold=75, dev="", hardwareID="1B4F:9206"):
        self._hardwareID = hardwareID
        self._com = None
        self.dev = dev
        self.interp_map = [max(
            0, (((i - lower_threshold) * 255) / (255 - lower_threshold))) for i in range(256)]

        resp = self._connect()
        if resp != RETURN_CODES.SUCCESS:
            MSGEQ7._printError(resp)

    def close(self):
        if self._com != None:
            log.info("Closing connection to: " + self.dev)
            self._com.close()

    def __exit__(self, type, value, traceback):
        self.close()

    @staticmethod
    def findSerialDevices(hardwareID="1B4F:9206"):
        hardwareID = "(?i)" + hardwareID  # forces case insensitive
        if len(MSGEQ7.foundDevices) == 0:
            MSGEQ7.foundDevices = []
            for port in serial.tools.list_ports.grep(hardwareID):
                MSGEQ7.foundDevices.append(port[0])

        return MSGEQ7.foundDevices

    @staticmethod
    def _printError(error):
        msg = "Unknown error occured."
        if error == RETURN_CODES.ERROR_SIZE:
            msg = "Data packet size incorrect."
        elif error == RETURN_CODES.ERROR_UNSUPPORTED:
            msg = "Unsupported configuration attempted."
        elif error == RETURN_CODES.ERROR_BAD_CMD:
            msg = "Unsupported protocol command. Check your device version."

        log.error("{}: {}".format(error, msg))
        raise SerialError(msg)

    @staticmethod
    def _comError():
        error = "There was an unknown error communicating with the device."
        log.error(error)
        raise IOError(error)

    def _connect(self):
        try:
            if(self.dev == ""):
                MSGEQ7.findSerialDevices(self._hardwareID)

                if len(MSGEQ7.foundDevices) > 0:
                    self.dev = MSGEQ7.foundDevices[0]
                    log.info("Using COM Port: {}".format(self.dev))

            try:
                self._com = serial.Serial(self.dev, timeout=5)
            except serial.SerialException as e:
                print e
                ports = MSGEQ7.findSerialDevices(self._hardwareID)
                error = "Invalid port specified. No COM ports available."
                if len(ports) > 0:
                    error = "Invalid port specified. Try using one of: \n" + \
                        "\n".join(ports)
                log.info(error)
                raise SerialError(error)

            packet = MSGEQ7._generateHeader(CMDTYPE.INIT, 0)
            self._com.write(packet)

            resp = self._com.read(1)
            if len(resp) == 0:
                MSGEQ7._comError()

            return ord(resp)

        except serial.SerialException as e:
            error = "Unable to connect to the device. Please check that it is connected and the correct port is selected."
            log.exception(e)
            log.error(error)
            raise e

    @staticmethod
    def _generateHeader(cmd, size):
        packet = bytearray()
        packet.append(cmd)
        packet.append(size & 0xFF)
        packet.append(size >> 8)
        return packet

    def get_audio_data(self):
        try:
            packet = MSGEQ7._generateHeader(CMDTYPE.GET, 0)
            self._com.write(packet)
            resp = self._com.read(1)

            if len(resp) == 0:
                MSGEQ7._comError()
            elif ord(resp) != RETURN_CODES.SUCCESS:
                MSGEQ7._printError(ord(resp))
            resp = self._com.read(14)
            if len(resp) != 14:
                MSGEQ7._comError()

            return (
                [self.interp_map[ord(i)] for i in resp[0:7]],
                [self.interp_map[ord(i)] for i in resp[7:14]],
            )
        except IOError:
            log.error("IO Error Communicatng With Game Pad!")


from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors


class BaseSpectrumDraw(object):

    def __init__(self, anim):
        self.anim = anim
        self.width = anim.width
        self.height = anim.height
        self.led = anim._led

    def draw(self, left, right):
        raise NotImplementedError("Cannot call draw on the base class.")


class BaseSpectrumGraph(BaseSpectrumDraw):

    def __init__(self, anim, fill=True):
        super(BaseSpectrumGraph, self).__init__(anim)
        self.height_map = [((i * (self.height - 1)) / (255))
                           for i in range(256)]
        if fill:
            self.rect = self.led.fillRect
        else:
            self.rect = self.led.drawRect


class BasicSpectrumGraph(BaseSpectrumGraph):

    def __init__(self, anim, fill=True, use_hue = False, colors=[colors.Red]):
        super(BasicSpectrumGraph, self).__init__(anim, fill=True)
        self.colors = colors
        self.use_hue = use_hue

    def draw(self, anim, left, right):
        chan = (len(left) + len(right))
        bar_w = int(self.width / chan)

        pos = (self.width - (bar_w * chan)) / 2
        count = 0
        for level in left + right:
            if self.use_hue:
                c = colors.hue2rgb(level)
            else:
                c = self.colors[count % len(self.colors)]
            self.rect(pos, self.height - self.height_map[level],
                      bar_w, self.height, c)
            pos += bar_w
            count += 1


class Spectrum(BaseMatrixAnim):

    def __init__(self, led, audio_source):
        super(Spectrum, self).__init__(led)
        self.source = audio_source
        self.draw_obj = None

    def set_draw_obj(self, obj):
        self.draw_obj = obj

    def step(self, amt=1):
        assert self.draw_obj, "Must call set_draw_obj first!"
        led.all_off()
        data = self.source.get_audio_data()
        self.draw_obj.draw(self._led, data[0], data[1])


if __name__ == "__main__":
    from bibliopixel.drivers.visualizer import DriverVisualizer
    from bibliopixel.led import LEDMatrix
    testcolors = [colors.Red, colors.Orange,
                  colors.Yellow, colors.Green,
                  colors.Blue, colors.Indigo,
                  colors.Violet]

    driver = DriverVisualizer(width=64, height=48)
    led = LEDMatrix(driver, width=0, height=0,
                    serpentine=False, threadedUpdate=True)
    source = MSGEQ7(lower_threshold=65, dev="", hardwareID="1B4F:9206")
    anim = Spectrum(led, audio_source=source)
    draw = BasicSpectrumGraph(anim, fill=True, use_hue = False, colors=testcolors)
    anim.set_draw_obj(draw)
    anim.run(fps=20)
    try:
        while True:
            print audio.get_audio_data()
            time.sleep(0.1)
    except KeyboardInterrupt:
        raise
