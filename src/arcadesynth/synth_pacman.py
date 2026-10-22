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


def _pm_wakka_bass(ms, freq):
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
    beat = 66
    buf = new_buffer()
    buf = add(buf, _pm_wakka_bass(beat * 4, 130.813), 0) # C3
    buf = add(buf, make_sin(beat, 0.5, 523.251), 0) # C5
    buf = add(buf, make_sin(beat, 0.5, 1046.502), beat * 2) # C6
    buf = add(buf, make_sin(beat, 0.5, 783.991), beat * 4) # G5
    buf = add(buf, _pm_wakka_bass(beat * 4, 195.998), beat * 6) # G3
    buf = add(buf, make_sin(beat, 0.5, 659.255), beat * 6) # E5
    buf = add(buf, _pm_wakka_bass(beat * 4, 130.813), beat * 8) # C3
    buf = add(buf, make_sin(beat, 0.5, 1046.502), beat * 8) # C6
    buf = add(buf, make_sin(beat, 0.5, 783.991), beat * 9) # G5
    buf = add(buf, make_sin(beat * 2, 0.5, 659.255), beat * 12) # E5
    buf = add(buf, _pm_wakka_bass(beat * 4, 195.998), beat * 14) # G3

    buf = add(buf, _pm_wakka_bass(beat * 4, 138.591), beat * 16) # C#3
    buf = add(buf, make_sin(beat, 0.5, 554.365), beat * 16) # C#5
    buf = add(buf, make_sin(beat, 0.5, 1108.731), beat * 18) # C#6
    buf = add(buf, make_sin(beat, 0.5, 830.609), beat * 20) # G#5
    buf = add(buf, _pm_wakka_bass(beat * 4, 207.652), beat * 22) # G#3
    buf = add(buf, make_sin(beat, 0.5, 698.456), beat * 22) # F5
    buf = add(buf, _pm_wakka_bass(beat * 4, 138.591), beat * 24) # C#3
    buf = add(buf, make_sin(beat, 0.5, 1108.731), beat * 24) # C#6
    buf = add(buf, make_sin(beat, 0.5, 830.609), beat * 25) # G#5
    buf = add(buf, make_sin(beat * 2, 0.5, 698.456), beat * 28) # F5
    buf = add(buf, _pm_wakka_bass(beat * 4, 207.652), beat * 30) # G#3

    buf = add(buf, _pm_wakka_bass(beat * 4, 130.813), beat * 32) # C3
    buf = add(buf, make_sin(beat, 0.5, 523.251), beat * 32) # C5
    buf = add(buf, make_sin(beat, 0.5, 1046.502), beat * 34) # C6
    buf = add(buf, make_sin(beat, 0.5, 783.991), beat * 36) # G5
    buf = add(buf, _pm_wakka_bass(beat * 4, 195.998), beat * 38) # G3
    buf = add(buf, make_sin(beat, 0.5, 659.255), beat * 38) # E5
    buf = add(buf, _pm_wakka_bass(beat * 4, 130.813), beat * 40) # C3
    buf = add(buf, make_sin(beat, 0.5, 1046.502), beat * 40) # C6
    buf = add(buf, make_sin(beat, 0.5, 783.991), beat * 41) # G5
    buf = add(buf, make_sin(beat * 2, 0.5, 659.255), beat * 44) # E5
    buf = add(buf, _pm_wakka_bass(beat * 4, 195.998), beat * 46) # G3

    buf = add(buf, _pm_wakka_bass(beat * 4, 195.998), beat * 48) # G3
    buf = add(buf, make_sin(beat, 0.5, 622.254), beat * 48) # D#5
    buf = add(buf, make_sin(beat, 0.5, 659.255), beat * 49) # E5
    buf = add(buf, make_sin(beat, 0.5, 698.456), beat * 50) # F5

    buf = add(buf, _pm_wakka_bass(beat * 4, 220.0), beat * 52) # A3
    buf = add(buf, make_sin(beat, 0.5, 739.989), beat * 52) # F#5
    buf = add(buf, make_sin(beat, 0.5, 783.991), beat * 53) # G5
    buf = add(buf, make_sin(beat, 0.5, 830.609), beat * 54) # G#5

    buf = add(buf, _pm_wakka_bass(beat * 4, 246.942), beat * 56) # B3
    buf = add(buf, make_sin(beat, 0.5, 880.0), beat * 56) # A5
    buf = add(buf, make_sin(beat, 0.5, 932.328), beat * 57) # A#5
    buf = add(buf, make_sin(beat, 0.5, 987.767), beat * 58) # B5

    buf = add(buf, _pm_wakka_bass(beat * 4, 261.626), beat * 60) # C4
    buf = add(buf, make_sin(beat * 3, 0.5, 1046.502), beat * 60) # C6

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