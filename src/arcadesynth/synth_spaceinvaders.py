"""Space Invaders sound effects"""
from .synth import *


def si_extralife():
    """Space Invaders extra life notification"""
    ms = 1360
    buf1 = make_triangle(ms, 1.0, 490)
    buf2 = make_sawtooth(ms, 1.0, 490)
    buf = combine(buf1, buf2)
    tremolo(buf, 120.0, 0.9, shape=triangle)
    buf = boost(buf, 5.0)
    envelope(buf, 20, 0, 1.0, 20, end=200)
    for i in range(8):
        s = i * 145 + 200
        e = s + 135
        mute = e + 10
        envelope(buf, 30, 0, 0.9, 30, start=s, end=e)
        envelope(buf, 0, 0, 0.0, 0, start=e, end=mute)
    echo(buf, 30, 0.4)
    return tobytes(buf)


def si_ufodie():
    """Space Invaders UFO exploding sound"""
    low = 150.0
    high = 1320.0
    buf = make_sweep(2210, low, high, triangle, 0.5, 170)
    envelope(buf, 10, 0, 1.0, 350)
    echo(buf, 20, 0.3)
    return tobytes(buf)


def si_ufo():
    """Space Invaders UFO on screen sound"""
    low = 400.0
    high = 1550.0
    buf = make_sweep(170, low, high, square, 0.4, 170)
    return tobytes(buf)


def si_aliendie():
    """Space Invaders enemy exploding sound"""
    buf = new_buffer()
    params = {
        "amplitude" : (0.7, 0.7, 0.4, 0.3, 0.25),
        "length" : (80, 80, 80, 100, 120)
    }
    for i in range(len(params["amplitude"])):
        s = 1500.0 if i < len(params["amplitude"]) - 1 else 1900.0
        f = 200.0 if 1 < len(params["amplitude"]) - 1 else 1100.0
        tempbuf = make_sweep(params["length"][i], s, f, triangle, params["amplitude"][i], 0)
        envelope(tempbuf, 5, 0, 1.0, 5)
        buf += tempbuf
    envelope(buf, 5, 0, 1.0, 300)
    echo(buf, 20, 0.3)
    return tobytes(buf)


def si_explosion():
    """Space Invaders player exploding sound"""
    ms = 1600
    buf = make_white(ms, 1.0)
    buf = lowpass_filter(buf, 350.0, order=1)
    noisalise(buf, gain=0.35)
    buf = lowpass_filter(buf, 2600.0)
    buf = median_filter(buf)
    buf = lowpass_filter(buf, 2600.0)
    envelope(buf, 20, 0, 1.0, 20, start=0, end=100)
    envelope(buf, 20, 0, 1.0, 20, start=100, end=180)
    envelope(buf, 5, 0, 0.1, 5, start=180, end=200)
    envelope(buf, 20, 0, 1.0, 20, start=200, end=250)
    envelope(buf, 20, 0, 1.0, 20, start=250, end=300)
    envelope(buf, 20, 0, 0.6, 20, start=300, end=400)
    envelope(buf, 20, 0, 1.0, 20, start=400, end=450)
    envelope(buf, 20, 0, 1.0, 20, start=450, end=500)
    envelope(buf, 20, 20, 0.6, 500, start=500)
    echo(buf, 80, 0.5)
    return tobytes(buf)


def si_playerfire():
    """Space Invaders player firing sound"""
    ms = 400
    freq = 2490.0
    buf = make_white(ms, 1.0)
    start = slice(buf, 0, 300)
    for _ in range(5):
        start = lowpass_filter(start, freq, order=6)
        start = highpass_filter(start, freq, order=6)
    mid = slice(buf, 300, 350)
    for _ in range(5):
        mid = lowpass_filter(mid, freq - 75, order=6)
        mid = highpass_filter(mid, freq - 75, order=6)
    end = slice(buf, 350, 400)
    for _ in range(5):
        end = lowpass_filter(end, freq - 150, order=6)
        end = highpass_filter(end, freq - 150, order=6)
    buf = start + mid + end
    noisalise(buf, gain=0.15)
    envelope(buf, 10, 0, 1.0, 100)
    echo(buf, 40, 0.4)
    return tobytes(buf)


def si_march(freq=53.650):
    """Space Invaders low-frequency marching sound

    Expected frequencies in Hz, 53.650, 50.114, 46.178, 62.465
    """
    ms = 80
    buf = make_sin(ms, 1.0, freq)
    buf = constrain(buf, 0.5, 1.0)
    buf = vmove(buf, -0.6)
    buf = median_filter(buf)
    envelope(buf, 5, 0, 1.0, 5)
    echo(buf, 20, 0.3)
    return tobytes(buf)


