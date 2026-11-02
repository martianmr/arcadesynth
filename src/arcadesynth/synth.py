"""functions to programmatically synthesize retro arcade sound effects

[source](../src/arcadesynth/synth.py)
"""

import array
import math
import random
import numpy as np
from scipy.signal import butter, filtfilt, medfilt

FREQUENCY = 44100
CHANNELS = 2
MAX_LEN = 3600000
SAMPLE_RATE = FREQUENCY * CHANNELS
CACHE = {}

# ---------------------------------------------------------------------------
# Internal functions
# ---------------------------------------------------------------------------


def _check_cache(func, length, volume, frequency):
    hash_value = hash((func, length, volume, frequency))
    if hash_value not in CACHE:
        CACHE[hash_value] = func(length, volume, frequency)
    return CACHE[hash_value]


def _limit(d, limit = 1.0, llimit = None):
    """Force value to a limit

    Args:
        d: data point to limit
        limit: upper limit
        llimit: lower limit (optional)

    Returns:
        limited value
    """
    return min(max(d, (-limit if llimit is None else llimit)), limit)


def _butterworth_filter(buf, cutoff, type='lowpass', order=2):
    """A butterworth filter to reduce unwanted frequencies

    Args:
        buf: sample buffer
        cutoff: cutoff frequency in Hz
        type: one of 'lowpass', 'highpass', 'bandpass', 'bandstop'
        order: determines how much effect the filter has, order 1 is lowest effect, 6 is more dramatic

    Returns:
        updated buffer with filter applied    
    """
    nyq = 0.5 * SAMPLE_RATE
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=type)
    buf = new_buffer(filtfilt(b, a, buf))
    return buf


# ---------------------------------------------------------------------------
# Functions to calculate amplitude depending on phase
# ---------------------------------------------------------------------------


def sawtooth(phase, _=None):
    """Calculate amplitude for a sawtooth wave at the given phase

    Args:
        phase: calculated phase based on frequency and time

    Returns:
        amplitude of sample
    """
    return (2.0 / math.pi) * ((phase / 2.0) % math.pi) - 1.0


def triangle(phase, _=None):
    """Calculate amplitude for a triangle wave at the given phase
    
    Args:
        phase: calculated phase based on frequency and time

    Returns:
        amplitude of sample
    """
    return ((2.0 / math.pi) * (math.pi - abs(phase % (2.0 * math.pi) - math.pi)) - 1.0)


def square(phase, pwm=None):
    """Calculate amplitude for a square wave at the given phase
    
    Args:
        phase: calculated phase based on frequency and time
        pwm: cutoff value between -1.0 and 1.0 to create pulse wave modulation on the intersection (optional) 

    Returns:
        amplitude of sample
    """
    cutoff = 0.0 if pwm is None else pwm
    return 1.0 if math.sin(phase) > cutoff else -1.0


def sin(phase, precision=None):
    """Calculate amplitude for a sine wave at the given phase

    Args:
        phase: calculated phase based on frequency and time
        precision: set to an integer value to simulate lower precision math (optional)

    Returns:
        amplitude of sample
    """
    return math.sin(phase) if precision is None else round((math.sin(phase) / precision), 1) * precision


def synth_organ(p, _=None):
    """Calculate amplitude for a synth organ sound at the given phase

    Combination of octave harmonics of sine waves and a triangle wave at first octave to give a synth organ sound
    As used in pac-man intermission music and pac-man die sounds

    Args:
        phase: calculated phase based on frequency and time

    Returns:
        amplitude of sample
    """
    return (sin(p * 8) / 12) + (sin(p * 4) / 6) + (triangle(p * 2) / 3) + (sin(p) / 3)


# ---------------------------------------------------------------------------
# Initialisation functions
# ---------------------------------------------------------------------------


def init(frequency=FREQUENCY, channels=CHANNELS):
    """Set up sample rate, do this first to avoid using defaults

    The init function calculates the number of samples needed to construct consistent sounds for internal use
    E.g. get these values from pygame with 'frequency, _, channels = pygame.mixer.get_init()'

    Args:
        frequency: frequency of each channel
        channels: number of channels

    Returns:
        None

    """
    global SAMPLE_RATE, CHANNELS, FREQUENCY
    CHANNELS = channels
    FREQUENCY = frequency
    SAMPLE_RATE = frequency * channels
    return


def get_init():
    """Return the configured calculated sample rate
    
    Returns:
        calculated sample rate
    """
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
    """For a given note return the frequency

    Args:
        note: note name as a string, e.g. "A4" or "C#3", flats are not supported

    Returns:
        frequency in Hz
    """
    hz = frequency9[note[:-1]]
    octave = int(note[-1])
    for _ in range(9, octave, -1):
        hz /= 2
    return hz


def samplept(func, i, f, harmonics=0, p=[], special=None):
    """Calculate amplitude of a sample for a buffer position

    Given a function to calculate amplitude of a wave (func) for a buffer position (i)
    and frequency (f) calculate and return the amplitude.
    If harmonics is not zero also add in the amplitude of the given order of harmonics.
    If frequency is not constant throughout the buffer, track the current phase during the
    building process and pass the current phase of the primary and any harmonics through 
    the list (p), otherwise phase can be calculated on the fly.

    Args:
        func: the function to use to calculate the amplitude for the sample
        i: numeric index to position of sample in buffer
        f: target frequency
        harmonics: number of natural harmonics to add (optional)
        p: list containing current phase of primary and any harmonics (optional)
        special: special parameters for modifying some functions (optional)

    Returns:
        - amplitude of sample at current index and phase,
        - updated phase list (if optional p parameter was provided)
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


def ms_to_samples(ms):
    """Convert time in milliseconds to number of samples

    Args:
        ms: time in milliseconds

    Returns:
        number of samples in buffer
    """
    return int(SAMPLE_RATE * ms / 1000.0)


def samples_to_ms(n):
    """Convert number of samples to time in milliseconds

    Args:
        n: number of samples in buffer

    Returns:
        time in milliseconds
    """
    return (n / SAMPLE_RATE) * 1000.0


# ---------------------------------------------------------------------------
# Functions to manipulate buffers and return a new buffer
# ---------------------------------------------------------------------------


def tobytes(buf):
    """Convert buffer with range -1.0 to 1.0 to short signed integers then output as a byte stream

    Use this to convert a sound held in internal format to a byte list for external processing, e.g. by
    pygame.

    Args:
        buf: sample buffer

    Returns:
        byte list
    """
    a = array.array("h")
    for i in range(len(buf)):
        a.append(int(_limit(buf[i]) * 32767))
    return a.tobytes()


def boost(buf, gain):
    """Apply gain to buffer

    Args:
        buf: sample buffer
        gain: amount to multiply amplitude by

    Returns:
        new sample buffer
    """
    nparray = np.array(buf)
    npnew = nparray * gain
    buf = new_buffer(npnew)
    return buf


def reverse(buf):
    """Return backwards copy of the buffer

    Args:
        buf: sample buffer

    Returns:
        new sample buffer
    """
    nparray = np.array(buf)
    npnew = np.flip(nparray)
    buf = new_buffer(npnew)
    return buf


def combine(buf1, buf2):
    """Combine 2 buffers giving average amplitude for each sample

    Args:
        buf1: first sample buffer
        buf2: second sample buffer

    Returns:
        new sample buffer
    """
    if (len(buf1) != len(buf2)):
        pad(buf1 if len(buf1) < len(buf2) else buf2, max(len(buf1), len(buf2)))
    nparray1 = np.array(buf1)
    nparray2 = np.array(buf2)
    npsummed = nparray1 + nparray2 / 2
    buf = new_buffer(npsummed)
    return buf


def add(target, source, offset=0):
    """Add the source sample to the target buffer

    Args:
        target: a sample buffer to be updated with the new sound
        source: a sample buffer containing the sound to add
        offset: number of milliseconds from the start of the target where we insert the source (optional)

    Returns:
        new sample buffer
    """
    olen = ms_to_samples(offset)
    slen = len(source)
    tlen = slen + olen
    if (len(target) < tlen):
        pad(target, tlen)
    post = target[tlen:]
    pre = target[:olen]
    nparray1 = np.array(target[olen:tlen])
    nparray2 = np.array(source[:slen])
    npsummed = nparray1 + nparray2
    buf = pre + new_buffer(npsummed) + post
    return buf


def constrain(buf, lower, upper):
    """Clip a buffer to an upper and lower constraint

    Args:
        buf: sample buffer
        lower: lower constraint from -1.0 to 1.0
        upper: upper constraint from -1.0 to 1.0

    Returns:
        new sample buffer
    """
    nparray = np.array(buf)
    np.clip(nparray, lower, upper, nparray)
    buf = new_buffer(nparray)
    return buf


def vmove(buf, amount):
    """Shift samples in the Y axis

    Args:
        buf: sample buffer
        amount: magnitude of move from -1.0 to 1.0

    Returns:
        new sample buffer
    """
    nparray = np.array(buf)
    nparray += amount
    buf = new_buffer(nparray)
    return buf


def fade(buf, a1, a2):
    """Change start and end amplitude and scale smoothly between

    Args:
        buf: sample buffer
        a1: start amplitude from -1.0 to 1.0
        a2: end amplitude from -1.0 to 1.0

    Returns:
        new sample buffer
    """
    buf = boost(buf, a1)
    ms = samples_to_ms(len(buf))
    envelope(buf, 0, ms, a2 / a1, 0)
    return buf


def slice(buf, start, end):
    """Extract a section of a buffer with start and end times in ms

    Args:
        buf: sample buffer
        start: start position in milliseconds
        end: end position in milliseconds

    Returns:
        new sample buffer containing just the sliced samples
    """
    s = ms_to_samples(start)
    e = min(len(buf), ms_to_samples(end))
    return buf[s:e]


def median_filter(buf):
    """Perform a median filter

    Args:
        buf: sample buffer

    Returns:
        new filtered sample buffer
    """
    return new_buffer(medfilt(buf, kernel_size=5))


def lowpass_filter(buf, cutoff, order=6):
    """Apply a filter that progressively removes frequencies above the cutoff

    Args:
        buf: sample buffer
        cutoff: cutoff frequency in Hz
        order: determines how much effect the filter has, order 1 is lowest effect, 6 is more dramatic (optional)

    Returns:
        new filtered sample buffer
    """
    return _butterworth_filter(buf, cutoff, type='lowpass', order=order)


def highpass_filter(buf, cutoff, order=6):
    """Apply a filter that progressively removes frequencies below the cutoff

    Args:
        buf: sample buffer
        cutoff: cutoff frequency in Hz
        order: determines how much effect the filter has, order 1 is lowest effect, 6 is more dramatic (optional)

    Returns:
        new filtered sample buffer
    """
    return _butterworth_filter(buf, cutoff, type='highpass', order=order)


# ---------------------------------------------------------------------------
# Functions to create new buffers
# ---------------------------------------------------------------------------


def new_buffer(content=[]):
    """Create a new buffer of floating point amplitudes

    Args:
        content: optional list of values to populate the buffer with

    Returns:
        new sample buffer
    """
    return array.array("d", content)


def sequence(beatlen, notes, finetune=1.0):
    """Sequence notes to a buffer for creating music

    Args:
        beatlen: length of each beat in the sequence in milliseconds
        notes: list of notes, each element of the list is in the following format:  
                [note_name, start_beat, length_in_beats, velocity, creation_function]  
                The creation function must have the parameter format (ms, volume, frequency)
        finetune: multiply the frequency by this amount to make the notes consistently slightly sharp/flat (optional)

    Returns:
        new sample buffer containing completed sequence
    """
    buf = new_buffer()
    for note in notes:
        hz = notehz(note[0]) * finetune
        beat = note[1] * beatlen
        length = note[2] * beatlen
        velocity = note[3]
        func = note[4]
        source = _check_cache(func, length, velocity, hz)
        buf = add(buf, source, beat)
    return buf


def make_sawtooth(ms, vol, freq):
    """Make a sawtooth wave

    Args:
        ms: time in milliseconds
        vol: volume from 0.0 to 1.0
        freq: frequency in Hz

    Returns:
        new sample buffer
    """
    n = ms_to_samples(ms)
    buf = new_buffer()
    for i in range(n):
        buf.append(samplept(sawtooth, i, freq) * vol)
    return buf


def make_triangle(ms, vol, freq):
    """Make a triangle wave

    Args:
        ms: time in milliseconds
        vol: volume from 0.0 to 1.0
        freq: frequency in Hz

    Returns:
        new sample buffer
    """
    n = ms_to_samples(ms)
    buf = new_buffer()
    for i in range(n):
        buf.append(samplept(triangle, i, freq) * vol)
    return buf


def make_square(ms, vol, freq, pwm=None):
    """Make a square wave

    Args:
        ms: time in milliseconds
        vol: volume from 0.0 to 1.0
        freq: frequency in Hz
        pwm: cutoff value between -1.0 and 1.0 to create pulse wave modulation on the intersection (optional)

    Returns:
        new sample buffer
    """
    n = ms_to_samples(ms)
    buf = new_buffer()
    for i in range(n):
        buf.append(samplept(square, i, freq, 0, [], pwm) * vol)
    return buf


def make_sin(ms, vol, freq, harmonics=0, precision=None):
    """Make a sine wave

    Args:
        ms: time in milliseconds
        vol: volume from 0.0 to 1.0
        freq: frequency in Hz
        harmonics: number of natural harmonics to add (optional)
        precision: set to an integer value to simulate lower precision math (optional)

    Returns:
        new sample buffer
    """
    n = ms_to_samples(ms)
    buf = new_buffer()
    for i in range(n):
        buf.append(samplept(sin, i, freq, harmonics, [], precision) * vol)
    return buf


def make_synth_organ(ms, vol, freq):
    """Combination of octave harmonics of sine waves and a triangle wave at first octave to give a synth organ sound
    
    As used in pac-man intermission music and pac-man die sounds

    Args:
        ms: time in milliseconds
        vol: volume from 0.0 to 1.0
        freq: frequency in Hz

    Returns:
        new sample buffer
    """
    n = ms_to_samples(ms)
    buf = new_buffer()
    for i in range(n):
        buf.append(samplept(synth_organ, i, freq) * vol)
    return buf


def make_white(ms, vol, smooth=False):
    """Fill a buffer with random amplitudes to produce white noise

    Args:
        ms: time in milliseconds
        vol: volume from 0.0 to 1.0
        smooth: if smooth is False use values of 1.0 or -1.0 randomly to produce white noise similar to the SN76477 Complex Sound Generator chip,  
                otherwise generate purely random amplitudes which gives a more natural noise. (optional)

    Returns:
        new sample buffer
    """
    n = ms_to_samples(ms)
    buf = new_buffer()
    random.seed(0)
    rng = random.Random()
    for _ in range(n):
        r = rng.uniform(-1.0, 1.0) * vol
        buf.append(r if smooth else 1.0 if r > 0.0 else -1.0)
    return buf


def make_brown(ms, vol, freq, order=1):
    """Apply a lowpass filter to white noise to produce brown noise

    Args:
        ms: time in milliseconds
        vol: volume from 0.0 to 1.0
        freq: filter cutoff frequency in Hz
        order: magnitude of filter effect, order 1 is lowest effect, 6 is more dramatic (optional)

    Returns:
        new sample buffer
    """
    buf = make_white(ms, vol)
    buf = lowpass_filter(buf, freq, order)
    return buf


def make_sweep(ms, startf, endf, shape, vol, repeat=0, harmonics=0, special=None):
    """Create a buffer that starts at frequency startf and ends at endf

    Args:
        ms: time in milliseconds
        startf: start frequency in Hz
        endf: end frequency in Hz
        shape: the function to use to calculate the amplitude for each sample, e.g. sin() or square()
        vol: volume from 0.0 to 1.0
        repeat: If repeat is not zero the cycle goes from startf to endf and back to startf in repeat milliseconds and
                    continues to cycle until ms milliseconds have been filled (optional)
        harmonics: number of natural harmonics to add (optional)
        special: special parameters for modifying some functions (optional)

    Returns:
        new sample buffer
    """
    n = ms_to_samples(ms)
    loop = n * 2 if repeat == 0 else ms_to_samples(repeat)
    period = loop // 2
    buf = new_buffer()
    phase = [0.0 for _ in range(harmonics + 1)]
    for i in range(n):
        x = i % loop
        if x > period:
            x = loop - x
        else:
            pass
        f = (startf - ((startf - endf) * (x / period)))
        a, phase = samplept(shape, i, f, harmonics, phase, special)
        buf.append(a * vol)
    return buf


def make_silence(ms):
    """Create a buffer filled with silence

    Args:
        ms: time in milliseconds

    Returns:
        new sample buffer
    """
    return new_buffer([0.0] * ms_to_samples(ms))


# ---------------------------------------------------------------------------
# Functions to manipulate buffers in place
# ---------------------------------------------------------------------------


def pad(buf, length):
    """Pad out a buffer with zeroes to length

    Args:
        buf: sample buffer
        length: target length of buffer in number of samples

    Returns:
        new sample buffer
    """
    if len(buf) < length:
        buf += new_buffer([0.0] * (length - len(buf)))
    return


def tremolo(buf, freq, intensity, shape, special=None):
    """Modify a buffer in place so that amplitude increases and decreases according to shape and intensity

    Args:
        buf: sample buffer
        freq: frequency in Hz of tremolo effect
        intensity: amount to change amplitude from 0.0 to 1.0
        shape: the function to use to calculate the amplitude for each sample e.g. sin() or square()
        special: special parameters for modifying some functions (optional)

    Returns:
        None
    """
    for i in range(len(buf)):
        phase = i * math.pi * freq / SAMPLE_RATE
        buf[i] *= (1.0 - intensity) + abs(((shape(phase, special) + 1.0) / 2.0) * intensity)
    return


def noisalise(buf, vol=1.0, gain=1.0):
    """Apply gain to buffer proportional to mean amplitude, useful for restoring a constant RMS after processing noise

    Args:
        buf: sample buffer
        vol: target volume from 0.0 to 1.0 (optional)
        gain: amount to change amplitude from 0.0 to 1.0 (optional)

    Returns:
        None
    """
    data = np.array(buf)
    av = (data[data > 0].mean() + -data[data < 0].mean()) / 2.0
    r = gain / (av / 2.0)
    for i in range(len(buf)):
        buf[i] = _limit(buf[i], limit=vol / gain) * r * vol
    return


def envelope(buf, attack, decay, sustain, release, start=0, end=MAX_LEN):
    """Modify a buffer in place with an ADSR envelope

    Args:
        buf: sample buffer
        attack: attack time in milliseconds
        decay: decay time in milliseconds
        sustain: volume of sustain from 0.0 to 1.0
        release: release time in milliseconds
        start: start milliseconds in sample to apply effect (optional)
        end: end milliseconds in sample to apply effect (optional)

    Returns:
        None
    """
    attack_start = ms_to_samples(start)
    attack_end = min(len(buf), ms_to_samples(start + attack))
    decay_end = min(len(buf), ms_to_samples(decay) + attack_end)
    release_end = min(len(buf), ms_to_samples(end))
    sustain_end = min(len(buf), release_end - ms_to_samples(release))
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
    """Modify buffer in place to add a short delay to the sound

    Args:
        buf: sample buffer
        ms: delay in milliseconds
        vol: volume of effect from 0.0 to 1.0

    Returns:
        None
    """
    delay = ms_to_samples(ms)
    for _ in range(delay):
        buf.append(0.0)
    for i in range(len(buf)):
        buf[i] *= 1 - vol
        if i >= delay:
            buf[i] += buf[i - delay] * vol
    return
