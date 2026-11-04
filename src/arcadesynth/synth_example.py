"""some generic retro sound effects

[source](../src/arcadesynth/synth_example.py)
"""
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


def eg_fur_elise():
    notes = (
        ("E5", 0, 0.7, 0.2, make_piano),
        ("D#5", 0.7, 0.7, 0.3, make_piano),
        ("E5", 1.4, 0.6, 0.4, make_piano),
        ("D#5", 2, 0.5, 0.5, make_piano),
        ("E5", 2.5, 0.5, 0.5, make_piano),
        ("B4", 3, 0.5, 0.5, make_piano),
        ("D5", 3.5, 0.5, 0.5, make_piano),
        ("C5", 4, 0.5, 0.5, make_piano),
        ("A4", 4.5, 2, 0.5, make_piano),
        ("A2", 4.5, 2, 0.5, make_piano),
        ("E3", 5, 2, 0.5, make_piano),
        ("A3", 5.5, 2, 0.5, make_piano),
    )
    buf = sequence(bpm_to_beatlen(150), notes, 1.022)
    return tobytes(buf)


def eg_piano():
    buf = make_piano(8000, 1.0, notehz('C4'), 4)
    return tobytes(buf)