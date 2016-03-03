from bibliopixel.animation import BaseMatrixAnim
import bibliopixel.colors as colors


class BaseSpectrumDraw(object):

    def __init__(self, anim):
        self.anim = anim
        self.width = anim.width
        self.height = anim.height
        self.led = anim._led

    def draw(self, data):
        raise NotImplementedError("Cannot call draw on the base class.")


class BaseSpectrumGraph(BaseSpectrumDraw):

    def __init__(self, anim, fill=True):
        super(BaseSpectrumGraph, self).__init__(anim)
        self.height_map = [((i * (self.height - 1)) / (1023))
                           for i in range(1024)]
        if fill:
            self.rect = self.led.fillRect
        else:
            self.rect = self.led.drawRect


class BasicSpectrumGraphOld(BaseSpectrumGraph):

    def __init__(self, anim, fill=True, use_hue=False, color_list=[colors.Red]):
        super(BasicSpectrumGraphOld, self).__init__(anim, fill=True)
        self.colors = color_list
        self.use_hue = use_hue

    def draw(self, data):
        chan = len(data)
        bar_w = int(self.width / chan)

        pos = (self.width - (bar_w * chan)) / 2
        count = 0
        for level in data:
            if self.use_hue:
                c = colors.hue2rgb(level)
            else:
                c = self.colors[count % len(self.colors)]
            self.rect(pos, self.height - self.height_map[level],
                      bar_w, self.height, c)
            pos += bar_w
            count += 1


class BasicLineGraph(BaseSpectrumDraw):

    def __init__(self, anim, fill=True, use_hue=False, color_list=[colors.Red]):
        super(BasicLineGraph, self).__init__(anim)
        self.height_map = [((i * (self.height - 1)) / (1023))
                           for i in range(1024)]
        self.colors = color_list
        self.use_hue = use_hue

    def draw(self, data):
        chan = len(data)

        pos = (self.width - chan)
        count = 0
        for level in data:
            if self.use_hue:
                c = colors.hue2rgb(level)
            else:
                c = self.colors[count % len(self.colors)]
            self.led.drawLine(pos, self.height, pos, self.height - self.height_map[level], c)
            pos += 1
            count += 1


class SpreadOld(BaseSpectrumDraw):

    def __init__(self, anim, use_hue=False, color_list=[colors.Red]):
        super(SpreadOld, self).__init__(anim)
        self.height_map = [((i * (self.height / 2 - 1)) / (1023))
                           for i in range(1024)]
        self.color_map = [colors.hue2rgb((i * (255)) / (self.width - 1)) for i in range(self.width)]
        self.center_line = self.height / 2
        self.colors = color_list
        self.use_hue = use_hue
        self.offset = 0

    def draw(self, data):
        chan = len(data)
        left = data[0:chan / 2]
        right = data[chan / 2:chan]
        for i in range(self.width):
            h = self.height_map[left[(i + self.offset) % len(left)]]
            c = self.color_map[i]
            if h:
                self.led.drawLine(i * 2, self.center_line, i * 2, self.center_line + h, c)
                self.led.drawLine(i * 2, self.center_line - 1, i * 2, self.center_line - 1 - h, c)

            h = self.height_map[right[(i + self.offset) % len(right)]]
            if h:
                self.led.drawLine(i * 2 + 1, self.center_line, i * 2 + 1, self.center_line + h, c)
                self.led.drawLine(i * 2 + 1, self.center_line - 1, i * 2 + 1, self.center_line - 1 - h, c)
        self.offset += 1


class Spread(BaseSpectrumDraw):

    def __init__(self, anim, use_hue=False, color_list=[colors.Red]):
        super(Spread, self).__init__(anim)
        self.height_map = [((i * (self.height / 2 - 1)) / (1023))
                           for i in range(1024)]
        self.color_map = [colors.hue2rgb((i * (255)) / (self.width - 1)) for i in range(self.width)]
        self.center_line = self.height / 2
        self.colors = color_list
        self.use_hue = use_hue
        self.offset = 0

    def draw(self, data):
        # chan = len(data)
        # left = data[0:chan / 2]
        # right = data[chan / 2:chan]
        print data
        for i in range(self.width):
            h = self.height_map[data[(i + self.offset) % len(data)]]
            c = self.color_map[i]
            if h:
                self.led.drawLine(i, self.center_line, i, self.center_line + h, c)
                self.led.drawLine(i, self.center_line - 1, i, self.center_line - 1 - h, c)

        #     h = self.height_map[right[(i + self.offset) % len(right)]]
        #     if h:
        #         self.led.drawLine(i * 2 + 1, self.center_line, i * 2 + 1, self.center_line + h, c)
        #         self.led.drawLine(i * 2 + 1, self.center_line - 1, i * 2 + 1, self.center_line - 1 - h, c)
        # self.offset += 1


class SpectrumMirror(BaseSpectrumDraw):

    def __init__(self, anim, fill=True, use_hue=False, color_list=[colors.Red]):
        super(SpectrumMirror, self).__init__(anim)
        self.height_map = [((i * (self.height / 2 - 1)) / (1023))
                           for i in range(1024)]
        if fill:
            self.rect = self.led.fillRect
        else:
            self.rect = self.led.drawRect

        self.center_line = self.height / 2
        self.colors = color_list
        self.use_hue = use_hue

    def draw(self, data):
        chan = len(data)
        left = data[0:chan / 2]
        right = data[chan / 2:chan]
        bar_w = int(self.width / (chan / 2))

        pos = (self.width - (bar_w * chan)) / 2
        count = 0
        for i in range(chan / 2):
            ll = left[i]
            lr = right[i]
            if self.use_hue:
                cl = colors.hue2rgb(ll)
                cr = colors.hue2rgb(lr)
            else:
                cl = cr = self.colors[count % len(self.colors)]

            if self.height_map[ll]:
                self.rect(pos, self.center_line -
                          self.height_map[ll], bar_w, self.height_map[ll], cl)

            if self.height_map[lr]:
                self.rect(pos, self.center_line, bar_w,
                          self.height_map[lr], cr)
            pos += bar_w
            count += 1


class Spectrum(BaseMatrixAnim):

    def __init__(self, led, audio_source):
        super(Spectrum, self).__init__(led)
        self.source = audio_source
        self.draw_obj = None

    def preRun(self, amt=1):
        self.source.start()

    def _exit(self, type, value, traceback):
        self.source.stop()

    def set_draw_obj(self, obj):
        self.draw_obj = obj

    def step(self, amt=1):
        assert self.draw_obj, "Must call set_draw_obj first!"
        self._led.all_off()
        data = self.source.get_audio_data()
        self.draw_obj.draw(data)
