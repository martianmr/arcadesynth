"""Pac-Man sound effects"""
from .synth import *


def _pm_wakka_wave(freq):
    ms = 1000 / freq
    buf1 = make_sin(ms, 0.8, freq, precision=2)
    buf2 = make_triangle(ms, 1.0, freq/3.5)
    buf = vmove(combine(buf1, buf2), 0.25)
    return buf, ms


def _pm_wakka_single(freq):
    buf, _ = _pm_wakka_wave(freq)
    return buf


def _pm_wakka_trio(freq):
    ms = 0
    buf = new_buffer()
    for mult in [1.0, 1.5, 4.5]:
        tempbuf, t = _pm_wakka_wave(freq * mult)
        buf += tempbuf
        ms += t
    return buf, ms


def _pm_wakka_sweep(ms, fs, fe):
    t = 0
    buf = new_buffer()
    while t < ms:
        mult = t / ms
        f = fs + ((fe - fs) * mult)
        tempbuf, dt = _pm_wakka_trio(f)
        buf += tempbuf
        t += dt
    return buf


def _pm_wakka_bass(ms, vol, freq):
    f = freq * 0.9333
    buf = _pm_wakka_sweep(ms, f, f)
    envelope(buf, 0, 0, 0.5, ms)
    return buf


def pm_credit():
    """Sound on entering a coin"""
    buf = new_buffer()
    buf += _pm_wakka_sweep(80, 650, 150)
    buf += _pm_wakka_single(60.0)
    buf += _pm_wakka_sweep(80, 150, 816)
    buf += _pm_wakka_sweep(30, 816, 816)
    return tobytes(buf)


def pm_wakka1():
    buf = _pm_wakka_sweep(83, 350, 816)
    return tobytes(buf)


def pm_wakka2():
    buf = _pm_wakka_sweep(83, 816, 350)
    return tobytes(buf)


def pm_siren_low():
    """Lower siren at start of level"""
    buf = make_sweep(400, 350, 950, triangle, 0.25, 400)
    return tobytes(buf)


def pm_siren_high():
    """Higher siren later in level"""
    buf = make_sweep(350, 500, 1100, triangle, 0.25, 400)
    return tobytes(buf)


def pm_intro():
    """Pac-Man intro music"""
    notes = (
        ("C3", 0, 4, 0.5, _pm_wakka_bass),
        ("C5", 0, 1, 0.5, make_sin),
        ("C6", 2, 1, 0.5, make_sin),
        ("G5", 4, 1, 0.5, make_sin),
        ("G3", 6, 4, 0.5, _pm_wakka_bass),
        ("E5", 6, 1, 0.5, make_sin),
        ("C3", 8, 4, 0.5, _pm_wakka_bass),
        ("C6", 8, 1, 0.5, make_sin),
        ("G5", 9, 1, 0.5, make_sin),
        ("E5", 12, 2, 0.5, make_sin),
        ("G3", 14, 4, 0.5, _pm_wakka_bass),
        ("C#3", 16, 4, 0.5, _pm_wakka_bass),
        ("C#5", 16, 1, 0.5, make_sin),
        ("C#6", 18, 1, 0.5, make_sin),
        ("G#5", 20, 1, 0.5, make_sin),
        ("G#3", 22, 4, 0.5, _pm_wakka_bass),
        ("F5", 22, 1, 0.5, make_sin),
        ("C#3", 24, 4, 0.5, _pm_wakka_bass),
        ("C#6", 24, 1, 0.5, make_sin),
        ("G#5", 25, 1, 0.5, make_sin),
        ("F5", 28, 2, 0.5, make_sin),
        ("G#3", 30, 4, 0.5, _pm_wakka_bass),
        ("C3", 32, 4, 0.5, _pm_wakka_bass),
        ("C5", 32, 1, 0.5, make_sin),
        ("C6", 34, 1, 0.5, make_sin),
        ("G5", 36, 1, 0.5, make_sin),
        ("G3", 38, 4, 0.5, _pm_wakka_bass),
        ("E5", 38, 1, 0.5, make_sin),
        ("C3", 40, 4, 0.5, _pm_wakka_bass),
        ("C6", 40, 1, 0.5, make_sin),
        ("G5", 41, 1, 0.5, make_sin),
        ("E5", 44, 2, 0.5, make_sin),
        ("G3", 46, 4, 0.5, _pm_wakka_bass),
        ("G3", 48, 4, 0.5, _pm_wakka_bass),
        ("D#5", 48, 1, 0.5, make_sin),
        ("E5", 49, 1, 0.5, make_sin),
        ("F5", 50, 1, 0.5, make_sin),
        ("A3", 52, 4, 0.5, _pm_wakka_bass),
        ("F#5", 52, 1, 0.5, make_sin),
        ("G5", 53, 1, 0.5, make_sin),
        ("G#5", 54, 1, 0.5, make_sin),
        ("B3", 56, 4, 0.5, _pm_wakka_bass),
        ("A5", 56, 1, 0.5, make_sin),
        ("A#5", 57, 1, 0.5, make_sin),
        ("B5", 58, 1, 0.5, make_sin),
        ("C4", 60, 4, 0.5, _pm_wakka_bass),
        ("C6", 60, 3, 0.5, make_sin),
    )

    buf = sequence(66, notes)
    return tobytes(buf)



def pm_test():
    buf = new_buffer()
    buf = add(buf, make_sweep(400, 350, 950, triangle, 0.25, 400), 0)
    buf = add(buf, make_sweep(400, 350, 950, triangle, 0.25, 400), 400)
    buf = add(buf, make_sweep(400, 350, 950, triangle, 0.25, 400), 800)
    buf = add(buf, make_sweep(400, 350, 950, triangle, 0.25, 400), 1200)
    buf = add(buf, _pm_wakka_sweep(83, 350, 816), 80)
    buf = add(buf, _pm_wakka_sweep(83, 816, 350), 240)
    return tobytes(buf)