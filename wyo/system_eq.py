import numpy as np
import pyaudio
import threading

from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors

# class taken from the SciPy 2015 Vispy talk opening example
# see https://github.com/vispy/vispy/pull/928
class Recorder(object):
    def __init__(self, rate=8000, chunksize=128):
        self.rate = rate
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.new_frame)
        self.lock = threading.Lock()
        self.stop = False
        self.frames = []

    def new_frame(self, data, frame_count, time_info, status):
        data = np.fromstring(data, 'int16')
        with self.lock:
            self.frames.append(data)
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue

    def get_frames(self):
        with self.lock:
            frames = self.frames
            self.frames = []
            return frames

    def start(self):
        self.stream.start_stream()

    def close(self):
        with self.lock:
            self.stop = True
        self.stream.close()
        self.p.terminate()


class EQ(object):

    def __init__(self, width, auto_gain=False, gain=2):
        self.rec = Recorder(rate=8000, chunksize=width*2)
        self.width = width
        self.auto_gain = auto_gain
        self.gain = gain

        # computes the parameters that will be used during plotting
        self.freq_vect = np.fft.rfftfreq(self.rec.chunksize, 1. / self.rec.rate)
        print max(self.freq_vect), len(self.freq_vect)
        self.time_vect = np.arange(self.rec.chunksize, dtype=np.float32) / self.rec.rate * 1000

    def start(self):
        self.rec.start()

    def stop(self):
        self.rec.close()

    def get_audio_data(self):
        frames = self.rec.get_frames()
        result = [0] * self.width
        if len(frames) > 0:
            # keeps only the last frame
            current_frame = frames[-1]
            # plots the time signal
            # self.line_top.set_data(self.time_vect, current_frame)
            # computes and plots the fft signal
            fft_frame = np.fft.rfft(current_frame)
            if self.auto_gain:
                fft_frame /= np.abs(fft_frame).max()
            else:
                fft_frame *= (1 + self.gain) / 5000000.
            #print max(np.abs(fft_frame))
            #print max(np.log10(np.multiply(20, np.abs(fft_frame))))

            fft_frame = np.log10(np.add(1, np.multiply(10, np.abs(fft_frame))))
            #print fft_frame
            result = [min(int(max(i, 0.) * 1023), 1023) for i in fft_frame][0:self.width]

            #result = [min(int(max(i, 0.) * 1023), 1023) for i in np.abs(fft_frame)][0:self.width]
        #print result
        return result


class EQAnim(BaseMatrixAnim):

    def __init__(self, led, minFrequency=10, maxFrequency=20000):
        super(EQAnim, self).__init__(led)
        self.rec = Recorder()
        self.colors = [colors.hue_helper(y, self.height, 0)
                       for y in range(self.height)]
        self.frequency_limits = self.rec.calculate_channel_frequency(
            minFrequency, maxFrequency, self.width)

    def preRun(self, amt=1):
        self._led.all_off()
        self.rec.setup()
        self.rec.continuousStart()

    def endRecord(self):
        self.rec.continuousEnd()

    def _exit(self, type, value, traceback):
        self.endRecord()

    def step(self, amt=1):
        self._led.all_off()
        eq_data = self.rec.calculate_levels(self.frequency_limits, self.width)
        # print eq_data
        for x in range(self.width):
            # normalize output
            height = (eq_data[x] - 10.2) / 5
            if height < .05:
                height = .05
            elif height > 1.0:
                height = 1.0

            numPix = int(round(height * (self.height + 1)))

            for y in range(self.height):
                if y < int(numPix):
                    self._led.set(x, self.height - y + 1, self.colors[y])

        self._step += amt


if __name__ == "__main__":
    pass
