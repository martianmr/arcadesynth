"""arcadesynth - programmatically synthesize retro arcade sound effects
"""

import array
import math
import random
import numpy as np
from scipy.signal import butter, filtfilt, medfilt

DEFAULT_FREQUENCY = 44100
DEFAULT_CHANNELS = 1
MAX_LEN = 3600000
SAMPLE_RATE = DEFAULT_FREQUENCY * DEFAULT_CHANNELS

# ---------------------------------------------------------------------------
# Internal functions
# ---------------------------------------------------------------------------


def _limit(d, limit = 1.0, llimit = None):
    """Force value to a limit"""
    return min(max(d, (-limit if llimit is None else llimit)), limit)


def _butterworth_filter(buf, cutoff, type='lowpass', order=2):
    """A butterworth filter to reduce unwanted frequencies, order 1 is lowest effect, 6 is more dramatic"""
    nyq = 0.5 * SAMPLE_RATE
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=type)
    buf = array.array("d", filtfilt(b, a, buf))
    return buf


def _samplept(func, i, f, harmonics=0, p=[], special=None):
    """Calculate amplitude of a sample for a buffer position

    Given a function to calculate amplitude of a wave (func) for a buffer position (i)
    and frequency (f) calculate and return the amplitude.
    If harmonics is not zero also add in the amplitude of the given order of harmonics.
    If frequency is not constant throughout the buffer, track the current phase during the
    building process and pass the current phase of the primary and any harmonics through 
    the list (p), otherwise phase can be calculated on the fly.
    """
    amp = 0.0
    scaling = math.pow(2, harmonics) / (math.pow(2, harmonics + 1) - 1)
    for h in range(harmonics + 1):
        freq = f * (h + 1)
        vol = (1.0 / (h + 1)) * scaling
        dp = 2 * math.pi * freq / SAMPLE_RATE
        if len(p) == 0:
            phase = dp * i
        else:
            phase = p[h] = p[h] + dp
        a = func(phase, special)
        amp += a * vol
    return amp if len(p) == 0 else (amp, p)


# ---------------------------------------------------------------------------
# Functions to calculate amplitude depending on phase
# ---------------------------------------------------------------------------


def sawtooth(phase, special = None):
    """Calculate amplitude for a sawtooth wave at the given phase"""
    return (2.0 / math.pi) * ((phase / 2.0) % math.pi) - 1.0


def triangle(phase, special = None):
    """Calculate amplitude for a triangle wave at the given phase"""
    return ((2.0 / math.pi) * (math.pi - abs(phase % (2.0 * math.pi) - math.pi)) - 1.0)


def square(phase, special = None):
    """Calculate amplitude for a square wave at the given phase"""
    cutoff = 0.0 if special is None else special
    return 1.0 if math.sin(phase) > cutoff else -1.0


def sin(phase, special = None):
    """Calculate amplitude for a sine wave at the given phase"""
    return math.sin(phase)


# ---------------------------------------------------------------------------
# Functions to manipulate buffers and return a new buffer
# ---------------------------------------------------------------------------


def init(frequency=DEFAULT_FREQUENCY, channels=DEFAULT_CHANNELS):
    """Set up sample rate, do this first to avoid using defaults

    E.g. get these values from pygame with 'frequency, _, channels = pygame.mixer.get_init()'
    """
    global SAMPLE_RATE
    SAMPLE_RATE = frequency * channels
    print("SAMPLE_RATE: ", SAMPLE_RATE)
    return


def tobytes(buf):
    """Convert buffer with range -1.0 to 1.0 to short signed integers then output as a byte stream

    Use this to convert a sound held in internal format to a byte list for external processing, e.g. by
    pygame.
    """
    a = array.array("h")
    for i in range(len(buf)):
        a.append(int(_limit(buf[i]) * 32767))
    return a.tobytes()


def boost(buf, gain):
    """Apply gain to buffer"""
    nparray = np.array(buf)
    npnew = nparray * gain
    buf = array.array("d", npnew)
    return buf


def reverse(buf):
    """Return backwards copy of the buffer"""
    nparray = np.array(buf)
    npnew = np.flip(nparray)
    buf = array.array("d", npnew)
    return buf

def combine(buf1, buf2):
    """Combine 2 buffers giving average amplitude for each sample
    
    N.b. buffers must be of identical length"""
    nparray1 = np.array(buf1)
    nparray2 = np.array(buf2)
    npsummed = nparray1 + nparray2 / 2
    buf = array.array("d", npsummed)
    return buf


def constrain(buf, lower, upper):
    """Clip a buffer to an upper and lower constraint"""
    nparray = np.array(buf)
    np.clip(nparray, lower, upper, nparray)
    buf = array.array("d", nparray)
    return buf


def vmove(buf, amount):
    """Shift samples in the Y axis"""
    nparray = np.array(buf)
    nparray += amount
    buf = array.array("d", nparray)
    return buf


def fade(buf, a1, a2):
    """Change start and end amplitude and scale smoothly between"""
    buf = boost(buf, a1)
    ms = (len(buf) / SAMPLE_RATE) * 1000.0
    envelope(buf, 0, ms, a2 / a1, 0)
    return buf


def noisalise(buf, vol = 1.0, gain = 1.0):
    """Apply gain to buffer proportional to mean amplitude, useful for restoring a constant RMS after processing noise"""
    data = np.array(buf)
    av = (data[data > 0].mean() + -data[data < 0].mean()) / 2.0
    r = gain / (av / 2.0)
    for i in range(len(buf)):
        buf[i] = _limit(buf[i], limit=vol / gain) * r * vol
    return


def slice(buf, start, end):
    """Extract a section of a buffer with start and end times in ms"""
    s = int(SAMPLE_RATE * start / 1000.0)
    e = min(len(buf), int(SAMPLE_RATE * end / 1000.0))
    return buf[s:e]


def median_filter(buf):
    """Perform a median filter"""
    return array.array("d", medfilt(buf, kernel_size=5))


def lowpass_filter(buf, cutoff, order=6):
    """Apply a filter that progressively removes frequencies above the cutoff"""
    return _butterworth_filter(buf, cutoff, type='lowpass', order=order)


def highpass_filter(buf, cutoff, order=6):
    """Apply a filter that progressively removes frequencies below the cutoff"""
    return _butterworth_filter(buf, cutoff, type='highpass', order=order)


# ---------------------------------------------------------------------------
# Functions to create new buffers
# ---------------------------------------------------------------------------


def make_sawtooth(ms, vol=0.2, freq=140.0):
    """Make a sawtooth wave"""
    n = int(SAMPLE_RATE * ms / 1000.0)
    buf = array.array("d")
    for i in range(n):
        buf.append(_samplept(sawtooth, i, freq) * vol)
    return buf


def make_triangle(ms, vol=0.2, freq=140.0):
    """Make a triangle wave"""
    n = int(SAMPLE_RATE * ms / 1000.0)
    buf = array.array("d")
    for i in range(n):
        buf.append(_samplept(triangle, i, freq) * vol)
    return buf


def make_square(ms, vol=0.2, freq=140.0):
    """Make a square wave"""
    n = int(SAMPLE_RATE * ms / 1000.0)
    buf = array.array("d")
    for i in range(n):
        buf.append(_samplept(square, i, freq) * vol)
    return buf


def make_sin(ms=600, vol=0.4, freq=50.0, harmonics=0):
    """Make a sine wave"""
    n = int(SAMPLE_RATE * ms / 1000.0)
    buf = array.array("d")
    for i in range(n):
        a = _samplept(sin, i, freq, harmonics)
        buf.append(a * vol)
    return buf


def make_white(ms=600, vol=0.4, smooth=False):
    """Fill a buffer with random amplitudes to produce white noise

    If smooth is False use values of 1.0 or -1.0 randomly to produce white noise similar to the SN76477 Complex Sound Generator chip,
    otherwise generate purely random amplitudes which gives a more natural noise.
    """
    n = int(SAMPLE_RATE * ms / 1000.0)
    buf = array.array("d")
    random.seed(0)
    rng = random.Random()
    for _ in range(n):
        r = rng.uniform(-1.0, 1.0) * vol
        buf.append(r if smooth else 1.0 if r > 0.0 else -1.0)
    return buf


def make_brown(ms=600, vol=0.1, freq=150.0, order=1):
    """Apply a lowpass filter to white noise to produce brown noise"""
    buf = make_white(ms, vol)
    buf = lowpass_filter(buf, freq, order)
    return buf


def make_sweep(ms=80, startf=1500.0, endf=400.0, shape=triangle, vol=1.0, repeat=0, harmonics=0, special=None):
    """Create a buffer that starts at frequency startf and ends at endf

    If repeat is not zero the cycle goes from startf to endf and back to startf in repeat milliseconds and
    continues to cycle until ms milliseconds have been filled.
    """
    n = int(SAMPLE_RATE * ms / 1000.0)
    loop = n * 2 if repeat == 0 else int(SAMPLE_RATE * repeat / 1000.0)
    period = loop // 2
    buf = array.array("d")
    phase = [0.0 for _ in range(harmonics + 1)]
    for i in range(n):
        x = i % loop
        if x > period:
            x = loop - x
        else:
            pass
        f = (startf - ((startf - endf) * (x / period) ))
        a, phase = _samplept(shape, i, f, harmonics, phase, special)
        buf.append(a * vol)
    return buf


# ---------------------------------------------------------------------------
# Functions to manipulate buffers in place
# ---------------------------------------------------------------------------


def tremolo(buf, freq, intensity, shape=sin):
    """Modify a buffer in place so that amplitude increases and decreases according to shape and intensity"""
    for i in range(len(buf)):
        phase = i * math.pi * freq / SAMPLE_RATE
        buf[i] *= (1.0 - intensity) + abs(((shape(phase) + 1.0) / 2.0) * intensity)
    return


def envelope(buf, attack, decay, sustain, release, start=0, end=MAX_LEN):
    """Modify a buffer in place with an ADSR envelope"""
    attack_start = int(SAMPLE_RATE * start / 1000.0)
    attack_end = min(len(buf), int(SAMPLE_RATE * (start + attack) / 1000.0))
    decay_end = min(len(buf), int(SAMPLE_RATE * decay / 1000.0) + attack_end)
    release_end = min(len(buf), int(SAMPLE_RATE * end / 1000.0))
    sustain_end = min(len(buf), release_end - int(SAMPLE_RATE * release / 1000.0))
    if attack != 0.0:
        for i in range(attack_start, attack_end):
            buf[i] *= (i - attack_start) / (attack_end - attack_start)
    for i in range(attack_end, decay_end):
        buf[i] *= ((decay_end - i) / (decay_end - attack_end)) * (1.0 - sustain) + sustain
    for i in range(decay_end, sustain_end):
        buf[i] *= sustain
    for i in range(sustain_end, release_end):
        buf[i] *= ((release_end - i) / (release_end - sustain_end)) * sustain
    return


def echo(buf, ms, vol):
    """Modify buffer in place to add a short delay to the sound"""
    delay = int(SAMPLE_RATE * ms / 1000.0)
    for _ in range(delay):
        buf.append(0.0)
    for i in range(len(buf)):
        buf[i] *= 1 - vol
        if i >= delay:
            buf[i] += buf[i - delay] * vol
    return




# ---------------------------------------------------------------------------
# Basic sample sounds
# ---------------------------------------------------------------------------


def sawtooth_wave(ms=1600, vol=1.0, freq=150.0):
    """Return bytes representing a simple sawtooth wave"""
    buf = make_sawtooth(ms, vol, freq)
    return tobytes(buf)


def triangle_wave(ms=1600, vol=1.0, freq=150.0):
    """Return bytes representing a simple triangle wave"""
    buf = make_triangle(ms, vol, freq)
    return tobytes(buf)


def sine_wave(ms=600, vol=1.0, freq=150.0):
    """Return bytes representing a simple sine wave"""
    buf = make_sin(ms, vol, freq)
    return tobytes(buf)


def square_wave(ms=90, vol=0.4, freq=144.0):
    """Return bytes representing a simple square wave"""
    buf = make_square(ms, vol, freq)
    return tobytes(buf)


def brown_noise(ms=600, vol=0.4, freq=150.0):
    """Return bytes representing brown noise"""
    buf = make_brown(ms, vol, freq)
    return tobytes(buf)


def white_noise(ms=600, vol=0.4, smooth=False):
    """Return bytes representing white noise"""
    buf = make_white(ms, vol, smooth)
    return tobytes(buf)


def sweep(ms=80, startf=1500.0, endf=100.0, shape=sin, vol=1.0, repeat=0):
    """Return bytes representing a frequency sweep from startf to endf"""
    buf = make_sweep(ms, startf, endf, shape, vol, repeat)
    return tobytes(buf)


def chord(ms=600, vol=0.4, f1=261.6256, f2=329.6276):
    """Return bytes representing a 2 note chord"""
    buf1 = make_square(ms, vol, freq=f1)
    buf2 = make_square(ms, vol, freq=f2)
    buf1 = combine(buf1, buf2)
    return tobytes(buf1)


def fadeup(ms=999, a1=0.2, a2=0.8):
    buf = make_triangle(ms, 1.0, 261.6256)
    buf = fade(buf, a1, a2)
    return tobytes(buf)