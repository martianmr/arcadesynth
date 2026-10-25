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


def _pm_bass(ms, vol, freq):
    f = freq * 0.9333 # Compensate for harmonically complex wave so it sounds in tune.
    buf = _pm_wakka_sweep(ms, f, f)
    return buf


def _pm_intro_bass(ms, vol, freq):
    buf = _pm_bass(ms, vol, freq)
    envelope(buf, 0, 0, vol, ms)
    return buf


def _pm_inter_bass(ms, vol, freq):
    buf = _pm_bass(ms, vol, freq)
    envelope(buf, 0, 0, vol, 0)
    envelope(buf, 0, ms, 0.8, 0)
    return buf


def _pm_organ_sample(p, _):
    return (sin(p * 4) / 4) + (triangle(p * 2) / 2) + (sin(p) / 2)


def _pm_organ(ms, vol, freq):
    n = ms_to_samples(ms)
    buf = new_buffer()
    for i in range(n):
        a = samplept(_pm_organ_sample, i, freq)
        buf.append(a * vol)
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
    """First part of pac-man chomping sound, there is a gap of about 83ms between parts 1 and 2"""
    buf = _pm_wakka_sweep(83, 350, 816)
    return tobytes(buf)


def pm_wakka2():
    """Second part of pac-man chomping sound, there is a gap of about 83ms between parts 1 and 2"""
    buf = _pm_wakka_sweep(83, 816, 350)
    return tobytes(buf)


def pm_siren1():
    """Lower siren 1 at start of level"""
    buf = make_sweep(400, 350, 900, triangle, 0.25, 400)
    return tobytes(buf)


def pm_siren2():
    """Higher siren 2"""
    buf = make_sweep(365, 500, 1050, triangle, 0.25, 365)
    return tobytes(buf)


def pm_siren3():
    """Higher siren 3"""
    buf = make_sweep(330, 600, 1200, triangle, 0.25, 330)
    return tobytes(buf)


def pm_siren4():
    """Higher siren 4"""
    buf = make_sweep(300, 700, 1350, triangle, 0.25, 300)
    return tobytes(buf)


def pm_siren5():
    """Higher siren 5"""
    buf = make_sweep(265, 800, 1500, triangle, 0.25, 265)
    return tobytes(buf)


def pm_die():
    """Noise made when pac-man dies"""
    buf = make_sweep(180, 725, 575, _pm_organ_sample, 0.6, 180)
    buf += make_sweep(200, 625, 510, _pm_organ_sample, 0.57, 200)
    buf += make_sweep(200, 590, 460, _pm_organ_sample, 0.54, 200)
    buf += make_sweep(200, 520, 410, _pm_organ_sample, 0.51, 200)
    buf += make_sweep(200, 490, 380, _pm_organ_sample, 0.48, 200)
    buf += make_sweep(130, 450, 320, _pm_organ_sample, 0.45, 130)
    buf += make_sweep(180, 150, 2000, sin, 0.35)
    pad(buf, len(buf) + ms_to_samples(17))
    buf += make_sweep(180, 150, 2000, sin, 0.35)
    return tobytes(buf)


def pm_energizer():
    """Noise made after eating the big pill when ghosts turn blue, repeats"""
    buf = new_buffer()
    lengths = (970, 675, 457, 429, 341, 341, 277, 272, 272, 228, 228, 228, 210, 195, 195, 195, 182, 173, 170, 170, 170)
    for i in range(len(lengths)):
        ms = samples_to_ms(lengths[i]) * 0.916
        f = 8 / (ms / 1000.0)
        tempbuf = make_square(ms, 0.5, f)
        envelope(tempbuf, 0, 0, 1.0, ms)
        buf += tempbuf
    return tobytes(buf)


def pm_eat_ghost():
    """Noise made when eating a blue ghost"""
    buf = new_buffer()
    lengths = (3273, 1330, 1226, 927, 800, 700, 680, 650, 630, 580, 560, 535, 500, 490, 470, 460, 440, 415, 415, 410, 410, 390, 390,
               360, 360, 350, 350, 335, 335, 320, 320, 320, 320, 300, 300, 280, 280, 280, 280, 270, 270, 270, 270, 270, 270, 270, 240, 240)
    for i in range(len(lengths)):
        ms = samples_to_ms(lengths[i]) * 0.94
        f = 8 / (ms / 1000.0)
        tempbuf = make_square(ms, 0.5, f)
        if i % 2 == 0:
            envelope(tempbuf, ms, 0, 1.0, 0)
        else:
            envelope(tempbuf, 0, 0, 1.0, ms)
        buf += tempbuf
    return tobytes(buf)


def pm_intermission():
    """Intermission music played after levels 2, 5 and 9"""
    buf = new_buffer()
    notes = (
        ("F#3", 0, 2, 0.5, _pm_inter_bass),
        ("F4", 0, 0.5, 0.5, _pm_organ),
        ("F#4", 0.5, 2, 0.5, _pm_organ),
        ("F4", 2.5, 0.5, 0.5, _pm_organ),
        ("F#4", 3.0, 2, 0.5, _pm_organ),
        ("F#3", 3.5, 1, 0.5, _pm_inter_bass),
        ("F#3", 5, 2, 0.5, _pm_inter_bass),
        ("F4", 5, 0.5, 0.5, _pm_organ),
        ("F#4", 5.5, 2, 0.5, _pm_organ),
        ("D4", 7.5, 0.5, 0.5, _pm_organ),
        ("D#4", 8, 1.0, 0.5, _pm_organ),
        ("F#3", 8.5, 1, 0.5, _pm_inter_bass),
        ("C#4", 9, 1, 0.5, _pm_organ),
        ("F#3", 10, 2, 0.5, _pm_inter_bass),
        ("F#4", 10, 1, 0.5, _pm_organ),
        ("F#4", 11.5, 2, 0.5, _pm_organ),
        ("F#3", 13.5, 1, 0.5, _pm_inter_bass),
        ("A4", 13.5, 0.5, 0.5, _pm_organ),
        ("A#4", 14, 4, 0.5, _pm_organ),
        ("A#3", 14.95, 0.9, 0.5, _pm_inter_bass),
        ("B3", 16.2, 0.9, 0.5, _pm_inter_bass),
        ("C4", 17.45, 0.9, 0.5, _pm_inter_bass),
        ("C#4", 18.7, 0.9, 0.5, _pm_inter_bass),
        ("F#3", 19.95, 2, 0.5, _pm_inter_bass),
        ("F4", 19.95, 0.45, 0.5, _pm_organ),
        ("F#4", 20.4, 1.85, 0.5, _pm_organ),
        ("F4", 22.25, 0.5, 0.5, _pm_organ),
        ("F#4", 22.75, 2, 0.5, _pm_organ),
    )
    buf = add(buf, sequence(66, notes, 0.978), 0)
    notes = (
        ("F#3", 0, 1, 0.5, _pm_inter_bass),
        ("F#3", 1.5, 2, 0.5, _pm_inter_bass),
        ("F4", 1.5, 0.5, 0.5, _pm_organ),
        ("F#4", 2, 2, 0.5, _pm_organ),
        ("D4", 4, 0.5, 0.5, _pm_organ),
        ("D#4", 4.5, 1.0, 0.5, _pm_organ),
        ("F#3", 5, 1, 0.5, _pm_inter_bass),
        ("C#4", 5.5, 1, 0.5, _pm_organ),
        ("F#3", 6.5, 2, 0.5, _pm_inter_bass),
        ("F#4", 6.5, 1, 0.5, _pm_organ),
        ("F#4", 8, 2, 0.5, _pm_organ),
        ("F#3", 10, 1, 0.5, _pm_inter_bass),
        ("D4", 10, 0.5, 0.5, _pm_organ),
        ("D#4", 10.5, 4, 0.5, _pm_organ),
        ("A#3", 11.45, 0.9, 0.5, _pm_inter_bass),
        ("B3", 12.7, 0.9, 0.5, _pm_inter_bass),
        ("C4", 13.95, 0.9, 0.5, _pm_inter_bass),
        ("C#4", 15.2, 0.9, 0.5, _pm_inter_bass),
    )
    buf = add(buf, sequence(66, notes, 0.978), 1523)
    notes = (
        ("F#3", 0, 2, 0.5, _pm_inter_bass),
        ("F4", 0, 0.5, 0.5, _pm_organ),
        ("F#4", 0.5, 2, 0.5, _pm_organ),
        ("F4", 2.5, 0.5, 0.5, _pm_organ),
        ("F#4", 3.0, 2, 0.5, _pm_organ),
        ("F#3", 3.5, 1, 0.5, _pm_inter_bass),
        ("F#3", 5, 2, 0.5, _pm_inter_bass),
        ("F4", 5, 0.5, 0.5, _pm_organ),
        ("F#4", 5.5, 2, 0.5, _pm_organ),
        ("D4", 7.5, 0.5, 0.5, _pm_organ),
        ("D#4", 8, 1.0, 0.5, _pm_organ),
        ("F#3", 8.5, 1, 0.5, _pm_inter_bass),
        ("C#4", 9, 1, 0.5, _pm_organ),
        ("F#3", 10, 2, 0.5, _pm_inter_bass),
        ("F#4", 10, 1, 0.5, _pm_organ),
        ("F#4", 11.5, 2, 0.5, _pm_organ),
        ("F#3", 13.5, 1, 0.5, _pm_inter_bass),
        ("G#4", 13.5, 0.5, 0.5, _pm_organ),
        ("A4", 14, 1.85, 0.5, _pm_organ),
        ("A#3", 14.95, 0.9, 0.5, _pm_inter_bass),
        ("A#4", 15.85, 0.35, 0.5, _pm_organ),
        ("B3", 16.2, 0.9, 0.5, _pm_inter_bass),
        ("B4", 16.2, 2.15, 0.5, _pm_organ),
        ("C4", 17.45, 0.9, 0.5, _pm_inter_bass),
        ("C#4", 18.7, 0.9, 0.5, _pm_inter_bass),
        ("B4", 19, 0.3, 0.5, _pm_organ),
        ("C5", 19.3, 2.95, 0.5, _pm_organ),
        ("F#4", 19.95, 2, 0.5, _pm_inter_bass),
        ("C#4", 21.95, 1.4, 0.5, _pm_inter_bass),
        ("A#4", 22.25, 0.3, 0.5, _pm_organ),
        ("B4", 22.55, 2.35, 0.5, _pm_organ),
        ("C4", 23.65, 0.85, 0.5, _pm_inter_bass),
        ("B3", 24.9, 0.9, 0.5, _pm_inter_bass),
        ("G#4", 24.9, 0.3, 0.5, _pm_organ),
        ("A4", 25.2, 2.2, 0.5, _pm_organ),
        ("A3", 26.19, 0.8666, 0.5, _pm_inter_bass),
        ("F#4", 27.4, 2.5, 0.5, _pm_organ),
        ("F#3", 27.4, 0.8565, 0.5, _pm_inter_bass),
        ("F#3", 28.65, 0.8565, 0.5, _pm_inter_bass),
        ("E3", 29.9, 1.9, 0.5, _pm_inter_bass),
        ("G#4", 29.9, 0.3, 0.5, _pm_organ),
        ("A4", 30.2, 2.6, 0.5, _pm_organ),
        ("F3", 32.4, 1.95, 0.5, _pm_inter_bass),
        ("F4", 32.8, 0.3, 0.3, _pm_organ),
        ("F#4", 33.1, 4.6, 0.5, _pm_organ),
        ("F#3", 34.9, 1.85, 0.5, _pm_inter_bass),
        ("F#3", 36.85, 0.6, 0.5, _pm_inter_bass),
    )
    buf = add(buf, sequence(66, notes, 0.978), 2607)
    notes = (
        ("F#3", 0, 2, 0.5, _pm_inter_bass),
        ("F4", 0, 0.5, 0.5, _pm_organ),
        ("F#4", 0.5, 2, 0.5, _pm_organ),
        ("F4", 2.5, 0.5, 0.5, _pm_organ),
        ("F#4", 3.0, 2, 0.5, _pm_organ),
        ("F#3", 3.5, 1, 0.5, _pm_inter_bass),
        ("F#3", 5, 2, 0.5, _pm_inter_bass),
        ("F4", 5, 0.5, 0.5, _pm_organ),
        ("F#4", 5.5, 2, 0.5, _pm_organ),
        ("D4", 7.5, 0.5, 0.5, _pm_organ),
        ("D#4", 8, 1.0, 0.5, _pm_organ),
        ("F#3", 8.5, 1, 0.5, _pm_inter_bass),
        ("C#4", 9, 1, 0.5, _pm_organ),
        ("F#3", 10, 2, 0.5, _pm_inter_bass),
        ("F#4", 10, 1, 0.5, _pm_organ),
        ("F#4", 11.5, 2, 0.5, _pm_organ),
        ("F#3", 13.5, 1, 0.5, _pm_inter_bass),
        ("A4", 13.5, 0.5, 0.5, _pm_organ),
        ("A#4", 14, 4, 0.5, _pm_organ),
        ("A#3", 14.95, 0.9, 0.5, _pm_inter_bass),
        ("B3", 16.2, 0.9, 0.5, _pm_inter_bass),
        ("C4", 17.45, 0.9, 0.5, _pm_inter_bass),
        ("C#4", 18.7, 0.9, 0.5, _pm_inter_bass),
    )
    buf = add(buf, sequence(66, notes, 0.978), 5235)
    notes = (
        ("F#3", 0, 2, 0.5, _pm_inter_bass),
        ("F4", 0, 0.5, 0.5, _pm_organ),
        ("F#4", 0.5, 2, 0.5, _pm_organ),
        ("F4", 2.5, 0.5, 0.5, _pm_organ),
        ("F#4", 3.0, 2, 0.5, _pm_organ),
        ("F#3", 3.5, 1, 0.5, _pm_inter_bass),
        ("F#3", 5, 2, 0.5, _pm_inter_bass),
        ("F4", 5, 0.5, 0.5, _pm_organ),
        ("F#4", 5.5, 2, 0.5, _pm_organ),
        ("D4", 7.5, 0.5, 0.5, _pm_organ),
        ("D#4", 8, 1.0, 0.5, _pm_organ),
        ("F#3", 8.5, 1, 0.5, _pm_inter_bass),
        ("C#4", 9, 1, 0.5, _pm_organ),
        ("F#3", 10, 2, 0.5, _pm_inter_bass),
        ("F#4", 10, 1, 0.5, _pm_organ),
        ("F#4", 11.5, 2, 0.5, _pm_organ),
        ("F#3", 13.5, 1, 0.5, _pm_inter_bass),
        ("D4", 13.5, 0.5, 0.5, _pm_organ),
        ("D#4", 14, 4, 0.5, _pm_organ),
        ("A#3", 14.95, 0.9, 0.5, _pm_inter_bass),
        ("B3", 16.2, 0.9, 0.5, _pm_inter_bass),
        ("C4", 17.45, 0.9, 0.5, _pm_inter_bass),
        ("C#4", 18.7, 0.9, 0.5, _pm_inter_bass),
    )
    buf = add(buf, sequence(66, notes, 0.978), 6551)
    notes = (
        ("F#3", 0, 2, 0.5, _pm_inter_bass),
        ("F4", 0, 0.5, 0.5, _pm_organ),
        ("F#4", 0.5, 2, 0.5, _pm_organ),
        ("F4", 2.5, 0.5, 0.5, _pm_organ),
        ("F#4", 3.0, 2, 0.5, _pm_organ),
        ("F#3", 3.5, 1, 0.5, _pm_inter_bass),
        ("F#3", 5, 2, 0.5, _pm_inter_bass),
        ("F4", 5, 0.5, 0.5, _pm_organ),
        ("F#4", 5.5, 2, 0.5, _pm_organ),
        ("D4", 7.5, 0.5, 0.5, _pm_organ),
        ("D#4", 8, 1.0, 0.5, _pm_organ),
        ("F#3", 8.5, 1, 0.5, _pm_inter_bass),
        ("C#4", 9, 1, 0.5, _pm_organ),
        ("F#3", 10, 2, 0.5, _pm_inter_bass),
        ("F#4", 10, 1, 0.5, _pm_organ),
        ("F#4", 11.5, 2, 0.5, _pm_organ),
        ("F#3", 13.5, 1, 0.5, _pm_inter_bass),
        ("G#4", 13.5, 0.5, 0.5, _pm_organ),
        ("A4", 14, 1.85, 0.5, _pm_organ),
        ("A#3", 14.95, 0.9, 0.5, _pm_inter_bass),
        ("A#4", 15.85, 0.35, 0.5, _pm_organ),
        ("B3", 16.2, 0.9, 0.5, _pm_inter_bass),
        ("B4", 16.2, 2.15, 0.5, _pm_organ),
        ("C4", 17.45, 0.9, 0.5, _pm_inter_bass),
        ("C#4", 18.7, 0.9, 0.5, _pm_inter_bass),
        ("B4", 19, 0.3, 0.5, _pm_organ),
        ("C5", 19.3, 2.95, 0.5, _pm_organ),
        ("F#4", 19.95, 2, 0.5, _pm_inter_bass),
        ("C#4", 21.95, 1.4, 0.5, _pm_inter_bass),
        ("A#4", 22.25, 0.3, 0.5, _pm_organ),
        ("B4", 22.55, 2.35, 0.5, _pm_organ),
        ("C4", 23.65, 0.85, 0.5, _pm_inter_bass),
        ("B3", 24.9, 0.9, 0.5, _pm_inter_bass),
        ("G#4", 24.9, 0.3, 0.5, _pm_organ),
        ("A4", 25.2, 2.2, 0.5, _pm_organ),
        ("A3", 26.19, 0.8666, 0.5, _pm_inter_bass),
        ("F#4", 27.4, 2.5, 0.5, _pm_organ),
        ("F#3", 27.4, 0.8565, 0.5, _pm_inter_bass),
        ("F#3", 28.65, 0.8565, 0.5, _pm_inter_bass),
        ("E3", 29.9, 1.9, 0.5, _pm_inter_bass),
        ("G#4", 29.9, 0.3, 0.5, _pm_organ),
        ("A4", 30.2, 2.6, 0.5, _pm_organ),
        ("F3", 32.4, 1.95, 0.5, _pm_inter_bass),
        ("F4", 32.8, 0.3, 0.3, _pm_organ),
        ("F#4", 33.1, 4.6, 0.5, _pm_organ),
        ("F#3", 34.9, 1.85, 0.5, _pm_inter_bass),
        ("F#3", 36.85, 0.6, 0.5, _pm_inter_bass),
    )
    buf = add(buf, sequence(66, notes, 0.978), 7864)
    return tobytes(buf)


def pm_intro():
    """Pac-Man intro music"""
    notes = (
        ("C3", 0, 4, 0.5, _pm_intro_bass),
        ("C5", 0, 1, 0.5, make_sin),
        ("C6", 2, 1, 0.5, make_sin),
        ("G5", 4, 1, 0.5, make_sin),
        ("G3", 6, 4, 0.5, _pm_intro_bass),
        ("E5", 6, 1, 0.5, make_sin),
        ("C3", 8, 4, 0.5, _pm_intro_bass),
        ("C6", 8, 1, 0.5, make_sin),
        ("G5", 9, 1, 0.5, make_sin),
        ("E5", 12, 2, 0.5, make_sin),
        ("G3", 14, 4, 0.5, _pm_intro_bass),
        ("C#3", 16, 4, 0.5, _pm_intro_bass),
        ("C#5", 16, 1, 0.5, make_sin),
        ("C#6", 18, 1, 0.5, make_sin),
        ("G#5", 20, 1, 0.5, make_sin),
        ("G#3", 22, 4, 0.5, _pm_intro_bass),
        ("F5", 22, 1, 0.5, make_sin),
        ("C#3", 24, 4, 0.5, _pm_intro_bass),
        ("C#6", 24, 1, 0.5, make_sin),
        ("G#5", 25, 1, 0.5, make_sin),
        ("F5", 28, 2, 0.5, make_sin),
        ("G#3", 30, 4, 0.5, _pm_intro_bass),
        ("C3", 32, 4, 0.5, _pm_intro_bass),
        ("C5", 32, 1, 0.5, make_sin),
        ("C6", 34, 1, 0.5, make_sin),
        ("G5", 36, 1, 0.5, make_sin),
        ("G3", 38, 4, 0.5, _pm_intro_bass),
        ("E5", 38, 1, 0.5, make_sin),
        ("C3", 40, 4, 0.5, _pm_intro_bass),
        ("C6", 40, 1, 0.5, make_sin),
        ("G5", 41, 1, 0.5, make_sin),
        ("E5", 44, 2, 0.5, make_sin),
        ("G3", 46, 4, 0.5, _pm_intro_bass),
        ("G3", 48, 4, 0.5, _pm_intro_bass),
        ("D#5", 48, 1, 0.5, make_sin),
        ("E5", 49, 1, 0.5, make_sin),
        ("F5", 50, 1, 0.5, make_sin),
        ("A3", 52, 4, 0.5, _pm_intro_bass),
        ("F#5", 52, 1, 0.5, make_sin),
        ("G5", 53, 1, 0.5, make_sin),
        ("G#5", 54, 1, 0.5, make_sin),
        ("B3", 56, 4, 0.5, _pm_intro_bass),
        ("A5", 56, 1, 0.5, make_sin),
        ("A#5", 57, 1, 0.5, make_sin),
        ("B5", 58, 1, 0.5, make_sin),
        ("C4", 60, 4, 0.5, _pm_intro_bass),
        ("C6", 60, 2, 0.5, make_sin),
    )
    buf = sequence(66, notes, 1.022)
    return tobytes(buf)


def pm_wakkatest():
    buf = new_buffer()
    buf = add(buf, make_sweep(400, 350, 950, triangle, 0.25, 400), 0)
    buf = add(buf, make_sweep(400, 350, 950, triangle, 0.25, 400), 400)
    buf = add(buf, make_sweep(400, 350, 950, triangle, 0.25, 400), 800)
    buf = add(buf, make_sweep(400, 350, 950, triangle, 0.25, 400), 1200)
    buf = add(buf, _pm_wakka_sweep(83, 350, 816), 80)
    buf = add(buf, _pm_wakka_sweep(83, 816, 350), 240)
    return tobytes(buf)

def pm_sirentest():
    return pm_siren1() + pm_siren2() + pm_siren3() + pm_siren4() + pm_siren5()