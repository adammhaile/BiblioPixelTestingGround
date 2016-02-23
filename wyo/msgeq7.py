try:
    import serial
    import serial.tools.list_ports
except ImportError as e:
    error = "Please install pyserial 2.7+! pip install pyserial"
    raise ImportError(error)


import logging
log = logging.getLogger()

from distutils.version import LooseVersion

if LooseVersion(serial.VERSION) < LooseVersion('2.7'):
    error = "pyserial v{} found, please upgrade to v2.7+! pip install pyserial --upgrade".format(
        serial.VERSION)
    log.logger.error(error)
    raise ImportError(error)

import struct


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

class DummyData(object):
    def __init__(self, data="eq.dat"):
        self.file = data
        self.f = open(self.file, mode="rb")
        self._struct = struct.Struct("<hhhhhhh")

    def get_audio_data(self):
        resp = self.f.read(28)
        if len(resp) != 28:
            self.f.seek(0)
            resp = self.f.read(28)

        return (
            [i for i in self._struct.unpack(resp[0:14])],
            [i for i in self._struct.unpack(resp[14:28])]
        )

class MSGEQ7(object):
    foundDevices = []

    def __init__(self, lower_threshold=70, dev="", hardwareID="1B4F:9206"):
        self._hardwareID = hardwareID
        self._com = None
        self.dev = dev
        self.interp_map = [max(
            0, (((i - lower_threshold) * 1023) / (1023 - lower_threshold))) for i in range(1024)]

        self._struct = struct.Struct("<hhhhhhh")
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
            resp = self._com.read(28)
            if len(resp) != 28:
                MSGEQ7._comError()

            return (
                [self.interp_map[i] for i in self._struct.unpack(resp[0:14])],
                [self.interp_map[i] for i in self._struct.unpack(resp[14:28])]
            )
        except IOError:
            log.error("IO Error Communicatng With Game Pad!")

# import time
# eq = MSGEQ7(lower_threshold=70, dev="", hardwareID="1B4F:9206")
# with open("eq.dat", mode="wb+") as f:
#     s = struct.Struct("<hhhhhhh")
#     while True:
#         data = eq.get_audio_data()
#         print data
#         f.write(s.pack(*data[0]))
#         f.write(s.pack(*data[1]))
#         time.sleep(30.0/1000.0)
