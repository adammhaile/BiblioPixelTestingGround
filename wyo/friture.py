#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2009 Timothée Lecomte

# This file is part of Friture.
#
# Friture is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# Friture is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Friture.  If not, see <http://www.gnu.org/licenses/>.

from numpy import linspace, log2, floor, log10, cos, arange, pi
from numpy.fft import rfft

DEFAULT_FFT_SIZE = 7  # 4096 points
DEFAULT_FREQ_SCALE = 1  # log10
SAMPLING_RATE = 44100
DEFAULT_MAXFREQ = SAMPLING_RATE / 2
DEFAULT_MINFREQ = 20
fft_size = 2 ** DEFAULT_FFT_SIZE * 32


class audioproc():

    def __init__(self):
        self.freq = linspace(0, SAMPLING_RATE / 2, 10)
        self.A = 0. * self.freq
        self.B = 0. * self.freq
        self.C = 0. * self.freq
        self.maxfreq = 1.
        self.decimation = 1
        self.window = arange(0, 1)
        self.size_sq = 1.

        self.fft_size = 10

    def analyzelive(self, samples):
        samples = self.decimate(samples)

        # uncomment the following to disable the decimation altogether
        # decimation = 1

        # FFT for a linear transformation in frequency scale
        fft = rfft(samples * self.window)
        spectrum = self.norm_square(fft)

        return spectrum

    def norm_square(self, fft):
        return (fft.real**2 + fft.imag**2) / self.size_sq
        # This is done in Cython, too costly in numpy
        #return pyx_norm_square(fft, 1. / self.size_sq)

    def decimate(self, samples):
        # first we remove as much points as possible
        if self.decimation > 1:
            samples.shape = len(samples) / self.decimation, self.decimation
            # the full way
            # samples = samples.mean(axis=1)
            # the simplest way
            samples = samples[:, 0]
        return samples

    def set_fftsize(self, fft_size):
        if fft_size != self.fft_size:
            self.fft_size = fft_size
            self.update_freq_cache()
            self.update_window()
            self.update_size()

    def set_maxfreq(self, maxfreq):
        if maxfreq != self.maxfreq:
            self.maxfreq = maxfreq
            decimation = SAMPLING_RATE / (2 * maxfreq)
            self.decimation = 2 ** (floor(log2(decimation)))

            if self.decimation < 1:
                self.decimation = 1

            self.update_freq_cache()
            self.update_window()
            self.update_size()

    def get_freq_scale(self):
        return self.freq

    def get_freq_weighting(self):
        return self.A, self.B, self.C

    def update_size(self):
        self.size_sq = float(self.fft_size / self.decimation) ** 2

    def update_window(self):
        N = self.fft_size / self.decimation
        n = arange(0, N)
        # Hann window : better frequency resolution than the rectangular window
        self.window = 0.5 * (1. - cos(2 * pi * n / (N - 1)))

    def update_freq_cache(self):
        if len(self.freq) != self.fft_size / (2 * self.decimation) + 1:
            self.freq = linspace(0, SAMPLING_RATE / (2 * self.decimation), self.fft_size / (2 * self.decimation) + 1)

            # compute psychoacoustic weighting. See http://en.wikipedia.org/wiki/A-weighting
            f = self.freq
            Rc = 12200. ** 2 * f ** 2 / ((f ** 2 + 20.6 ** 2) * (f ** 2 + 12200. ** 2))
            Rb = 12200. ** 2 * f ** 3 / ((f ** 2 + 20.6 ** 2) * (f ** 2 + 12200. ** 2) * ((f ** 2 + 158.5 ** 2) ** 0.5))
            Ra = 12200. ** 2 * f ** 4 / ((f ** 2 + 20.6 ** 2) * (f ** 2 + 12200. ** 2) * ((f ** 2 + 107.7 ** 2) ** 0.5) * ((f ** 2 + 737.9 ** 2) ** 0.5))
            eps = 1e-50
            self.C = 0.06 + 20. * log10(Rc + eps)
            self.B = 0.17 + 20. * log10(Rb + eps)
            self.A = 2.0 + 20. * log10(Ra + eps)

    # above is done a FFT of the signal. This is ok for linear frequency scale, but
    # not satisfying for logarithmic scale, which is much more adapted to voice or music
    # analysis
    # Instead a constant Q transform should be used

    # Alternatively, we could use a ear/cochlear model : logarithmic
    # frequency scale, 4000 logarithmic-spaced bins, quality factors
    # determined from mechanical model, and 50 ms smoothing afterwards
    # for the sensor cell response time. The problem here comes from the
    # implementation: how to do it cleverly ?
    # on top of that, we could add the reponse of the middle ear, which is
    # a roughly band-pass filter centered around 1 kHz (see psychoacoustic
    # models)

    # def analyzelive_cochlear(self, samples, num_channels, lowfreq, maxfreq):
    #       samples -= samples.mean()
    #
    #       fs = 16000.

    #       [ERBforward, ERBfeedback] = MakeERBFilters(SAMPLING_RATE, num_channels, lowfreq)
    #       filtered_samples = ERBFilterBank(ERBforward, ERBfeedback, samples)

    #       spectrum = (abs(filtered_samples)**2).mean(axis=1)
    #       self.freq = frequencies(SAMPLING_RATE, num_channels, lowfreq)
    #
    #       return spectrum[::-1], self.freq[::-1]
