"""some simple basic sounds

[source](../src/arcadesynth/synth_sample.py)
"""
from .synth import *


def sawtooth_wave(ms=500, vol=1.0, freq=150.0):
    """Return bytes representing a simple sawtooth wave"""
    buf = make_sawtooth(ms, vol, freq)
    return tobytes(buf)


def triangle_wave(ms=500, vol=1.0, freq=150.0):
    """Return bytes representing a simple triangle wave"""
    buf = make_triangle(ms, vol, freq)
    return tobytes(buf)


def sine_wave(ms=500, vol=1.0, freq=150.0):
    """Return bytes representing a simple sine wave"""
    buf = make_sin(ms, vol, freq)
    return tobytes(buf)


def square_wave(ms=500, vol=1.0, freq=150.0):
    """Return bytes representing a simple square wave"""
    buf = make_square(ms, vol, freq)
    return tobytes(buf)


def brown_noise(ms=500, vol=1.0, freq=150.0):
    """Return bytes representing brown noise"""
    buf = make_brown(ms, vol, freq)
    return tobytes(buf)


def white_noise(ms=500, vol=1.0, smooth=False):
    """Return bytes representing white noise"""
    buf = make_white(ms, vol, smooth)
    return tobytes(buf)


def sweep(ms=500, startf=1500.0, endf=100.0, shape=sin, vol=1.0, repeat=0):
    """Return bytes representing a frequency sweep from startf to endf"""
    buf = make_sweep(ms, startf, endf, shape, vol, repeat)
    return tobytes(buf)


def chord(ms=500, vol=1.0, f1=notehz("C3"), f2=notehz("E3")):
    """Return bytes representing a 2 note chord"""
    buf1 = make_triangle(ms, vol, freq=f1)
    buf2 = make_triangle(ms, vol, freq=f2)
    buf1 = combine(buf1, buf2)
    return tobytes(buf1)


def fadeup(ms=500, a1=0.2, a2=1.0):
    """Return bytes representing a note that fades up in amplitude"""
    buf = make_triangle(ms, 1.0, 261.6256)
    buf = fade(buf, a1, a2)
    return tobytes(buf)


def silence(ms=500):
    """Return bytes containing silence"""
    return tobytes(make_silence(ms))