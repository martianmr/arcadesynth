"""Asteroids sound effects"""
from .synth import *


def as_playerfire():
    """Asteroids player firing sound"""
    ms = 260
    buf = make_sweep(ms, 820, 100, square, 0.5, 0, special=-0.8)
    envelope(buf, 0, ms, 0.2, 0)
    envelope(buf, 0, 100, 0.5, 0, 0, 100)
    envelope(buf, 0, 0, 0.5, 0, 100, ms)
    return tobytes(buf)


def as_ufofire():
    """Asteroids flying saucer firing sound"""
    ms = 260
    buf = make_sweep(ms, 820, 650, square, 0.5, 0, special=-0.8)
    return tobytes(buf)


def as_bump(freq = 81.516):
    """Asteroids periodic heartbeat bump
    
    Expected frequencies in Hz, 81.516, 87.500
    """
    buf = make_square(50, 0.5, freq)
    return tobytes(buf)


def as_bump1():
    """Lower periodic heartbeat bump"""
    return as_bump(81.516)


def as_bump2():
    """Higher periodic heartbeat bump"""
    return as_bump(87.500)


def as_explode(freq = 200.0):
    """Asteroids things blowing up
    
    Estimated frequencies:
    Large rock   170 Hz
    Medium Rock  220 Hz
    Small Rock   270 Hz
    
    """
    ms = 1000
    buf = make_white(ms, 1.0)
    buf = lowpass_filter(buf, freq, order=1)
    noisalise(buf, gain=0.1)
    envelope(buf, 20, 0, 1.0, ms)
    return tobytes(buf)


def as_explode_large():
    """Large rock exploding"""
    return as_explode(170.0)


def as_explode_medium():
    """Medium rock exploding"""
    return as_explode(220.0)


def as_explode_small():
    """Small rock exploding"""
    return as_explode(270.0)


def as_ufo(ms, low, high):
    """Asteroids flying saucer on screen noise
    
    Large 180, 600, 1400
    Small 120, 800, 1600
    """
    buf = make_sweep(ms, low, high, triangle, 0.5, ms)
    return tobytes(buf)


def as_ufo_large():
    """Large flying saucer noise"""
    return as_ufo(180, 600.0, 1400.0)


def as_ufo_small():
    """Small flying saucer noise"""
    return as_ufo(120, 800.0, 1600.0)


def as_thrust():
    """Asteroids player ship thrusting"""
    buf = make_brown(1000, 0.5, 30, 1)
    noisalise(buf, gain=0.12)
    buf = median_filter(buf)
    reversebuf = reverse(buf)
    buf = buf + reversebuf
    return tobytes(buf)


def as_extralife():
    """Asteroids extra life notification"""
    buf = make_sin(1300, 0.5, 2940)
    tremolo(buf, 16.8, 1.0, square)
    return tobytes(buf)



