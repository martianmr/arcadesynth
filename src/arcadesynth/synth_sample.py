"""Basic sample sounds"""
from .synth import *


def sawtooth_wave(ms=1600, vol=1.0, freq=150.0):
    """Return bytes representing a simple sawtooth wave"""
    buf = make_sawtooth(ms, vol, freq)
    return tobytes(buf)


def triangle_wave(ms=1600, vol=1.0, freq=150.0):
    """Return bytes representing a simple triangle wave"""
    buf = make_triangle(ms, vol, freq)
    return tobytes(buf)


def sine_wave(ms=600, vol=1.0, freq=150.0):
    """Return bytes representing a simple sine wave"""
    buf = make_sin(ms, vol, freq)
    return tobytes(buf)


def square_wave(ms=90, vol=0.4, freq=144.0):
    """Return bytes representing a simple square wave"""
    buf = make_square(ms, vol, freq)
    return tobytes(buf)


def brown_noise(ms=600, vol=0.4, freq=150.0):
    """Return bytes representing brown noise"""
    buf = make_brown(ms, vol, freq)
    return tobytes(buf)


def white_noise(ms=600, vol=0.4, smooth=False):
    """Return bytes representing white noise"""
    buf = make_white(ms, vol, smooth)
    return tobytes(buf)


def sweep(ms=80, startf=1500.0, endf=100.0, shape=sin, vol=1.0, repeat=0):
    """Return bytes representing a frequency sweep from startf to endf"""
    buf = make_sweep(ms, startf, endf, shape, vol, repeat)
    return tobytes(buf)


def chord(ms=600, vol=0.4, f1=261.6256, f2=329.6276):
    """Return bytes representing a 2 note chord"""
    buf1 = make_square(ms, vol, freq=f1)
    buf2 = make_square(ms, vol, freq=f2)
    buf1 = combine(buf1, buf2)
    return tobytes(buf1)


def fadeup(ms=999, a1=0.2, a2=0.8):
    buf = make_triangle(ms, 1.0, 261.6256)
    buf = fade(buf, a1, a2)
    return tobytes(buf)