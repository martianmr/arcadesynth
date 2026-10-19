"""Generic retro sound effects"""
from .synth import *


def eg_gunshot():
    """Retro gunshot sound"""
    ms = 500
    buf = make_white(ms, 1.0)
    buf = lowpass_filter(buf, 1200.0, order=4)
    noisalise(buf, gain=0.5)
    envelope(buf, 20, 30, 0.2, ms - 10)
    return tobytes(buf)


def eg_boom():
    """A booming explosion"""
    ms = 1500
    buf = make_white(ms, 1.0)
    buf = lowpass_filter(buf, 500.0, order=4)
    noisalise(buf, gain=0.5)
    envelope(buf, 20, 30, 0.2, ms - 10)
    return tobytes(buf)


def eg_zap():
    """The sound of a Kill-o-Zap gun, probably"""
    ms = 200
    buf = make_sweep(ms, 1000, 200, triangle, 1.0, 0)
    envelope(buf, 20, 30, 0.2, ms - 10)
    return tobytes(buf)