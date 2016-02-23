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
        self.height_map = [((i * (self.height - 1)) / (1023))
                           for i in range(1024)]
        if fill:
            self.rect = self.led.fillRect
        else:
            self.rect = self.led.drawRect

class BasicSpectrumGraph(BaseSpectrumGraph):

    def __init__(self, anim, fill=True, use_hue=False, colors=[colors.Red]):
        super(BasicSpectrumGraph, self).__init__(anim, fill=True)
        self.colors = colors
        self.use_hue = use_hue

    def draw(self, left, right):
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

class SpectrumMirror(BaseSpectrumDraw):
    def __init__(self, anim, fill=True, use_hue=False, colors=[colors.Red]):
        super(SpectrumMirror, self).__init__(anim)
        self.height_map = [((i * (self.height/2 - 1)) / (1023))
                           for i in range(1024)]
        if fill:
            self.rect = self.led.fillRect
        else:
            self.rect = self.led.drawRect

        self.center_line = self.height / 2
        self.colors = colors
        self.use_hue = use_hue
        print self.center_line

    def draw(self, left, right):
        chan = len(left)
        bar_w = int(self.width / chan)

        pos = (self.width - (bar_w * chan)) / 2
        count = 0
        for i in range(chan):
            ll = left[i]
            lr = right[i]
            if self.use_hue:
                cl = colors.hue2rgb(ll)
                cr = colors.hue2rgb(lr)
            else:
                cl = cr = self.colors[count % len(self.colors)]

            if self.height_map[ll]:
                self.rect(pos, self.center_line  - self.height_map[ll], bar_w, self.height_map[ll], cl)

            if self.height_map[lr]:
                self.rect(pos, self.center_line , bar_w, self.height_map[lr], cr)
            pos += bar_w
            count += 1



class SpectrumGrid(BaseSpectrumDraw):

    def __init__(self, anim):
        super(SpectrumGrid, self).__init__(anim)
        self.value_map = [((i * 255) / 1023) for i in range(1024)]

    def draw(self, left, right):
        bands = len(left)
        w = int(self.width / bands)
        h = int(self.height / bands)

        lpos = 0
        for l in left:
            rpos = 0
            for r in right:
                vr = self.value_map[r]
                #level = self.value_map[l]
                c = colors.hue2rgb_360(vr)
                #c = colors.color_scale(c, level)
                self.led.fillRect(rpos, lpos, rpos+w, lpos+h, c)
                rpos += w
            lpos += h

        # pos = (self.width - (bar_w * chan)) / 2
        # count = 0
        # for level in left + right:
        #     if self.use_hue:
        #         c = colors.hue2rgb(level)
        #     else:
        #         c = self.colors[count % len(self.colors)]
        #     self.rect(pos, self.height - self.height_map[level],
        #               bar_w, self.height, c)
        #     pos += bar_w
        #     count += 1


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
        self.draw_obj.draw(data[0], data[1])
