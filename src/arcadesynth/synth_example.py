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
    """Für Elise on synth piano"""
    notes = (
        ("E5", 0, 0.7, 0.3, make_piano),
        ("D#5", 0.7, 0.65, 0.4, make_piano),
        ("E5", 1.35, 0.6, 0.5, make_piano),
        ("D#5", 1.95, 0.55, 0.6, make_piano),
        ("E5", 2.5, 0.5, 0.7, make_piano),
        ("B4", 3, 0.5, 0.6, make_piano),
        ("D5", 3.5, 0.5, 0.5, make_piano),
        ("C5", 4, 0.5, 0.5, make_piano),
        ("A4", 4.5, 1, 0.5, make_piano),
        ("A2", 4.5, 0.8, 0.5, make_piano),
        ("E3", 5, 0.8, 0.5, make_piano),
        ("A3", 5.5, 0.8, 0.5, make_piano),
        ("C4", 6.0, 0.5, 0.5, make_piano),
        ("E4", 6.5, 0.5, 0.5, make_piano),
        ("A4", 7.0, 0.5, 0.5, make_piano),
        ("B4", 7.5, 1, 0.5, make_piano),
        ("E2", 7.5, 0.8, 0.5, make_piano),
        ("E3", 8, 0.8, 0.5, make_piano),
        ("G#3", 8.5, 0.8, 0.5, make_piano),
        ("E4", 9, 0.5, 0.5, make_piano),
        ("G#4", 9.5, 0.5, 0.5, make_piano),
        ("B4", 10, 0.5, 0.5, make_piano),
        ("C5", 10.5, 1.0, 0.5, make_piano),
        ("A2", 10.5, 0.8, 0.5, make_piano),
        ("E3", 11, 0.8, 0.5, make_piano),
        ("A3", 11.5, 0.8, 0.5, make_piano),
        ("E4", 12, 0.5, 0.5, make_piano),
        ("E5", 12.5, 0.7, 0.3, make_piano),
        ("D#5", 13.2, 0.65, 0.4, make_piano),
        ("E5", 13.85, 0.6, 0.5, make_piano),
        ("D#5", 14.45, 0.55, 0.6, make_piano),
        ("E5", 15, 0.5, 0.7, make_piano),
        ("B4", 15.5, 0.5, 0.6, make_piano),
        ("D5", 16, 0.5, 0.5, make_piano),
        ("C5", 16.5, 0.5, 0.5, make_piano),
        ("A4", 17, 1, 0.5, make_piano),
        ("A2", 17, 0.8, 0.5, make_piano),
        ("E3", 17.5, 0.8, 0.5, make_piano),
        ("A3", 18, 0.8, 0.5, make_piano),
        ("C4", 18.5, 0.5, 0.5, make_piano),
        ("E4", 19, 0.5, 0.5, make_piano),
        ("A4", 19.5, 0.5, 0.5, make_piano),
        ("B4", 20, 1, 0.5, make_piano),
        ("E2", 20, 0.8, 0.5, make_piano),
        ("E3", 20.5, 0.8, 0.5, make_piano),
        ("G#3", 21, 0.8, 0.5, make_piano),
        ("D4", 21.5, 0.5, 0.5, make_piano),
        ("C5", 22, 0.5, 0.5, make_piano),
        ("B4", 22.5, 0.5, 0.5, make_piano),
        ("A4", 23, 1.0, 0.5, make_piano),
        ("A2", 23, 0.8, 0.5, make_piano),
        ("E3", 23.5, 0.8, 0.5, make_piano),
        ("A3", 24, 0.8, 0.5, make_piano),
    )
    buf = sequence(bpm_to_beatlen(120), notes)
    return tobytes(buf)
