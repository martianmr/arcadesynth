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
    buf = vmove(combine(buf1, buf2), 0.25)
    return buf, ms


def _pm_wakka_trio(freq):
    ms = 0
    buf = array.array("d")
    for mult in [1.0, 1.43, 4.8]:
        tempbuf, t = _pm_wakka_wave(freq * mult)
        buf += tempbuf
        ms += t
    return buf, ms


def _pm_wakka_sweep(ms, fs, fe):
    t = 0
    buf = array.array("d")
    while t < ms:
        mult = t / ms
        f = fs + ((fe - fs) * mult)
        tempbuf, dt = _pm_wakka_trio(f)
        buf += tempbuf
        t += dt
    return buf


def pm_credit():
    """Sound on entering a coin"""
    buf = array.array("d")
    buf += _pm_wakka_sweep(80, 650, 150)
    tempbuf, _ = _pm_wakka_wave(60.0)
    buf += tempbuf
    buf += _pm_wakka_sweep(80, 150, 816)
    buf += _pm_wakka_sweep(30, 816, 816)
    return tobytes(buf)


def pm_wakka1():
    buf = _pm_wakka_sweep(83, 350, 816)
    return tobytes(buf)


def pm_wakka2():
    buf = _pm_wakka_sweep(83, 816, 350)
    return tobytes(buf)