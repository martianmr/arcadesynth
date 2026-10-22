"""Pac-Man sound effects"""
from .synth import *

def pm_siren_low():
    """Lower siren at start of level"""
    buf = make_sweep(400, 350, 950, triangle, 0.25, 400)
    return tobytes(buf)


def pm_siren_high():
    """Higher siren later in level"""
    buf = make_sweep(350, 500, 1100, triangle, 0.25, 400)
    return tobytes(buf)


def _pm_wakka_wave(freq):
    ms = 1000 / freq
    buf1 = make_sin(ms, 0.8, freq, precision=2)
    buf2 = make_triangle(ms, 1.0, freq/3.5)
    return vmove(combine(buf1, buf2), 0.25)


def _pm_wakka_trio(freq):
    buf = array.array("d")
    for mult in [1.0, 1.43, 4.8]:
        buf += _pm_wakka_wave(freq * mult)
    return buf


def pm_credit():
    """Sound on entering a coin"""
    buf = array.array("d")
    for i in reversed(range(7, 70, 5)):
        buf += _pm_wakka_trio((i + 12) * 8)
    buf += _pm_wakka_wave(60.0)
    for i in range(7, 90, 5):
        buf += _pm_wakka_trio((i + 12) * 8)
    for i in range(10):
        buf += _pm_wakka_trio((90 + 12) * 8)
    return tobytes(buf)