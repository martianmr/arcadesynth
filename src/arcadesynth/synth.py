"""synth - programmatically synthesize retro arcade sound effects
"""

import array
import math
import random
import numpy as np
from scipy.signal import butter, filtfilt, medfilt

DEFAULT_FREQUENCY = 44100
DEFAULT_CHANNELS = 2
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
    buf = new_buffer(filtfilt(b, a, buf))
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


def _ms_to_samples(ms):
    """Convert time in milliseconds to number of samples"""
    return int(SAMPLE_RATE * ms / 1000.0)


def _samples_to_ms(n):
    """Convert number of samples to time in milliseconds"""
    return (n / SAMPLE_RATE) * 1000.0


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
    """Calculate amplitude for a square wave at the given phase
    
    special can be specified as a cutoff for generating PWM
    """
    cutoff = 0.0 if special is None else special
    return 1.0 if math.sin(phase) > cutoff else -1.0


def sin(phase, special = None):
    """Calculate amplitude for a sine wave at the given phase
    
    special can be used to simulate lower precision math
    """
    return math.sin(phase) if special is None else round((math.sin(phase) / special), 1) * special


# ---------------------------------------------------------------------------
# Initialisation functions
# ---------------------------------------------------------------------------


def init(frequency=DEFAULT_FREQUENCY, channels=DEFAULT_CHANNELS):
    """Set up sample rate, do this first to avoid using defaults

    E.g. get these values from pygame with 'frequency, _, channels = pygame.mixer.get_init()'
    """
    global SAMPLE_RATE
    SAMPLE_RATE = frequency * channels
    return


def get_init():
    return SAMPLE_RATE


# ---------------------------------------------------------------------------
# General helper functions
# ---------------------------------------------------------------------------


# Note frequencies starting at C9, flats are omitted
frequency9 = {
    "C": 8372.018,
    "C#": 8869.844,
    "D": 9397.272,
    "D#": 9956.064,
    "E": 10548.084,
    "F": 11175.304,
    "F#": 11839.82,
    "G": 12543.856,
    "G#": 13289.752,
    "A": 14080,
    "A#": 14917.24,
    "B": 15804.264,
}



def notehz(note):
    """For a given note e.g. "A4", return the frequency in Hz"""
    hz = frequency9[note[:-1]]
    octave = int(note[-1])
    for _ in range(9, octave, -1):
        hz /= 2
    return hz


# ---------------------------------------------------------------------------
# Functions to manipulate buffers and return a new buffer
# ---------------------------------------------------------------------------


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
    buf = new_buffer(npnew)
    return buf


def reverse(buf):
    """Return backwards copy of the buffer"""
    nparray = np.array(buf)
    npnew = np.flip(nparray)
    buf = new_buffer(npnew)
    return buf


def combine(buf1, buf2):
    """Combine 2 buffers giving average amplitude for each sample"""
    if (len(buf1) != len(buf2)):
        pad(buf1 if len(buf1) < len(buf2) else buf2, max(len(buf1), len(buf2)))
    nparray1 = np.array(buf1)
    nparray2 = np.array(buf2)
    npsummed = nparray1 + nparray2 / 2
    buf = new_buffer(npsummed)
    return buf


def add(target, source, offset=0):
    """Add the source sample to the target buffer"""
    olen = _ms_to_samples(offset)
    tlen = len(source) + olen
    if (len(target) < tlen):
        pad(target, tlen)
    post = target[tlen:]
    pre = target[:olen]
    nparray1 = np.array(target[olen:tlen])
    nparray2 = np.array(source)
    npsummed = nparray1 + nparray2
    buf = pre + new_buffer(npsummed) + post
    return buf


def constrain(buf, lower, upper):
    """Clip a buffer to an upper and lower constraint"""
    nparray = np.array(buf)
    np.clip(nparray, lower, upper, nparray)
    buf = new_buffer(nparray)
    return buf


def vmove(buf, amount):
    """Shift samples in the Y axis"""
    nparray = np.array(buf)
    nparray += amount
    buf = new_buffer(nparray)
    return buf


def fade(buf, a1, a2):
    """Change start and end amplitude and scale smoothly between"""
    buf = boost(buf, a1)
    ms = _samples_to_ms(len(buf))
    envelope(buf, 0, ms, a2 / a1, 0)
    return buf


def slice(buf, start, end):
    """Extract a section of a buffer with start and end times in ms"""
    s = _ms_to_samples(start)
    e = min(len(buf), _ms_to_samples(end))
    return buf[s:e]


def median_filter(buf):
    """Perform a median filter"""
    return new_buffer(medfilt(buf, kernel_size=5))


def lowpass_filter(buf, cutoff, order=6):
    """Apply a filter that progressively removes frequencies above the cutoff"""
    return _butterworth_filter(buf, cutoff, type='lowpass', order=order)


def highpass_filter(buf, cutoff, order=6):
    """Apply a filter that progressively removes frequencies below the cutoff"""
    return _butterworth_filter(buf, cutoff, type='highpass', order=order)


# ---------------------------------------------------------------------------
# Functions to create new buffers
# ---------------------------------------------------------------------------


def new_buffer(content=[]):
    """Create a new buffer of floating point amplitudes"""
    return array.array("d", content)


def sequence(beatlen, notes):
    """Sequence notes to a buffer for creating music
    
    'beatlen' is the length of each beat in the sequence in milliseconds.
    'notes' is a list of notes, each element of the list is in the following format:
    [note_name, start_beat, length_in_beats, velocity, creation_function]
    The creation function must have the parameter format (ms, volume, frequency)
    """
    buf = new_buffer()
    for note in notes:
        hz = notehz(note[0])
        beat = note[1] * beatlen
        length = note[2] * beatlen
        velocity = note[3]
        func = note[4]
        buf = add(buf, func(length, velocity, hz), beat)
    return buf


def make_sawtooth(ms, vol=0.2, freq=140.0):
    """Make a sawtooth wave"""
    n = _ms_to_samples(ms)
    buf = new_buffer()
    for i in range(n):
        buf.append(_samplept(sawtooth, i, freq) * vol)
    return buf


def make_triangle(ms, vol=0.2, freq=140.0):
    """Make a triangle wave"""
    n = _ms_to_samples(ms)
    buf = new_buffer()
    for i in range(n):
        buf.append(_samplept(triangle, i, freq) * vol)
    return buf


def make_square(ms, vol=0.2, freq=140.0, pwm=None):
    """Make a square wave"""
    n = _ms_to_samples(ms)
    buf = new_buffer()
    for i in range(n):
        buf.append(_samplept(square, i, freq, 0, special=pwm) * vol)
    return buf


def make_sin(ms=600, vol=0.4, freq=50.0, harmonics=0, precision=None):
    """Make a sine wave"""
    n = _ms_to_samples(ms)
    buf = new_buffer()
    for i in range(n):
        a = _samplept(sin, i, freq, harmonics, special=precision)
        buf.append(a * vol)
    return buf


def make_white(ms=600, vol=0.4, smooth=False):
    """Fill a buffer with random amplitudes to produce white noise

    If smooth is False use values of 1.0 or -1.0 randomly to produce white noise similar to the SN76477 Complex Sound Generator chip,
    otherwise generate purely random amplitudes which gives a more natural noise.
    """
    n = _ms_to_samples(ms)
    buf = new_buffer()
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
    n = _ms_to_samples(ms)
    loop = n * 2 if repeat == 0 else _ms_to_samples(repeat)
    period = loop // 2
    buf = new_buffer()
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


def pad(buf, length):
    """Pad out a buffer with zeroes to length"""
    if len(buf) < length:
        buf += new_buffer([0.0] * (length - len(buf)))
    return


def tremolo(buf, freq, intensity, shape=sin, special=None):
    """Modify a buffer in place so that amplitude increases and decreases according to shape and intensity"""
    for i in range(len(buf)):
        phase = i * math.pi * freq / SAMPLE_RATE
        buf[i] *= (1.0 - intensity) + abs(((shape(phase, special) + 1.0) / 2.0) * intensity)
    return


def noisalise(buf, vol = 1.0, gain = 1.0):
    """Apply gain to buffer proportional to mean amplitude, useful for restoring a constant RMS after processing noise"""
    data = np.array(buf)
    av = (data[data > 0].mean() + -data[data < 0].mean()) / 2.0
    r = gain / (av / 2.0)
    for i in range(len(buf)):
        buf[i] = _limit(buf[i], limit=vol / gain) * r * vol
    return


def envelope(buf, attack, decay, sustain, release, start=0, end=MAX_LEN):
    """Modify a buffer in place with an ADSR envelope"""
    attack_start = _ms_to_samples(start)
    attack_end = min(len(buf), _ms_to_samples(start + attack))
    decay_end = min(len(buf), _ms_to_samples(decay) + attack_end)
    release_end = min(len(buf), _ms_to_samples(end))
    sustain_end = min(len(buf), release_end - _ms_to_samples(release))
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
    delay = _ms_to_samples(ms)
    for _ in range(delay):
        buf.append(0.0)
    for i in range(len(buf)):
        buf[i] *= 1 - vol
        if i >= delay:
            buf[i] += buf[i - delay] * vol
    return
