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

    def __init__(self, anim, fill=True, use_hue=False, colors=[colors.Red]):
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
        self._led.all_off()
        data = self.source.get_audio_data()
        self.draw_obj.draw(self._led, data[0], data[1])
