<a id="arcadesynth.synth"></a>

# arcadesynth.synth

functions to programmatically synthesize retro arcade sound effects

[source](../src/arcadesynth/synth.py)

<a id="arcadesynth.synth.sawtooth"></a>

#### sawtooth

```python
def sawtooth(phase, _=None)
```

Calculate amplitude for a sawtooth wave at the given phase

**Arguments**:

- `phase` - calculated phase based on frequency and time
  

**Returns**:

  amplitude of sample

<a id="arcadesynth.synth.triangle"></a>

#### triangle

```python
def triangle(phase, _=None)
```

Calculate amplitude for a triangle wave at the given phase

**Arguments**:

- `phase` - calculated phase based on frequency and time
  

**Returns**:

  amplitude of sample

<a id="arcadesynth.synth.square"></a>

#### square

```python
def square(phase, pwm=None)
```

Calculate amplitude for a square wave at the given phase

**Arguments**:

- `phase` - calculated phase based on frequency and time
- `pwm` - cutoff value between -1.0 and 1.0 to create pulse wave modulation on the intersection (optional)
  

**Returns**:

  amplitude of sample

<a id="arcadesynth.synth.sin"></a>

#### sin

```python
def sin(phase, precision=None)
```

Calculate amplitude for a sine wave at the given phase

**Arguments**:

- `phase` - calculated phase based on frequency and time
- `precision` - set to an integer value to simulate lower precision math (optional)
  

**Returns**:

  amplitude of sample

<a id="arcadesynth.synth.synth_organ"></a>

#### synth\_organ

```python
def synth_organ(p, _=None)
```

Calculate amplitude for a synth organ sound at the given phase

Combination of octave harmonics of sine waves and a triangle wave at first octave to give a synth organ sound
As used in pac-man intermission music and pac-man die sounds

**Arguments**:

- `phase` - calculated phase based on frequency and time
  

**Returns**:

  amplitude of sample

<a id="arcadesynth.synth.init"></a>

#### init

```python
def init(frequency=FREQUENCY, channels=CHANNELS)
```

Set up sample rate, do this first to avoid using defaults

The init function calculates the number of samples needed to construct consistent sounds for internal use
E.g. get these values from pygame with 'frequency, _, channels = pygame.mixer.get_init()'

**Arguments**:

- `frequency` - frequency of each channel
- `channels` - number of channels
  

**Returns**:

  None

<a id="arcadesynth.synth.get_init"></a>

#### get\_init

```python
def get_init()
```

Return the configured calculated sample rate

**Returns**:

  calculated sample rate

<a id="arcadesynth.synth.notehz"></a>

#### notehz

```python
def notehz(note)
```

For a given note return the frequency

**Arguments**:

- `note` - note name as a string, e.g. "A4" or "C#3", flats are not supported
  

**Returns**:

  frequency in Hz

<a id="arcadesynth.synth.samplept"></a>

#### samplept

```python
def samplept(func, i, f, harmonics=0, p=[], special=None)
```

Calculate amplitude of a sample for a buffer position

Given a function to calculate amplitude of a wave (func) for a buffer position (i)
and frequency (f) calculate and return the amplitude.
If harmonics is not zero also add in the amplitude of the given order of harmonics.
If frequency is not constant throughout the buffer, track the current phase during the
building process and pass the current phase of the primary and any harmonics through
the list (p), otherwise phase can be calculated on the fly.

**Arguments**:

- `func` - the function to use to calculate the amplitude for the sample
- `i` - numeric index to position of sample in buffer
- `f` - target frequency
- `harmonics` - number of natural harmonics to add (optional)
- `p` - list containing current phase of primary and any harmonics (optional)
- `special` - special parameters for modifying some functions (optional)
  

**Returns**:

  amplitude of sample at current index and phase
  updated phase list (if optional p parameter was provided)

<a id="arcadesynth.synth.ms_to_samples"></a>

#### ms\_to\_samples

```python
def ms_to_samples(ms)
```

Convert time in milliseconds to number of samples

**Arguments**:

- `ms` - time in milliseconds
  

**Returns**:

  number of samples in buffer

<a id="arcadesynth.synth.samples_to_ms"></a>

#### samples\_to\_ms

```python
def samples_to_ms(n)
```

Convert number of samples to time in milliseconds

**Arguments**:

- `n` - number of samples in buffer
  

**Returns**:

  time in milliseconds

<a id="arcadesynth.synth.tobytes"></a>

#### tobytes

```python
def tobytes(buf)
```

Convert buffer with range -1.0 to 1.0 to short signed integers then output as a byte stream

Use this to convert a sound held in internal format to a byte list for external processing, e.g. by
pygame.

**Arguments**:

- `buf` - sample buffer
  

**Returns**:

  byte list

<a id="arcadesynth.synth.boost"></a>

#### boost

```python
def boost(buf, gain)
```

Apply gain to buffer

**Arguments**:

- `buf` - sample buffer
- `gain` - amount to multiply amplitude by
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.reverse"></a>

#### reverse

```python
def reverse(buf)
```

Return backwards copy of the buffer

**Arguments**:

- `buf` - sample buffer
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.combine"></a>

#### combine

```python
def combine(buf1, buf2)
```

Combine 2 buffers giving average amplitude for each sample

**Arguments**:

- `buf1` - first sample buffer
- `buf2` - second sample buffer
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.add"></a>

#### add

```python
def add(target, source, offset=0)
```

Add the source sample to the target buffer

**Arguments**:

- `target` - a sample buffer to be updated with the new sound
- `source` - a sample buffer containing the sound to add
- `offset` - number of milliseconds from the start of the target where we insert the source (optional)
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.constrain"></a>

#### constrain

```python
def constrain(buf, lower, upper)
```

Clip a buffer to an upper and lower constraint

**Arguments**:

- `buf` - sample buffer
- `lower` - lower constraint from -1.0 to 1.0
- `upper` - upper constraint from -1.0 to 1.0
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.vmove"></a>

#### vmove

```python
def vmove(buf, amount)
```

Shift samples in the Y axis

**Arguments**:

- `buf` - sample buffer
- `amount` - magnitude of move from -1.0 to 1.0
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.fade"></a>

#### fade

```python
def fade(buf, a1, a2)
```

Change start and end amplitude and scale smoothly between

**Arguments**:

- `buf` - sample buffer
- `a1` - start amplitude from -1.0 to 1.0
- `a2` - end amplitude from -1.0 to 1.0
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.slice"></a>

#### slice

```python
def slice(buf, start, end)
```

Extract a section of a buffer with start and end times in ms

**Arguments**:

- `buf` - sample buffer
- `start` - start position in milliseconds
- `end` - end position in milliseconds
  

**Returns**:

  new sample buffer containing just the sliced samples

<a id="arcadesynth.synth.median_filter"></a>

#### median\_filter

```python
def median_filter(buf)
```

Perform a median filter

**Arguments**:

- `buf` - sample buffer
  

**Returns**:

  new filtered sample buffer

<a id="arcadesynth.synth.lowpass_filter"></a>

#### lowpass\_filter

```python
def lowpass_filter(buf, cutoff, order=6)
```

Apply a filter that progressively removes frequencies above the cutoff

**Arguments**:

- `buf` - sample buffer
- `cutoff` - cutoff frequency in Hz
- `order` - determines how much effect the filter has, order 1 is lowest effect, 6 is more dramatic (optional)
  

**Returns**:

  new filtered sample buffer

<a id="arcadesynth.synth.highpass_filter"></a>

#### highpass\_filter

```python
def highpass_filter(buf, cutoff, order=6)
```

Apply a filter that progressively removes frequencies below the cutoff

**Arguments**:

- `buf` - sample buffer
- `cutoff` - cutoff frequency in Hz
- `order` - determines how much effect the filter has, order 1 is lowest effect, 6 is more dramatic (optional)
  

**Returns**:

  new filtered sample buffer

<a id="arcadesynth.synth.new_buffer"></a>

#### new\_buffer

```python
def new_buffer(content=[])
```

Create a new buffer of floating point amplitudes

**Arguments**:

- `content` - optional list of values to populate the buffer with
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.sequence"></a>

#### sequence

```python
def sequence(beatlen, notes, finetune=1.0)
```

Sequence notes to a buffer for creating music

**Arguments**:

- `beatlen` - length of each beat in the sequence in milliseconds
- `notes` - list of notes, each element of the list is in the following format:
  [note_name, start_beat, length_in_beats, velocity, creation_function]
  The creation function must have the parameter format (ms, volume, frequency)
- `finetune` - multiply the frequency by this amount to make the notes consistently slightly sharp/flat (optional)
  

**Returns**:

  new sample buffer containing completed sequence

<a id="arcadesynth.synth.make_sawtooth"></a>

#### make\_sawtooth

```python
def make_sawtooth(ms, vol, freq)
```

Make a sawtooth wave

**Arguments**:

- `ms` - time in milliseconds
- `vol` - volume from 0.0 to 1.0
- `freq` - frequency in Hz
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.make_triangle"></a>

#### make\_triangle

```python
def make_triangle(ms, vol, freq)
```

Make a triangle wave

**Arguments**:

- `ms` - time in milliseconds
- `vol` - volume from 0.0 to 1.0
- `freq` - frequency in Hz
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.make_square"></a>

#### make\_square

```python
def make_square(ms, vol, freq, pwm=None)
```

Make a square wave

**Arguments**:

- `ms` - time in milliseconds
- `vol` - volume from 0.0 to 1.0
- `freq` - frequency in Hz
- `pwm` - cutoff value between -1.0 and 1.0 to create pulse wave modulation on the intersection (optional)
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.make_sin"></a>

#### make\_sin

```python
def make_sin(ms, vol, freq, harmonics=0, precision=None)
```

Make a sine wave

**Arguments**:

- `ms` - time in milliseconds
- `vol` - volume from 0.0 to 1.0
- `freq` - frequency in Hz
- `harmonics` - number of natural harmonics to add (optional)
- `precision` - set to an integer value to simulate lower precision math (optional)
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.make_synth_organ"></a>

#### make\_synth\_organ

```python
def make_synth_organ(ms, vol, freq)
```

Combination of octave harmonics of sine waves and a triangle wave at first octave to give a synth organ sound

As used in pac-man intermission music and pac-man die sounds

**Arguments**:

- `ms` - time in milliseconds
- `vol` - volume from 0.0 to 1.0
- `freq` - frequency in Hz
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.make_white"></a>

#### make\_white

```python
def make_white(ms, vol, smooth=False)
```

Fill a buffer with random amplitudes to produce white noise

**Arguments**:

- `ms` - time in milliseconds
- `vol` - volume from 0.0 to 1.0
- `smooth` - if smooth is False use values of 1.0 or -1.0 randomly to produce white noise similar to the SN76477 Complex Sound Generator chip,
  otherwise generate purely random amplitudes which gives a more natural noise. (optional)
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.make_brown"></a>

#### make\_brown

```python
def make_brown(ms, vol, freq, order=1)
```

Apply a lowpass filter to white noise to produce brown noise

**Arguments**:

- `ms` - time in milliseconds
- `vol` - volume from 0.0 to 1.0
- `freq` - filter cutoff frequency in Hz
- `order` - magnitude of filter effect, order 1 is lowest effect, 6 is more dramatic (optional)
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.make_sweep"></a>

#### make\_sweep

```python
def make_sweep(ms,
               startf,
               endf,
               shape,
               vol,
               repeat=0,
               harmonics=0,
               special=None)
```

Create a buffer that starts at frequency startf and ends at endf

**Arguments**:

- `ms` - time in milliseconds
- `startf` - start frequency in Hz
- `endf` - end frequency in Hz
- `shape` - the function to use to calculate the amplitude for each sample, e.g. sin() or square()
- `vol` - volume from 0.0 to 1.0
- `repeat` - If repeat is not zero the cycle goes from startf to endf and back to startf in repeat milliseconds and
  continues to cycle until ms milliseconds have been filled (optional)
- `harmonics` - number of natural harmonics to add (optional)
- `special` - special parameters for modifying some functions (optional)
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.make_silence"></a>

#### make\_silence

```python
def make_silence(ms)
```

Create a buffer filled with silence

**Arguments**:

- `ms` - time in milliseconds
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.pad"></a>

#### pad

```python
def pad(buf, length)
```

Pad out a buffer with zeroes to length

**Arguments**:

- `buf` - sample buffer
- `length` - target length of buffer in number of samples
  

**Returns**:

  new sample buffer

<a id="arcadesynth.synth.tremolo"></a>

#### tremolo

```python
def tremolo(buf, freq, intensity, shape, special=None)
```

Modify a buffer in place so that amplitude increases and decreases according to shape and intensity

**Arguments**:

- `buf` - sample buffer
- `freq` - frequency in Hz of tremolo effect
- `intensity` - amount to change amplitude from 0.0 to 1.0
- `shape` - the function to use to calculate the amplitude for each sample e.g. sin() or square()
- `special` - special parameters for modifying some functions (optional)
  

**Returns**:

  None

<a id="arcadesynth.synth.noisalise"></a>

#### noisalise

```python
def noisalise(buf, vol=1.0, gain=1.0)
```

Apply gain to buffer proportional to mean amplitude, useful for restoring a constant RMS after processing noise

**Arguments**:

- `buf` - sample buffer
- `vol` - target volume from 0.0 to 1.0 (optional)
- `gain` - amount to change amplitude from 0.0 to 1.0 (optional)
  

**Returns**:

  None

<a id="arcadesynth.synth.envelope"></a>

#### envelope

```python
def envelope(buf, attack, decay, sustain, release, start=0, end=MAX_LEN)
```

Modify a buffer in place with an ADSR envelope

**Arguments**:

- `buf` - sample buffer
- `attack` - attack time in milliseconds
- `decay` - decay time in milliseconds
- `sustain` - volume of sustain from 0.0 to 1.0
- `release` - release time in milliseconds
- `start` - start milliseconds in sample to apply effect (optional)
- `end` - end milliseconds in sample to apply effect (optional)
  

**Returns**:

  None

<a id="arcadesynth.synth.echo"></a>

#### echo

```python
def echo(buf, ms, vol)
```

Modify buffer in place to add a short delay to the sound

**Arguments**:

- `buf` - sample buffer
- `ms` - delay in milliseconds
- `vol` - volume of effect from 0.0 to 1.0
  

**Returns**:

  None

